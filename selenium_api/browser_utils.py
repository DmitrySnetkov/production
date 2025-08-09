from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import enum
import fastapi as fapi
import asyncio as aio

app = fapi.FastAPI()

class ClickType(enum.Enum):
    traffick_click_1 = 1


@app.get('/browser_page_screen_shot')
async def browser_page_screen_shot(
    file_name: str = "screenshot",
    url: str = "https://yandex.ru/pogoda/ru/krasnodar?lat=45.03547&lon=38.975313",
    time_sleep: float = 2.5,
    width: int = 2000,
    heigth: int = 1000,
    click_type: int | None = None,
):
    # print(url)
    try:
        print('browser_page_screen_shot')
        file_name = file_name + '_' + str(time.monotonic_ns()) + '.png'
        options = Options()
        options.add_argument("--headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )
        # options.add_argument(
        #     "accept = text/html"
        # )

        print('browser_page_screen_shot - 0.5')
        driver = webdriver.Chrome(options=options)

        driver.set_window_size(width, heigth)
        print('browser_page_screen_shot -1')
        driver.get(url)
        print('browser_page_screen_shot -2')
        print(f'жду {file_name}')
        await aio.sleep(time_sleep)
        print(f'закончил ждать {file_name}')

        match click_type:
            case ClickType.traffick_click_1:
                try:
                    # aio.sleep(0.2)
                    driver.find_element(
                        By.XPATH, "/html/body/div[1]/div[2]/div[8]/div/span"
                    ).click()
                    await aio.sleep(0.4)
                except:
                    print("кнопка не найдена")
            case _:
                pass
        print('browser_page_screen_shot -3')
        driver.save_screenshot(file_name)
        driver.quit()
        print('browser_page_screen_shot end')
        return fapi.responses.FileResponse(file_name)
    except Exception as error:
        return fapi.HTTPException(500, error) 

# if __name__ == "__main__":
#     browser_page_screen_shot(
#         "file.png",
#         "https://yandex.ru/maps/35/krasnodar/house/ulitsa_budyonnogo_2/Z0EYfwJjTEcOQFpvfXxydnhqYg==/?l=trf%2Ctrfe%2Cmasstransit&ll=38.963987%2C45.039967&z=15.8",
#         click_type=ClickType.traffick_click_1,
#     )

#     # "https://yandex.ru/maps/35/krasnodar/house/ulitsa_budyonnogo_2/Z0EYfwJjTEcOQFpvfXxydnhqYg==/?l=trf%2Ctrfe%2Cmasstransit&ll=38.963987%2C45.039967&z=15.8"
    # browser_page_screen_shot("file.png")