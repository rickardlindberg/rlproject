from collections import namedtuple

import time

from rlprojectlib.domains.generic import SuperTuple
from rlprojectlib.domains.terminaltext import SizeEvent
from rlprojectlib.domains.terminaltext import TerminalCursor
from rlprojectlib.domains.terminaltext import TerminalText
from rlprojectlib.domains.terminaltext import TerminalTextFragment
from rlprojectlib.domains.terminaltext import TerminalTextProjection

class Editor(
    namedtuple("Editor", "projection terminal_text width"),
    TerminalTextProjection
):

    @staticmethod
    def project(terminal_text, event=None, width=0, ms=0):
        """
        I project a status bar followed by the given terminal text:

        >>> Editor.project(TerminalText(
        ...     fragments=SuperTuple([TerminalTextFragment(0, 0, "hello")]),
        ...     cursors=SuperTuple([TerminalCursor(0, 0)])
        ... )).print_fragments_and_cursors()
        TerminalTextFragment(x=0, y=1, text='hello', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=0, y=0, text='None 0ms', bold=None, bg='MAGENTA', fg='WHITE')
        TerminalCursor(x=0, y=1)
        """
        return Editor(
            projection=terminal_text.translate(dy=1).add_fragment(
                TerminalTextFragment(
                    text=f"{event} {ms}ms".ljust(width),
                    x=0,
                    y=0,
                    bg="MAGENTA",
                    fg="WHITE"
                )
            ),
            terminal_text=terminal_text,
            width=width
        )

    def keyboard_event(self, event):
        terminal_text, ms = measure_ms(lambda:
            self.terminal_text.keyboard_event(event)
        )
        return Editor.project(
            terminal_text=terminal_text,
            event=event,
            width=self.width,
            ms=ms
        )

    def size_event(self, event):
        terminal_text, ms = measure_ms(lambda:
            self.terminal_text.size_event(SizeEvent(
                width=event.width,
                height=event.height-1
            ))
        )
        return Editor.project(
            terminal_text=terminal_text,
            event=event,
            width=event.width,
            ms=ms
        )

def measure_ms(fn):
    t1 = time.perf_counter()
    return_value = fn()
    t2 = time.perf_counter()
    return (return_value, int((t2-t1)*1000))
