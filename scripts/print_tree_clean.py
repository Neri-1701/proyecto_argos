import os

EXCLUDE_DIRS = {'.venv', '.git', '__pycache__', '.dvc', '.vscode'}

def print_tree(startpath, max_depth=3):
    for root, dirs, files in os.walk(startpath):
        # Filtra carpetas excluidas
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        level = root.replace(startpath, '').count(os.sep)
        if level >= max_depth:
            continue
        indent = '    ' * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = '    ' * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    print_tree(".", max_depth=3)