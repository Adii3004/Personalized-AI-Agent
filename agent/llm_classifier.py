# agent/llm_classifier.py

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def classify_memory_update(command):
    if not OPENROUTER_API_KEY:
        print("❌ Error: OPENROUTER_API_KEY environment variable not set.")
        return {"field": "none"}
        
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "ShadowClone-Memory",
    }

    system_prompt = """
You are an assistant that parses user commands to edit their memory profile.

Your task is to extract ONLY the JSON object that defines the memory update.

Return a JSON object with:
- field: one of [tone, goals, education, projects, roles]
- action: one of [add, update, remove]
- value: cleaned string the user wants to add or update

Examples:
Input: "I was a research intern at Razorpay"
Output: { "field": "roles", "action": "add", "value": "Research intern at Razorpay" }

Input: "Remove my role as project head"
Output: { "field": "roles", "action": "remove", "value": "Project Head" }

Do NOT wrap the JSON in code blocks. Do NOT add any explanation or context. Only return the raw JSON object.
"""
    data = {
        "model": "meta-llama/llama-4-scout:free",
        "messages": [
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": command }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"LLM classification failed: {response.status_code}")
            return { "field": "none" }

        content = response.json()["choices"][0]["message"]["content"].strip()
        print("🔍 Raw LLM response:", repr(content))

        try:
            # Better JSON extraction with error tolerance
            if '{' in content and '}' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                cleaned_json = content[start:end]
                parsed = json.loads(cleaned_json)
                
                # Validate fields and provide default values if needed
                if "field" not in parsed or parsed["field"] not in ["tone", "goals", "education", "projects", "roles"]:
                    print("⚠️ Invalid field in parsed JSON")
                    return { "field": "none" }
                if "action" not in parsed or parsed["action"] not in ["add", "update", "remove", "delete"]:
                    parsed["action"] = "add"  # Default to add if action is missing or invalid
                if "value" not in parsed or not parsed["value"]:
                    print("⚠️ Missing value in parsed JSON")
                    return { "field": "none" }
                    
                return parsed
            else:
                print("⚠️ No JSON object found in response")
                return { "field": "none" }
        except Exception as e:
            print(f"⚠️ Parsing error: {e}")
            return { "field": "none" }

    except Exception as e:
        print(f"❌ LLM request failed: {e}")
        return { "field": "none" }