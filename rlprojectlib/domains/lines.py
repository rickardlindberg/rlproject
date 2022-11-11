from collections import namedtuple

from rlprojectlib.domains.string import Selection as StringSelection

class Lines(
    namedtuple("Lines", "lines selections")
):
    pass

class Line(
    namedtuple("Line", "text number")
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

    @property
    def string_selections(self):
        """
        >>> Selection(
        ...     start=Position(row=0, col=0),
        ...     end=Position(row=0, col=5)
        ... ).string_selections
        [(0, Selection(start=0, length=5))]
        """
        left = self.start
        right = self.end
        return [(left.row, StringSelection(start=left.col, length=right.col-left.col))]

class Position(
    namedtuple("Selection", "row col")
):
    pass
