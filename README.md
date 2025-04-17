**ShadowClone – Agent Documentation** 

**Overview**

**ShadowClone** is a personalized AI agent that mimics a user’s tone, writing style, memory, and professional background to generate high-context content like cover letters, applications, summaries, and more. Designed as a productivity assistant for students, job seekers, and professionals, ShadowClone blends memory management, natural language interaction, and dynamic content creation into one unified agent.

It supports both **Command Line Interface (CLI)** interaction and **REST API access (Flask)**, allowing users to interact programmatically or casually through natural language. It’s optimized for agent deployment on platforms, with full memory control, rollback support, and contextual LLM responses.

**Functional Capabilities**

**1. Writing Assistant**

Generates tailored responses based on user memory. Supports generation of:

- Cover letters
- Applications
- Emails
- Formal or casual letters
- Professional summaries

The output reflects the persona’s background and memory context such as goals, projects, and achievements.

-----
**2. Memory Management System**

A core JSON memory file (data/memory.json) stores structured info about the user. It includes:

- roles – e.g., "Project Head at XYZ"
- projects – key projects with short descriptions
- goals – current objectives
- achievements – highlights and milestones
- background – educational and personal context
- tone – sets the overall writing tone
- experience – internships, volunteering, etc.

Users can:

- Add new entries (e.g., “Add my internship at Turing”)
- Update existing entries (e.g., “Change my goal to ML research”)
- Delete entries (e.g., “Remove project head role”)
- Roll back last update (e.g., “Undo”)

All of these work via **natural language commands**, with robust parsing handled in the backend.

-----
**3. Natural Language Interface**

ShadowClone supports flexible inputs like:

- “Add my internship at Google”
- “Write a detailed cover letter for Microsoft”
- “Update my tone to casual”
- “Summarize my profile in a LinkedIn tone”
- “Delete the achievement about hackathon”

It intelligently parses intent using an LLM-powered internal parser and routes the action to the memory or generation engine accordingly.

-----
**4. Web API (Flask-based)**

For remote interaction or integration with platforms, a RESTful Flask API is included:

- POST /run → Generate writing with memory context
- GET /profile → Return current memory in formatted profile
- GET /summarize?style=linkedin|brief|detailed → Get summary
- POST /edit → Update memory via natural language
- POST /rollback → Undo last memory edit

Auth is mock-handled using User-Token headers.

-----
**5. Prompt Engineering**

Every writing task sends:

- A system prompt to define the role of the agent
- Contextual memory
- The user’s request (command)

LLM calls are routed via **OpenRouter** to meta-llama/llama-4-scout:free, ensuring high-quality, context-aware generation without excessive cost.

-----
**Technologies Used**

|**Layer**|**Tech / Package**|**Purpose**|
| :- | :- | :- |
|Web server|Flask|REST API layer|
|LLM connection|requests, OpenRouter API|Chat-based model calls|
|Prompt management|Custom prompt builder|Inject memory + structure requests|
|Memory system|JSON|Read/write/update/rollback memory|
|Config management|python-dotenv|Secure API key handling|
|CLI support|Built-in input() + logic|For quick local testing|
|Logging (optional)|rich|CLI formatting|
|Testing |pytest|Dev and code quality tools|

-----
**Extensibility**

ShadowClone can easily be extended to:

- Add UI (Streamlit, Flask + React)
- Include database persistence (MongoDB, SQLite)
- Integrate with resume parsers or ATS systems
- Generate PDFs or formatted DOCX files
- Be deployed as a Dockerized microservice
-----
**Use Case**

Perfect for:

- Final-year students preparing internship/job applications
- Professionals automating personal branding
- Agents that adapt and evolve with memory

