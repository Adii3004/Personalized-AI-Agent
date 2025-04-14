from agent.memory import load_memory

def generate_summary(style="brief"):
    memory = load_memory()

    tone = memory.get("tone", "neutral")
    goals = memory.get("goals", "")
    education = memory.get("education", "")
    roles = memory.get("roles", [])
    projects = memory.get("projects", [])

    if style == "linkedin":
        return _linkedin_style(education, roles, projects, goals, tone)
    elif style == "detailed":
        return _detailed_style(education, roles, projects, goals, tone)
    elif style == "casual":
        return _casual_style(education, roles, projects, goals, tone)
    else:
        return _brief_style(education, roles, projects, goals, tone)


def _brief_style(education, roles, projects, goals, tone):
    summary = ["🔹 Brief Profile Summary 🔹"]
    if education:
        summary.append(f"🎓 Education: {education}")
    if roles:
        summary.append("💼 Roles:")
        summary.extend([f"   - {r}" for r in roles])
    if projects:
        summary.append("🛠️ Projects:")
        summary.extend([f"   - {p}" for p in projects])
    if goals:
        summary.append(f"🎯 Goals: {goals}")
    summary.append(f"🗣️ Tone: {tone}")
    return "\n".join(summary)


def _detailed_style(education, roles, projects, goals, tone):
    summary = ["Here's a detailed summary of your profile:\n"]
    if education:
        summary.append(f"You have an academic background in {education}.")
    if roles:
        summary.append("You've gained hands-on experience through roles such as:")
        summary.extend([f"- {r}" for r in roles])
    if projects:
        summary.append("Your project portfolio includes:")
        summary.extend([f"- {p}" for p in projects])
    if goals:
        summary.append(f"You’re currently focused on: {goals}.")
    summary.append(f"Your communication tone is best described as: {tone}.")
    return "\n".join(summary)


def _linkedin_style(education, roles, projects, goals, tone):
    summary = ["🔗 LinkedIn-Style Summary 🔗\n"]
    if education:
        summary.append(f"{education}")
    if roles:
        summary.append(f"Experienced in roles such as " + ", ".join(roles) + ".")
    if projects:
        summary.append("Built projects like " + ", ".join(projects) + ".")
    if goals:
        summary.append(f"Currently aiming to {goals}.")
    summary.append(f"Communicates with a {tone} tone.")
    return "\n".join(summary)


def _casual_style(education, roles, projects, goals, tone):
    summary = ["😎 Your Profile, the Chill Way 😎\n"]
    if education:
        summary.append(f"Studied at: {education}")
    if roles:
        summary.append("Tried out some cool roles like:")
        summary.extend([f"👉 {r}" for r in roles])
    if projects:
        summary.append("Built stuff like:")
        summary.extend([f"🚀 {p}" for p in projects])
    if goals:
        summary.append(f"Right now, you're vibing toward: {goals}")
    summary.append(f"Vibes? Definitely {tone}.")
    return "\n".join(summary)
