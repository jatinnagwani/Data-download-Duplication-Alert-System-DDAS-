"""
hasher.py
---------
Responsible for generating a unique 'fingerprint' (hash) for any file.

Why hashing instead of comparing filenames?
Two files can have completely different names but identical content
(e.g., "report.pdf" and "report_copy.pdf"). Comparing names would miss
this duplicate. Hashing looks at the actual content, so it catches
duplicates regardless of what the file is called.

Why SHA-256 and not MD5?
MD5 is faster but has known collision weaknesses (two different files
can, in rare cases, produce the same MD5 hash). SHA-256 is much more
reliable for this purpose and is available in Python's built-in
hashlib module, so no extra installation is needed.

Why read in chunks instead of the whole file at once?
- If someone tries to hash a 2GB video file, loading it all into RAM
  at once could crash the program on low-memory systems.
- Reading in small chunks (4096 bytes at a time) keeps memory usage
  constant no matter how big the file is.
"""


import hashlib
import os

CHUNK_SIZE = 4096  # bytes read per iteration

def compute_file_hash(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()

def get_file_metadata(file_path: str) -> dict:
    if not os.path.isfile(file_path):
        raise ValueError(f"'{file_path}' is not a valid file.")
    return {
        "filename": os.path.basename(file_path),
        "filesize": os.path.getsize(file_path),
        "filehash": compute_file_hash(file_path),
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python hasher.py <file_path>")
        sys.exit(1)
    metadata = get_file_metadata(sys.argv[1])
    print(f"Filename : {metadata['filename']}")
    print(f"Size     : {metadata['filesize']} bytes")
    print(f"SHA-256  : {metadata['filehash']}")