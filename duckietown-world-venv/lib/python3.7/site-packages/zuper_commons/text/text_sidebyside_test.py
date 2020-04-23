from zuper_commons.text.text_sidebyside import side_by_side


def test1():
    a = """
This is the first
one. With Three
lines.
    """.strip()

    b = """
    This is the first
    one. Now with
    four
    lines!
        """.strip()

    print(side_by_side([a, b]))
