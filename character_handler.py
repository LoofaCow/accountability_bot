import json
import os
import time

CHARACTER_FILE = "characters.json"

def load_characters():
    """Load saved characters from file."""
    if not os.path.exists(CHARACTER_FILE):
        return []
    with open(CHARACTER_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    return data

def save_character(character):
    """
    Save a character.
    character: dict with keys:
      - id: unique identifier (timestamp)
      - title: a title for the character
      - description: the character's description
      - initial_message: the character's initial message
    """
    characters = load_characters()
    characters.append(character)
    with open(CHARACTER_FILE, "w") as f:
        json.dump(characters, f, indent=2)

def get_character_by_id(char_id):
    """Retrieve a character by its id."""
    characters = load_characters()
    for character in characters:
        if character.get("id") == char_id:
            return character
    return None
