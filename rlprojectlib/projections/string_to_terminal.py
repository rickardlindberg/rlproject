from collections import namedtuple

from rlprojectlib.domains.generic import Selections
from rlprojectlib.domains.string import Selection
from rlprojectlib.domains.string import String
from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.domains.terminal import TextFragmentsBuilder

class Meta(
    namedtuple("Meta", "string")
):
    pass

class StringToTerminal(Terminal):

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
        return StringToTerminal.create(
            fragments=fragments.get(),
            cursors=cursors,
            meta=Meta(string=string)
        )

    @staticmethod
    def test_project(string, selection_start=0, selection_length=0):
        StringToTerminal.project(
            String(
                meta=None,
                string=string,
                selections=Selections([
                    Selection(start=selection_start, length=selection_length)
                ])
            )
        ).print_fragments_and_cursors()

    def keyboard_event(self, event):
        if event.unicode_character == "\x06": # Ctrl-F
            return self.meta.string.move_cursor_forward()
        elif event.unicode_character == "\x02": # Ctrl-B
            return self.meta.string.move_cursor_back()
        elif event.unicode_character == "\x0e": # Ctrl-N
            return self.meta.string.select_next_word()
        elif event.unicode_character == "\x08": # Backspace
            return self.meta.string.delete_back()
        elif event.unicode_character and ord(event.unicode_character) >= 32:
            return self.meta.string.replace(event.unicode_character)
        else:
            return self.meta.string
