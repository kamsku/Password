import secrets
import string
import logging
from typing import List, Set

from config import SPECIAL_CHARACTERS

class PasswordValidationError(ValueError):
    """Custom exception for password validation errors."""
    pass

def validate_password(pwd: str, length: int) -> None:
    """
    Validates a password against specified requirements:
    - length: `length`
    - contains exactly 1 special character (from `SPECIAL_CHARACTERS`)
    - at least 1 uppercase letter
    - at least 1 digit
    - all other characters are alphanumeric
    """
    if len(pwd) != length:
        raise PasswordValidationError(f"Incorrect password length (expected {length}).")

    special_char_count = sum(1 for c in pwd if c in SPECIAL_CHARACTERS)
    if special_char_count != 1:
        raise PasswordValidationError("Password must contain exactly 1 special character.")

    if not any(c.isupper() for c in pwd):
        raise PasswordValidationError("Password must contain at least one uppercase letter.")

    if not any(c.isdigit() for c in pwd):
        raise PasswordValidationError("Password must contain at least one digit.")

    for char in pwd:
        if char not in SPECIAL_CHARACTERS and not char.isalnum():
            raise PasswordValidationError("Password contains an invalid character (not alphanumeric or allowed special). ")


class PasswordGenerator:

    @staticmethod
    def generate_one(length: int) -> str:
        """
        Generates a single password of the given length, meeting validation requirements.
        """
        if length < 4: 
            raise PasswordValidationError("Minimum length is 4 (required: 1 special + 1 uppercase + 1 digit + 1 lowercase).")

        # Ensure the password contains at least one character from each required category
        special = secrets.choice(SPECIAL_CHARACTERS)
        upper = secrets.choice(string.ascii_uppercase)
        digit = secrets.choice(string.digits)
        lower = secrets.choice(string.ascii_lowercase) 

        # Remaining characters can be any alphanumeric characters
        remaining_len = length - 4 
        # A better approach is to generate remaining characters from an alphanumeric pool and then shuffle
        alnum_pool_for_remaining = string.ascii_letters + string.digits
        remaining = [secrets.choice(alnum_pool_for_remaining) for _ in range(remaining_len)]

        chars = [special, upper, digit, lower] + remaining
        secrets.SystemRandom().shuffle(chars)

        password = "".join(chars)
        validate_password(password, length)
        return password

    @classmethod
    def generate_batch(cls, count: int, length: int) -> List[str]:
        """
        Generates a list of unique passwords.
        May raise RuntimeError if unable to generate enough unique passwords.
        """
        seen: Set[str] = set()
        passwords: List[str] = []

        attempts = 0
        max_attempts = max(10_000, count * 200) 

        logging.info(f"Generating {count} unique passwords of length {length}...")

        while len(passwords) < count:
            attempts += 1
            if attempts > max_attempts:
                raise RuntimeError(
                    "Could not generate enough unique passwords with these parameters. "
                    "Increase length or decrease the number of passwords."
                )
            try:
                pwd = cls.generate_one(length)
                if pwd not in seen:
                    seen.add(pwd)
                    passwords.append(pwd)
            except PasswordValidationError as e:
                # It's possible that the generated password did not meet the requirements, try again
                logging.debug(f"Generated password failed validation: {e}. Retrying.")
                continue

        return passwords