import os
from openai import OpenAI
from core.memory import Memory

try:
    from config import AI_NAME, CREATOR, API_KEY, MEMORY_FILE
except ImportError:
    AI_NAME = "Leenax"
    CREATOR = "Obelix Trigger"
    API_KEY = ""
    MEMORY_FILE = "data/memory.json"


class Brain:

    def __init__(self, memory=None):
        self.name = AI_NAME
        self.creator = CREATOR
        self.memory = memory or Memory(MEMORY_FILE)

        api_key = API_KEY or os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None

    def remember(self, key, value, append=True):
        self.memory.remember(key, value, append=append)

    def think(self, message):
        msg = message.lower().strip()

        if "remember that" in msg:
            fact = message.split("remember that", 1)[1].strip()
            if not fact:
                return "What should I remember?"
            self.remember("facts", fact)
            return "Okay, I will remember that."

        if "my name is" in msg:
            start = msg.find("my name is")
            name = message[start + len("my name is"):].strip().strip(".!?")
            if not name:
                return "I didn't catch your name. Can you say that again?"
            self.memory.remember("owner_name", name, append=False)
            return f"Nice to meet you {name}. I will remember you."

        if "what is my name" in msg:
            owner_name = self.memory.get("owner_name")
            if owner_name:
                return f"Your name is {owner_name}."
            return "I don't know your name yet."

        if "what do you remember" in msg or "what do you know" in msg:
            data = self.memory.get_all()
            if not data:
                return "I don't remember anything yet."

            summary = []
            for key, value in data.items():
                if key == "conversation":
                    continue
                if isinstance(value, list):
                    value = ", ".join(value)
                summary.append(f"{key}: {value}")

            if summary:
                return "I remember: " + "; ".join(summary)
            return "I don't remember anything useful yet."

        if "who created you" in msg:
            return f"I was created by {self.creator}."

        if self.client:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are {self.name}.\n"
                            f"You were created by {self.creator}.\n"
                            "Be intelligent, helpful and friendly."
                        )
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            return response.choices[0].message.content

        return (
            "My AI connection is not activated yet. "
            "Add your API key in config.py or set OPENAI_API_KEY."
        )