from pathlib import Path
import json


def birthday_open_json():
    with open(Path(__file__).parent / "birthday_congratulations.json", encoding="utf-8") as f:
        return json.load(f)