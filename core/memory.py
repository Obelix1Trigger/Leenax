import json
import os


class Memory:
    def __init__(self, file_path="data/memory.json"):
        self.file = file_path

        folder = os.path.dirname(self.file)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({}, f, indent=4)

    def load_memory(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def save_memory(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def get(self, key, default=None):
        data = self.load_memory()
        return data.get(key, default)

    def remember(self, key, value, append=True):
        data = self.load_memory()

        if append:
            existing = data.get(key)
            if existing is None:
                data[key] = []
            elif not isinstance(existing, list):
                data[key] = [existing]

            if value not in data[key]:
                data[key].append(value)
        else:
            data[key] = value

        self.save_memory(data)

    def recall(self, key):
        value = self.get(key)
        if isinstance(value, list):
            return ", ".join(value)
        if value is not None:
            return str(value)
        return "I don't remember that yet."

    def get_all(self):
        return self.load_memory()