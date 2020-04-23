from typing import Dict

from zuper_typing.annotations_tricks import get_Dict_args, is_Any
from zuper_typing.my_dict import make_dict, make_list, make_set


def test_dict_1():
    K, V = get_Dict_args(Dict)
    assert is_Any(K), K
    assert is_Any(V), V


def test_dict_2_copy():
    A = make_dict(int, str)
    a = A({1: "one"})
    a.copy()


def test_list_2_copy():
    A = make_list(int)
    a = A([1])
    a.copy()


def test_set_2_copy():
    A = make_set(int)
    a = A([1])
    a.copy()
