import hashlib
import bcrypt
import secrets
from typing import Tuple, Any

from config import BCRYPT_ROUNDS, SCRYPT_N, SCRYPT_R, SCRYPT_P, SCRYPT_DKLEN, SCRYPT_SALT_BYTES

class HashFunctions:
    """A collection of hashing functions returning hash in hex format (or additional data)."""

    @staticmethod
    def md5_hex(text: str) -> str:
        """Generates an MD5 hash for the given text."""
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def sha1_hex(text: str) -> str:
        """Generates a SHA-1 hash for the given text."""
        return hashlib.sha1(text.encode()).hexdigest()

    @staticmethod
    def sha256_hex(text: str) -> str:
        """Generates a SHA-256 hash for the given text."""
        return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def sha512_hex(text: str) -> str:
        """Generates a SHA-512 hash for the given text."""
        return hashlib.sha512(text.encode()).hexdigest()

    @staticmethod
    def bcrypt_hex(text: str, rounds: int = BCRYPT_ROUNDS) -> Tuple[str, str]:
        """
        Generates a bcrypt hash for the given text.
        Returns: (hash_hex, hash_str)
        """
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(text.encode(), salt)  # bytes
        return hashed.hex(), hashed.decode(errors="replace")

    @staticmethod
    def scrypt_hex(text: str) -> Tuple[str, str]:
        """
        Generates a scrypt hash for the given text.
        Returns: (hash_hex, salt_hex)
        """
        salt = secrets.token_bytes(SCRYPT_SALT_BYTES)
        hashed = hashlib.scrypt(
            text.encode(),
            salt=salt,
            n=SCRYPT_N,
            r=SCRYPT_R,
            p=SCRYPT_P,
            dklen=SCRYPT_DKLEN
        )
        return hashed.hex(), salt.hex()