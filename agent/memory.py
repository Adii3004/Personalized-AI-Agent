# agent/memory.py

import json
import os
import copy

# Fix path handling with consistent approach
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_PATH = os.path.join(BASE_DIR, "data", "memory.json")

# 🔁 In-memory store for rollback
memory_history = []

def load_memory():
    """Load the memory JSON file."""
    try:
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize with default structure if file doesn't exist or is invalid
        default_memory = {
            "tone": "professional and confident",
            "goals": "secure a software engineering role at a tech company",
            "education": "Computer Science undergraduate",
            "projects": [],
            "roles": []
        }
        save_memory(default_memory)
        return default_memory

def save_memory(memory):
    """Save the memory to disk."""
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def backup_memory():
    """Create a deep backup of current memory before changes."""
    current = load_memory()
    memory_history.append(copy.deepcopy(current))

def rollback_memory():
    """Undo or rollback the last memory update."""
    if memory_history:
        previous = memory_history.pop()
        save_memory(previous)
        return "✅ Last memory update has been undone."
    return "⚠️ No memory update to undo."

def update_field(field, value):
    """Update a single-value field like tone, goals, education."""
    backup_memory()
    memory = load_memory()
    memory[field] = value
    save_memory(memory)
    return f"✅ {field.capitalize()} updated to: {value}"

def add_to_list(field, value):
    """Add a value to a list field like projects or roles."""
    backup_memory()
    memory = load_memory()
    if field not in memory:
        memory[field] = []
    memory[field].append(value)
    save_memory(memory)
    return f"➕ {field[:-1].capitalize()} added: {value}"

def remove_from_list(field, value):
    """Remove matching values from a list field like projects or roles."""
    backup_memory()
    memory = load_memory()
    if field not in memory:
        return f"⚠️ No such field: {field}"

    original_len = len(memory[field])
    memory[field] = [item for item in memory[field] if value.lower() not in item.lower()]
    removed_count = original_len - len(memory[field])
    save_memory(memory)

    if removed_count == 0:
        return f"⚠️ No match found to remove: {value}"
    return f"🗑️ Removed {removed_count} item(s) from {field} matching: {value}"

def get_background_section(key):
    """Helper to get sections from memory."""
    memory = load_memory()
    return memory.get(key, "No information found.")

def get_memory():
    """Retrieve the last 3 memory update commands (stub)."""
    # If needed, integrate command history here
    return memory_history[-3:] if memory_history else []

command_log = []
def add_to_memory(command, response):
    command_log.append({"command": command, "response": response})