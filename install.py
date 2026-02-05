import os
from subprocess import run
from colorama import Fore, Style
import sys
import json
from getpass import getpass

# Сообщение при котором не возможна дальнейшая работа скрипта с выходом 
def errorMessage():
    print(Fore.RED + "[-] Дальнейшая работа скрипта не может быть возможной" + Style.RESET_ALL)
    sys.exit()

# Центрирование текста
def center_text(text):
    try:
        # Получаем размер терминала
        terminal_width = os.get_terminal_size().columns
        # Убираем цветовые коды для подсчета длины текста
        clean_text = text.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, '')
        text_length = len(clean_text)
        
        # Вычисляем отступы
        if text_length >= terminal_width:
            return text  # Если текст длиннее терминала, не центрируем
        
        padding = (terminal_width - text_length) // 2
        return " " * padding + text
    except (OSError, AttributeError):
        # Если не удалось получить размер терминала
        return text

# Окрашивание текста c центрированием
def colorText(color, text, isCenter=False):
    colors = ['GREEN', 'RED', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']
    color_upper = str(color).upper()
    result = None
    if color_upper in colors:
        color_map = {
            'GREEN': Fore.GREEN,
            'RED': Fore.RED,
            'YELLOW' : Fore.YELLOW,
            'BLUE': Fore.BLUE,
            'MAGENTA': Fore.MAGENTA,
            'CYAN': Fore.CYAN,
            'WHITE': Fore.WHITE
        }
        result = color_map[color_upper] + text + Style.RESET_ALL
    else:
        result = text

    if isCenter:
        return center_text(result)
    else:
        return result
    
print()
print(colorText('cyan', (('=') * 5 + " Установка HackMe Hospital " + ('=') * 5), True))
print()

# Десериализация данных components.json для чтения конфигурации
with open('components.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Изменение параметров components.json
def changeComponentsConfig(itemName, newValue):
    data[itemName] = newValue

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
    isDownloaded = True
    print(colorText("blue", "[~] Скачивание XAMPP"))

    # Скачивание XAMPP
    try:
        installedResult = run(["curl", "-L", "-o", "xampp-linux-installer.run https://sourceforge.net/projects/xampp/files/XAMPP%20Linux/8.2.12/xampp-linux-x64-8.2.12-0-installer.run/download"])
    except Exception as XamppInstalledError:
        print(colorText("red", f"[-] Во время установки XAMPP произошла ошибка:{XamppInstalledError}"))
        errorMessage() # Выход в случае неудачного скачивания

    print(colorText('green', '[+] Установка XAMPP завершилась успешно'))
    changeComponentsConfig("xamppInstalled", True)

isXamppExists = checkXamppExists()

# Запуск скачивания Xampp в случае отсутствия
if not isXamppExists:
    xamppDownload()
