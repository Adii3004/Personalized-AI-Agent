# agent/memory_editor.py

import re
from agent.memory import load_memory, save_memory, backup_memory
from agent.llm_classifier import classify_memory_update

def edit_memory(command):
    """Process natural language commands to edit memory"""
    
    # First try the LLM-based classifier
    update = classify_memory_update(command)
    
    field = update.get("field")
    action = update.get("action")
    value = update.get("value")
    
    # If LLM classifier worked, process the structured update
    if field != "none":
        return process_structured_update(field, action, value)
    
    # Fallback to regex-based parsing if LLM classifier failed
    return regex_edit_memory(command)

def process_structured_update(field, action, value):
    """Process a structured update from the LLM classifier"""
    backup_memory()  # Always backup before changes
    memory = load_memory()
    
    # Handle single value fields
    if field in ["tone", "goals", "education"]:
        if action in ["add", "update", "set"]:
            memory[field] = value
            save_memory(memory)
            return f"✅ {field.capitalize()} updated to: {value}"
        elif action in ["remove", "delete"]:
            memory[field] = ""
            save_memory(memory)
            return f"✅ {field.capitalize()} removed"
        else:
            return f"⚠️ Cannot {action} {field}. Use 'update' instead."
    
    # Handle list fields
    if field in ["projects", "roles"]:
        if action in ["add", "update", "set"]:
            if field not in memory:
                memory[field] = []
            memory[field].append(value)
            save_memory(memory)
            return f"➕ {field[:-1].capitalize()} added: {value}"
        elif action in ["remove", "delete"]:
            if field not in memory:
                return f"⚠️ No such field: {field}"
                
            original_len = len(memory[field])
            memory[field] = [item for item in memory[field] if value.lower() not in item.lower()]
            removed_count = original_len - len(memory[field])
            save_memory(memory)
            
            if removed_count == 0:
                return f"⚠️ No match found to remove: {value}"
            return f"🗑️ Removed {removed_count} item(s) from {field} matching: {value}"
        else:
            return f"⚠️ Unknown action: {action} for {field}."
    
    return "⚠️ Unrecognized memory field."

def regex_edit_memory(command):
    """Fallback to regex parsing for memory edits"""
    backup_memory()  # Always backup before changes
    memory = load_memory()
    command_lower = command.lower()

    # Match tone updates
    tone_patterns = [
        r"(?:change|update|set) (?:my )?tone (?:to|as)? (.+)",
        r"my tone (?:is|should be) (.+)"
    ]
    for pattern in tone_patterns:
        match = re.search(pattern, command_lower)
        if match:
            new_tone = match.group(1).strip()
            memory['tone'] = new_tone
            save_memory(memory)
            return f"🗣️ Tone updated to: {new_tone}"

    # Match project additions
    project_patterns = [
        r"(?:add|include|create) (?:a )?project(?: called)? (.+)",
        r"i (?:made|built|created|developed) (?:a )?project(?: called)? (.+)"
    ]
    for pattern in project_patterns:
        match = re.search(pattern, command_lower)
        if match:
            new_project = match.group(1).strip()
            if 'projects' not in memory:
                memory['projects'] = []
            memory['projects'].append(new_project)
            save_memory(memory)
            return f"📁 Project added: {new_project}"

    # Match role/experience additions
    role_patterns = [
        r"(?:add|include) (?:a )?role(?: as)? (.+)",
        r"(?:i )?(?:worked|served|was employed|interned)(?: as)? (.+?)(?:\.|,|$)"
    ]
    for pattern in role_patterns:
        match = re.search(pattern, command_lower)
        if match:
            new_role = match.group(1).strip()
            if 'roles' not in memory:
                memory['roles'] = []
            memory['roles'].append(new_role)
            save_memory(memory)
            return f"💼 Role/Experience added: {new_role}"
    
    # Match education updates
    edu_patterns = [
        r"(?:change|update|set) (?:my )?education(?: to)? (.+)",
        r"my education (?:is|should be) (.+)"
    ]
    for pattern in edu_patterns:
        match = re.search(pattern, command_lower)
        if match:
            new_edu = match.group(1).strip()
            memory['education'] = new_edu
            save_memory(memory)
            return f"🎓 Education updated to: {new_edu}"

    # Match goal updates
    goal_patterns = [
        r"(?:change|update|set) (?:my )?goals?(?: to)? (.+)",
        r"my goals? (?:is|are|should be) (.+)"
    ]
    for pattern in goal_patterns:
        match = re.search(pattern, command_lower)
        if match:
            new_goal = match.group(1).strip()
            memory['goals'] = new_goal
            save_memory(memory)
            return f"🎯 Goals updated to: {new_goal}"

    # Match project removals
    remove_patterns = [
        r"(?:remove|delete) project (.+)",
        r"(?:remove|delete) role (.+)"
    ]
    for pattern in remove_patterns:
        match = re.search(pattern, command_lower)
        if match:
            target = match.group(1).strip().lower()
            field = 'projects' if 'project' in pattern else 'roles'
            
            if field not in memory:
                return f"⚠️ No {field} exist in memory"
                
            original_len = len(memory[field])
            memory[field] = [item for item in memory[field] if target not in item.lower()]
            removed_count = original_len - len(memory[field])
            save_memory(memory)
            
            if removed_count == 0:
                return f"⚠️ No {field} containing '{target}' found to remove"
            return f"🗑️ Removed {removed_count} item(s) from {field} containing: {target}"

    return "No valid memory update command found."