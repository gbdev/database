import os
import hashlib
import json
import argparse

"""
Run like this
python dupe-check-against-dict.py /home/avivace/<USER>/database/scrapers/py_importers/py_common/beta /home/<USER>/gbdev/database/scripts/hashes.json

After having generated the 'hashes.json' file running scripts/dupe-finder.py once

"""


def get_file_hash(filename, alg="md5", chunksize=131072):
    if alg == "sha256":
        h = hashlib.sha256()
    elif alg == "sha1":
        h = hashlib.sha1()
    elif alg == "md5":
        h = hashlib.md5()

    with open(filename, "rb", buffering=0) as f:
        for b in iter(lambda: f.read(chunksize), b""):
            h.update(b)
    return h.hexdigest()


def find_rom_files(folder):
    """Find all .gb and .gbc files in subfolders of the given folder."""
    rom_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".gb") or file.endswith(".gbc"):
                rom_files.append(os.path.join(root, file))
    return rom_files


def check_md5_against_json(rom_files, json_path):
    """Check the MD5 of each ROM file against the keys in the JSON file."""
    with open(json_path, "r") as f:
        md5_dict = json.load(f)

    md5_list = list(md5_dict.keys())

    for rom_file in rom_files:
        md5_checksum = get_file_hash(rom_file)
        if md5_checksum in md5_list:
            print(
                f"[FOUND] {rom_file} has a known MD5 checksum: {md5_dict[md5_checksum]}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check MD5 checksums of ROM files against a JSON file."
    )
    parser.add_argument(
        "folder_path",
        type=str,
        help="Path to folder A containing subfolders with ROM files.",
    )
    parser.add_argument(
        "json_file_path",
        type=str,
        help="Path to the JSON file containing MD5 checksums.",
    )

    args = parser.parse_args()

    # Find ROM files in the folder
    rom_files = find_rom_files(args.folder_path)

    if not rom_files:
        print("No .gb or .gbc files found.")
    else:
        # Check their MD5 checksums against the JSON file
        check_md5_against_json(rom_files, args.json_file_path)
