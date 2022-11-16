from collections import namedtuple

from rlprojectlib.domains.generic import SuperTuple
from rlprojectlib.domains.terminaltext import TerminalCursor
from rlprojectlib.domains.terminaltext import TerminalText
from rlprojectlib.domains.terminaltext import TerminalTextFragment
from rlprojectlib.domains.terminaltext import TerminalTextFragmentsBuilder
from rlprojectlib.domains.terminaltext import TerminalTextProjection

class ClipScroll(
    namedtuple("ClipScroll", "projection terminal_text width height"),
    TerminalTextProjection
):

    @staticmethod
    def project(terminal_text, width=0, height=0):
        """
        >>> ClipScroll.project(
        ...     terminal_text=TerminalText(
        ...         fragments=SuperTuple([TerminalTextFragment(0, 0, "hello")]),
        ...         cursors=SuperTuple([TerminalCursor(5, 0)]),
        ...     ),
        ...     width=2,
        ...     height=1,
        ... ).projection.print_fragments_and_cursors()
        TerminalTextFragment(x=0, y=0, text='o', bold=None, bg=None, fg=None)
        TerminalCursor(x=1, y=0)
        """
        visible_cursor = terminal_text.cursors[-1]
        if visible_cursor.x >= width:
            dx = width - visible_cursor.x - 1
        else:
            dx = 0
        if visible_cursor.y >= height:
            dy = height - visible_cursor.y - 1
        else:
            dy = 0
        return ClipScroll(
            projection=terminal_text.translate(dx=dx, dy=dy).clip(width, height),
            terminal_text=terminal_text,
            width=width,
            height=height
        )

    def keyboard_event(self, event):
        return ClipScroll.project(
            terminal_text=self.terminal_text.keyboard_event(event),
            width=self.width,
            height=self.height
        )

    def size_event(self, event):
        return ClipScroll.project(
            terminal_text=self.terminal_text.size_event(event),
            width=event.width,
            height=event.height
        )
