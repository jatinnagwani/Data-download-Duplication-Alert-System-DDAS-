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