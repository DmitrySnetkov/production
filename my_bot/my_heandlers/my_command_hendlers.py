from bot.bot import Bot
from bot.event import Event
import utils.image_utils as imut
from worker import worker_queue, Worker_data, Worker_type
from utils.browser_utils import browser_page_screen_shot
from settings import chat_id
from utils.utils import send_file_to_chat
from settings import bot



def send_weather():
    global bot
    file_name = "weather_image_source.png"
    new_file_name = "cut_image.png"

    browser_page_screen_shot(file_name=file_name)
    imut.image_cut(file_name_old=file_name, file_name_new=new_file_name)
    send_file_to_chat(bot = bot, file_name = new_file_name, chat_id= chat_id)



def send_weather_in_chat(bot: Bot, event: Event) -> None:
    """отправка погоды в чат через очередь"""
    worker_queue.put(  # отправка погоды в чат
        Worker_data(
            Worker_type.send_weather,
            send_weather,
            None
        )
    )
