import schedule as sch
import time
from settings import bot
import my_heandlers.my_command_hendlers as ch
import multiprocessing as mp
import functools as fnt


def end_day_send(queue:mp.Queue):
    # print('end_day_send')
    # print(queue)
    ch.evening_newsletter(worker_queue=queue)


def scheduler_main(queue:mp.Queue):
    fn = fnt.partial(end_day_send, queue = queue)

    # sch.every().minute.at(":05").do(fn)
    sch.every().day.at("17:50:00").do(fn)
    # sch.every().day.at("00:30:00").do(fn)


    while True:
        #проверка на время, и пауза на час при необходимости
        try:
            sch.run_pending()
            time.sleep(1)
        except Exception as error:
            print(f'ошибка в цикле заданий {error}')



# <multiprocessing.queues.Queue object at 0x0000029250385B50>
# <multiprocessing.queues.Queue object at 0x000001ED7F490BF0>

# if __name__ == '__main__':
#     scheduler_main()