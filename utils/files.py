import shutil


def files_copier(data: dict):
    for idx, file_name in enumerate(data['paths']):
        try:
            shutil.copyfile(f'clone/{file_name}', f'moss/{data["fileNames"][idx]}')
        except FileNotFoundError as e:
            print(e)
            continue
        else:
            print(f'Extracted user code to moss/{file_name}')

    return None
