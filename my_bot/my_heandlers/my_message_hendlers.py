from bot.bot import Bot
from bot.event import Event
from settings import TOKEN, chat_id, is_test
import json as js
# from my_log import log
import utils.utils as utils


except_str_set = {"http"}
json_keys = [
    {"text": "Перевести с клингонского", "callbackData": "button_1"}
    # {"text": "button_2", "callbackData": "button_2"},
]

def message_cb(bot: Bot, event: Event) -> None:
    # log.logger.info(event)
    if utils.check_except_str(event.data['text'], except_str_set):
        # log.logger.info('запретные строки')
        return None
    if utils.check_send_keybord(event.data['text'], 0.7):
        bot.send_text(
            chat_id=chat_id,
            text=event.data["text"],
            inline_keyboard_markup=f"[{js.dumps(json_keys)}]",
        )
        # log.logger.info("предложен перевод")
    else:
        # log.logger.info("перевод не требуется")
        pass
