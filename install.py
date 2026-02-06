import os
import sys
from subprocess import run
from pathlib import Path

# Проверка есть ли requirments
script_dir = Path(__file__).parent.absolute()
allScriptNeed = ["requirements.txt"]

is_all_files_exists = True

for item in allScriptNeed:
    if item not in os.listdir(script_dir):
        print(f"[!] Файл {item} отсутствует")
        is_all_files_exists = False

if not is_all_files_exists:
    print("[-] Отстуствуют необходимые файлы.")
    sys.exit()

# Установка необходимых пакетов

# Обновление доступных пакетов
try:
    print("[~] Обновление информации о возможности обновления доступных пакетов")
    result = run(["sudo", "apt", "update"])
except Exception as PackagesUpdateError:
    print(f"[-] Обновление списка доступных пакетов и их версий завершилось с ошибкой:\n{PackagesUpdateError}")

print("[+] Обновлен список доступных пакетов и их версий")

# Необходимые пакеты для корректной работы системы
packages = [
    'curl'
]

# Установка пакетов из списка
for package in packages:
    try:
        print(f"[~] Установка пакета: {package}")
        packageInstallResult = run(["apt", "install", package], capture_output=True)
    except Exception as PackageInstallError:
        print(f"[-] Установка пакета {package} завершилась с ошибкой:\n{PackageInstallError}")

print(f"[+] Пакет {package} успешно был установлен")

# Установка необходимых библиотек из requirments.txt

# Создание виртаульного оркужения
try:
    print("[~] Создание виртуального окружения")
    venvCreationResult = run(["python3", "-m", "venv", "venv"], capture_output=True)
except Exception as venvCreationError:
    print(f"[-] При создании виртуального окружения произошла ошибка:\n{venvCreationError}")
    sys.exit()

print("[+] Виртуальное окружение успешно создано")

print("[?] Перейдите в source venv/bin/activate и запустите:\npip install -r requirements.txt")

