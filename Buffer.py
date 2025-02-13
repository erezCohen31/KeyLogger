class Buffer:
    def __init__(self):
        self.data = []
        self.max_size = 100

    def add_data(self, char):
        self.data.append(char)

    def flush(self):
        self.data = []

    def get_data(self):
        return self.data

    def is_full(self):
        return len(self.data) >= self.max_size
