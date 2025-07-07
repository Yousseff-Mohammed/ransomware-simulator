import datetime

def log_encrypted(file_path):
    with open("encrypted_files.log", 'a') as f:
        f.write(f"[{datetime.datetime.now()}] {file_path}\n")