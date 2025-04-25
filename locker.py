import os
from cryptography.fernet import Fernet
from hashlib import sha256
from base64 import urlsafe_b64encode

def generate_key(password: str) -> bytes:
    return sha256(password.encode()).digest()

class LockerItem: 
    def __init__(self, filename, filedata):
        self.filename = filename
        self.filedata = filedata

class DigitalLocker: # main class
    def __init__(self, username, password):
        self.username = username
        self.folder = os.path.join("data", username)
        os.makedirs(self.folder, exist_ok=True)

        key = generate_key(password)
        self.fernet = Fernet(urlsafe_b64encode(key))
        self.password_hash = sha256(password.encode()).hexdigest()

    def add_item(self, filename, data):
        encrypted = self.fernet.encrypt(data)
        with open(os.path.join(self.folder, filename), "wb") as f:
            f.write(encrypted)

    def list_items(self):
        return [f for f in os.listdir(self.folder)]

    def get_item(self, filename):
        with open(os.path.join(self.folder, filename), "rb") as f:
            return self.fernet.decrypt(f.read())

    def delete_item(self, filename):
        os.remove(os.path.join(self.folder, filename))
