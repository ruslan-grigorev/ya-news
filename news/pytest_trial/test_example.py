# test_example.py
import pytest
from time import sleep


def one_more(x):
    return x + 1


def get_sort_list(str):
    new_list = sorted(str.split(', '))
    return new_list

@pytest.mark.parametrize(
    'input_arg, expected_result',  # Названия аргументов, передаваемых в тест.
    [
        (4, 5),
        pytest.param(3, 5, marks=pytest.mark.skip, )  # Ожидается падение теста.
    ],
    ids=['First parameter', 'Second parameter',]
)
def test_one_more(input_arg, expected_result):  # Те же параметры, что и в декораторе.
    assert one_more(input_arg) == expected_result


def test_sort():
    """Тестируем функцию get_sort_list()."""    
    result = get_sort_list('Яша, Саша, Маша, Даша')
    assert result == ['Даша', 'Маша', 'Саша', 'Яша']

@pytest.mark.slow
def test_type():
    """Тестируем тип данных, возвращаемых из get_sort_list()."""
    # Провальный тест:
    # ожидаем число, но вернётся список.
    sleep(3)
    result = get_sort_list('Яша, Саша, Маша, Даша')
    assert isinstance(result, int)

old_version = True


@pytest.mark.skipif(
    "sys.version_info > (2, 7)",
    reason='Только для старых версий Python'
)
def test_for_old_versions():
    assert old_version == True


@pytest.mark.xfail(reason='Пусть пока падает, завтра починю.')
def test_false():
    assert False
