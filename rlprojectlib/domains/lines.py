from collections import namedtuple

from rlprojectlib.domains.generic import ImmutableList, Selections
from rlprojectlib.domains.string import Selection as StringSelection

class Lines(
    namedtuple("Lines", "meta lines selections")
):

    @staticmethod
    def create(lines, selections):
        return Lines(
            meta=None,
            lines=ImmutableList(lines),
            selections=Selections(selections)
        )

    def print_lines_selections(self):
        self.lines.print()
        self.selections.print()

    def move_cursor_forward(self):
        return NotImplementedError()

    def move_cursor_back(self):
        return NotImplementedError()

    def select_next_word(self):
        return NotImplementedError()

    def replace(self, text):
        return NotImplementedError()

class Projection:

    @property
    def lines(self):
        return self.projection.lines

    @property
    def selections(self):
        return self.projection.selections

    def print_lines_selections(self):
        self.projection.print_lines_selections()

class Line(
    namedtuple("Line", "text number")
):
    pass

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
