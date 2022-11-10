from collections import namedtuple

from rlprojectlib.domains.string import String
from rlprojectlib.domains.lines import Lines
from rlprojectlib.domains.generic import Selections
from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextProjection
from rlprojectlib.projections.string_to_terminal_text import StringToTerminalText

class LinesToTerminalText(
    namedtuple("LinesToTerminalText", "terminal_text lines"),
    TerminalTextProjection
):

    @staticmethod
    def project(lines):
        """
        >>> tt = LinesToTerminalText.project(
        ...     Lines(lines=("one", "two"), selections=Selections([]))
        ... ).terminal_text
        >>> tt.fragments
        [TerminalTextFragment(x=0, y=0, text='one', bold=None, bg=None, fg=None), TerminalTextFragment(x=0, y=1, text='two', bold=None, bg=None, fg=None)]
        >>> tt.cursors
        []
        """
        fragments = []
        cursors = []
        for index, string in enumerate(lines.lines):
            y = String(string=string, selections=tuple())
            x = StringToTerminalText.project(y, y=index)
            fragments.extend(x.fragments)
            #cursors.extend(x.cursors)
            # TODO: fixme!
        return LinesToTerminalText(
            terminal_text=TerminalText(fragments=fragments, cursors=cursors),
            lines=lines
        )

    def keyboard_event(self, event):
        return LinesToTerminalText.project(self.lines.keyboard_event(event))
