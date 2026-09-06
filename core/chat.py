from .brain import Brain
from .memory import Memory


class Chat:
    def __init__(self):
        self.memory = Memory()
        self.brain = Brain(memory=self.memory)

    def respond(self, message):
        response = self.brain.think(message)

        # Save conversation history
        self.memory.remember(
            "conversation",
            f"User: {message} | Leenax: {response}"
        )

        return response