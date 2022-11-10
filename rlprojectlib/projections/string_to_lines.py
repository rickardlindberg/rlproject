from collections import namedtuple

from rlprojectlib.domains.string import String
from rlprojectlib.domains.lines import Lines, Selection, Position, LinesProjection
from rlprojectlib.domains.generic import Selections

class StringToLines(
    namedtuple("StringToLines", "string projected_lines"),
    LinesProjection
):

    @staticmethod
    def project(string):
        """
        >>> StringToLines.test_project("one\\ntwo")
        ('one', 'two')
        Selection(start=Position(row=0, col=0), end=Position(row=0, col=0))

        >>> StringToLines.test_project("one\\ntwo", 3)
        ('one', 'two')
        Selection(start=Position(row=0, col=3), end=Position(row=0, col=3))

        >>> StringToLines.test_project("one\\ntwo", 4)
        ('one', 'two')
        Selection(start=Position(row=1, col=0), end=Position(row=1, col=0))
        """
        lines = []
        pos = 0
        while True:
            match_index = string.string.find("\n", pos)
            if match_index >= 0:
                lines.append((
                    string.string[pos:match_index],
                    pos,
                    match_index
                ))
                pos = match_index + 1
            else:
                break
        lines.append((
            string.string[pos:len(string.string)],
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
        return StringToLines(
            string=string,
            projected_lines=Lines(
                lines=tuple(line[0] for line in lines),
                selections=Selections(selections)
            )
        )

    @staticmethod
    def test_project(string, start=0):
        lines = StringToLines.project(
            String.from_string(string=string, selection_start=start)
        ).projected_lines
        print(lines.lines)
        print_namedtuples(lines.selections)

    def keyboard_event(self, event):
        return StringToLines.project(self.string.keyboard_event(event))

def print_namedtuples(namedtuples):
    print("\n".join(repr(x) for x in namedtuples))
