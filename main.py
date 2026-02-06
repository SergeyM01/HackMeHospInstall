import os
from subprocess import run
import sys
import json
from getpass import getpass

# Сообщение при котором не возможна дальнейшая работа скрипта с выходом 
def errorMessage():
    print(colorText("red", "[-] Дальнейшая работа скрипта не может быть возможной"))
    sys.exit()

# Окрашивание текста c центрированием
def colorText(color, text):
    colors = ['GREEN', 'RED', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']
    color_upper = str(color).upper()
    result = None
    if color_upper in colors:
         # Сброс стиля
        RESET = '\033[0m'
        color_map = {
            'GREEN': '\033[32m',
            'RED': '\033[31m',
            'YELLOW' : '\033[33m',
            'BLUE': '\033[34m',
            'MAGENTA': '\033[35m',
            'CYAN': '\033[36m',
            'WHITE': '\033[37m'
        }
        result = color_map[color_upper] + text + RESET
    else:
        result = text

    return result
    
print()
print(colorText('cyan', (('=') * 5 + " Установка HackMe Hospital " + ('=') * 5)))
print()

# Десериализация данных components.json для чтения конфигурации
with open('components.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Изменение параметров components.json
def changeComponentsConfig(itemName, newValue):
    global data
    data[itemName] = newValue
    with open('components.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(colorText("green", f"[+] Конфиг обновлен: {itemName}:{newValue}"))

# Проверка Установлен ли Xampp
def checkXamppExists():
    print(colorText("blue", "[~] Проверка наличия XAMPP"))
    isExists = data["xamppInstalled"] # Сущестувует ли нужный софт и директории

    if isExists:
        print(colorText("green", "[+] XAMPP установлен"))
    else:
        print(colorText("yellow", "[!] XAMPP не установлен"))

    return isExists

def xamppDownload():
    print(colorText("cyan", "[~] Скачивание XAMPP"))
    print()
    # Скачивание XAMPP
    try:
        run(["curl", "-L", "-o", "xampp-linux-installer.run", "https://sourceforge.net/projects/xampp/files/XAMPP%20Linux/8.2.12/xampp-linux-x64-8.2.12-0-installer.run/download"])
    except Exception as XamppInstalledError:
        print(colorText("red", f"[-] Во время установки XAMPP произошла ошибка:{XamppInstalledError}"))
        errorMessage() # Выход в случае неудачного скачивания

    print(colorText('green', '[+] Скачивание XAMPP завершилась успешно'))
    changeComponentsConfig("xamppInstalled", True)

isXamppExists = checkXamppExists()

# Запуск скачивания Xampp в случае отсутствия
if not isXamppExists:
    xamppDownload()

print()