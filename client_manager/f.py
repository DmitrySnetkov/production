import pathlib as plib
import os
import shutil as sh
import enum



class CommandSet(enum.Enum):
    add = 1,
    update_all = 2,
    update = 3,
    delete = 4,
    run  = 5,
    exit = 100
    


def f_add(path:str|None = None):
    if not path:
        print("Неоходимо указать путь до клиента") 

    p = plib.Path(path)

    if not p.exists():
        print('Путь не существует')

    dir_list = tuple(p.iterdir())

    print(f'Найдено {len(dir_list)} файлов')
    print(*dir_list, sep = '\n')

    if not plib.Path('test_dir').exists():
        os.mkdir('test_dir')
        
    print('\n')
    print(p)
    print(p.joinpath(p, 'test_dir'))

    print(plib.Path())
    sh.copytree(p.joinpath('selenium_api'), 'test_dir', dirs_exist_ok=True)

    # for i in dir_list:
    #     print(i.name)
    #     print(p.joinpath(p, 'test_dir', i.name))
    #     sh.copy(i, p.joinpath(p, 'test_dir', i.name))
    #     # print(i)
    print('Скопировано')