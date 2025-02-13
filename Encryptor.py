class Encryptor:
    def __init__(self, key):
        self.key = key

    def encrypt(self, text):
        encrypted_text = ""
        for char in text:
            encrypted_char = chr(ord(char) ^ ord(self.key))
            encrypted_text += encrypted_char
        return encrypted_text

    def decrypt(self, encrypted_text):
        decrypted_text = ""
        for char in encrypted_text:
            decrypted_char = chr(ord(char) ^ ord(self.key))
            decrypted_text += decrypted_char
        return decrypted_text