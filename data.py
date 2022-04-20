import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ID = "id"
# XPATH = "xpath"
# LINK_TEXT = "link text"
# PARTIAL_LINK_TEXT = "partial link text"
# NAME = "name"
# TAG_NAME = "tag name"
# CLASS_NAME = "class name"
# CSS_SELECTOR = "css selector"

# url = f'https://steamcommunity.com/profiles/76561199172709832/games?tab=all'
# url = f'https://steamcommunity.com/profiles/76561198395102109/games?tab=all'


def get_gameHours(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options,executable_path="data\chromedriver.exe")
    driver.get(url)
    timeout = 5
    number_of_games = 0
    try:
        # Вместо body возможно нужен другой тег указывать, характерный для сайта
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@class="gameListRow"]'))
        WebDriverWait(driver, timeout).until(element_present)
        sleep(0.2)
        # получаю блоки
        games_blocks = driver.find_elements(By.XPATH, '//*[@class="gameListRow"]')
        games_hours = []

        for games_block in games_blocks:
            number_of_games = number_of_games + 1
            name = games_block.find_element(By.CSS_SELECTOR,
                                            'div.gameListRowItem > div.gameListRowItemTop > '
                                            'div.gameListRowItemTopPrimary '
                                            '> div').text

            try:
                hours = games_block.find_element(By.CSS_SELECTOR,
                                                 'div.gameListRowItem > div.gameListRowItemTop > '
                                                 'div.gameListRowItemTopPrimary > h5').text
            except Exception:
                hours = None

            games_hourss = {
                "name_game": name,
                "time_in_the_game": hours
            }

            games_hours.append(games_hourss)

        driver.close()
        driver.quit()

        return games_hours, number_of_games

    except TimeoutException:
        driver.close()
        driver.quit()
        print("Минув час очікування завантаження сторінки")

        return None, number_of_games

# print(get_gameHours(url))
def notification_in_tg():
    """Відправляю сповіщення в телеграм бота"""

    # Дані TG бота
    bot_id = '{bot_id}'
    chat_id = '{chat_id}'

    requests.get(
        f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text=Готовооо❗")
