from bot.bot import Bot
from bot.event import Event
import utils.image_utils as imut
from worker import worker_queue, Worker_data, Worker_type
from utils.browser_utils import browser_page_screen_shot
from settings import chat_id, bot
from utils.utils import send_file_to_chat


def send_weather():
    global bot
    file_name = "my_bot/files/image/weather_image_source.png"
    new_file_name = "my_bot/files/image/cut_image.png"
    url = "https://yandex.ru/pogoda/ru/krasnodar?lat=45.03547&lon=38.975313"

    browser_page_screen_shot(file_name=file_name, url=url)
    imut.image_cut(file_name_old=file_name, file_name_new=new_file_name)
    send_file_to_chat(bot=bot, file_name=new_file_name, chat_id=chat_id)
    bot.send_text(chat_id=chat_id, text=url)


def send_traffic():
    global bot
    file_name = "my_bot/files/image/traffic_image_source.png"
    url = "https://yandex.ru/maps/35/krasnodar/house/ulitsa_budyonnogo_2/Z0EYfwJjTEcOQFpvfXxydnhqYg==/?l=trf%2Ctrfe%2Cmasstransit&ll=38.963987%2C45.039967&z=15.8"

    browser_page_screen_shot(file_name=file_name, url=url)
    send_file_to_chat(bot=bot, file_name=file_name, chat_id=chat_id)
    # bot.send_text(chat_id=chat_id, text=url)


def send_weather_in_chat(bot: Bot, event: Event) -> None:
    """отправка погоды в чат через очередь"""
    worker_queue.put(  # отправка погоды в чат
        Worker_data(Worker_type.send_weather, send_weather, None)
    )


def send_traffic_in_chat(bot: Bot, event: Event) -> None:
    """отправка пробок в чат через очередь"""
    worker_queue.put(  # отправка погоды в чат
        Worker_data(Worker_type.send_trffic, send_traffic, None)
    )
