from cryptography.fernet import Fernet

class PasswordCipher:
    def __init__(self, key: bytes = None):
        """
        Initialize the cipher.
        If no key is given, a new one is generated.
        """
        if key is None:
            key = Fernet.generate_key()
        self.key = key
        self.cipher = Fernet(key)

    def encrypt(self, plaintext: str) -> bytes:
        """
        Encrypt a string and return encrypted bytes.
        """
        return self.cipher.encrypt(plaintext.encode())

    def decrypt(self, ciphertext: bytes) -> str:
        """
        Decrypt encrypted bytes and return the original string.
        """
        return self.cipher.decrypt(ciphertext).decode()

    def get_key(self) -> bytes:
        """
        Return the encryption key (store this safely!).
        """
        return self.key
