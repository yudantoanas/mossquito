import os
from pathlib import Path
import nbformat
import sys

try:
    dir_list = os.listdir(sys.argv[1])

    for i in dir_list:
        if i.endswith(".ipynb"):
            filePath = sys.argv[1] + "/" + i

            # read file
            nb = nbformat.read(filePath, as_version=4)
            user_code = ''

            # exract contents
            for cell in nb.cells:
                if cell.cell_type == 'code' and '# EXCLUDE' not in cell.source:
                    user_code += cell.source + '\n\n'
                elif cell.cell_type == 'markdown':
                    if "[INSIGHT]" in cell.source:
                        user_code += "'''\n" + \
                            cell.source.replace(
                                "[INSIGHT]", "").strip() + "\n'''" + "\n\n"
                    else:
                        user_code += cell.source.replace("```", "'''") + '\n\n'

            # create new directory
            directory_name = "extracted"
            try:
                newPath = sys.argv[1] + "/" + directory_name
                os.mkdir(newPath)
                print(f"Directory '{directory_name}' created successfully.")
            except FileExistsError:
                print(f"Directory '{directory_name}' already exists.")

            p = Path(newPath + "/" + i)
            output_path = os.path.join(p.parent, p.stem + '.py')

            # write converted file
            with open(output_path, mode='w', encoding='utf-8') as f:
                f.write(user_code)

            print(f'Extracted user code to {output_path}')
except IndexError:
    print("Missing directory path! Try again.")
