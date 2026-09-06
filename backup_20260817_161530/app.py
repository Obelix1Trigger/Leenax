from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from pathlib import Path
import json
import ast
import operator
import re

BASE_DIR = Path(__file__).resolve().parent
WEBSITE_DIR = BASE_DIR / "website"
DATA_DIR = BASE_DIR / "data"
MEMORY_FILE = DATA_DIR / "memory.json"

DATA_DIR.mkdir(exist_ok=True)
WEBSITE_DIR.mkdir(exist_ok=True)

app = Flask(__name__, static_folder=str(WEBSITE_DIR), static_url_path="")

# ---------------- MEMORY ----------------

def load_memory():
    try:
        if MEMORY_FILE.exists():
            data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
            if isinstance(data, list):
                return {"conversations": data, "facts": {}}
    except Exception:
        pass
    return {"conversations": [], "facts": {}}

memory = load_memory()
memory.setdefault("conversations", [])
memory.setdefault("facts", {})

def save_memory():
    memory["conversations"] = memory["conversations"][-100:]
    MEMORY_FILE.write_text(
        json.dumps(memory, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def remember_conversation(user, assistant):
    memory["conversations"].append({
        "time": datetime.now().isoformat(timespec="seconds"),
        "user": user,
        "assistant": assistant
    })
    save_memory()

# ---------------- SAFE CALCULATOR ----------------

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def calculate(expression):
    expression = expression.replace("^", "**").strip()

    if len(expression) > 100:
        raise ValueError

    tree = ast.parse(expression, mode="eval")

    def walk(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left = walk(node.left)
            right = walk(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError

            return OPS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](walk(node.operand))

        raise ValueError

    result = walk(tree.body)

    if isinstance(result, float) and result.is_integer():
        return str(int(result))

    return str(round(result, 10))

# ---------------- LOCAL BRAIN ----------------

def get_recent_context():
    return memory["conversations"][-6:]

def local_brain(message):
    text = message.strip()
    low = text.lower()

    if not text:
        return "I'm listening. What would you like to do?"

    # Greetings
    if re.search(r"^(hi|hello|hey|yo|good morning|good afternoon|good evening)\b", low):
        return "Hello! I'm Leenax. I'm online and ready. What are we working on?"

    # Identity
    if "who are you" in low or "what are you" in low:
        return "I'm Leenax — your personal AI assistant project. My interface and Python brain are connected."

    if "your name" in low:
        return "My name is Leenax."

    if "who made you" in low or "who created you" in low or "your creator" in low:
        return "I was created by Obelix Trigger."

    # Remembering facts
    remember_match = re.search(
        r"(?:remember|save this|don't forget)\s+(?:that\s+)?(.+)",
        text,
        re.IGNORECASE
    )

    if remember_match:
        fact = remember_match.group(1).strip().rstrip(".")
        memory["facts"][f"fact_{len(memory['facts']) + 1}"] = fact
        save_memory()
        return f"Got it. I've saved that to my local memory: “{fact}”"

    if "what do you remember" in low or "show my memory" in low:
        facts = list(memory["facts"].values())
        if not facts:
            return "My memory is empty so far. Tell me something and say 'remember that...'."
        return "Here's what I remember:\n• " + "\n• ".join(facts[-10:])

    if "memory" in low:
        return f"I have {len(memory['facts'])} saved facts and {len(memory['conversations'])} conversation entries."

    # Time/date
    if re.search(r"\b(what time|current time|time is it)\b", low):
        return f"The computer time is {datetime.now().strftime('%H:%M:%S')}."

    if re.search(r"\b(what date|today's date|what day is it)\b", low):
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

    # Math
    math_match = re.fullmatch(
        r"(?:calculate|compute|what is)\s+([0-9\s\+\-\*\/\%\^\(\)\.]+)\??",
        low
    )

    if math_match:
        try:
            return f"The answer is {calculate(math_match.group(1))}."
        except Exception:
            return "I couldn't safely calculate that expression."

    # Simple project commands
    if "status" in low or "are you online" in low:
        return "All systems are online. Website, Flask server and local brain are connected."

    if "what can you do" in low or "help me" in low:
        return (
            "Right now I can chat, remember facts locally, recall memory, "
            "tell time/date, calculate expressions and manage the local AI interface. "
            "My architecture is ready for a stronger language model later."
        )

    # Conversation awareness
    recent = get_recent_context()

    if low in {"thanks", "thank you", "thx"}:
        return "You're welcome. Let's keep building."

    if low in {"ok", "okay", "cool", "nice", "great"}:
        return "Understood. I'm ready for the next command."

    if "what did i just say" in low:
        if recent:
            return f'You just said: “{recent[-1]["user"]}”'
        return "This is the beginning of our current memory."

    # Explain some common coding/project terms
    if "what is an api" in low:
        return (
            "An API is a bridge that lets one program communicate with another. "
            "For Leenax, an AI API could provide a powerful language model while "
            "your website and Python code remain your own interface."
        )

    if "what is flask" in low:
        return (
            "Flask is the Python web framework we're using to connect your Leenax "
            "website to Python endpoints such as /api/chat."
        )

    # General fallback
    return (
        "I understand the message, but my current brain is still a local starter "
        "model rather than a full language model. The important part is that the "
        "architecture is ready: we can upgrade the reasoning engine without "
        "rebuilding your website."
    )

# ---------------- WEB ROUTES ----------------

@app.get("/")
def home():
    return send_from_directory(str(WEBSITE_DIR), "index.html")

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Message is empty."}), 400

    reply = local_brain(message)
    remember_conversation(message, reply)

    return jsonify({
        "reply": reply,
        "memory_count": len(memory["conversations"]),
        "facts_count": len(memory["facts"]),
        "online": True
    })

@app.get("/api/status")
def status():
    return jsonify({
        "name": "Leenax",
        "online": True,
        "brain": "Leenax Local Brain v2",
        "memory": len(memory["conversations"]),
        "facts": len(memory["facts"]),
        "time": datetime.now().isoformat(timespec="seconds")
    })

if __name__ == "__main__":
    print("====================================")
    print("      LEENAX LOCAL BRAIN v2")
    print("====================================")
    print("🤖 Website + Python brain connected")
    print("💾 Persistent memory enabled")
    print("🧮 Calculator enabled")
    print("🧠 Conversation context enabled")
    print("🌐 Open http://127.0.0.1:5000")
    print("====================================")
    app.run(host="127.0.0.1", port=5000, debug=True)
