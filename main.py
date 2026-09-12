"""
main.py
-------
Entry point for DDAS. Provides a simple terminal menu that lets the
user "simulate" a download, checks it against the database for
duplicates, and reports results.
"""

import os
from hasher import compute_file_hash, get_file_metadata
from database import create_table, insert_record, check_duplicate, get_all_records


def simulate_download():
    username = input("Enter your username: ").strip()
    file_path = input("Enter the file path you want to download: ").strip()

    if not username:
        print("\n[ERROR] Username cannot be empty.\n")
        return

    if not os.path.isfile(file_path):
        print(f"\n[ERROR] '{file_path}' is not a valid file. Try again.\n")
        return

    try:
        metadata = get_file_metadata(file_path)
    except ValueError as e:
        print(f"\n[ERROR] {e}\n")
        return
    filehash = metadata["filehash"]

    existing = check_duplicate(filehash)

    if existing:
        existing_filename, existing_user, existing_time, existing_location = existing
        print("\n[DUPLICATE ALERT]")
        print(f"This file has already been downloaded before!")
        print(f"  Original filename : {existing_filename}")
        print(f"  Downloaded by     : {existing_user}")
        print(f"  Downloaded on     : {existing_time}")
        print(f"  Location          : {existing_location}")
        print("No new download needed.\n")
    else:
        insert_record(
            filename=metadata["filename"],
            filehash=filehash,
            filesize=metadata["filesize"],
            username=username,
            location=file_path,
        )
        print(f"\n[OK] New file recorded successfully.")
        print(f"  Filename : {metadata['filename']}")
        print(f"  Size     : {metadata['filesize']} bytes")
        print(f"  Hash     : {filehash}\n")


def view_records():
    records = get_all_records()
    if not records:
        print("\nNo records found yet.\n")
        return

    print("\n=== All Download Records ===")
    print(f"{'ID':<4}{'Filename':<20}{'User':<12}{'Timestamp':<22}{'Location'}")
    print("-" * 80)
    for r in records:
        rec_id, filename, filehash, filesize, username, timestamp, location = r
        print(f"{rec_id:<4}{filename:<20}{username:<12}{timestamp:<22}{location}")
    print(f"\nTotal records: {len(records)}\n")


def main():
    create_table()

    while True:
        print("=== DDAS - Data Download Duplication Alert System ===")
        print("1. Simulate a download")
        print("2. View all records")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            simulate_download()
        elif choice == "2":
            view_records()
        elif choice == "3":
            print("Exiting DDAS. Goodbye!")
            break
        else:
            print("\n[ERROR] Invalid choice, try again.\n")


if __name__ == "__main__":
    main()