from IWriter import IWriter


class FileWriter(IWriter):
    def __init__(self, filename="log.txt"):
        self.filename = filename

    def send_data(self, data,name_machine):
        """Écrit du texte dans le fichier"""
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(data + "\n")