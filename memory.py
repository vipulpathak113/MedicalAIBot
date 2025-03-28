class ChatMemory:
    def __init__(self):
        self.history = []

    def add_message(self, sender, text):
        self.history.append({"sender": sender, "text": text})

    def get_history(self):
        return self.history

    def reset(self):
        self.history = []
