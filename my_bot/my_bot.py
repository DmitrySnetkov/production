from bot.bot import Bot
import time
from bot.handler import MessageHandler, BotButtonCommandHandler, CommandHandler
from settings import TOKEN, chat_id, is_test, bot
import my_heandlers.my_message_hendlers as mmh
import my_heandlers.my_button_hendlers as mbh
from my_log import log
import multiprocessing as mp
import worker as wr
import my_heandlers.my_command_hendlers as mch
import scheduler as scr


def check_settings(tab: int = 2) -> None:
    if TOKEN is None or chat_id is None or is_test is None:
        print("Не указаны настроки:".center(50, "_"))
        if TOKEN is None or TOKEN == "":
            print(f"{' '*tab}Укажите токен")
        if chat_id is None:
            print(f"{' '*tab}Укажите id чата")
        if is_test is None:
            print(f"{' '*tab}Укажите режим запуска(тест/работчий режим)")
        # //TODO Добавить запись в лог
        time.sleep(5)
        exit()


def main() -> None:
    bot.dispatcher.add_handler(CommandHandler(command="weather", callback=mch.send_weather_in_chat))
    bot.dispatcher.add_handler(CommandHandler(command="traffic", callback=mch.send_traffic_in_chat))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=mbh.button_cb))
    bot.dispatcher.add_handler(MessageHandler(
        filters=lambda event: not event.data["text"].startswith("/"),
        callback=mmh.message_cb,
    ))

    worker_process = mp.Process(
        daemon=True,
        name="worker_process",
        target=wr.worker_main_loop,
        args=(wr.worker_queue,),
    )
    worker_process.start()

    scheduler_process = mp.Process(
        daemon=True,
        name="scheduler_process",
        target=scr.scheduler_main,
        args=(wr.worker_queue,),
    )
    scheduler_process.start()


    print("Бот запущен")
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    try:
        check_settings()
        main()
    except Exception as error:
        # log.logger.error(error)
        print(f"Ошибка - {error}")


# # //TODO надо добавить проверку на почтовые ящики, чтобы при ссылке на человека не предлагало
# #       перевод
# # //TODO надо сделать чтобы переводило только необходимые слова в сообщении(чтобы не переводило
# #       ссылки, почтовые ящики и аналогичное)
# # //TODO надо сделать чтобы при старте бота он начинал обрабатывать только новые сообщения и не
# #       предлагал перевод к сообщениям, которые были написаны до старта бота
# # //TODO добавить в логи то с какими настройками стартовал бот(обрезать токен до последних
# #       нескольких цифр)