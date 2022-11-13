from collections import namedtuple

from rlprojectlib.domains.generic import SuperTuple
from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextProjection, TerminalTextFragment, SizeEvent

class Editor(
    namedtuple("Editor", "projection terminal_text width"),
    TerminalTextProjection
):

    @staticmethod
    def project(terminal_text, unicode_character=None, width=0):
        """
        >>> Editor.project(TerminalText(fragments=SuperTuple([]), cursors=SuperTuple([]))).print_fragments_and_cursors()
        TerminalTextFragment(x=0, y=0, text='STATUS: None', bold=None, bg='MAGENTA', fg='WHITE')
        """
        return Editor(
            projection=TerminalText(
                fragments=SuperTuple([
                    TerminalTextFragment(
                        text=f"STATUS: {repr(unicode_character)}".ljust(width),
                        x=0,
                        y=0,
                        bg="MAGENTA",
                        fg="WHITE"
                    )
                ]+[x.move(dy=1) for x in terminal_text.fragments]),
                cursors=terminal_text.cursors.map(lambda x: x.move(dy=1))
            ),
            terminal_text=terminal_text,
            width=width
        )

    def keyboard_event(self, event):
        return Editor.project(
            terminal_text=self.terminal_text.keyboard_event(event),
            unicode_character=event.unicode_character,
            width=self.width
        )

    def size_event(self, event):
        return Editor.project(
            terminal_text=self.terminal_text.size_event(SizeEvent(
                width=event.width,
                height=event.height-1
            )),
            width=event.width
        )
