from agent.memory import load_memory

from agent.memory import load_memory

def build_prompt(command, context, memory=None):
    long_term = load_memory()
    if memory is None:
        memory = []

    # 🔹 Allow overrides if user updated tone/goals/education during the session
    override = {"tone": None, "goals": None, "education": None}
    for turn in memory:
        content = turn["command"].lower()
        if "tone" in content:
            override["tone"] = turn["command"].split(":", 1)[-1].strip()
        if "goal" in content:
            override["goals"] = turn["command"].split(":", 1)[-1].strip()
        if "education" in content:
            override["education"] = turn["command"].split(":", 1)[-1].strip()

    # 🔹 Use override if present, else fallback to long-term memory
    tone = override["tone"] if override["tone"] else long_term["tone"]
    goals = override["goals"] if override["goals"] else long_term["goals"]
    education = override["education"] if override["education"] else long_term["education"]
    roles = "\n".join(f"- {role}" for role in long_term["roles"])
    projects = "\n".join(f"- {project}" for project in long_term["projects"])

    background = f"""
You are ShadowClone, an AI that writes exactly like <YOUR_NAME>, a final-year Computer Science student. Write everything in first-person as her.

Tone: {tone}
Goals: {goals}
Education: {education}

Projects:
{projects}

Roles and Achievements:
{roles}
"""

    messages = [{"role": "system", "content": background}]

    for turn in memory:
        messages.append({"role": "user", "content": turn["command"]})
        messages.append({"role": "assistant", "content": turn["response"]})

    messages.append({"role": "user", "content": f"{command}\n\nContext: {context}"})

    return messages