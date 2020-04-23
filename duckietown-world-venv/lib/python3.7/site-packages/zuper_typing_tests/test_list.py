from typing import Iterable, List

from zuper_typing.annotations_tricks import get_Iterable_arg, get_List_arg, is_Any
from zuper_typing.my_dict import make_list, get_ListLike_arg, get_ListLike_name


def test_list_1():
    X = get_List_arg(List)
    assert is_Any(X), X


def test_iterable1():
    # noinspection PyTypeChecker
    X = get_Iterable_arg(Iterable)
    assert is_Any(X), X


def test_iterable2():
    X = get_Iterable_arg(Iterable[int])
    assert X is int, X


def test_list_2():
    X = int
    a = make_list(X)
    X2 = get_ListLike_arg(a)
    assert X == X2


def test_list_name_2():
    X = int
    a = make_list(X)
    n = get_ListLike_name(a)
    assert n == "List[int]"
