# вывод дерева проекта без папки .venv:
# python utils/show_tree.py
# python utils/show_tree.py --save utils/project_tree.txt

import os
import sys

# Принудительно устанавливаем кодировку UTF-8
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def print_tree(directory, ignore_dirs=None, prefix=""):
    if ignore_dirs is None:
        ignore_dirs = {'.venv', '__pycache__', '.git', '.idea', 'node_modules', 'other'}

    try:
        items = sorted(os.listdir(directory))
        dirs = [item for item in items if os.path.isdir(os.path.join(directory, item)) and item not in ignore_dirs]
        files = [item for item in items if os.path.isfile(os.path.join(directory, item))]

        # Выводим папки
        for i, dir_name in enumerate(dirs):
            is_last_dir = i == len(dirs) - 1 and len(files) == 0
            print(f"{prefix}{'└── ' if is_last_dir else '├── '}{dir_name}/")

            extension = "    " if is_last_dir else "│   "
            print_tree(os.path.join(directory, dir_name), ignore_dirs, prefix + extension)

        # Выводим файлы
        for i, file_name in enumerate(files):
            is_last = i == len(files) - 1
            print(f"{prefix}{'└── ' if is_last else '├── '}{file_name}")

    except PermissionError:
        print(f"{prefix}[Permission Denied]")


if __name__ == "__main__":
    import sys

    # Определяем, нужно ли сохранять в файл
    if len(sys.argv) > 1 and sys.argv[1] == "--save":
        filename = sys.argv[2] if len(sys.argv) > 2 else "project_tree.txt"

        # Сохраняем в файл с UTF-8 кодировкой
        with open(filename, 'w', encoding='utf-8') as f:
            original_stdout = sys.stdout
            sys.stdout = f

            print("STRUCTURE of PROJECT:")
            print_tree(".")

            sys.stdout = original_stdout

        print(f"✅ Structure of project was saved in file: {filename}")
    else:
        print("Structure of project:")
        print_tree(".")
