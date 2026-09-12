# DDAS - Data Download Duplication Alert System

A terminal-based tool that detects duplicate file downloads using file hashing (SHA-256), helping avoid unnecessary storage and bandwidth usage.

## Problem it solves
In shared environments (like institutes or research teams), multiple users often download the same datasets without knowing others already have them — wasting storage and bandwidth. DDAS maintains a record of downloaded files and alerts users if they're about to download something that already exists, showing who downloaded it, when, and where.

## Features
1. **Simulate a download** — checks a file against past records using its SHA-256 hash; alerts if it's a duplicate, otherwise saves it as a new record
2. **View records** — view all recorded downloads, or filter by username
3. **Scan a folder for duplicates** — recursively scans a folder (skipping hidden folders like `.git`) and finds files with identical content, even if named differently; can export the result to a text report
4. **View statistics** — shows total files tracked, total storage used, and the most active user

## Project structure
- `hasher.py` — computes file hashes and metadata, and scans folders for duplicate content
- `database.py` — SQLite-based storage for download records, filtering, and statistics
- `main.py` — terminal menu that ties everything together

## How to run
```bash
python3 main.py
```

## Menu options
1. Simulate a download
2. View all records (or filter by username)
3. Scan a folder for duplicates (with option to export a report)
4. View statistics
5. Exit

## Tech stack
Python (built-in `hashlib`, `sqlite3`, `os` — no external dependencies for core logic)

## Design notes
- **Why hashing instead of filenames?** Files can have different names but identical content — hashing catches these duplicates by looking at actual content.
- **Why SHA-256 over MD5?** SHA-256 has a much lower collision probability, making duplicate detection more reliable.
- **Why chunked file reading?** Large files are read in small chunks (4096 bytes at a time) instead of loading them fully into memory, preventing crashes on low-memory systems.
- **Why SQLite?** It's built into Python and stores everything in a single file — no separate database server needed for a small CLI tool like this.# DDAS - Data Download Duplication Alert System

A terminal-based tool that detects duplicate file downloads using file hashing (SHA-256), helping avoid unnecessary storage and bandwidth usage.

## Problem it solves
In shared environments (like institutes or research teams), multiple users often download the same datasets without knowing others already have them — wasting storage and bandwidth. DDAS maintains a record of downloaded files and alerts users if they're about to download something that already exists, showing who downloaded it, when, and where.

## How it works
1. User "simulates" a download by providing a file path
2. The system computes a SHA-256 hash of the file (a unique fingerprint based on content, not filename)
3. It checks this hash against a local database of previously recorded downloads
4. If a match is found, it alerts the user with details of the existing copy
5. If no match is found, it saves the new record

## Project structure
- `hasher.py` — computes file hashes and metadata
- `database.py` — SQLite-based storage for download records
- `main.py` — terminal menu that ties everything together

## How to run
```bash
python3 main.py
```

## Menu options
1. Simulate a download — check a file for duplicates and record it
2. View all records — see everything recorded so far
3. Exit

## Tech stack
Python (built-in `hashlib`, `sqlite3`, `os` — no external dependencies for core logic)# DDAS - Data Download Duplication Alert System

A terminal-based tool that detects duplicate file downloads using file hashing (SHA-256), helping avoid unnecessary storage and bandwidth usage.

## Status
Work in progress.
