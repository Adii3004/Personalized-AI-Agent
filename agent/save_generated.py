# agent/save_generated.py

import os
from datetime import datetime

def save_response(command, response):
    # Basic type detection from command
    if "cover letter" in command.lower():
        folder = "cover_letters"
    elif "email" in command.lower():
        folder = "emails"
    elif "message" in command.lower():
        folder = "messages"
    elif "application" in command.lower():
        folder = "applications"
    elif "letter" in command.lower():
        folder = "letters"
    else:
        folder = "misc"

    # Fix path handling to use consistent directory structure
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(BASE_DIR, "data", "generated", folder)
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{timestamp}.txt"
    filepath = os.path.join(save_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response)

    print(f"\n>> Saved to {filepath}")
    return filepath