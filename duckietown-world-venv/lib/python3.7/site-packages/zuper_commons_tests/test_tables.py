import math
import random

from zuper_commons.text.table import format_table


def test_table1():
    cells = {}

    r = lambda T: random.randint(0, T)
    for _ in range(20):
        i = r(5)
        j = r(5)

        cells[(i, j)] = ("blah" * r(3) + "\n") * r(3)

    T = {}
    styles = ["pipes", "heavy", "light", "circo"]
    for i, style in enumerate(styles):
        for j, light_inside in enumerate((True, False)):
            T[(i, j)] = format_table(
                cells, style=style, color="red", light_inside=light_inside
            )

    s = format_table(T, style="light", color="yellow", light_inside=False)
    print(s)
