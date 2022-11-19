from collections import namedtuple

from rlprojectlib.domains.generic import SuperTuple
from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.domains.terminal import TextFragmentsBuilder
from rlprojectlib.domains.terminal import Projection

class ClipScroll(
    namedtuple("ClipScroll", "projection terminal width height"),
    Projection
):

    @staticmethod
    def project(terminal, width=0, height=0):
        """
        >>> ClipScroll.project(
        ...     terminal=Terminal(
        ...         fragments=SuperTuple([TextFragment(0, 0, "hello")]),
        ...         cursors=SuperTuple([Cursor(5, 0)]),
        ...     ),
        ...     width=2,
        ...     height=1,
        ... ).projection.print_fragments_and_cursors()
        TextFragment(x=0, y=0, text='o', bold=None, bg=None, fg=None)
        Cursor(x=1, y=0)
        """
        visible_cursor = terminal.cursors[-1]
        if visible_cursor.x >= width:
            dx = width - visible_cursor.x - 1
        else:
            dx = 0
        if visible_cursor.y >= height:
            dy = height - visible_cursor.y - 1
        else:
            dy = 0
        return ClipScroll(
            projection=terminal.translate(dx=dx, dy=dy).clip(width, height),
            terminal=terminal,
            width=width,
            height=height
        )

    def keyboard_event(self, event):
        return ClipScroll.project(
            terminal=self.terminal.keyboard_event(event),
            width=self.width,
            height=self.height
        )

    def size_event(self, event):
        return ClipScroll.project(
            terminal=self.terminal.size_event(event),
            width=event.width,
            height=event.height
        )
