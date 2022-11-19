from collections import namedtuple

from rlprojectlib.domains.generic import Selections, SuperTuple
from rlprojectlib.domains.string import String, Selection
from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.domains.terminal import TextFragmentsBuilder
from rlprojectlib.domains.terminal import Projection

class StringToTerminal(
    namedtuple("StringToTerminal", "projection string"),
    Projection
):

    """
    I project a String to a Terminal.

    >>> StringToTerminal.test_project("hello", 1, 3)
    TextFragment(x=0, y=0, text='h', bold=None, bg=None, fg=None)
    TextFragment(x=1, y=0, text='ell', bold=None, bg='YELLOW', fg=None)
    TextFragment(x=4, y=0, text='o', bold=None, bg=None, fg=None)
    Cursor(x=4, y=0)

    >>> StringToTerminal.test_project("1\\n2", 1, 0)
    TextFragment(x=0, y=0, text='1', bold=None, bg=None, fg=None)
    TextFragment(x=1, y=0, text='\\\\n', bold=None, bg=None, fg='MAGENTA')
    TextFragment(x=3, y=0, text='2', bold=None, bg=None, fg=None)
    Cursor(x=1, y=0)
    """

    @staticmethod
    def project(string, x=0, y=0):
        fragments = TextFragmentsBuilder()
        cursors = []
        last_pos = 0
        for selection in string.selections:
            x += fragments.extend(TextFragment(
                text=string.string[last_pos:selection.pos_start],
                y=y,
                x=x
            ).replace_newlines(fg="MAGENTA"))
            x += fragments.extend(TextFragment(
                text=string.string[selection.pos_start:selection.pos_end],
                y=y,
                x=x,
                bg="YELLOW"
            ).replace_newlines())
            cursors.append(Cursor(x=x, y=y))
            last_pos = selection.pos_end
        fragments.extend(TextFragment(
            text=string.string[last_pos:],
            y=y,
            x=x
        ).replace_newlines(fg="MAGENTA"))
        return StringToTerminal(
            projection=Terminal(fragments=fragments.to_immutable(), cursors=SuperTuple(cursors)),
            string=string
        )

    @staticmethod
    def test_project(string, selection_start=0, selection_length=0):
        StringToTerminal.project(
            String(
                string,
                Selections([
                    Selection(start=selection_start, length=selection_length)
                ])
            )
        ).print_fragments_and_cursors()

    def keyboard_event(self, event):
        return StringToTerminal.project(
            self.string.keyboard_event(event)
        )

    def size_event(self, event):
        return self
