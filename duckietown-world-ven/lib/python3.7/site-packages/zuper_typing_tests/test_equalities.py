from dataclasses import dataclass
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    NewType,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from nose.tools import assert_equal, raises

from zuper_typing.annotations_tricks import is_Dict, is_List, is_Set
from zuper_typing.get_patches_ import assert_equivalent_types, NotEquivalentException
from zuper_typing.monkey_patching_typing import original_dict_getitem
from zuper_typing.my_dict import make_CustomTuple, make_dict, make_list, make_set
from zuper_typing.my_intersection import make_Intersection


def test_eq_list1():
    a = make_list(int)
    b = make_list(int)
    assert a == b
    assert_equal(a, b)


def test_eq_set():
    a = make_set(int)
    b = make_set(int)
    assert a == b
    assert_equal(a, b)


def test_eq_dict():
    a = make_dict(int, str)
    b = make_dict(int, str)

    assert a == b
    assert_equal(a, b)


def test_eq_list2():
    a = make_list(int)
    b = List[int]
    # print(type(a), type(b))
    assert is_List(b), type(b)
    assert not is_List(a), a

    assert a == b


def test_eq_dict2():
    a = make_dict(int, str)
    # print(original_dict_getitem)
    b = original_dict_getitem((int, str))
    # print(type(a), type(b))
    assert is_Dict(b), type(b)
    assert not is_Dict(a), a

    assert a == b


def test_eq_set2():
    a = make_set(int)
    b = Set[int]
    # print(type(a), type(b))
    assert is_Set(b), type(b)
    assert not is_Set(a), a
    assert a == b


@raises(NotEquivalentException)
def test_cover_equiv0():
    @dataclass
    class Eq1:
        pass

    assert_equivalent_types(Eq1, bool)


@raises(NotEquivalentException)
def test_cover_equiv1():
    @dataclass
    class Eq2:
        pass

    assert_equivalent_types(bool, Eq2)


@raises(NotEquivalentException)
def test_cover_equiv2():
    @dataclass
    class Eq3:
        pass

    @dataclass
    class Eq4:
        a: int

    assert_equivalent_types(Eq4, Eq3)


@raises(NotEquivalentException)
def test_cover_equiv03():
    assert_equivalent_types(ClassVar[int], bool)


@raises(NotEquivalentException)
def test_cover_equiv04():
    assert_equivalent_types(Dict[int, bool], bool)


@raises(NotEquivalentException)
def test_cover_equiv05():
    assert_equivalent_types(List[int], bool)


@raises(NotEquivalentException)
def test_cover_equiv06():
    assert_equivalent_types(Any, bool)


@raises(NotEquivalentException)
def test_cover_equiv07():
    assert_equivalent_types(Set[int], bool)


@raises(NotEquivalentException)
def test_cover_equiv08():
    X = TypeVar("X")
    assert_equivalent_types(X, bool)


@raises(NotEquivalentException)
def test_cover_equiv09():
    X = TypeVar("X")
    Y = TypeVar("Y")
    assert_equivalent_types(X, Y)


def test_cover_equiv09b():
    X = TypeVar("X")
    Y = TypeVar("X")
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv10():
    X = Tuple[int, bool]
    assert_equivalent_types(X, bool)


@raises(NotEquivalentException)
def test_cover_equiv11():
    X = Tuple[int, ...]
    assert_equivalent_types(X, bool)


@raises(NotEquivalentException)
def test_cover_equiv12():
    X = Tuple[int, bool]
    Y = Tuple[int, str]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv13():
    X = Tuple[int, ...]
    Y = Tuple[bool, ...]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv14():
    X = Optional[int]
    Y = Optional[bool]
    assert_equivalent_types(X, Y)


# @raises(NotEquivalentException)
def test_cover_equiv15():
    X = make_CustomTuple((int, str))
    Y = Tuple[int, str]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv16_set():
    X = Set[int]
    Y = Set[bool]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv17():
    X = Union[int, str]
    Y = Union[bool, str]
    assert_equivalent_types(X, Y)


def test_cover_equiv17b():
    X = Union[bool, str]
    Y = Union[bool, str]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv17c():
    X = Union[bool, str, float]
    Y = Union[bool, str]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv17c():
    X = Union[bool, str]
    Y = int
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv18_set():
    X = List[int]
    Y = List[bool]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv19():
    X = Dict[int, int]
    Y = Dict[bool, int]
    assert_equivalent_types(X, Y)


def test_cover_equiv20():
    X = make_dict(int, int)
    Y = Dict[int, int]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv21():
    X = Any
    Y = int
    assert_equivalent_types(X, Y)


def test_cover_equiv22():
    X = Any
    Y = Any
    assert_equivalent_types(X, Y)


def test_cover_equiv23():
    X = NewType("a", int)
    Y = NewType("a", int)
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv24():
    X = NewType("a", int)
    Y = NewType("b", int)
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv25():
    X = NewType("a", bool)
    Y = NewType("a", int)
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv26():
    X = NewType("a", bool)
    Y = int
    assert_equivalent_types(X, Y)


def test_cover_equiv27():
    X = Type
    Y = Type
    assert_equivalent_types(X, Y)


def test_cover_equiv28():
    X = Type[int]
    Y = Type[int]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv29():
    X = Type[int]
    Y = Type[str]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv30():
    X = Type[int]
    Y = str
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv31():
    X = Optional[int]
    Y = str
    assert_equivalent_types(X, Y)


def test_cover_equiv32():
    X = Optional[str]
    Y = Optional[str]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv33():
    X = Optional[int]
    Y = Optional[str]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv34():
    X = int
    Y = str
    assert_equivalent_types(X, Y)


def test_cover_equiv35():
    X = ClassVar[int]
    Y = ClassVar[int]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv36():
    X = ClassVar[int]
    Y = ClassVar[str]
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv37():
    X = ClassVar[int]
    Y = int
    assert_equivalent_types(X, Y)


def test_cover_equiv38():
    X = make_Intersection((int, bool))
    Y = make_Intersection((int, bool))
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv39():
    X = make_Intersection((int, bool))
    Y = make_Intersection((int, str))
    assert_equivalent_types(X, Y)


@raises(NotEquivalentException)
def test_cover_equiv40():
    X = make_Intersection((int, bool))
    Y = int
    assert_equivalent_types(X, Y)
