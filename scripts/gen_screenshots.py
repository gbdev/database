# Script requires ImageMagick installed.
# sameboy_tester can be in PATH or provided as the first argument
# (build with "make tester" in SameBoy source code)

import glob
import json
import os
import os.path
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def locate_rom(data):
	if "rom" in data:
		rom_path = data["rom"]
		if os.path.exists(rom_path):
			return rom_path
	if "files" in data:
		for file in data["files"]:
			if ("filename" in file) and file.get("playable", False):
				if os.path.exists(file["filename"]):
					return file["filename"]
	return None

def clear_dir(dir):
	for f in glob.glob(str(dir) + "/*"):
		os.remove(f)

allowed_suffixes = [".gb", ".gbc", ".cgb"]
entry_path = Path('../entries').absolute()
sameboy_tester_name = "sameboy_tester"
if len(sys.argv) > 1:
	sameboy_tester_name = sys.argv[1]

still_missing = []

with tempfile.TemporaryDirectory(prefix="gb-screenshot-") as tmp_dir_obj:
	tmp_dir = Path(tmp_dir_obj)
	for folder in os.listdir(entry_path):
		game_path = entry_path / folder
		os.chdir(game_path)
		with open('game.json') as f:
			data = json.load(f)
		if ("screenshots" in data) and (len(data["screenshots"]) > 0):
			continue
		print("Checking %s..." % data["slug"])

		# Some directories seem to have a PNG that is not connected
		if not ("screenshots" in data):
			data["screenshots"] = []
		for ext in ("*.png", "*.PNG"):
			for f in glob.glob(ext):
				if os.path.exists(f):
					data["screenshots"].append(f)
		if (len(data["screenshots"]) > 0):
			print("Found existing screenshots not tied to JSON.")
			with open('game.json', 'w') as f:
				json.dump(data, f, indent=4, sort_keys=True)
			continue

		# Generate screenshot
		rom_filename = locate_rom(data)
		if rom_filename is None:
			print("ROM not found, cannot generate screenshot!")
			still_missing.append(data["slug"])
			continue
		if not (Path(rom_filename).suffix in allowed_suffixes):
			print("Incompatible ROM suffix: %s" % Path(rom_filename).suffix)
			still_missing.append("%s: %s" % (data["slug"], Path(rom_filename).suffix))
			continue
		print("Generating screenshot...")
		
		clear_dir(tmp_dir)
		shutil.copyfile(rom_filename, tmp_dir / rom_filename)
		os.chdir(tmp_dir)
		subprocess.call([sameboy_tester_name, "--tga", rom_filename])

		bmp_path = Path(rom_filename).with_suffix(".tga")
		png_path = game_path / (Path(rom_filename).with_suffix(".png").name)
		if bmp_path.exists():
			subprocess.call(["convert", bmp_path.name, "-alpha", "off", str(png_path)])
			if png_path.exists():
				os.chdir(game_path)
				data["screenshots"].append(png_path.name)
				with open('game.json', 'w') as f:
					json.dump(data, f, indent=4, sort_keys=True)
			else:
				print("Error converting screenshot to PNG!")
				still_missing.append(data["slug"])
				continue
		else:
			print("Error generating screenshot!")
			still_missing.append(data["slug"])
			continue
	clear_dir(tmp_dir)

if len(still_missing) > 0:
	print("")
	print("*****")
	print("")
	print("The following entries are still missing screenshots:")
	for p in still_missing:
		print("- %s" % p)