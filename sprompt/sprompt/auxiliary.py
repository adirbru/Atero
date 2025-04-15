# my_library/auxiliary.py

import base64

class EncryptionHelper:
    """
    Simulated encryption helper that 'encrypts' data by a simple base64 encoding.
    """
    def encrypt(self, data: str) -> str:
        encoded_bytes = base64.b64encode(data.encode("utf-8"))
        return encoded_bytes.decode("utf-8")

    def decrypt(self, data: str) -> str:
        decoded_bytes = base64.b64decode(data.encode("utf-8"))
        return decoded_bytes.decode("utf-8")

class NoiseGenerator:
    """
    Generates random noise strings which serve no useful purpose.
    """
    def generate(self, length: int = 10) -> str:
        import random, string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def dummy_api_call(endpoint: str, payload: dict) -> dict:
    """
    A dummy function that simulates an API call.
    """
    import time
    time.sleep(0.5)
    return {"status": "success", "endpoint": endpoint, "payload": payload}
