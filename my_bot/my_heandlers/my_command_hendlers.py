from bot.bot import Bot
from bot.event import Event
import utils.image_utils as imut
from worker import worker_queue, Worker_data, Worker_type
# from utils.browser_utils import browser_page_screen_shot, ClickType
from settings import chat_id, bot
from utils.utils import send_file_to_chat
# import requests as req
import enum
import aiohttp
import time
# import asyncio



class ClickType(enum.Enum):
    traffick_click_1 = 1

async def send_weather(is_send_message:bool = False):
    print('send_weather')
    global bot
    file_name = "files/image/weather_image_source_" + str(time.monotonic_ns())  + ".png"
    new_file_name = "files/image/cut_image_" + str(time.monotonic_ns()) + ".png"
    url = "https://yandex.ru/pogoda/ru/krasnodar?lat=45.03547&lon=38.975313"
    # timeout = aiohttp.ClientTimeout(1)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/browser_page_screen_shot', params = {'file_name': 'test', 'url':url}, timeout = 30) as response:
                print('response ', response)
                if response.ok:
                    with open(file_name, 'wb') as file:
                        while True:
                            # print('while')
                            chunk = await response.content.readany()
                            if not chunk:
                                break
                            file.write(chunk)
                else:
                    raise Exception('Не удалось получить данные')
        imut.image_cut(file_name_old=file_name, file_name_new=new_file_name)
        send_file_to_chat(bot=bot, file_name=new_file_name, chat_id=chat_id)
    except Exception as error:
        error_message = "Не удалось получить погоду"
        print(f'ошибка "{error}"  ;;')
        if is_send_message:
            bot.send_text(chat_id=chat_id, text=error_message)
        
        print(error_message + " " + str(error))
        raise Exception(error_message + " " + str(error))
    # else:
        # bot.send_text(chat_id=chat_id, text=url)
        # pass
    print('end')


async def send_traffic(is_send_message:bool = False):
    print('send_traffic')
    global bot
    file_name = "files/image/traffic_image_source.png"
    url = "https://yandex.ru/maps/35/krasnodar/house/ulitsa_budyonnogo_2/Z0EYfwJjTEcOQFpvfXxydnhqYg==/?l=trf%2Ctrfe%2Cmasstransit&ll=38.963987%2C45.039967&z=15.8"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/browser_page_screen_shot', params = {'file_name': 'traffic', 'url':url}, timeout = 30) as response:
                if response.ok:
                    with open(file_name, 'wb') as file:
                        while True:
                            chunk = await response.content.readany()
                            if not chunk:
                                break
                            else:
                                file.write(chunk)
                else:
                    raise Exception('Не удалось получить данные')
        send_file_to_chat(bot=bot, file_name=file_name, chat_id=chat_id)
    except Exception as error:
        error_message = "Не удалось получить дорожный трафик"
        if is_send_message:
            bot.send_text(chat_id=chat_id, text=error_message)
        raise Exception(error_message + " " + str(error))
    # else:
        # bot.send_text(chat_id=chat_id, text=url)
        # pass


async def send_evening_newsletter_in_chat(is_send_message:bool = False):
    global bot
    weather_file_name = "files/image/weather_image_source.png"
    weather_new_file_name = "files/image/cut_image.png"
    weather_url = "https://yandex.ru/pogoda/ru/krasnodar?lat=45.03547&lon=38.975313"
    traffic_file_name = "files/image/traffic_image_source.png"
    traffic_url = "https://yandex.ru/maps/35/krasnodar/house/ulitsa_budyonnogo_2/Z0EYfwJjTEcOQFpvfXxydnhqYg==/?l=trf%2Ctrfe%2Cmasstransit&ll=38.963987%2C45.039967&z=15.8"

    try:
        # browser_page_screen_shot(file_name=weather_file_name, url=weather_url)
        # imut.image_cut(file_name_old=weather_file_name, file_name_new=weather_new_file_name)
        # browser_page_screen_shot(file_name=traffic_file_name, url=traffic_url, click_type=ClickType.traffick_click_1)

        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/browser_page_screen_shot', params = {'file_name': 'test', 'url':weather_url}, timeout = 30) as response:
                print('response ', response)
                if response.ok:
                    with open(weather_file_name, 'wb') as file:
                        while True:
                            # print('while')
                            chunk = await response.content.readany()
                            if not chunk:
                                break
                            file.write(chunk)
                else:
                    raise Exception('Не удалось получить данные')
        imut.image_cut(file_name_old=weather_file_name, file_name_new=weather_new_file_name)
        


        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/browser_page_screen_shot', params = {'file_name': 'traffic', 'url':traffic_url}, timeout = 30) as response:
                if response.ok:
                    with open(traffic_file_name, 'wb') as file:
                        while True:
                            chunk = await response.content.readany()
                            if not chunk:
                                break
                            else:
                                file.write(chunk)
                else:
                    raise Exception('Не удалось получить данные')
                

        bot.send_text(chat_id=chat_id, text="Вечерняя рассылка:")
        send_file_to_chat(bot=bot, file_name=weather_new_file_name, chat_id=chat_id)
        send_file_to_chat(bot=bot, file_name=traffic_file_name, chat_id=chat_id)

        # bot.send_text(chat_id=chat_id, text='Вечерняя рассылка')
        # send_file_to_chat(bot=bot, file_name=weather_new_file_name, chat_id=chat_id)
        # send_file_to_chat(bot=bot, file_name=traffic_file_name, chat_id=chat_id)
    except Exception as error:
        error_message = 'Не удалось получить данные для вечерней рассылки('
        if is_send_message:
            bot.send_text(chat_id=chat_id, text=error_message)
        raise Exception(error_message + " " + str(error))


def send_weather_in_chat(bot: Bot | None = None, event: Event | None = None) -> None:
    """отправка погоды в чат через очередь"""
    worker_queue.put(  # отправка погоды в чат
        Worker_data(Worker_type.send_weather, send_weather, None)
    )
    print('положили в очередь')


def send_traffic_in_chat(bot: Bot | None = None, event: Event | None = None) -> None:
    """отправка пробок в чат через очередь"""
    worker_queue.put(  # отправка погоды в чат
        Worker_data(Worker_type.send_trffic, send_traffic, None)
    )
    print('положили в очередь')


def evening_newsletter(bot: Bot | None = None, event: Event | None = None, worker_queue= None) -> None:
    """"Отправка вечерней рассылки с погодой и дорожным трафиком"""
    worker_queue.put(
        Worker_data(Worker_type.evening_newsletter, send_evening_newsletter_in_chat, None)
    )