# wallet.py
import ecdsa
import hashlib

class Wallet:
    def __init__(self):
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def get_address(self):
        pub_key_str = self.public_key.to_string().hex()
        return hashlib.sha256(pub_key_str.encode()).hexdigest()

    def sign_transaction(self, transaction_hash):
        return self.private_key.sign(transaction_hash.encode()).hex()

def verify_signature(public_key_hex, signature_hex, transaction_hash):
    try:
        public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=ecdsa.SECP256k1)
        return public_key.verify(bytes.fromhex(signature_hex), transaction_hash.encode())
    except (ecdsa.keys.BadSignatureError, ValueError):
        return False