import base58
from cryptography.hazmat.primitives.asymmetric import ed25519
from mnemonic import Mnemonic


class Address:
    private_key: bytes = None
    public_key: bytes = None
    address: str = None

    def __init__(self):
        pk = ed25519.Ed25519PrivateKey.generate()
        private_key = pk.private_bytes_raw()
        public_key = pk.public_key().public_bytes_raw()
        address = base58.b58encode(public_key).decode("ascii")
