"""
Validate every game manifest and event manifest against their JSON schemas.
"""

import json
import os
import progressbar
import sys

from jsonschema import validate, ValidationError


def validate_folder(schema_path, path, manifest):
    with open(schema_path) as f:
        schema = json.load(f)

    errors = 0

    for item in progressbar.progressbar(os.listdir(path), redirect_stdout=True):
        try:
            with open(f"{path}{item}/{manifest}") as f:
                metadata = json.load(f)

            validate(metadata, schema)
        except Exception as e:
            errors += 1
            print(f"Failed {item}: \n {e}")

    return errors


game_errors = validate_folder("../schemas/game-schema-d5.json", "../entries/", "game.json")
event_errors = validate_folder("../schemas/event-schema-d1.json", "../events/", "event.json")

if game_errors > 0:
    print(f"\n {game_errors} entrie(s) have failed validation")
if event_errors > 0:
    print(f"\n {event_errors} event(s) have failed validation")
if game_errors + event_errors > 0:
    sys.exit(1)
