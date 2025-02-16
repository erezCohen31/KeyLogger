class Buffer:
    def __init__(self):
        self.data = []

    def add_data(self, char):
        self.data.append(char)

    def flush(self):
        self.data = []

    def get_data(self):
        return self.data

