class FileWriter:
    def __init__(self, filename="log.txt"):
        self.filename = filename

    def write(self, text):
        """Écrit du texte dans le fichier"""
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(text + "\n")
            print("ecris")
