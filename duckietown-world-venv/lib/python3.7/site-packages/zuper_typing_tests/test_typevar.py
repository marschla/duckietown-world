from typing import TypeVar

from zuper_typing.annotations_tricks import (
    get_TypeVar_bound,
    get_TypeVar_name,
    is_TypeVar,
)


def test_typevars1():
    X = TypeVar("X")
    assert is_TypeVar(X)
    assert get_TypeVar_name(X) == "X"
    assert get_TypeVar_bound(X) is object


def test_typevars2():
    Y = TypeVar("Y", bound=int)
    assert is_TypeVar(Y)
    assert get_TypeVar_name(Y) == "Y"
    assert get_TypeVar_bound(Y) is int
