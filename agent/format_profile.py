# agent/format_profile.py

from agent.memory import load_memory

def format_profile():
    memory = load_memory()

    tone = memory.get("tone", "N/A")
    goals = memory.get("goals", "N/A")
    education = memory.get("education", "N/A")
    projects = memory.get("projects", [])
    roles = memory.get("roles", [])

    profile = f"""
ShadowClone Memory Snapshot:

Tone:
{tone}

Goals:
{goals}

Education:
{education}

Projects:
""" + "\n".join(f"  - {p}" for p in projects) + """

Roles:
""" + "\n".join(f"  - {r}" for r in roles)

    return profile.strip()
