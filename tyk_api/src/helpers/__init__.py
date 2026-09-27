from .encrypt import PasswordCipher
from ..settings import settings


def create_email(username: str) -> str:
    """Build a user email using the configured domain."""
    return f"{username}@{settings.EMAIL_DOMAIN}"


password_cipher = PasswordCipher(bytes(settings.CIPHER_KEY, "utf-8"))

__all__ = [
    "password_cipher",
    "create_email",
]

# Expose helpers modules for convenient imports like `from ..helpers import syntax`
from . import syntax  # noqa: E402,F401
__all__.append("syntax")