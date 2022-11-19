from collections import namedtuple

from rlprojectlib.domains.generic import Selections
from rlprojectlib.domains.lines import Line
from rlprojectlib.domains.lines import Lines
from rlprojectlib.domains.lines import Position
from rlprojectlib.domains.lines import Selection
from rlprojectlib.domains.string import Selection as StringSelection
from rlprojectlib.domains.string import String
from rlprojectlib.domains.terminal import Projection
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.projections.string_to_terminal import StringToTerminal

class LinesToTerminalText(
    namedtuple("LinesToTerminalText", "projection lines"),
    Projection
):

    @staticmethod
    def project(lines):
        """
        >>> LinesToTerminalText.test_project([
        ...     Line(text="one", number=1),
        ...     Line(text="two", number=2),
        ... ])
        TextFragment(x=0, y=0, text='1', bold=None, bg=None, fg='YELLOW')
        TextFragment(x=2, y=0, text='one', bold=None, bg=None, fg=None)
        TextFragment(x=0, y=1, text='2', bold=None, bg=None, fg='YELLOW')
        TextFragment(x=2, y=1, text='two', bold=None, bg=None, fg=None)

        >>> LinesToTerminalText.test_project([
        ...     Line(text="one", number=1),
        ...     Line(text="two", number=2),
        ... ], [Selection(start=Position(row=0, col=0), end=Position(row=0, col=1))])
        TextFragment(x=0, y=0, text='1', bold=None, bg=None, fg='YELLOW')
        TextFragment(x=2, y=0, text='o', bold=None, bg='YELLOW', fg=None)
        TextFragment(x=3, y=0, text='ne', bold=None, bg=None, fg=None)
        TextFragment(x=0, y=1, text='2', bold=None, bg=None, fg='YELLOW')
        TextFragment(x=2, y=1, text='two', bold=None, bg=None, fg=None)
        Cursor(x=3, y=0)
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
            x = StringToTerminal.project(y, y=index, x=line_number_len+1)
            fragments.append(TextFragment(x=0, y=index, text=str(line.number), fg="YELLOW"))
            fragments.extend(x.fragments)
            cursors.extend(x.cursors)
        return LinesToTerminalText(
            projection=Terminal.create(
                fragments=fragments,
                cursors=cursors
            ),
            lines=lines,
        )

    @staticmethod
    def test_project(lines, selections=[]):
        LinesToTerminalText.project(
            Lines.create(lines=lines, selections=selections)
        ).print_fragments_and_cursors()

    def keyboard_event(self, event):
        if event.unicode_character == "\x06": # Ctrl-F
            lines = self.lines.move_cursor_forward()
        elif event.unicode_character == "\x02": # Ctrl-B
            lines = self.lines.move_cursor_back()
        elif event.unicode_character == "\x0e": # Ctrl-N
            lines = self.lines.select_next_word()
        elif event.unicode_character and ord(event.unicode_character) >= 32:
            lines = self.lines.replace(event.unicode_character)
        else:
            lines = self.lines
        return LinesToTerminalText.project(lines)

    def size_event(self, event):
        return self
