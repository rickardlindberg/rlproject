from collections import namedtuple

from rlprojectlib.domains.generic import Selections
from rlprojectlib.domains.string import String, Selection
from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextProjection, TerminalTextFragment, TerminalTextFragmentsBuilder, TerminalCursor

class StringToTerminalText(
    namedtuple("StringToTerminalText", "terminal_text string"),
    TerminalTextProjection
):

    """
    I project a String to a TerminalText.

    >>> StringToTerminalText.test_project("hello", 1, 3)
    TerminalTextFragment(x=0, y=0, text='h', bold=None, bg=None, fg=None)
    TerminalTextFragment(x=1, y=0, text='ell', bold=None, bg='YELLOW', fg=None)
    TerminalTextFragment(x=4, y=0, text='o', bold=None, bg=None, fg=None)
    TerminalCursor(x=4, y=0)

    >>> StringToTerminalText.test_project("1\\n2", 1, 0)
    TerminalTextFragment(x=0, y=0, text='1', bold=None, bg=None, fg=None)
    TerminalTextFragment(x=1, y=0, text='\\\\n', bold=None, bg=None, fg='MAGENTA')
    TerminalTextFragment(x=3, y=0, text='2', bold=None, bg=None, fg=None)
    TerminalCursor(x=1, y=0)
    """

    @staticmethod
    def project(string, x=0, y=0):
        fragments = TerminalTextFragmentsBuilder()
        cursors = []
        last_pos = 0
        for selection in string.selections:
            x += fragments.extend(TerminalTextFragment(
                text=string.string[last_pos:selection.pos_start],
                y=y,
                x=x
            ).replace_newlines(fg="MAGENTA"))
            x += fragments.extend(TerminalTextFragment(
                text=string.string[selection.pos_start:selection.pos_end],
                y=y,
                x=x,
                bg="YELLOW"
            ).replace_newlines())
            cursors.append(TerminalCursor(x=x, y=y))
            last_pos = selection.pos_end
        fragments.extend(TerminalTextFragment(
            text=string.string[last_pos:],
            y=y,
            x=x
        ).replace_newlines(fg="MAGENTA"))
        return StringToTerminalText(
            terminal_text=TerminalText(fragments=fragments.to_tuple(), cursors=cursors),
            string=string
        )

    @staticmethod
    def test_project(string, selection_start=0, selection_length=0):
        StringToTerminalText.project(
            String(
                string,
                Selections([
                    Selection(start=selection_start, length=selection_length)
                ])
            )
        ).print_fragments_and_cursors()
