from .encrypt import PasswordCipher
from ..settings import settings

password_cipher = PasswordCipher(settings.CIPHER_KEY)

__all__ = [
    "password_cipher",
]