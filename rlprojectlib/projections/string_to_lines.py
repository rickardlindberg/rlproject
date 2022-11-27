from collections import namedtuple

from rlprojectlib.domains.lines import Line
from rlprojectlib.domains.lines import Lines
from rlprojectlib.domains.lines import Position
from rlprojectlib.domains.lines import Selection
from rlprojectlib.domains.string import String

class Meta(
    namedtuple("Meta", "string")
):
    pass

class StringToLines(Lines):

    @staticmethod
    def project(string):
        """
        >>> StringToLines.test_project("one\\ntwo")
        Line(text='one', number=1)
        Line(text='two', number=2)
        Selection(start=Position(row=0, col=0), end=Position(row=0, col=0))

        >>> StringToLines.test_project("one\\ntwo", 3)
        Line(text='one', number=1)
        Line(text='two', number=2)
        Selection(start=Position(row=0, col=3), end=Position(row=0, col=3))

        >>> StringToLines.test_project("one\\ntwo", 4)
        Line(text='one', number=1)
        Line(text='two', number=2)
        Selection(start=Position(row=1, col=0), end=Position(row=1, col=0))
        """
        lines = []
        pos = 0
        while True:
            match_index = string.string.find("\n", pos)
            if match_index >= 0:
                lines.append((
                    Line(text=string.string[pos:match_index], number=len(lines)+1),
                    pos,
                    match_index
                ))
                pos = match_index + 1
            else:
                break
        lines.append((
            Line(text=string.string[pos:len(string.string)], number=len(lines)+1),
            pos,
            len(string.string)
        ))
        selections = []
        for selection in string.selections:
            for row, (_, x, y) in enumerate(lines):
                if x <= selection.pos_start <= y:
                    start = Position(row=row, col=selection.pos_start-x)
                if x <= selection.pos_end <= y:
                    end = Position(row=row, col=selection.pos_end-x)
            selections.append(Selection(start=start, end=end))
        return StringToLines.create(
            lines=(line[0] for line in lines),
            selections=selections,
            meta=Meta(string=string)
        )

    @staticmethod
    def test_project(string, start=0):
        StringToLines.project(
            String.from_string(string=string, selection_start=start)
        ).print_lines_selections()

    def move_cursor_forward(self):
        return self.meta.string.move_cursor_forward()

    def move_cursor_back(self):
        return self.meta.string.move_cursor_back()

    def select_next_word(self):
        return self.meta.string.select_next_word()

    def replace(self, text):
        return self.meta.string.replace(text)

    def get_edited_document(self):
        return self.meta.string
