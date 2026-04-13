import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        if 'venv' in root or '__pycache__' in root or '.git' in root or '.pytest_cache' in root:
            continue
        for file in files:
            if file in ['arthsahay.db', 'arthsahay_deploy.zip', 'zip_it.py']:
                continue
            fpath = os.path.join(root, file)
            ziph.write(fpath, os.path.relpath(fpath, path))

if __name__ == '__main__':
    zipf = zipfile.ZipFile('arthsahay_deploy.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
    print("Zipped successfully!")
