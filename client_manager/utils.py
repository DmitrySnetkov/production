import pathlib as plib
import os
import shutil as sh
import enum
import pytest as pt
import dataclasses as dt
import tabulate as tab
import json
import re

class CheckType(enum.Enum):
    update = 1
    delete = 2

clien_manager_file_name = 'client_manager_settings.json'

def files_copy(path:str|None = None, root_path:plib.Path=None) -> tuple[bool, plib.Path]:
    path = path.strip()
    if not path:
        print(' '*4+"Неоходимо указать путь до клиента") 
        return None

    p = plib.Path(path)

    if not p.exists():
        print(' '*4+'Путь не существует')
        return None

    dir_list = tuple(p.iterdir())

    print(' '*4+f'Найдено {len(dir_list)} файлов/папок')

    # print(f'{p=}')
    new_directory_name = p.name

    target_path = root_path.joinpath(new_directory_name)
    sh.copytree(p, target_path, dirs_exist_ok=True, is_root = True)
    return (True, target_path)

def client_add(command:str, root_path:plib.Path):
    command = command.strip()
    if not command:
        print(' '*4+"Комманда не найдена")
        return None
    command = command.split(' ')

    if len(command) < 2:
        print(' '*4+'Не укзан путь папке с клиентом, который необходимо скачать')
        return None

    #TODO надо добавить проверку для формата пути
    responce = files_copy(path = command[1], root_path = root_path)
    if responce[0]:
        with open(responce[1]/clien_manager_file_name, 'w', encoding='utf-8') as file:
            # print(responce[1]/clien_manager_file_name)
            js = {'client_path' : str(command[1])}
            # print(js)
            json.dump(js, file, indent=4, ensure_ascii = False)
        print(' '*4+"Клиент успешно скачан")

def update_delete_check(command, root_path, check_type:CheckType):
    match check_type:
        case CheckType.update:
            error_text = 'обновить'
        case CheckType.delete:
            error_text = 'удалить'
        case _:
            return None
        
    command = command.strip()
    if not command:
        print(' '*4+"Комманда не найдена")
        return None
    command = command.split(' ')

    if len(command) < 2:
        print(' '*4+f'Не указан номер клиента, который необходимо {error_text}')
        return None
    # TODO надо добавить проверку для формата пути
    
    if not command[1].isdigit():
        print(' '*4+"Второй параметр комманды должен быть числовым, это номер клиента")
        return None
    number = int(command[1])
    client_list = client_list_get(root_path=root_path)

    if len(client_list) < int(number):
        print(' '*4+"Указанный номер клиента больше чем их количество")
        return None
    return number

def client_delete(command:str, root_path):
    number = update_delete_check(command, root_path, CheckType.delete)
    if number is None:
        return None
    delete_path = client_list_get(root_path)[number-1]
    if delete_path.exists():
        print(' '*4+f"Вы удаляете клиент {delete_path.name}")
        responce = input(' '*4+"Вы точно уверены что хотите удалить Y/N:  ").lower()
        if responce in ('y', 'yes'):
            sh.rmtree(delete_path)
            print(' '*4+"Успешно удалено")
    else:
        print(' '*4+'Не найден путь удаляемого клиента')
        return None

def client_update(command:str, root_path):
    number = update_delete_check(command, root_path, CheckType.delete)
    if number is None:
        return None
    
    
    # поулучение пути для папки с этим номером
    
    update_path = client_list_get(root_path)[number-1]
    # print(update_path)

    settings_file_path = plib.Path(update_path)/clien_manager_file_name
    # print(f'{settings_file_path=}')
    if not settings_file_path.exists():
        print(' '*4+"Не найден файл настроек для данного клиента")
        return None

    with open(settings_file_path, 'r', encoding='utf-8') as file:
        try:
            js_settings = json.load(file)
            # print(f'{js_settings=}')
        except Exception as error:
            js_settings = None

    # print(js_settings.get('client_path', ''))
    # print(root_path)

    if js_settings:
        responce = files_copy(js_settings.get('client_path', ''), root_path = root_path)
        if responce:
            print(' '*4+'Клиент успешно обновлён')
            return responce
    else:
        print(' '*4+'Не получен путь для обновления клиента')
        return None

