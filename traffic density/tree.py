from pathlib import Path

def print_tree(path: Path, max_depth=5, current_depth=0):
    if current_depth > max_depth:
        return

    for item in sorted(path.iterdir()):
        indent = "│   " * current_depth + ("├── " if current_depth > 0 else "")
        print(f"{indent}{item.name}")

        if item.is_dir():
            print_tree(item, max_depth, current_depth + 1)

if __name__ == "__main__":
    root = Path(".")  # change to any directory
    print_tree(root, max_depth=5)
