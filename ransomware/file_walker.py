import os

def find_files(start_path, extensions):
    targets = []
    for root, dirs, files  in os.walk(start_path):
        for file in files:
            if file.endswith(tuple(extensions)):
                targets.append(os.path.join(root, file))
    return targets