def tab_client_print(dir_list:plib.Path)-> list:
    print('На вашем комьпьютере найдены следующие клиенты PharmNet:')
    tab_list =[('№', 'Клиент', 'Путь')]
    for i, data in enumerate(dir_list):
        tab_list.append((i+1, data.name, data))
    print(tab.tabulate(tab_list))
    return tab_list

def client_list(command:str, root_path):
    dir_tab = client_list_get(root_path=root_path)
    tab_client_print(dir_tab)

def command_list_print(*args):
    print('Доступны следующие команды для работы с клиентом:')
    print(*(f'  {i.command} - {i.description}'  for i in command_set), sep = '\n')
    print(f'  exit/close - закрыть программу')
    print('\n')
    print("Вводите команды для работы с менеджером клиентов:")

@dt.dataclass
class MyCommand():
    pass
    
class Command_ADD(MyCommand):
    command = 'add'
    description = 'Комманда для скачивания нового клиента'
    func = client_add

class Command_DELETE(MyCommand):
    command = 'delete'
    description = 'Комманда для удаления клиента'
    func = client_delete

class Command_CLIENT_LIST(MyCommand):
    command = 'client_list'
    description = 'Команда для получения скачаных клиентов'
    func = client_list

class Command_CLIENT_UPDATE(MyCommand):
    command = 'update'
    description = 'Команда для обновления клиента'
    func = client_update

class Command_COMMAND_LIST(MyCommand):
    command = 'command'
    description = 'Команда для получения списка доступных комманд'
    func = command_list_print

command_set = tuple([Command_ADD, Command_DELETE, Command_CLIENT_LIST, Command_CLIENT_UPDATE, Command_COMMAND_LIST])

    



# def command_parser(command:str):
#     command = command.strip()
#     if not command:
#         return None
#     command = command.split(' ')


        


def client_list_get(root_path:plib.Path) -> tuple[plib.Path]:
    """Возвращает tuple(pathlib.Path) папок находящихся по пути root_path и являющихся только клиентами pharm_net"""
    if not root_path.exists() or root_path == plib.Path('.'):
        raise Exception ('Путь не найден')
    x = tuple(sorted((i for i in root_path.iterdir() if i.is_dir() and re.match('^\d+-', i.name)), key =  lambda i: i.name))
    return x #надо добавить проверку на названия папки, чтобы отборажало только папки клиентов


def check_exists_command(command:str) -> MyCommand:
    """проверка на то что указанная комманда существует,
    в command передаётся введёная пользователем команда.
    если комманда найдена, то возвращается класс найденой комманды, иначе None"""
    if command is None:
        return None
    else:
        com = command.strip().split(' ')[0] # получам комманду из комманды, введённой пользователем 
        if com:
            if tuple_command:= tuple(filter(lambda i: i.command == com, command_set)):
                return tuple_command[0]
        return None

# def command_runner(command:str, com:MyCommand):
#     print(command)
#     print(com)

    







if __name__ == "__main__":
#    import tqdm


#    x = tqdm.tqdm(range(10000000000))
#    for i in x:
#     #    print('fasef')
#         pass
    # client_delete('delete 3', plib.Path(r'C:\Users\User\Desktop\программирование\production\production\client_manager'), None)


    # client_update('update 4',  plib.Path(r'c:\Users\User\Desktop\программирование\production\production\client_manager'))
    # command_list_print()
    # print(command_set)


    # \\b2-gitfs\data\pharm.net\79466-tsm-router-pl


    # C:\Users\User\Desktop\программирование\production\production\test\b2-gitfs\data\pharm.net\79466-tsm-router-pl
    pass