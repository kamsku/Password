import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Constants for password generator
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.?/"
DEFAULT_PASSWORD_LENGTH = 14
DEFAULT_PASSWORDS_COUNT = 100

# Constants for export
DEFAULT_OUTPUT_CSV = "passwords.csv"
DEFAULT_OUTPUT_XLSX = "passwords.xlsx"

# Constants for hashing functions
BCRYPT_ROUNDS = 12
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_DKLEN = 64
SCRYPT_SALT_BYTES = 16