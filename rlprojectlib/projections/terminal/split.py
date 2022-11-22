from collections import namedtuple

from rlprojectlib.domains.terminal import Projection
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.domains.terminal import TextFragmentsBuilder

class Meta(
    namedtuple("Meta", "terminals width split_height")
):
    pass

class Split(Terminal):

    @staticmethod
    def project(terminals, width=0, split_height=0):
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
                    width=width,
                    split_height=split_height
                )
            )
        )

    def keyboard_event(self, event):
        return Split.project(
            terminals=[x.keyboard_event(event) for x in self.meta.terminals],
            width=self.meta.width,
            split_height=self.meta.split_height,
        )

    def size_event(self, event):
        number_of_bars = len(self.meta.terminals) - 1
        split_height = max(
            1,
            (event.height - number_of_bars) // len(self.meta.terminals)
        )
        sized_terminal_texts = []
        for terminal in self.meta.terminals:
            sized_terminal_texts.append(terminal.size_event(event.resize(
                height=split_height
            )))
        return Split.project(
            terminals=sized_terminal_texts,
            width=event.width,
            split_height=split_height
        )
