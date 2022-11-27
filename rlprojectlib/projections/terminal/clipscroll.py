from collections import namedtuple

from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.domains.terminal import TextFragmentsBuilder

class Meta(
    namedtuple("Meta", "terminal")
):
    pass

class ClipScroll(Terminal):

    @staticmethod
    def project(terminal, width, height):
        """
        >>> ClipScroll.project(
        ...     terminal=Terminal.create(
        ...         fragments=[TextFragment(0, 0, "hello")],
        ...         cursors=[Cursor(5, 0)],
        ...     ),
        ...     width=2,
        ...     height=1,
        ... ).print_fragments_and_cursors()
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
            *terminal.translate(
                dx=dx,
                dy=dy
            ).clip(
                width,
                height
            ).replace_meta(Meta(
                terminal=terminal
            ))
        )

    def keyboard_event(self, event):
        return self.meta.terminal.keyboard_event(event)
