# Script requires ImageMagick and Python Pillow installed.
# sameboy_tester can be in PATH or provided as the first argument
# (build with "make tester" in SameBoy source code)

import glob
import json
import os
import os.path
from pathlib import Path
from PIL import Image
import shutil
import subprocess
import sys
import tempfile
import traceback

sameboy_tester_name = "sameboy_tester"
if len(sys.argv) > 1:
	sameboy_tester_name = sys.argv[1]

def image_all_solid_color(im):
	first_pixel = im.getpixel((0, 0))
	for iy in range(0, im.height):
		for ix in range(0, im.width):
			if im.getpixel((ix, iy)) != first_pixel:
				return False
	return True

def is_screenshot_png_valid(filename):
	try:
		with Image.open(str(filename)) as im:
			if (im.width < 1) or (im.height < 1):
				return False
			if image_all_solid_color(im):
				return False
			return True
	except:
		return False

screenshot_generators = {}

def generate_screenshot_sameboy(input_file, output_file):
	tester_out_path = input_file.with_suffix(".tga")
	subprocess.call([sameboy_tester_name, "--tga", str(input_file)])

	if tester_out_path.exists():
		subprocess.call(["convert", tester_out_path.name, "-alpha", "off", str(output_file)])
		if output_file.exists():
			if not is_screenshot_png_valid(output_file):
				os.remove(str(tester_out_path))
				os.remove(str(output_file))

				subprocess.call([sameboy_tester_name, "--start", "--tga", str(input_file)])

				if tester_out_path.exists():
					subprocess.call(["convert", tester_out_path.name, "-alpha", "off", str(output_file)])
					if output_file.exists():
						if not is_screenshot_png_valid(output_file):
							os.remove(str(output_file))
							return False
						else:
							return True
			else:
				return True

	return False

screenshot_generators[".gb"] = generate_screenshot_sameboy
screenshot_generators[".gbc"] = generate_screenshot_sameboy
screenshot_generators[".cgb"] = generate_screenshot_sameboy

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
		rom_suffix = Path(rom_filename).suffix.lower()
		if not (rom_suffix in screenshot_generators):
			print("Error generating screenshot - incompatible type - %s" % rom_suffix)
			still_missing.append("%s: Incompatible type - %s" % (data["slug"], rom_suffix))
			continue
		print("Generating screenshot...")
		
		clear_dir(tmp_dir)
		shutil.copyfile(rom_filename, tmp_dir / rom_filename)
		os.chdir(tmp_dir)

		png_path = game_path / (Path(rom_filename).with_suffix(".png").name)
		try:
			if screenshot_generators[rom_suffix](Path(rom_filename), png_path) and png_path.exists():
				os.chdir(game_path)
				data["screenshots"].append(png_path.name)
				with open('game.json', 'w') as f:
					json.dump(data, f, indent=4, sort_keys=True)
			else:
				print("Error converting screenshot to PNG - invalid results")
				still_missing.append("%s: Invalid results" % data["slug"])
				continue
		except Exception:
			print("Error converting screenshot to PNG - Python exception:")
			traceback.print_exc()
			still_missing.append("%s: Python exception/script error" % data["slug"])
			continue
	clear_dir(tmp_dir)

if len(still_missing) > 0:
	print("")
	print("*****")
	print("")
	print("The following entries are still missing screenshots:")
	for p in still_missing:
		print("- %s" % p)
