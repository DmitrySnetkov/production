from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def browser_page_screen_shot(
    file_name: str = "my_bot/files/image/screenshot.png",
    url: str = "https://yandex.ru/pogoda/ru/krasnodar?lat=45.03547&lon=38.975313",
    time_sleep: int = 5,
) -> None:
    options = Options()
    # options.add_argument('headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    )
    driver = webdriver.Chrome(options=options)

    driver.maximize_window()
    driver.get(url)
    time.sleep(time_sleep)
    driver.get_screenshot_as_file(file_name)
    driver.quit()
