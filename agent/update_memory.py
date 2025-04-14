# agent/update_memory.py

import json
import os
from agent.memory import backup_memory  # Add this import

# Fix path handling
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_PATH = os.path.join(BASE_DIR, "data", "memory.json")

def update_memory(field, value):
    if not os.path.exists(MEMORY_PATH):
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
        
        memory = {
            "history": [],
            "education": "",
            "projects": [],
            "roles": [],
            "goals": "",
            "tone": ""
        }
    else:
        try:
            with open(MEMORY_PATH, "r") as f:
                memory = json.load(f)
        except json.JSONDecodeError:
            # Handle corrupt JSON file
            print("Warning: Memory file corrupted, creating new one")
            memory = {
                "history": [],
                "education": "",
                "projects": [],
                "roles": [],
                "goals": "",
                "tone": ""
            }

    # Create a backup before making changes
    backup_memory()  # Add this line

    if field in ["projects", "roles"]:
        if field not in memory:
            memory[field] = []
        memory[field].append(value)
    elif field in ["tone", "goals", "education"]:
        memory[field] = value
    else:
        print(f"Unknown field: {field}")
        return

    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)
    
    print(f">> Updated {field} with: {value}")