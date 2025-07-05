from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def browser_page_screen_shot(
    file_name: str = "my_bot/files/image/screenshot.png",
    url: str = "https://yandex.ru/pogoda/ru/krasnodar?lat=45.03547&lon=38.975313",
    time_sleep: int = 2,
    width:int = 2000,
    heigth: int = 1000
) -> None:
    options = Options()
    options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    )
    driver = webdriver.Chrome(options=options)

    driver.set_window_size(width, heigth)
    driver.get(url)
    time.sleep(time_sleep)
    driver.save_screenshot(file_name)
    driver.quit()



if __name__ == '__main__':
    browser_page_screen_shot('file.png',     "https://yandex.ru/maps/35/krasnodar/house/ulitsa_budyonnogo_2/Z0EYfwJjTEcOQFpvfXxydnhqYg==/?l=trf%2Ctrfe%2Cmasstransit&ll=38.963987%2C45.039967&z=15.8")


    # "https://yandex.ru/maps/35/krasnodar/house/ulitsa_budyonnogo_2/Z0EYfwJjTEcOQFpvfXxydnhqYg==/?l=trf%2Ctrfe%2Cmasstransit&ll=38.963987%2C45.039967&z=15.8"