import hashlib
from cryptography.fernet import Fernet
from item import LockerItem
import base64

class DigitalLocker:
    def __init__(self, password):
        self.password_hash = self.hash_password(password)
        self.key = self.generate_key(password)
        self.fernet = Fernet(self.key)
        self.items = []

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_key(self, password):
        # Derive key from password and salt (simple base64 padding for Fernet)
        key_base = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(key_base)

    def check_password(self, entered_password):
        return self.hash_password(entered_password) == self.password_hash

    def encrypt_data(self, data):
        return self.fernet.encrypt(data)

    def decrypt_data(self, data):
        return self.fernet.decrypt(data)

    def add_item(self, filename, filedata):
        encrypted = self.encrypt_data(filedata)
        self.items.append(LockerItem(filename, encrypted))

    def list_items(self):
        return self.items

    def delete_item(self, filename):
        self.items = [item for item in self.items if item.filename != filename]
