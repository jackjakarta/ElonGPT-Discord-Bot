import json
from discord import Embed


def load_json(filename: str):
    try:
        if isinstance(filename, str):
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            raise ValueError("JSON file path must be a string!")
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        with open(filename, 'w') as file:
            json.dump([], file)
        return []


def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def create_embed(title, description, color=0x4BA081):
    """Create a Discord embed."""
    return Embed(title=title, description=description, color=color)
