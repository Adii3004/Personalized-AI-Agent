# src/main.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.shadowclone import run_shadowclone
from agent.update_memory import update_memory
from agent.memory_editor import edit_memory
from agent.format_profile import format_profile
from agent.summary import generate_summary
from agent.memory import rollback_memory, load_memory

def ensure_directories():
    """Ensure all necessary directories exist"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    dirs = [
        os.path.join(base_dir, "data"),
        os.path.join(base_dir, "data", "generated"),
        os.path.join(base_dir, "data", "generated", "applications"),
        os.path.join(base_dir, "data", "generated", "cover_letters"),
        os.path.join(base_dir, "data", "generated", "emails"),
        os.path.join(base_dir, "data", "generated", "letters"),
        os.path.join(base_dir, "data", "generated", "messages"),
        os.path.join(base_dir, "data", "generated", "misc")
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

def main():
    # Make sure all directories exist
    ensure_directories()
    
    # Check if memory.json exists, create if needed
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    memory_path = os.path.join(base_dir, "data", "memory.json")
    if not os.path.exists(memory_path):
        try:
            # Try to load memory (our updated load_memory will create default memory)
            load_memory()
        except Exception as e:
            print(f"Error initializing memory: {e}")
            return

    print(">> ShadowClone is ready. Type your command or 'exit' to quit.\n")

    while True:
        try:
            command = input(">> ShadowClone Command: ").strip()
            if command.lower() == "exit":
                print(">> Exiting ShadowClone. Goodbye!")
                break
            
            if not command:
                continue  # Skip empty commands

            # Manual memory edit commands (fallbacks)
            field_map = {
                "add experience": "roles",
                "add role": "roles",
                "add project": "projects",
                "update tone": "tone",
                "update goal": "goals",
                "update education": "education"
            }

            command_matched = False
            for key in field_map:
                if command.lower().startswith(key):
                    value = command[len(key):].strip()
                    if value:  # Only update if there's content after the command
                        update_memory(field_map[key], value)
                        print(f"\n>> ShadowClone Memory Update:\n{field_map[key].capitalize()} updated manually.")
                        command_matched = True
                    else:
                        print("\n>> ShadowClone Error: Missing value for update")
                    break
            
            if command_matched:
                continue

            # Handle rollback/undo
            if command.lower() in ["undo", "undo last update", "rollback", "delete last update"]:
                msg = rollback_memory()
                print("\n>> ShadowClone Memory Update:\n" + msg)
                continue

            # Handle profile view
            if command.lower() in ["show my profile", "view profile", "profile"]:
                print("\n>> ShadowClone Profile:\n")
                print(format_profile())
                continue

            # Handle summary
            if command.lower().startswith("summarize my profile"):
                style = "brief"
                if "linkedin" in command.lower():
                    style = "linkedin"
                elif "detailed" in command.lower():
                    style = "detailed"
                elif "casual" in command.lower():
                    style = "casual"
                print("\n>> ShadowClone Summary:\n")
                print(generate_summary(style))
                continue

            # If it's a writing prompt - prioritize this BEFORE memory edits
            if any(word in command.lower() for word in ["write", "generate", "draft", "create", "email", "application", "letter"]):
                context = input(">> Additional Context (optional): ").strip()
                run_shadowclone(command, context)
                continue

            # Handle natural language memory edits AFTER writing command check
            if any(word in command.lower() for word in ["add", "remove", "change", "update", "delete", "set"]):
                result = edit_memory(command)
                print("\n>> ShadowClone Memory Update:\n")
                print(result)
                continue

            # If none of the above, treat as general AI command
            context = input(">> Additional Context (optional): ").strip()
            run_shadowclone(command, context)
            
        except KeyboardInterrupt:
            print("\n>> Exiting ShadowClone. Goodbye!")
            break
        except Exception as e:
            print(f"\n>> Error: {str(e)}")
            print(">> ShadowClone encountered an error. Please try again.")

if __name__ == "__main__":
    main()