from collections import namedtuple

from rlprojectlib.domains.string import Selection as StringSelection
from rlprojectlib.domains.string import String
from rlprojectlib.domains.lines import Lines, Line, Selection, Position
from rlprojectlib.domains.generic import Selections, SuperTuple
from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextProjection, TerminalTextFragment
from rlprojectlib.projections.string_to_terminal_text import StringToTerminalText

class LinesToTerminalText(
    namedtuple("LinesToTerminalText", "projection lines"),
    TerminalTextProjection
):

    @staticmethod
    def project(lines):
        """
        >>> LinesToTerminalText.test_project([
        ...     Line(text="one", number=1),
        ...     Line(text="two", number=2),
        ... ])
        TerminalTextFragment(x=0, y=0, text='1', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=2, y=0, text='one', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=0, y=1, text='2', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=2, y=1, text='two', bold=None, bg=None, fg=None)

        >>> LinesToTerminalText.test_project([
        ...     Line(text="one", number=1),
        ...     Line(text="two", number=2),
        ... ], [Selection(start=Position(row=0, col=0), end=Position(row=0, col=1))])
        TerminalTextFragment(x=0, y=0, text='1', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=2, y=0, text='o', bold=None, bg='YELLOW', fg=None)
        TerminalTextFragment(x=3, y=0, text='ne', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=0, y=1, text='2', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=2, y=1, text='two', bold=None, bg=None, fg=None)
        TerminalCursor(x=3, y=0)
        """
        fragments = []
        cursors = []
        line_number_len = max(len(str(line.number)) for line in lines.lines)
        selections_per_line = {}
        for selection in lines.selections:
            for index, selection in selection.string_selections:
                if index not in selections_per_line:
                    selections_per_line[index] = []
                selections_per_line[index].append(selection)
        for index, line in enumerate(lines.lines):
            y = String(string=line.text, selections=Selections(selections_per_line.get(index, [])))
            x = StringToTerminalText.project(y, y=index, x=line_number_len+1)
            fragments.append(TerminalTextFragment(x=0, y=index, text=str(line.number)))
            fragments.extend(x.fragments)
            cursors.extend(x.cursors)
        return LinesToTerminalText(
            projection=TerminalText(fragments=SuperTuple(fragments), cursors=SuperTuple(cursors)),
            lines=lines,
        )

    @staticmethod
    def test_project(lines, selections=[]):
        LinesToTerminalText.project(
            Lines.create(lines=lines, selections=selections)
        ).print_fragments_and_cursors()

    def keyboard_event(self, event):
        return LinesToTerminalText.project(self.lines.keyboard_event(event))

    def size_event(self, event):
        return self
