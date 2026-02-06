import os
import sys
from subprocess import run

# Проверка есть ли requirments
dirPath = "/".join(str(__file__).split("/")[:-1])
all_items = os.listdir(dirPath)
allScriptNeed = ["requirments.txt"]

is_all_files_exists = True

for item in allScriptNeed:
    if item not in os.listDir(all_items):
        print(f"[-] Файл {item} отсутствует")
        is_all_files_exists = False

if not is_all_files_exists:
    print("[-] Отстуствуют необходимые файлы.")
    sys.exit()

# Установка необходимых пакетов

# Обновление доступных пакетов
try:
    print("[~] Обновление информации о возможности обновления доступных пакетов")
    result = run(["sudo", "apt", "update"])
    if result.stderr == 0:
        print("[+] Обновлен список доступных пакетов и их версий")
except Exception as PackagesUpdateError:
    print(f"[-] Обновление списка доступных пакетов и их версий завершилось с ошибкой:\n{PackagesUpdateError}")

# Необходимые пакеты для корректной работы системы
packages = [
    'curl'
]

# Установка пакетов из списка
for package in packages:
    try:
        print(f"[~] Установка пакета: {package}")
        packageInstallResult = run(["apt", "install", package], capture_output=True)
        if packageInstallResult.stderr == 0:
            print(f"[+] Пакет {package} успешно был установлен")
    except Exception as PackageInstallError:
        print(f"[-] Установка пакета {package} завершилась с ошибкой:\n{PackageInstallError}")

# Установка необходимых библиотек из requirments.txt

# Создание виртаульного оркужения
try:
    print("[~] Создание виртуального окружения")
    venvCreationResult = run(["python3", "-m", "venv", "venv"], capture_output=True)
    if venvCreationResult.stderr == 0:
        print("[+] Виртуальное окружение успешно создано")
except Exception as venvCreationError:
    print(f"[-] При создании виртуального окружения произошла ошибка:\n{venvCreationError}")
    sys.exit()

# Активация виртуального окружения
try:
    print("[~] Активация виртуального окружения")
    run(["source", "venv/bin/activate"])
except Exception as venvActivationError:
    print(f"[-] При активации виртуального окружения произошла ошибка:\n{venvCreationError}")
    sys.exit()

# Установка зависимостей
try:
    print("[~] Установка зависимостей requirements.txt")
    reqInstallResults = run(["pip", "isntall", "-r", "requirements.txt"], capture_output=True)
    if reqInstallResults.stderr == 0:
        print("[+] Зависимости из requirements.txt были успешно установлены")
except Exception as reqInstallError:
    print(f"[-] При установке зависимостей requirements.txt произошла ошибка:\n{reqInstallResults}")
    sys.exit()

# Вывод имеющихся библиотек
currentPythonLibrary = run(["pip", "list"], capture_output=True, text=True)
print(currentPythonLibrary.stdout)
