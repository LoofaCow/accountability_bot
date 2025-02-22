# memory_handeling.py

import json
import os
import time

CHAT_HISTORY_FILE = "chat_history.json"

def load_chat_history():
    """Load the list of saved chats from the file."""
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []
    with open(CHAT_HISTORY_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    return data

def save_chat_history(chat_thread):
    """
    Save a chat thread. 
    chat_thread is expected to be a dict with at least:
      - id: unique id (we'll use a timestamp here)
      - title: a title for the chat
      - conversation: the conversation history (list)
    """
    chats = load_chat_history()
    chats.append(chat_thread)
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(chats, f, indent=2)

def get_chat_by_id(chat_id):
    """Retrieve a saved chat thread by its id."""
    chats = load_chat_history()
    for chat in chats:
        if chat.get("id") == chat_id:
            return chat
    return None
