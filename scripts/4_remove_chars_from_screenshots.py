#!/usr/bin/env python3
"""
Script to remove '%' characters from screenshot filenames in game.json files.
Processes all subfolders in the 'entries' folder, updating both the JSON and renaming files on disk.
"""

import json
import os
from pathlib import Path

def process_entries_folder(entries_path):
    """Process all subfolders in the entries folder."""
    entries_dir = Path(entries_path)
    
    if not entries_dir.exists():
        print(f"Error: Entries folder '{entries_path}' does not exist")
        return
    
    processed_count = 0
    renamed_count = 0
    
    # Iterate through all subfolders
    for subfolder in entries_dir.iterdir():
        if not subfolder.is_dir():
            continue
        
        game_json_path = subfolder / "game.json"
        
        if not game_json_path.exists():
            continue
        
        # Load game.json
        try:
            with open(game_json_path, 'r', encoding='utf-8') as f:
                game_data = json.load(f)
        except Exception as e:
            print(f"Error reading {game_json_path}: {e}")
            continue
        
        # Check if screenshots property exists
        if 'screenshots' not in game_data or not isinstance(game_data['screenshots'], list):
            continue
        
        screenshots = game_data['screenshots']
        updated = False
        
        # Process each screenshot entry
        for i, screenshot in enumerate(screenshots):
            if '%' in screenshot:
                # Remove '%' from the filename
                new_screenshot = screenshot.replace('%', '')
                
                # Get full paths for renaming the actual file
                old_file_path = subfolder / screenshot
                new_file_path = subfolder / new_screenshot
                
                # Rename the file on disk if it exists
                if old_file_path.exists():
                    try:
                        old_file_path.rename(new_file_path)
                        print(f"Renamed: {old_file_path} -> {new_file_path}")
                        renamed_count += 1
                    except Exception as e:
                        print(f"Error renaming {old_file_path}: {e}")
                else:
                    print(f"Warning: File not found: {old_file_path}")
                
                # Update the JSON entry
                screenshots[i] = new_screenshot
                updated = True
        
        # Save the updated game.json if changes were made
        if updated:
            try:
                with open(game_json_path, 'w', encoding='utf-8') as f:
                    json.dump(game_data, f, indent=4, ensure_ascii=False)
                    f.write('\n')  # Add newline at end of file
                print(f"Updated: {game_json_path}")
                processed_count += 1
            except Exception as e:
                print(f"Error writing {game_json_path}: {e}")
    
    print(f"\nSummary:")
    print(f"  - Updated {processed_count} game.json file(s)")
    print(f"  - Renamed {renamed_count} file(s) on disk")

if __name__ == "__main__":
    entries_folder = "../entries"
    process_entries_folder(entries_folder)
