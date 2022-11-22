from collections import namedtuple

import time

from rlprojectlib.domains.string import String
from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import Projection
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.projections.string_to_terminal import StringToTerminal

class Meta(
    namedtuple("Meta", "terminal width popup")
):
    pass

class Editor(Terminal):

    """
    I can edit an example document without crashing:

    >>> from rlprojectlib.domains.terminal import SizeEvent
    >>> from rlprojectlib.domains.terminal import KeyboardEvent
    >>> terminal = Editor.from_file("rlproject.py")
    >>> _ = terminal.size_event(SizeEvent(10, 10))
    >>> _ = terminal.keyboard_event(KeyboardEvent('a'))
    """

    @staticmethod
    def from_file(path):
        from rlprojectlib.domains.string import String
        from rlprojectlib.projections.lines_to_terminal import LinesToTerminal
        from rlprojectlib.projections.string_to_lines import StringToLines
        from rlprojectlib.projections.string_to_terminal import StringToTerminal
        from rlprojectlib.projections.terminal.clipscroll import ClipScroll
        from rlprojectlib.projections.terminal.editor import Editor
        from rlprojectlib.projections.terminal.split import Split
        return Editor.project(
            Split.project([
                ClipScroll.project(
                    LinesToTerminal.project(
                        StringToLines.project(
                            String.from_file(path)
                        )
                    ),
                ),
                ClipScroll.project(
                    StringToTerminal.project(
                        String.from_file(path)
                    ),
                ),
            ])
        )

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
                text=f"Filter:".ljust(width),
                x=0,
                y=1,
                bg="GREEN",
                fg="WHITE",
                bold=True
            )).merge(popup.style(bg="GREEN", fg="WHITE").translate(dy=1, dx=8))
        else:
            projection = terminal.translate(
                dy=1
            ).add_fragment(
                status_fragment
            )
        return Editor(
            *projection.with_meta(Meta(
                terminal=terminal,
                width=width,
                popup=popup
            ))
        )

    def keyboard_event(self, event):
        terminal = self.meta.terminal
        popup = self.meta.popup
        ms = 0
        if self.meta.popup:
            if event.unicode_character == "\x07":
                popup = None
            else:
                popup, ms = measure_ms(lambda:
                    self.meta.popup.keyboard_event(event)
                )
        elif event.unicode_character == "\x07":
            popup = StringToTerminal.project(String.from_string(""))
        else:
            terminal, ms = measure_ms(lambda:
                self.meta.terminal.keyboard_event(event)
            )
        return Editor.project(
            terminal=terminal,
            event=event,
            width=self.meta.width,
            ms=ms,
            popup=popup
        )

    def size_event(self, event):
        if self.meta.popup:
            popup_height = 1
        else:
            popup_height = 0
        terminal, ms = measure_ms(lambda:
            self.meta.terminal.size_event(event.resize(dh=-1-popup_height))
        )
        return Editor.project(
            terminal=terminal,
            event=event,
            width=event.width,
            ms=ms,
            popup=self.meta.popup
        )

def measure_ms(fn):
    t1 = time.perf_counter()
    return_value = fn()
    t2 = time.perf_counter()
    return (return_value, int((t2-t1)*1000))
