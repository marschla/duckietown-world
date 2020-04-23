from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple, TypeVar, Union

from zuper_typing.exceptions import ZValueError
from zuper_typing.get_patches_ import assert_equivalent_types, NotEquivalentException
from zuper_typing.my_intersection import Intersection
from zuper_typing.subcheck import can_be_used_as2
from zuper_typing.type_algebra import type_inf, type_sup
from zuper_typing.uninhabited import is_Uninhabited, make_Uninhabited


def test_algebra_sup_1():
    X = TypeVar("X")
    W = TypeVar("W")
    Z = TypeVar("Z")

    # noinspection PyTypeHints
    X2 = TypeVar("X")
    Y = TypeVar("Y")
    U = make_Uninhabited()

    @dataclass
    class D:
        a: int

    cases = [
        (bool, object, object),
        (bool, int, int),
        (bool, U, bool),
        (int, str, Union[int, str]),
        (int, type(None), Optional[int]),
        (List[bool], List[int], List[int]),
        (Set[bool], Set[int], Set[int]),
        (Dict[bool, str], Dict[int, str], Dict[int, str]),
        (Dict[str, bool], Dict[str, int], Dict[str, int]),
        (Tuple[bool, ...], Tuple[int, ...], Tuple[int, ...]),
        (Tuple[bool, str], Tuple[int, str], Tuple[int, str]),
        (X, Y, Union[X, Y]),
        (X, X2, X),
        (Set[bool], D, Union[Set[bool], D]),
        (Union[int, float], Union[str, datetime], Union[datetime, float, int, str]),
        (Optional[int], Optional[bool], Optional[int]),
        (Union[X, Y], Union[W, Z], Union[W, X, Y, Z]),
    ]
    for A, B, expect in cases:
        yield check_sup, A, B, expect
        yield check_sup, B, A, expect


def test_algebra_inf_1():
    X = TypeVar("X")
    W = TypeVar("W")
    Z = TypeVar("Z")

    # noinspection PyTypeHints
    X2 = TypeVar("X")
    Y = TypeVar("Y")
    U = make_Uninhabited()

    @dataclass
    class D:
        a: int

    cases = [
        (bool, object, bool),
        (bool, int, bool),
        (int, str, U),
        (U, str, U),
        (int, type(None), U),
        (List[bool], List[int], List[bool]),
        (List[bool], int, U),
        (List[bool], Set[int], U),
        (Set[bool], Set[int], Set[bool]),
        (Set[bool], int, U),
        (Set[bool], List[int], U),
        (Dict[bool, str], Dict[int, str], Dict[bool, str]),
        (Dict[str, bool], Dict[str, int], Dict[str, bool]),
        (Tuple[bool, ...], Tuple[int, ...], Tuple[bool, ...]),
        (Tuple[bool, str], Tuple[int, str], Tuple[bool, str]),
        (X, Y, Intersection[X, Y]),
        (X, X2, X),
        (Optional[bool], type(None), type(None)),  # ?
        (Set[bool], D, U),
        (Union[int, float], Union[str, datetime], U),
        (Optional[int], Optional[bool], Optional[bool]),
        (Intersection[X, Y], Intersection[W, Z], Intersection[W, X, Y, Z]),
    ]
    for A, B, expect in cases:
        yield check_inf, A, B, expect
        yield check_inf, B, A, expect


def check_sup(A, B, expect):
    r = can_be_used_as2(A, expect)

    if not r:
        msg = "I A <= expect"
        raise ZValueError(msg, A=A, expect=expect)
    r = can_be_used_as2(B, expect)

    if not r:
        msg = "I B <= expect"
        raise ZValueError(msg, B=B, expect=expect)

    res = type_sup(A, B)
    try:
        assert_equivalent_types(res, expect)
    except NotEquivalentException as e:
        msg = "Failed to compute sup (union)"
        raise ZValueError(msg, A=A, B=B, expect=expect, res=res) from e


def check_inf(A, B, expect):
    r = can_be_used_as2(expect, A)
    if not r:
        msg = "I expect <= A"
        raise ZValueError(msg, expect=expect, A=A)

    r = can_be_used_as2(expect, B)
    if not r:
        msg = "I expect <= B"
        raise ZValueError(msg, expect=expect, B=B)

    res = type_inf(A, B)
    try:
        assert_equivalent_types(res, expect)
    except NotEquivalentException as e:
        msg = "Failed to compute inf (intersection)"
        raise ZValueError(msg, A=A, B=B, expect=expect, res=res) from e


def test_optional1():
    r = can_be_used_as2(type(None), Optional[int])
    assert r, r


def test_algebra_dc1():
    @dataclass
    class A1:
        a: bool

    @dataclass
    class A2:
        a: int

    assert can_be_used_as2(A1, A2)

    ti = type_inf(A1, A2)
    ts = type_sup(A1, A2)

    eq1 = equivalent(ti, A1)
    assert eq1, eq1
    eq2 = equivalent(ts, A2)
    assert eq2, eq2


def test_algebra_dc2():
    @dataclass
    class A1:
        a: bool

    @dataclass
    class A2:
        a: str

    @dataclass
    class A3:
        a: Union[str, bool]

    ti = type_inf(A1, A2)
    ts = type_sup(A1, A2)

    assert is_Uninhabited(ti), ti

    assert equivalent(ts, A3)


def equivalent(x, y):
    r1 = can_be_used_as2(x, y)
    if not r1:
        return r1
    r2 = can_be_used_as2(x, y, r1.M)
    return r2
