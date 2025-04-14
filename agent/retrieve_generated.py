# agent/retrieve_generated.py

import os

def retrieve_response(command):
    # Fix path handling to be more consistent
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(BASE_DIR, "data", "generated")
    
    # Ensure the directory exists
    os.makedirs(base_dir, exist_ok=True)

    category_map = {
        "cover letter": "cover_letters",
        "cover letters": "cover_letters",
        "email": "emails",
        "emails": "emails",
        "application": "applications",
        "applications" : "applications",
        "message" : "messages",
        "messages" : "messages",
        "letter": "letters",
        "letters" : "letters",
        "goal" : "misc",
        "goals" : "misc",
        "aim" : "misc",
        "aims" : "misc"
    }

    matched_category = None
    for keyword, folder in category_map.items():
        if keyword in command.lower():
            matched_category = folder
            break

    if not matched_category:
        return "No matching category found in saved responses."

    folder_path = os.path.join(base_dir, matched_category)
    print(f"[DEBUG] Folder path: {folder_path}")
    
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    try:
        files = sorted(os.listdir(folder_path), reverse=True)
        print(f"[DEBUG] Files found: {files}")
        if not files:
            return f"No saved {matched_category} responses found."

        latest_file = os.path.join(folder_path, files[0])
        with open(latest_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error retrieving files: {e}")
        return f"Error retrieving {matched_category} responses."