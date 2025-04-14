# src/server.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
import os
from agent.shadowclone import run_shadowclone
from agent.memory import load_memory, rollback_memory
from agent.summary import generate_summary
from agent.format_profile import format_profile
from agent.memory_editor import edit_memory

app = Flask(__name__)

AGENT_ID = os.getenv("AGENT_ID", "test-agent-id")
CREATOR_API_KEY = os.getenv("CREATOR_API_KEY", "test-api-key")


def check_user_credits(user_token):
    # Mock logic for local testing — always allow
    if user_token:
        return {"status": "allowed"}
    return {"status": "error", "message": "Missing token"}


@app.route("/", methods=["GET"])
def home():
    return "Welcome to ShadowClone – Your Personalized AI Agent!"


@app.route("/run", methods=["POST"])
def run():
    auth_status = check_user_credits(request.headers.get("User-Token"))
    if auth_status.get("status") != "allowed":
        return jsonify({"error": "Unauthorized or insufficient credits"}), 403

    data = request.json or {}
    command = data.get("command", "")
    context = data.get("context", "")
    result = run_shadowclone(command, context)
    return jsonify({"result": result})


@app.route("/profile", methods=["GET"])
def profile():
    return jsonify({"profile": format_profile()})


@app.route("/summarize", methods=["GET"])
def summarize():
    style = request.args.get("style", "brief")
    return jsonify({"summary": generate_summary(style)})


@app.route("/edit", methods=["POST"])
def edit():
    command = request.json.get("command", "")
    result = edit_memory(command)
    return jsonify({"result": result})


@app.route("/rollback", methods=["POST"])
def rollback():
    result = rollback_memory()
    return jsonify({"result": result})


@app.route("/docs", methods=["GET"])
def docs():
    return """
    ShadowClone API Routes:
    - GET / → Welcome message
    - POST /run {command, context?} → Execute ShadowClone
    - GET /profile → View user profile
    - GET /summarize?style=brief|detailed|linkedin|casual → Get summary
    - POST /edit {command} → Memory update
    - POST /rollback → Undo last memory update
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)