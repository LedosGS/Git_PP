import re
import requests

hex_re = re.compile(r'\b#?([A-Fa-f0-9]{3}|[A-Fa-f0-9]{4}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})\b')


def hex_in_string(string: str):
    result = hex_re.findall(string)

    if len(result) == 0:
        return None

    else:
        for i in range(len(result)):
            result[i] = '#'+result[i]
        return result

def hex_bool(string: str):
    result = hex_re.findall(string)
    if len(result) != 0:
        return True
    else:
        return False

def hex_in_file():
    try:
        with open('file.txt', 'r') as f:
            data = f.read()
            result = hex_in_string(data)
            return result
    except Exception as E:
        print(f"Ошибка при запросе: {E}")
        return None

def hex_in_Web(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        page = response.text
        return hex_in_string(page)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


print(hex_in_string("##1230,112"))
print(hex_in_file())
print(hex_in_Web("https://colorscheme.ru/html-colors.html"))


# if __name__ == '__main__':
#     import unit_test
#     unit_test.run_tests()


