import os
import pathlib
import shutil
import sys
import nbformat

def readFile(folder_path):
    if not os.path.exists(folder_path):
        print(f"Directory '{folder_path}' was not found.")
        return

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".py"):
                filePath = os.path.join(root, filename)
                print(filePath)
                print(f"Read file: {filename}\n" + "-" * 40)

                shutil.copyfile(filePath, "./moss/"+filename)
                continue

            if filename.endswith(".ipynb"):
                filePath = os.path.join(root, filename)
                print(filePath)
                print(f"Read file: {filename}\n" + "-" * 40)

                try:
                    # read notebook file
                    nb = nbformat.read(filePath, as_version=4)
                except Exception as e:
                    print(e)
                    continue

                # extract code from cell
                user_code = ''
                for cell in nb.cells:
                    if cell.cell_type == 'code':
                        # append code from code cell
                        user_code += cell.source + '\n\n'
                    elif cell.cell_type == 'markdown':
                        # append markdown from markdown cell as comments
                        user_code += "'''" + cell.source + "'''\n\n"

                # generate output file
                output_path = os.path.join(
                    "moss",  # folder name in current directory
                    # extract filename from extension
                    f"{pathlib.Path(filePath).stem}.py"
                )

                with open(output_path, mode='w', encoding='utf-8') as f:
                    f.write(user_code)


if __name__ == "__main__":
    dir = sys.argv[1]
    readFile(dir)
