import os
from subprocess import run
from colorama import Fore, Style
import sys
import json
from getpass import getpass

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
    
# Сообщение при котором не возможна дальнейшая работа скрипта с выходом 
def errorMessage():
    print(Fore.RED + "[-] Дальнейшая работа скрипта не может быть возможной" + Style.RESET_ALL)
    sys.exit()

# Клонирование репозиториев
print()
print(colorText('cyan', (('=') * 5 + " Установка HackMe Hospital " + ('=') * 5), True))
print()

print(colorText('cyan', (('=') * 5 + " Клонирование необходимых репозиториев " + ('=') * 5), True))

# Получение текущего местоположения скрипта для получения информации о существовании необходимых файлов
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir) # Переход в текущее местоположение
files = os.listdir()

isReqiredFilesInDir = True
required_files = ['repos.json', 'xampp-linux-x64-8.0.30-0-installer.run'] # Необходимые файлы для работы скрипта

# Проверка что все необходимые файлы присутствуют
for file in required_files:
    if file not in files:
        print(colorText('red', f'[-] Нет необходимого для работы скрипта файла: {file}'))
        sys.exit()

with open('repos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

repositories = data['repos']

installed_repos = []
not_installed_repos = []

install_repos_count = 0

# Клонирование репозиториев по итерации
for reposit_name, repo_path in repositories.items():
    if len(repo_path) != 0 or repo_path != '':
        print(colorText('blue', f'[~] Клонирование репозитория: {reposit_name}'))
        try:
            # Клонирование репозитория c захватом stdout и stderr с временем на выполнение 5 секунд
            result = run(["git", "clone", repo_path], capture_output=True, text=True, timeout=5)
            if result.stderr != 0:
                print(colorText('red', f'Ошибка в клонировании репозитория {reposit_name}: {repo_path}\n{result.stderr}'))
                not_installed_repos.append(reposit_name)
                continue

            print(colorText('green', f'[+] Репозиторий {reposit_name} был успешно клонирован'))
            install_repos += 1 # Подсчет кол-ва клонированных репозиториев
            install_repos.append(reposit_name)
            
        except Exception as error:
            print(colorText('red', f'[-] Не удалось клонировать репозиторий {reposit_name}:{repo_path}\nОшибка:{error}'))
            # Выход в случае неудачной попытки клонирования репозитория
            errorMessage()
    else:
        print(colorText('red', f'[!] У репозитория {reposit_name} отсутсвует адрес\n[!] Репозиторий {reposit_name} не будет клонирован'))

# Общее кол-во репозиториев которые нужно было установить из repos.json
repos_count = len(data.keys())

if repos_count == install_repos_count:
    print(colorText('green', f'[+] Все репозитории были успешно клонированы. Кол-во клонированных репозиториев: {install_repos_count}'))
elif install_repos_count < repos_count:
    print(colorText('yellow', f'[!] Кол-во клонированных репозиториев: {install_repos_count}'))
    print(colorText('yellow', 'Не клонированные репозитории:'))
    for repo in not_installed_repos:
        print(colorText('yellow', f'- {repo};'))
    errorMessage()
else:
    print(colorText('red', f'[-] Кол-во клонированных репозиториев: 0'))
    errorMessage()

# Подготовка окружения
print()
print(colorText('cyan', (('=') * 5 + " Подготовка окружения " + ('=') * 5), True))
print()

# Запуск установки XAMPP
print(colorText('blue', '[~] Установка XAMPP'))
xampp_path = os.path.join(script_dir, "HackMeHospInstall", "xampp-linux-x64-8.0.30-0-installer.run")

# Назначение прав XAMPP
try:
    print(colorText("blue", "[~] Установка прав на исполнение XAMPP"))
    add_xampp_rights_result = run(["chmod", "+x", xampp_path], capture_output=True, text=True)
except:
    pass

try:
    xampp_launch_result = run(["sudo", "./" + xampp_path], capture_output=True, text=True)
    if result.stderr != 0:
        print(colorText('red', f"[-] Не удалось запустить xampp: {result.stderr}"))
        errorMessage() # Выход в случае неудачи в запуске xampp
    print(colorText('green', "[+] Запуск выполнен успешно"))
except Exception as error:
    print(colorText("red", f"[-] При запуске xampp произошла ошибка: {error}"))
    errorMessage()

all_opt_items = os.listdir("/opt")

print(colorText("blue", "[~] Проверка сущетсвования необходимых директорий XAMPP"))
isLamppExist = False

for item in all_opt_items:
    if os.path.isdir(item):
        if item == "lampp":
            isLamppExist = True

if isLamppExist:
    print(colorText("green", "[+] Директория /lampp присутствует"))
else:
    print(colorText("green", "[-] Директория /lampp отсутствует"))
    errorMessage()

# Запуск XAMPP
try:
    pass
except Exception as error:
    pass

# Переход в директорию Vulnerable-Hospital-Web-Application
try:
    os.chdir(os.path.join(script_dir, "Vulnerable-Hospital-Web-Application"))
except Exception as dir_changing_error:
    print(colorText("red", "[-] Отсутсвует директория Vulnerable-Hospital-Web-Application"))
    errorMessage()



print()
print(colorText("MAGENTA", "[?] Справки по установке компонентов:\nРепозиторий HackeMe Hospital: https://github.com/minaramez/Vulnerable-Hospital-Web-Application\nУстановка XAMPP: https://www.geeksforgeeks.org/linux-unix/how-to-install-xampp-in-linux/?ysclid=ml9brpc1yh149049143"))
