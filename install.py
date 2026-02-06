import os
import sys
from subprocess import run
from pathlib import Path

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

# Установка необходимых пакетов

# Обновление доступных пакетов
try:
    print(colorText("cyan", "[~] Обновление информации о возможности обновления доступных пакетов"))
    result = run(["sudo", "apt", "update"])
except Exception as PackagesUpdateError:
    print(colorText("yellow", f"[-] Обновление списка доступных пакетов и их версий завершилось с ошибкой:\n{PackagesUpdateError}"))

print(colorText("green", "[+] Обновлена информация о новых версиях доступных пакетов"))

# Необходимые пакеты для корректной работы системы
packages = [
    'curl',
    'python3.11-venv'
]

# Установка пакетов из списка
for package in packages:
    try:
        print(colorText("cyan", f"[~] Установка пакета: {package}"))
        packageInstallResult = run(["sudo" ,"apt", "install", "-y", package], capture_output=True)
    except Exception as PackageInstallError:
        print(colorText("red", f"[-] Установка пакета {package} завершилась с ошибкой:\n{PackageInstallError}"))
        sys.exit()

    print(colorText("green", f"[+] Пакет {package} успешно был установлен"))