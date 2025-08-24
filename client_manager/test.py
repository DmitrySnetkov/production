import utils as utils
import pathlib as plib
import pytest as pt

# можно создать фикстуру создающую тестовую директория с папками

def test_client_list_get():
    with pt.raises(Exception, match = 'Путь не найден'):
        utils.client_list_get(plib.Path('aefase'))
    
    with pt.raises(Exception, match = 'Путь не найден'):
        utils.client_list_get(plib.Path('.'))

    with pt.raises(Exception, match = 'Путь не найден'):
        utils.client_list_get(plib.Path(''))

    with pt.raises(Exception, match = 'Путь не найден'):
        utils.client_list_get(plib.Path('1513524'))

    assert len(utils.client_list_get(plib.Path(__file__).parent)) > 0


def test_check_exists_command():
    assert utils.check_exists_command(None) is None
    assert utils.check_exists_command('') is None
    assert utils.check_exists_command(' ') is None
    assert utils.check_exists_command('         ') is None
    assert utils.check_exists_command('asef') is None
    assert utils.check_exists_command('asef sefa') is None
    assert utils.check_exists_command('addsefa') is None

    for i in utils.command_set:
        assert utils.check_exists_command(f'{i.command}') == i
        assert utils.check_exists_command(f'{i.command} asefa') == i
        assert utils.check_exists_command(f'asefa {i.command}') is None

    
    