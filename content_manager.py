def save_content(filepath:str, content:str):
    with open(filepath, 'w+') as file:
        file.write(content)

def get_content(filepath:str):
    with open(filepath, 'r') as file:
        file.read()