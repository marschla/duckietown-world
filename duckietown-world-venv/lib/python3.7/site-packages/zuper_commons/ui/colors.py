from typing import Callable

import termcolor
from xtermcolor import colorize

__all__ = ['color_blue', 'color_blue_light', 'color_brown', 'color_constant',
           'color_float', 'color_green', 'color_int', 'color_ops', 'color_orange', 'color_orange_dark', 'color_par',
           'color_pink', 'color_synthetic_types', 'color_pink2', 'color_typename', 'color_typename2',
           'colorize_rgb']

color_orange = "#ffb342"
color_orange_dark = "#cfa342"

color_blue = "#42a0ff"
color_blue_light = "#62c0ff"
color_green = "#42ffa0"
color_pink = "#FF69B4"
color_pink2 = "#FF1493"

color_brown = "#b08100"


def colorize_rgb(x: str, rgb):
    assert rgb.startswith("#"), rgb
    r = colorize(x, int(rgb[1:], 16))
    if r is None:
        raise NotImplementedError()
    return r


def get_colorize_function(rgb: str) -> Callable[[str], str]:
    T = "template"
    Tc = colorize_rgb(T, rgb)

    def f(s: str) -> str:
        return Tc.replace(T, s)

    return f


color_ops = get_colorize_function(color_blue)
color_synthetic_types = get_colorize_function(color_green)
color_int = get_colorize_function(color_pink)
color_float = get_colorize_function(color_pink2)
color_typename = get_colorize_function(color_orange)
color_typename2 = get_colorize_function(color_orange_dark)

color_constant = get_colorize_function(color_pink2)


#
# def color_ops(x):
#     return colorize_rgb(x, color_blue)
#
#
# def color_synthetic_types(x):
#     return colorize_rgb(x, color_green)
#
#
# def color_int(x):
#     return colorize_rgb(x, color_pink)
#
#
# def color_float(x):
#     return colorize_rgb(x, color_pink2)
#
#
# def color_typename(x):
#     return colorize_rgb(x, color_orange)


def color_par(x):
    return termcolor.colored(x, attrs=["dark"])
