import json
from discord import Embed


def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def create_embed(title, description, color=0x4BA081):
    """Create a Discord embed."""
    return Embed(title=title, description=description, color=color)
