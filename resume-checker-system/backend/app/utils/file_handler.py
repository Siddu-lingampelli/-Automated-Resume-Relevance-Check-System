import os
UPLOAD_DIR="backend/uploads"
def save_file(file_bytes, filename):
    os.makedirs(UPLOAD_DIR,exist_ok=True)
    path=os.path.join(UPLOAD_DIR,filename)
    with open(path,"wb") as f: f.write(file_bytes)
    return path
