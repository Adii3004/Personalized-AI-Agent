# agent/shadowclone.py

import os
import requests
import json
from agent.prompt_builder import build_prompt
from dotenv import load_dotenv
from agent.save_generated import save_response
from agent.retrieve_generated import retrieve_response
from agent.memory_editor import edit_memory
from agent.memory import add_to_memory, get_memory

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def run_shadowclone(command, context=None):
    # Validate API key first
    if not OPENROUTER_API_KEY:
        print("\nError: OPENROUTER_API_KEY environment variable not set.")
        return "API key not configured. Please set the OPENROUTER_API_KEY environment variable."

    # Handle retrieval-type commands first
    if any(word in command.lower() for word in ["show", "list", "read", "see", "what was my"]):
        retrieved = retrieve_response(command)
        print("\n>> ShadowClone Retrieved Response:\n")
        print(retrieved)
        return retrieved
    
     # Handle rollback commands explicitly
    if command.lower() in ["undo", "undo last update", "rollback", "delete last update", "rollback last update"]:
        from agent.memory import rollback_memory
        result = rollback_memory()
        print(f"\n>> ShadowClone Memory Update:\n{result}")
        return result
        
    # Handle writing/generation commands BEFORE memory edits
    # This fixes the issue where "write an application" was being classified as a memory update
    if any(word in command.lower() for word in ["write", "generate", "draft", "create", "email", "application", "letter"]):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "ShadowClone",
        }
        
        # Build prompt with memory
        past_memory = get_memory()
        messages = build_prompt(command, context, memory=past_memory)

        data = {
            "model": "meta-llama/llama-4-scout:free",
            "messages": messages
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                text = response.json()["choices"][0]["message"]["content"].strip()

                # Append signature if formal
                if any(word in command.lower() for word in ["cover letter", "email", "application", "letter"]):
                    if not text.lower().endswith("<YOUR_NAME>"):
                        text += "\n\nSincerely,\n<YOUR_NAME>"
                    
                    # Only save formal stuff
                    save_response(command, text)

                print("\n>> ShadowClone Response:\n")
                print(text)

                add_to_memory(command, text)  # Save interaction to memory
                return text
            else:
                error_msg = f"Request failed: {response.status_code}\n{response.text}"
                print(error_msg)
                return error_msg
        except Exception as e:
            error_msg = f"Connection error: {str(e)}"
            print(error_msg)
            return error_msg

    # Handle memory edit commands AFTER writing checks
    memory_result = edit_memory(command)
    if memory_result != "No valid memory update command found.":
        print("\n>> ShadowClone Memory Update:\n")
        print(memory_result)
        return memory_result

    # If not a retrieval, writing, or memory command, treat as general query
    # Build prompt with memory
    past_memory = get_memory()
    messages = build_prompt(command, context, memory=past_memory)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "ShadowClone",
    }

    data = {
        "model": "meta-llama/llama-4-scout:free",
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            text = response.json()["choices"][0]["message"]["content"].strip()

            print("\n>> ShadowClone Response:\n")
            print(text)

            add_to_memory(command, text)  # Save interaction to memory
            return text
        else:
            error_msg = f"Request failed: {response.status_code}\n{response.text}"
            print(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"Connection error: {str(e)}"
        print(error_msg)
        return error_msg