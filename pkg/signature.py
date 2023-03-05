import base64


from cryptography.hazmat.primitives.asymmetric import ed25519


def load_ed25519_private_key_from_hex(private_key_hex: str):
    return ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(private_key_hex))


def ed25519_sign_data_base64(private_key_hex: str, plain_text: str):
    """
    signature = ed25519_sign_data_base64("text")
    """
    private_key = load_ed25519_private_key_from_hex(private_key_hex)
    signature_bytes = private_key.sign(plain_text.encode('utf-8'))

    return base64.b64encode(signature_bytes).decode()
