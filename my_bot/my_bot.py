from bot.bot import Bot
import os
import time
import datetime as dt
from bot.handler import MessageHandler
# from bot.handler import CommandHandler
from bot.handler import BotButtonCommandHandler
from bot.event import Event
# import requests as req
import json as js
import loguru as log
import pathlib as plib
from settings import TOKEN, chat_id, is_test
# os.system('cls')


# //TODO надо добавить проверку на почтовые ящики, чтобы при ссылке на человека не предлагало
#       перевод
# //TODO надо сделать чтобы переводило только необходимые слова в сообщении(чтобы не переводило
#       ссылки, почтовые ящики и аналогичное)
# //TODO надо сделать чтобы при старте бота он начинал обрабатывать только новые сообщения и не
#       предлагал перевод к сообщениям, которые были написаны до старта бота
# //TODO добавить в логи то с какими настройками стартовал бот(обрезать токен до последних
#       нескольких цифр)
# прогноз погоды
# пробки

# region logger

log_info_path  = plib.Path(__file__).parent /'log/log_info.log'
log_error_path = plib.Path(__file__).parent /'log/log_error.log'
# print(log_info_path.name)
# print(type(log_info_path.name))
# print(f'{log_info_path=}')
# print(f'{log_error_path=}')
# log_info_path = str(log_info_path)
# print(type(log_info_path))
# print(log_info_path)
# log_info_path.
# exit()

# log.logger.remove()
log.logger.add(str(log_info_path), format="{time} {level} {message}", level="INFO", rotation ="1 day")
log.logger.add(str(log_error_path), format="{time} {level} {message}", level="ERROR", rotation ="1 day")
# log.logger.remove()

# endregion


# region settings

translate_matrix_1 = str.maketrans(
    '''qwertyuiop[]';lkjhgfdsazxcvbnm,./`@#$^&''', '''йцукенгшщзхъэждлорпавыфячсмитьбю.ё"№;:?'''
)
json_keys = [
    {"text": "Перевести с клингонского", "callbackData": "button_1"}
    # {"text": "button_2", "callbackData": "button_2"},
]
except_str_set = {
    'http'
}

# endregion


def check_settings(tab: int = 2) -> None:
    if TOKEN is None or chat_id is None or is_test is None:
        print("Не указаны настроки:".center(50, '_'))
        if TOKEN is None or TOKEN == '':
            print(f"{' '*tab}Укажите токен")
        if chat_id is None:
            print(f"{' '*tab}Укажите id чата")
        if is_test is None:
            print(f"{' '*tab}Укажите режим запуска(тест/работчий режим)")
        # //TODO Добавить запись в лог
        time.sleep(5)
        exit()


def check_except_str(text: str, except_set: set[str] | list[str] | tuple[str]) -> bool:
    for i in except_set:
        if i in text:
            return True
    return False


def check_send_keybord(text: str, percent: float = 0.7) -> bool:
    cnt = 0
    l = [i for i in text if i.isalpha()]
    for i in l:
        if 'a' <= i <= 'z':
            cnt += 1
    if cnt/len(l) >= percent:
        return True
    return False


def message_cb(bot: Bot, event: Event) -> None:
    # print(event.data)
    if not is_test:
        log.logger.info(event)
        if check_except_str(event.data['text'], except_str_set):
            log.logger.info('запретные строки')
            return None
        if check_send_keybord(event.data['text'], 0.7):
            bot.send_text(
                chat_id=chat_id,
                text=event.data["text"],
                inline_keyboard_markup=f"[{js.dumps(json_keys)}]",
            )
            log.logger.info("предложен перевод")
        else:
            log.logger.info("перевод не требуется")
    else:
        print(event.data)


def button_cb(bot: Bot, event: Event) -> None:
    # print(f"{event.data=}")
    log.logger.info(event)
    time_start = dt.datetime.now()
    match str(event.data["callbackData"]):
        case "button_1":
            bot.send_text(
                chat_id=chat_id,
                text=str(event.data["message"]["text"]).lower().translate(translate_matrix_1),
            )
            bot.answer_callback_query(
                query_id=event.data["queryId"],
                text="Переведено",
                show_alert=False
            )
            log.logger.info("переведено")
        case _:
            log.logger.info(
                "Неизвестная кнопка или не реализован обработчик кнопки")
            bot.answer_callback_query(
                query_id=event.data["queryId"],
                text="Неизвестная кнопка или не реализован обработчик кнопки",
                show_alert=False,
            )
    log.logger.info(f"обработка запроса заняла: {dt.datetime.now() - time_start}" )


def main() -> None:
    bot = Bot(token=TOKEN)
    # print(bot.)
    # bot.
    # bot.
    # bot.send_text('689445373@chat.agent', 'ay')
    # with open(r"my_bot\shia-labeouf-magic.gif", 'rb') as file:
    #     bot.send_file('689445373@chat.agent', file = file)
    bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=button_cb))
    print("Бот запущен...")
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    try:
        check_settings()
        main()
    except Exception as error:
        log.logger.error(error)
        # print('конец')