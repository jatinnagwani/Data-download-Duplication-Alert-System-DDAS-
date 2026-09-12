# 🔍 DDAS — Data Download Duplication Alert System

A terminal-based Python tool that detects duplicate file downloads using content hashing (SHA-256), helping avoid unnecessary storage and bandwidth usage in shared environments.

---

## 📌 Problem Statement

In shared environments — institutes, research teams, government data repositories — multiple users often download the same datasets without knowing others already have them. This wastes storage, bandwidth, and time. **DDAS** solves this by maintaining a registry of downloaded files and alerting users *before* they duplicate a download that already exists — showing exactly who downloaded it, when, and where.

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Simulate a Download** | Computes a SHA-256 hash of a file and checks it against past records. Alerts if it's a duplicate; saves it if it's new. |
| 2 | **View Records** | View all recorded downloads, or filter by a specific username. |
| 3 | **Scan a Folder for Duplicates** | Recursively scans a folder (skipping hidden folders like `.git`) and groups files with identical content — even if named differently. Option to export results as a text report. |
| 4 | **View Statistics** | Displays total files tracked, total storage used, and the most active user. |
| 5 | **Exit** | Closes the application. |

---

## 🗂️ Project Structure

ddas/
├── hasher.py # File hashing + folder duplicate scanning
├── database.py # SQLite storage, filtering, statistics
├── main.py # Terminal menu — ties everything together
├── requirements.txt # External dependency (rich)
└── README.md


---

## ⚙️ How It Works

1. User "simulates" a download by providing a file path
2. `hasher.py` computes a **SHA-256 hash** — a unique fingerprint based on file content, not filename
3. `database.py` checks this hash against previously recorded downloads (SQLite)
4. If a match is found → user is alerted with the original file's details
5. If no match is found → the new file is recorded for future checks

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python3 main.py
```

---

## 🧠 Key Design Decisions

- **Why hashing instead of comparing filenames?**
  Two files can have completely different names but identical content. Hashing looks at actual content, catching duplicates that filename comparison would miss.

- **Why SHA-256 over MD5?**
  MD5 has known collision weaknesses. SHA-256 is far more reliable for duplicate detection and is available in Python's built-in `hashlib`.

- **Why read files in chunks?**
  Large files are read in small chunks (4096 bytes at a time) instead of loading them fully into memory — this keeps memory usage constant regardless of file size.

- **Why SQLite?**
  It's built into Python and stores everything in a single file (`ddas.db`) — no separate database server needed for a small CLI tool like this.

- **Why exclude hidden folders during scans?**
  Folders like `.git` contain internal duplicate files (e.g., Git refs) that aren't relevant to the user — excluding them avoids false positives.

---

## 🗃️ Database Schema

**Table: `records`**

| Column | Type | Description |
|--------|------|--------------|
| `id` | INTEGER (PK) | Auto-incrementing unique ID |
| `filename` | TEXT | Name of the file |
| `filehash` | TEXT | SHA-256 hash (content fingerprint) |
| `filesize` | INTEGER | Size in bytes |
| `username` | TEXT | Who "downloaded" the file |
| `timestamp` | TEXT | When it was recorded |
| `location` | TEXT | File path |

---

## 🎨 Terminal Output

Formatted using the [`rich`](https://github.com/Textualize/rich) library — this only affects **how output is displayed**, not the underlying logic:
- ✅ Success messages — green
- ⚠️ Errors — yellow
- 🚨 Duplicate alerts — red
- 📊 Records, duplicate groups, and statistics — displayed in bordered tables/panels

---

## 🔒 Scope & Limitations

- This is a **manual/simulated** system — the user explicitly tells DDAS what to check, rather than automatically intercepting real downloads (e.g., via a browser extension or OS-level hook). This keeps the implementation realistic for a solo, time-boxed project.
- Duplicate detection is **exact-hash-based only** — files with similar names but different content (or vice versa, e.g., resized images) are not treated as duplicates. Fuzzy/approximate matching is a possible future enhancement.

---

## 🛠️ Tech Stack

Python 3 · `hashlib` · `sqlite3` · `os` · [`rich`](https://pypi.org/project/rich/)
