import re



hex_re = re.compile(r'\b#?([A-Fa-f0-9]{3}|[A-Fa-f0-9]{4}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})\b')

def hex_in_string(string: str):
    result = hex_re.findall(string)

    if len(result) == 0:
        print("no results")
    else:
        for i in range(len(result)):
            result[i] = '#'+result[i]
        print("result:", result)

def hex_in_file():
    try:
        with open("file.txt", 'r') as f:
            data = f.read()
            hex_in_string(data)
    except Exception as E:
        print("ошибка открытия файла", E)


hex_in_string("##1230,#112")
hex_in_file()





