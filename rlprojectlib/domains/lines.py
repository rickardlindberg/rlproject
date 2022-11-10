from collections import namedtuple

class Lines(
    namedtuple("Lines", "lines selections")
):
    pass

class LinesProjection:

    @property
    def lines(self):
        return self.projected_lines.lines

    @property
    def selections(self):
        return self.projected_lines.selections

class Selection(
    namedtuple("Selection", "start end")
):
    pass

class Position(
    namedtuple("Selection", "row col")
):
    pass
