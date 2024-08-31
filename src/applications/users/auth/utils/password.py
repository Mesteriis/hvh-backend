import base64
import hashlib
import os

from passlib import pwd
from passlib.crypto.digest import pbkdf2_hmac


class BasePasswordHasher:
    algorithm = None
    iterations = None
    digest = None

    @staticmethod
    def generate_salt():
        """
        Generate a cryptographically secure nonce salt in ASCII.
        """
        return base64.b64encode(os.urandom(16)).decode("ascii").strip()

    def encode(self, password, salt, iterations=None):
        """
        Create an encoded database value formatted as 'algorithm$iterations$salt$hash'.
        """
        iterations = iterations or self.iterations
        hash = pbkdf2_hmac(
            self.digest().name,
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
            self.digest().digest_size,
        )
        hash = base64.b64encode(hash).decode("ascii").strip()
        return f"{self.algorithm}${iterations}${salt}${hash}"

    def verify(self, password, encoded):
        """
        Check if the given password is correct.
        """
        algorithm, iterations, salt, hash = encoded.split("$", 3)
        encoded_2 = self.encode(password, salt, int(iterations))
        return encoded_2 == encoded


class PBKDF2SHA256PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the PBKDF2 with SHA256.
    """

    algorithm = "pbkdf2_sha256"
    iterations = 600000  # Customize this based on security requirement
    digest = hashlib.sha256


HASHER = PBKDF2SHA256PasswordHasher()


def verify_and_update_password(plain_password: str, hashed_password: str) -> tuple[bool, str]:
    """
    Verifies the password by comparing it with the hash and returns whether the hash needs to be updated.
    """
    verified = HASHER.verify(plain_password, hashed_password)
    if verified:
        # Check if the hash needs to be updated (e.g., iterations count has changed)
        algorithm, iterations, salt, _ = hashed_password.split("$", 3)
        if int(iterations) != HASHER.iterations:
            new_hash = HASHER.encode(plain_password, salt)
            return True, new_hash
        return True, hashed_password
    return False, hashed_password


def get_password_hash(password: str) -> str:
    """
    Generates a hash of the password using the selected scheme.
    """
    salt = HASHER.generate_salt()
    return HASHER.encode(password, salt)


def generate_password() -> str:
    """
    Generates a random password.
    """
    return pwd.genword()
