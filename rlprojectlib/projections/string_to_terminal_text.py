from collections import namedtuple

from rlprojectlib.domains.string import String, StringSelection
from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextProjection, TerminalTextFragment, TerminalTextFragmentsBuilder, TerminalCursor

class StringToTerminalText(
    namedtuple("StringToTerminalText", "terminal_text string"),
    TerminalTextProjection
):

    """
    I project a String to a TerminalText.

    I project keyboard events back to the String.

    >>> terminal_text = StringToTerminalText.project(String("hello", [StringSelection(1, 3)]))
    >>> print_namedtuples(terminal_text.fragments)
    TerminalTextFragment(x=0, y=0, text='h', bold=None, bg=None, fg=None)
    TerminalTextFragment(x=1, y=0, text='ell', bold=None, bg='YELLOW', fg=None)
    TerminalTextFragment(x=4, y=0, text='o', bold=None, bg=None, fg=None)

    >>> terminal_text = StringToTerminalText.project(String("1\\n2", [StringSelection(1, 0)]))
    >>> print_namedtuples(terminal_text.fragments)
    TerminalTextFragment(x=0, y=0, text='1', bold=None, bg=None, fg=None)
    TerminalTextFragment(x=1, y=0, text='\\\\n', bold=None, bg=None, fg='MAGENTA')
    TerminalTextFragment(x=3, y=0, text='2', bold=None, bg=None, fg=None)
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

    def keyboard_event(self, event):
        return StringToTerminalText.project(
            self.string.move_cursor_forward()
        )

def print_namedtuples(namedtuples):
    print("\n".join(repr(x) for x in namedtuples))
