"""
main.py
-------
Entry point for DDAS. Provides a simple terminal menu that lets the
user "simulate" a download, checks it against the database for
duplicates, and reports results.
"""

import os
from hasher import compute_file_hash, get_file_metadata, scan_folder_for_duplicates
from database import create_table, insert_record, check_duplicate, get_all_records, get_records_by_user, get_statistics
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def simulate_download():
    username = input("Enter your username: ").strip()
    file_path = input("Enter the file path you want to download: ").strip()

    if not username:
        console.print("\n[bold yellow]\\[ERROR][/bold yellow] Username cannot be empty.\n")
        return

    if not file_path:
        console.print("\n[bold yellow]\\[ERROR][/bold yellow] File path cannot be empty.\n")
        return

    if not os.path.isfile(file_path):
        console.print(f"\n[bold yellow]\\[ERROR][/bold yellow] '{file_path}' is not a valid file. Try again.\n")
        return

    try:
        metadata = get_file_metadata(file_path)
    except ValueError as e:
        console.print(f"\n[bold yellow]\\[ERROR][/bold yellow] {e}\n")
        return
    filehash = metadata["filehash"]

    existing = check_duplicate(filehash)

    if existing:
        existing_filename, existing_user, existing_time, existing_location = existing
        console.print("\n[bold red]\\[DUPLICATE ALERT][/bold red]")
        console.print("This file has already been downloaded before!")
        console.print(f"  Original filename : {existing_filename}")
        console.print(f"  Downloaded by     : {existing_user}")
        console.print(f"  Downloaded on     : {existing_time}")
        console.print(f"  Location          : {existing_location}")
        console.print("No new download needed.\n")
    else:
        insert_record(
            filename=metadata["filename"],
            filehash=filehash,
            filesize=metadata["filesize"],
            username=username,
            location=file_path,
        )
        console.print(f"\n[bold green]\\[OK][/bold green] New file recorded successfully.")
        console.print(f"  Filename : {metadata['filename']}")
        console.print(f"  Size     : {metadata['filesize']} bytes")
        console.print(f"  Hash     : {filehash}\n")


def view_records():
    filter_choice = input("View (1) All records or (2) Filter by username? Enter 1 or 2: ").strip()

    if filter_choice == "2":
        username = input("Enter username to filter by: ").strip()
        records = get_records_by_user(username)
    else:
        records = get_all_records()

    if not records:
        console.print("\n[yellow]No records found.[/yellow]\n")
        return

    table = Table(title="Download Records")
    table.add_column("ID", style="cyan")
    table.add_column("Filename", style="white")
    table.add_column("User", style="magenta")
    table.add_column("Timestamp", style="white")
    table.add_column("Location", style="white")

    for r in records:
        rec_id, filename, filehash, filesize, username, timestamp, location = r
        table.add_row(str(rec_id), filename, username, timestamp, location)

    console.print(Panel(table, title="[bold]Records[/bold]", border_style="cyan"))
    console.print(f"\n[bold]Total records:[/bold] {len(records)}\n")


def show_statistics():
    stats = get_statistics()

    if stats["total_records"] == 0:
        console.print("\n[yellow]No data yet to show statistics.[/yellow]\n")
        return

    table = Table(title="DDAS Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Total files tracked", str(stats["total_records"]))
    table.add_row("Total storage used", f"{stats['total_size']} bytes")
    if stats["most_active_user"]:
        table.add_row("Most active user", f"{stats['most_active_user']} ({stats['most_active_count']} downloads)")

    console.print(Panel(table, title="[bold]Summary[/bold]", border_style="cyan"))
    console.print()


def scan_folder():
    folder_path = input("Enter folder path to scan: ").strip()

    if not folder_path:
        console.print("\n[bold yellow]\\[ERROR][/bold yellow] Folder path cannot be empty.\n")
        return

    if not os.path.isdir(folder_path):
        console.print(f"\n[bold yellow]\\[ERROR][/bold yellow] '{folder_path}' is not a valid folder.\n")
        return

    duplicates = scan_folder_for_duplicates(folder_path)

    if not duplicates:
        console.print("\n[bold green]\\[OK][/bold green] No duplicates found in this folder.\n")
        return

    console.print(f"\n[bold red]\\[FOUND][/bold red] {len(duplicates)} set(s) of duplicate files:\n")

    wasted_space = 0
    for file_hash, paths in duplicates.items():
        table = Table(title=f"Duplicate group (hash: {file_hash[:12]}...)")
        table.add_column("File path", style="white")
        for p in paths:
            table.add_row(p)
        console.print(Panel(table, border_style="red"))
        wasted_space += os.path.getsize(paths[0]) * (len(paths) - 1)

    console.print(f"\n[bold]Estimated wasted storage:[/bold] {wasted_space} bytes\n")

    save = input("Save this report to a file? (y/n): ").strip().lower()
    if save == "y":
        report_filename = "duplicate_report.txt"
        with open(report_filename, "w") as f:
            f.write(f"DDAS Duplicate Scan Report\n")
            f.write(f"Folder scanned: {folder_path}\n")
            f.write(f"Total duplicate sets found: {len(duplicates)}\n\n")
            for file_hash, paths in duplicates.items():
                f.write(f"Duplicate group (hash: {file_hash[:12]}...):\n")
                for p in paths:
                    f.write(f"  - {p}\n")
                f.write("\n")
            f.write(f"Estimated wasted storage: {wasted_space} bytes\n")
        console.print(f"[bold green]\\[SAVED][/bold green] Report saved to '{report_filename}'\n")


def main():
    create_table()

    while True:
        console.print("\n[bold cyan]=== DDAS - Data Download Duplication Alert System ===[/bold cyan]")
        console.print("1. Simulate a download")
        console.print("2. View all records")
        console.print("3. Scan a folder for duplicates")
        console.print("4. View statistics")
        console.print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            simulate_download()
        elif choice == "2":
            view_records()
        elif choice == "3":
            scan_folder()
        elif choice == "4":
            show_statistics()
        elif choice == "5":
            console.print("[bold magenta]Exiting DDAS. Goodbye![/bold magenta]")
            break
        else:
            console.print("\n[bold yellow]\\[ERROR][/bold yellow] Invalid choice, try again.\n")


if __name__ == "__main__":
    main()