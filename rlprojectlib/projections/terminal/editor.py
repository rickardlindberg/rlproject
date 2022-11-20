from collections import namedtuple

import time

from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.domains.terminal import Projection

class Editor(
    namedtuple("Editor", "projection terminal width popup"),
    Projection
):

    @staticmethod
    def project(terminal, event=None, width=0, ms=0, popup=None):
        """
        I project a status bar followed by the given terminal text:

        >>> Editor.project(Terminal.create(
        ...     fragments=[TextFragment(0, 0, "hello")],
        ...     cursors=[Cursor(0, 0)]
        ... )).print_fragments_and_cursors()
        TextFragment(x=0, y=1, text='hello', bold=None, bg=None, fg=None)
        TextFragment(x=0, y=0, text='None 0ms', bold=None, bg='MAGENTA', fg='WHITE')
        Cursor(x=0, y=1)
        """
        status_fragment = TextFragment(
            text=f"{event} {ms}ms".ljust(width),
            x=0,
            y=0,
            bg="MAGENTA",
            fg="WHITE"
        )
        if popup:
            projection = terminal.clear_cursors(
            ).translate(
                dy=2
            ).add_fragment(
                status_fragment
            ).add_fragment(TextFragment(
                text=f"Filter: ".ljust(width),
                x=0,
                y=1,
                bg="GREEN",
                fg="WHITE",
                bold=True
            ))
        else:
            projection = terminal.translate(
                dy=1
            ).add_fragment(
                status_fragment
            )
        return Editor(
            projection=projection,
            terminal=terminal,
            width=width,
            popup=popup
        )

    def keyboard_event(self, event):
        terminal = self.terminal
        popup = self.popup
        ms = 0
        if self.popup:
            if event.unicode_character == "\x07":
                popup = None
            else:
                popup, ms = measure_ms(lambda:
                    self.popup.keyboard_event(event)
                )
        elif event.unicode_character == "\x07":
            popup = Terminal.create()
        else:
            terminal, ms = measure_ms(lambda:
                self.terminal.keyboard_event(event)
            )
        return Editor.project(
            terminal=terminal,
            event=event,
            width=self.width,
            ms=ms,
            popup=popup
        )

    def size_event(self, event):
        if self.popup:
            popup_height = 1
        else:
            popup_height = 0
        terminal, ms = measure_ms(lambda:
            self.terminal.size_event(event.resize(dh=-1-popup_height))
        )
        return Editor.project(
            terminal=terminal,
            event=event,
            width=event.width,
            ms=ms,
            popup=self.popup
        )

def measure_ms(fn):
    t1 = time.perf_counter()
    return_value = fn()
    t2 = time.perf_counter()
    return (return_value, int((t2-t1)*1000))
