from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)


def encrypt(data: str) -> bytes:
    return cipher.encrypt(data.encode())


def decrypt(token: bytes) -> str:
    return cipher.decrypt(token).decode()