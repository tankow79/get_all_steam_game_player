#
# from AndraX
#
import json
import os
from json import load
from data import *

# создать новый текстовый файл
if not open("finished.txt", "a"):
    open("finished.txt", "w")

print("Все файлы:", os.listdir('./maFiles'))

games = []

# распечатать все файлы рекурсивно
for dirpath, dirnames, filenames in os.walk(".\maFiles"):
    # перебрать файлы
    for filename in filenames:
        if filename.split('.')[1] == 'maFile':
            maFile_filas = os.path.join(dirpath, filename)
            print("Файл:", maFile_filas)

            # Получаю логін файла
            login = filename.split('.')[0]
            # print('Логін: ', login)

            # Получаю SteamID
            maFile_data = load(open(maFile_filas))
            SteamID = maFile_data["Session"]["SteamID"]
            # print('SteamID: ', SteamID)

            # Cилка
            url = f'https://steamcommunity.com/profiles/{SteamID}/games?tab=all'
            # Парсинг
            games_hours, number_of_games = get_gameHours(url)

            if games_hours is None:
                user = {
                    'Login': login,
                    'SteamID': SteamID,
                    'Games': games_hours
                }
            else:
                user = {
                    'Login': login,
                    'SteamID': SteamID,
                    'number_of_games': number_of_games,
                    'Games': games_hours
                }

            games.append(user)
            # print(games)
            # Записування в файл
            with open(r"data.json", 'a', encoding='utf-8') as file:
                file.write(json.dumps(user, ensure_ascii=False, indent=2))
                # file.write(',\n')

    # Записування в файл
    with open(r'games.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(games, ensure_ascii=False, indent=2))

notification_in_tg()
