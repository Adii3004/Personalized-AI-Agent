# setup.py

import os
import json
import sys

def ensure_project_structure():
    """Create all required directories and initialize memory file if needed"""
    
    # Base directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    generated_dir = os.path.join(base_dir, "data", "generated")
    
    # Create base directories
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(generated_dir, exist_ok=True)
    
    # Create generated content folders
    content_folders = [
        "applications",
        "cover_letters", 
        "emails",
        "letters",
        "messages",
        "misc"
    ]
    
    for folder in content_folders:
        os.makedirs(os.path.join(generated_dir, folder), exist_ok=True)
    
    # Initialize memory.json if it doesn't exist
    memory_path = os.path.join(data_dir, "memory.json")
    if not os.path.exists(memory_path):
        initial_memory = {
            "tone": "professional and confident",
            "goals": "secure a software engineering role at a tech company",
            "education": "Computer Science undergraduate",
            "projects": [],
            "roles": []
        }
        
        with open(memory_path, "w") as f:
            json.dump(initial_memory, f, indent=2)
        print(f"Created initial memory.json at {memory_path}")
    else:
        print(f"memory.json already exists at {memory_path}")
    
    print("\nProject structure initialized!")
    print("\nDirectories created:")
    print(f"- {data_dir}")
    print(f"- {generated_dir}")
    for folder in content_folders:
        print(f"  - {os.path.join('data/generated', folder)}")
    
    # Check if .env file exists
    env_path = os.path.join(base_dir, ".env")
    if not os.path.exists(env_path):
        print("\nWARNING: No .env file found!")
        print("Create a .env file with your OpenRouter API key:")
        print('OPENROUTER_API_KEY="your-key-here"')

if __name__ == "__main__":
    ensure_project_structure()
    print("\nSetup complete! You can now run ShadowClone.")