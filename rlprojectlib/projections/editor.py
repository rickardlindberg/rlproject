from collections import namedtuple

from rlprojectlib.domains.generic import SuperTuple
from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextProjection, TerminalTextFragment

class Editor(
    namedtuple("Editor", "projection terminal_text"),
    TerminalTextProjection
):

    @staticmethod
    def project(terminal_text, unicode_character=None):
        """
        >>> Editor.project(TerminalText(fragments=SuperTuple([]), cursors=SuperTuple([]))).print_fragments_and_cursors()
        TerminalTextFragment(x=0, y=0, text='STATUS: None', bold=None, bg='MAGENTA', fg='WHITE')
        """
        return Editor(
            projection=TerminalText(
                fragments=SuperTuple([
                    TerminalTextFragment(
                        text=f"STATUS: {repr(unicode_character)}",
                        x=0,
                        y=0,
                        bg="MAGENTA",
                        fg="WHITE"
                    )
                ]+[x.move(dy=1) for x in terminal_text.fragments]),
                cursors=terminal_text.cursors.map(lambda x: x.move(dy=1))
            ),
            terminal_text=terminal_text,
        )

    def keyboard_event(self, event):
        return Editor.project(
            terminal_text=self.terminal_text.keyboard_event(event),
            unicode_character=event.unicode_character
        )
