from collections import namedtuple

from rlprojectlib.domains.generic import ImmutableList
from rlprojectlib.domains.generic import Document
from rlprojectlib.domains.generic import Selections
from rlprojectlib.domains.string import Selection as StringSelection

class Lines(
    namedtuple("Lines", "meta lines selections"),
    Document
):

    @classmethod
    def create(cls, lines, selections=[], meta=None):
        return cls(
            meta=meta,
            lines=ImmutableList(lines),
            selections=Selections(selections)
        )

    def print_lines_selections(self):
        self.lines.print()
        self.selections.print()

    def move_cursor_forward(self):
        raise NotImplementedError()

    def move_cursor_back(self):
        raise NotImplementedError()

    def select_next_word(self):
        raise NotImplementedError()

    def replace(self, text):
        raise NotImplementedError()

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
