import os

def rename_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace("ArthSahay", "ArthSahay")
        new_content = new_content.replace("ArthSahay", "ArthSahay")
        new_content = new_content.replace("arthsahay", "arthsahay")
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
    except Exception as e:
        print(f"Skipping {filepath} due to error: {e}")

if __name__ == "__main__":
    for root, dirs, files in os.walk('.'):
        if 'venv' in root or '.git' in root or '__pycache__' in root or '.pytest_cache' in root:
            continue
        for file in files:
            if file.endswith(('.py', '.html', '.css', '.js', '.txt', '.md', '.bat')):
                rename_in_file(os.path.join(root, file))
