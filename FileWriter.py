import json

from IWriter import IWriter


class FileWriter(IWriter):
    def __init__(self, filename="log.txt"):
        self.filename = filename

    def send_data(self, data, name_machine):

        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4)+"\n")
            print("done")
