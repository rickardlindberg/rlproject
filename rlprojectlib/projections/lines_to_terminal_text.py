from collections import namedtuple

from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextProjection
from rlprojectlib.projections.string_to_terminal_text import StringToTerminalText

class LinesToTerminalText(
    namedtuple("LinesToTerminalText", "terminal_text lines"),
    TerminalTextProjection
):

    @staticmethod
    def project(lines):
        fragments = []
        cursors = []
        for index, string in enumerate(lines.lines):
            x = StringToTerminalText.project(string, y=index)
            fragments.extend(x.fragments)
            cursors.extend(x.cursors)
        return LinesToTerminalText(
            terminal_text=TerminalText(fragments=fragments, cursors=cursors),
            lines=lines
        )

    def keyboard_event(self, event):
        return LinesToTerminalText.project(self.lines.keyboard_event(event))
