import json
import os


def lowercase_slug_json_and_rename_folders(folder_path):
    # Loop through each item in the given folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        # Check if the item is a folder/directory
        if os.path.isdir(item_path):
            # Generate new name with lowercase for the folder
            new_name = item.lower()
            new_path = os.path.join(folder_path, new_name)

            if new_name != item:
                # Path to the "game.json" file inside the folder
                game_json_path = os.path.join(item_path, "game.json")
                # Check if "game.json" exists in the folder
                if os.path.exists(game_json_path):
                    # Open and update "game.json" file
                    with open(game_json_path, "r+") as file:
                        game_data = json.load(file)
                        # Update the "slug" field with the new folder name
                        game_data["slug"] = new_name
                        # Move the file pointer to the beginning and truncate the file
                        file.seek(0)
                        json.dump(game_data, file, ensure_ascii=False, indent=4)
                        file.truncate()
                    print(f"Updated 'slug' in '{game_json_path}' to '{new_name}'")

                # Rename the folder to the new lowercase name
                os.rename(item_path, new_path)
                print(f"Renamed folder '{item}' to '{new_name}'")


# Example usage:
# Replace 'your_folder_path' with the actual path of your folder
folder_path = "../entries"
lowercase_slug_json_and_rename_folders(folder_path)
