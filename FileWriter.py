import json
import os
from datetime import datetime
from IWriter import IWriter

class FileWriter(IWriter):
    def send_data(self, data, computer_id):
        """Sauvegarde les données dans un fichier au format JSON."""
        try:
            log_dir = f"data/{computer_id}/"
            log_file=os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.txt")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            file_path = log_file
            with open(file_path, "a", encoding="utf-8") as f:
                json.dump(data, f, indent=4)  # Écrire la liste au format JSON
            print(f"Data written to {file_path}")
        except Exception as e:
            print(f"Error writing data to file: {e}")
