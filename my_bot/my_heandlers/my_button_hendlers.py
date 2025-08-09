from bot.bot import Bot
from bot.event import Event
# from my_log import log
import datetime as dt
from settings import chat_id

translate_matrix_1 = str.maketrans(
    """qwertyuiop[]';lkjhgfdsazxcvbnm,./`@#$^&""",
    """йцукенгшщзхъэждлорпавыфячсмитьбю.ё"№;:?""",
)


def button_cb(bot: Bot, event: Event) -> None:
    # log.logger.info(event)
    time_start = dt.datetime.now()
    match str(event.data["callbackData"]):
        case "button_1":
            bot.send_text(
                chat_id=chat_id,
                text=str(event.data["message"]["text"])
                .lower()
                .translate(translate_matrix_1),
            )
            bot.answer_callback_query(
                query_id=event.data["queryId"], text="Переведено", show_alert=False
            )
            # log.logger.info("переведено")
        case _:
            # log.logger.info("Неизвестная кнопка или не реализован обработчик кнопки")
            bot.answer_callback_query(
                query_id=event.data["queryId"],
                text="Неизвестная кнопка или не реализован обработчик кнопки",
                show_alert=False,
            )
    # log.logger.info(f"обработка запроса заняла: {dt.datetime.now() - time_start}")
