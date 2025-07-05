from bot.bot import Bot


def check_except_str(text: str, except_set: set[str] | list[str] | tuple[str]) -> bool:
    """проверка на запретные строки
    проверяет каждое слово входящего текста не является ли оно запрещённым для перевода словом
    """

    for i in except_set:
        if i in text:
            return True
    return False


def check_send_keybord(text: str, percent: float = 0.7) -> bool:
    """проверка надо ли переводить входной текст.
    переводит только в том случае если указанный процент текста(percent) является английским
    учитываются только те символы, которые являются буквами
    """
    cnt = 0
    l = [i for i in text if i.isalpha()]
    for i in l:
        if "a" <= i <= "z":
            cnt += 1
    if cnt / len(l) >= percent:
        return True
    return False


def send_file_to_chat(bot: Bot, file_name: str, chat_id: str):
    with open(file_name, "rb") as file:
        bot.send_file(chat_id=chat_id, file=file)
