import multiprocessing as mp
import enum
from typing import NamedTuple, Callable
from my_log import log


class Worker_type(enum.Enum):
    get_weather  = 1  # получение погоды
    send_weather = 2  # отправка погоды в чат
    cut_image    = 3  # обрезать изображение
    send_trffic  = 4  # отправить дорожный трафик


class Worker_data(NamedTuple):
    type: Worker_type
    function: Callable
    data: dict | None


worker_queue = mp.Queue(50)


def scheduler_main_loop(queue: mp.Queue):
    while True:
        if data := queue.get():
            # print(f"Задание с типом {data.type}")
            log.logger.info(f"Задание с типом {data.type}")
            match data.type:
                case type if type in Worker_type:
                    try:
                        if data.data is None:
                            data.function()
                        else:
                            data.function(**data.data)
                        log.logger.info("задание выполнено успешно")
                    except Exception as error:
                        log.logger.info(f"задание не выполнено. ошибка - {error}")
                        #TODO добавить запись о неудаче в базу
                case _:
                    log.logger.info(
                        "Тип задания не найден, задание возвращено в очередь"
                    )
                    queue.put(data)
