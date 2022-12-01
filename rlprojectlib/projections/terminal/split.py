from collections import namedtuple

from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.domains.terminal import TextFragmentsBuilder

class Meta(
    namedtuple("Meta", "terminals")
):
    pass

class Split(Terminal):

    @staticmethod
    def project(terminals, width, split_height):
        """
        >>> Split.project([
        ...     Terminal.create(fragments=[
        ...         TextFragment(0, 0, "one")
        ...     ]),
        ...     Terminal.create(fragments=[
        ...         TextFragment(0, 0, "two")
        ...     ]),
        ... ], width=10, split_height=1).print_fragments_and_cursors()
        TextFragment(x=0, y=0, text='one', bold=None, bg=None, fg=None)
        TextFragment(x=0, y=1, text='----------', bold=None, bg='FOREGROUND', fg='BACKGROUND')
        TextFragment(x=0, y=2, text='two', bold=None, bg=None, fg=None)
        """
        builder = TextFragmentsBuilder()
        cursors = []
        dy = 0
        for terminal in terminals:
            if dy > 0:
                builder.add(TextFragment(0, dy, "-"*width, bg="FOREGROUND", fg="BACKGROUND"))
                dy += 1
            for fragment in terminal.fragments:
                builder.add(fragment.move(dy=dy))
            cursors.extend(terminal.cursors.map(lambda x: x.move(dy=dy)))
            dy += split_height
        return Split(
            *Terminal.create(
                fragments=builder.get(),
                cursors=cursors,
                meta=Meta(
                    terminals=terminals,
                )
            )
        )

    def size_event(self, event):
        """
        A size event does nothing:

        >>> t1 = Terminal.create(cursors=[Cursor(0, 0)])
        >>> t2 = Terminal.create(cursors=[Cursor(0, 0)])
        >>> terminals = [t1, t2]
        >>> Split.project(terminals, 1, 1).size_event(None) is t2
        True
        """
        return self.meta.terminals[-1].get_source()

    def keyboard_event(self, event):
        return self.meta.terminals[-1].keyboard_event(event)
