from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from datetime import datetime
import json
import ast
import operator
import re

BASE = Path(__file__).resolve().parent
WEB = BASE / "website"
DATA = BASE / "data"
MEMORY_FILE = DATA / "memory.json"

WEB.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)

app = Flask(__name__, static_folder=str(WEB), static_url_path="")

# =========================
# MEMORY
# =========================

def load_memory():
    try:
        if MEMORY_FILE.exists():
            data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("facts", [])
                data.setdefault("history", [])
                return data
    except Exception:
        pass

    return {"facts": [], "history": []}


memory = load_memory()


def save_memory():
    MEMORY_FILE.write_text(
        json.dumps(memory, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


# =========================
# SAFE CALCULATOR
# =========================

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def calculate(expression):
    expression = expression.replace("^", "**")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError()

            return OPS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](evaluate(node.operand))

        raise ValueError()

    result = evaluate(tree.body)

    if isinstance(result, float) and result.is_integer():
        return str(int(result))

    return str(round(result, 8))


# =========================
# LEENAX BRAIN
# =========================

def brain(message):

    text = message.strip()
    lower = text.lower()

    if not text:
        return "I'm listening. What would you like to do?"

    # Greetings
    if re.match(r"^(hi|hello|hey|yo)\b", lower):
        return "Hello. Leenax is online and ready."

    # Identity
    if "who are you" in lower:
        return "I'm Leenax — your personal AI assistant."

    if "your name" in lower:
        return "My name is Leenax."

    if "who created you" in lower or "who made you" in lower:
        return "I was created by Obelix Trigger."

    # Time
    if "what time" in lower or "current time" in lower:
        return f"The current computer time is {datetime.now():%H:%M:%S}."

    # Date
    if "what date" in lower or "what day is it" in lower:
        return f"Today is {datetime.now():%A, %d %B %Y}."

    # Remember
    match = re.search(
        r"(?:remember|save this|don't forget)\s+(?:that\s+)?(.+)",
        text,
        re.IGNORECASE
    )

    if match:

        fact = match.group(1).strip().rstrip(".")

        memory["facts"].append(fact)
        memory["facts"] = memory["facts"][-50:]

        save_memory()

        return f"Got it. I saved this to memory: {fact}"

    # Recall
    if "what do you remember" in lower:

        if not memory["facts"]:
            return "My memory is empty."

        return (
            "Here's what I remember:\n\n"
            + "\n".join(
                f"• {fact}"
                for fact in memory["facts"][-10:]
            )
        )

    # Calculator
    math_match = re.fullmatch(
        r"(?:calculate|compute|what is)\s+"
        r"([0-9\s+\-*/%^().]+)\??",
        lower
    )

    if math_match:

        try:
            answer = calculate(math_match.group(1))
            return f"The answer is {answer}."
        except Exception:
            return "I couldn't safely calculate that."

    # Capabilities
    if "what can you do" in lower:

        return (
            "Current Leenax capabilities:\n\n"
            "🧠 Local AI core\n"
            "💾 Persistent memory\n"
            "🎙️ Browser voice recognition\n"
            "🧮 Calculator\n"
            "💬 Live website chat\n"
            "📡 Live system status\n"
            "🎨 Image-generation interface\n\n"
            "The architecture is ready for a real AI model."
        )

    # API explanation
    if "what is an api" in lower:

        return (
            "An API is a bridge between programs. "
            "For Leenax, an AI API can provide a powerful language "
            "model while your website and Python code remain yours."
        )

    # Default
    return (
        "I understand your message, but my current local brain "
        "doesn't have a full language model connected yet. "
        "The Leenax architecture is ready for that next upgrade."
    )


# =========================
# WEBSITE
# =========================

@app.get("/")
def home():
    return send_from_directory(str(WEB), "index.html")


# =========================
# CHAT API
# =========================

@app.post("/api/chat")
def chat():

    data = request.get_json(silent=True) or {}

    message = str(
        data.get("message", "")
    ).strip()

    if not message:
        return jsonify({
            "error": "Message is empty."
        }), 400

    reply = brain(message)

    memory["history"].append({
        "time": datetime.now().isoformat(timespec="seconds"),
        "user": message,
        "assistant": reply
    })

    memory["history"] = memory["history"][-100:]

    save_memory()

    return jsonify({
        "reply": reply,
        "online": True,
        "memory": len(memory["history"]),
        "facts": len(memory["facts"])
    })


# =========================
# SYSTEM STATUS
# =========================

@app.get("/api/status")
def status():

    return jsonify({
        "name": "Leenax",
        "online": True,
        "brain": "Leenax Local Core",
        "memory": len(memory["history"]),
        "facts": len(memory["facts"]),
        "voice": True,
        "image_mode": True,
        "live_mode": True
    })


# =========================
# IMAGE MODE
# =========================

@app.post("/api/image")
def image():

    data = request.get_json(silent=True) or {}

    prompt = str(
        data.get("prompt", "")
    ).strip()

    if not prompt:
        return jsonify({
            "error": "Image description is empty."
        }), 400

    return jsonify({
        "ready": False,
        "message": (
            "Image Mode is connected to Leenax, "
            "but a real image-generation model must be "
            "configured before an image can actually be generated."
        ),
        "prompt": prompt
    })


# =========================
# START
# =========================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("          🤖 LEENAX AI ONLINE")
    print("==========================================")
    print("🧠 Local brain       : ONLINE")
    print("💾 Persistent memory : ONLINE")
    print("🎙️ Voice interface   : READY")
    print("🎨 Image mode        : READY")
    print("⚡ Live mode         : ONLINE")
    print("🌐 Website           : http://127.0.0.1:5000")
    print("==========================================")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
