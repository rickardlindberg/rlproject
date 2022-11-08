from collections import namedtuple

class Lines(
    namedtuple("Lines", "lines selections")
):
    pass

class Selection(
    namedtuple("Selection", "start end")
):
    pass

class Position(
    namedtuple("Selection", "row col")
):
    pass
