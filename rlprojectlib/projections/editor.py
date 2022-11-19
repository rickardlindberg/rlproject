from collections import namedtuple

import time

from rlprojectlib.domains.generic import SuperTuple
from rlprojectlib.domains.terminal import SizeEvent
from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.domains.terminal import Projection

class Editor(
    namedtuple("Editor", "projection terminal width"),
    Projection
):

    @staticmethod
    def project(terminal, event=None, width=0, ms=0):
        """
        I project a status bar followed by the given terminal text:

        >>> Editor.project(Terminal(
        ...     fragments=SuperTuple([TextFragment(0, 0, "hello")]),
        ...     cursors=SuperTuple([Cursor(0, 0)])
        ... )).print_fragments_and_cursors()
        TextFragment(x=0, y=1, text='hello', bold=None, bg=None, fg=None)
        TextFragment(x=0, y=0, text='None 0ms', bold=None, bg='MAGENTA', fg='WHITE')
        Cursor(x=0, y=1)
        """
        return Editor(
            projection=terminal.translate(dy=1).add_fragment(
                TextFragment(
                    text=f"{event} {ms}ms".ljust(width),
                    x=0,
                    y=0,
                    bg="MAGENTA",
                    fg="WHITE"
                )
            ),
            terminal=terminal,
            width=width
        )

    def keyboard_event(self, event):
        terminal, ms = measure_ms(lambda:
            self.terminal.keyboard_event(event)
        )
        return Editor.project(
            terminal=terminal,
            event=event,
            width=self.width,
            ms=ms
        )

    def size_event(self, event):
        terminal, ms = measure_ms(lambda:
            self.terminal.size_event(SizeEvent(
                width=event.width,
                height=event.height-1
            ))
        )
        return Editor.project(
            terminal=terminal,
            event=event,
            width=event.width,
            ms=ms
        )

def measure_ms(fn):
    t1 = time.perf_counter()
    return_value = fn()
    t2 = time.perf_counter()
    return (return_value, int((t2-t1)*1000))
