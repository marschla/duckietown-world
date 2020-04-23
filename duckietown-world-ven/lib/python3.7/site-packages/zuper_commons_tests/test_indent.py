from nose.tools import assert_equal

from zuper_commons.text.coloring import get_length_on_screen, remove_escapes


def test_escape() -> None:
    l = remove_escapes("\x1b[38;5;75m#0 \x1b[0m")
    assert_equal(l, "#0 ")


def test_length() -> None:
    l = get_length_on_screen("\x1b[38;5;75m#0 \x1b[0m")
    assert_equal(l, 3)
