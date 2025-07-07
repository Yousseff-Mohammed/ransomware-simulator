from Crypto.Cipher import AES
import os

def encrypt_file(file_path, aes_key):
    with open(file_path, 'rb') as f:
        data = f.read()

        cipher = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        with open(file_path, 'wb') as f:
            f.write(cipher.nonce + tag + ciphertext)