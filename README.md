# DDAS - Data Download Duplication Alert System

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
