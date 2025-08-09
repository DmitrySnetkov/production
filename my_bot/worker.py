import multiprocessing as mp
import enum
from typing import NamedTuple, Callable
# from my_log import log
import asyncio as aio


class Worker_type(enum.Enum):
    get_weather  = 1  # получение погоды
    send_weather = 2  # отправка погоды в чат
    cut_image    = 3  # обрезать изображение
    send_trffic  = 4  # отправить дорожный трафик
    evening_newsletter = 5 # вечерняя рассылка


class Worker_data(NamedTuple):
    type: Worker_type
    function: Callable
    data: dict | None


worker_queue = mp.Queue(50)


# def worker_main_loop(queue: mp.Queue):
#     while True:
#         if data := queue.get():
#             # print(f"Задание с типом {data.type}")
#             # print(data)
#             # log.logger.info(f"Задание с типом {data.type}")
#             match data.type:
#                 case type if type in Worker_type:
#                     try:
#                         if data.data is None:
#                             data.function()
#                         else:
#                             data.function(**data.data)
#                         # log.logger.info("задание выполнено успешно")
#                     except Exception as error:
#                         pass
#                         # log.logger.info(f"задание не выполнено. ошибка - {error}")
#                         #TODO добавить запись о неудаче в базу
#                 case _:
#                     # log.logger.info(
#                     #     "Тип задания не найден, задание возвращено в очередь"
#                     # )
#                     queue.put(data)




async def worker_main_loop_async(queue: mp.Queue):
    # print('worker_main_loop_async')
    while True:
        if data := queue.get():
            print(f"Задание с типом {data.type}")
            print(data)
            # log.logger.info(f"Задание с типом {data.type}")
            match data.type:
                case type if type in Worker_type:
                    try:
                        if data.data is None:
                            task = aio.create_task(data.function())
                        else:
                            task = aio.create_task(data.function(**data.data))
                        # log.logger.info("задание выполнено успешно")
                        print(task)
                        await task
                    except Exception as error:
                        print(f'Ошибка {error}')
                        # pass
                        # log.logger.info(f"задание не выполнено. ошибка - {error}")
                        #TODO добавить запись о неудаче в базу
                case _:
                    print('не корректный тип')
                    # log.logger.info(
                    #     "Тип задания не найден, задание возвращено в очередь"
                    # )
                    pass
                    # queue.put(data)

def main(queue: mp.Queue):
    aio.run(worker_main_loop_async(queue))



# TODO допилить асинхронность