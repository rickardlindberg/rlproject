from collections import namedtuple

from rlprojectlib.domains.string import Selection as StringSelection
from rlprojectlib.domains.string import String
from rlprojectlib.domains.lines import Lines, Line, Selection, Position
from rlprojectlib.domains.generic import Selections
from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextProjection, TerminalTextFragment
from rlprojectlib.projections.string_to_terminal_text import StringToTerminalText

class LinesToTerminalText(
    namedtuple("LinesToTerminalText", "terminal_text lines"),
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
            selections_per_line[selection.start.row] = [
                StringSelection(start=selection.start.col, length=selection.end.col-selection.start.col)
            ]

        for index, line in enumerate(lines.lines):
            y = String(string=line.text, selections=Selections(selections_per_line.get(index, [])))
            x = StringToTerminalText.project(y, y=index, x=line_number_len+1)
            fragments.append(TerminalTextFragment(x=0, y=index, text=str(line.number)))
            fragments.extend(x.fragments)
            cursors.extend(x.cursors)
        return LinesToTerminalText(
            terminal_text=TerminalText(fragments=fragments, cursors=cursors),
            lines=lines
        )

    @staticmethod
    def test_project(lines, selections=[]):
        terminal_text = LinesToTerminalText.project(
            Lines(lines=lines, selections=Selections(selections))
        ).terminal_text
        for fragment in terminal_text.fragments:
            print(fragment)
        for cursor in terminal_text.cursors:
            print(cursor)

    def keyboard_event(self, event):
        return LinesToTerminalText.project(self.lines.keyboard_event(event))
