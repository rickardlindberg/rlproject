from collections import namedtuple

from rlprojectlib.domains.generic import SuperTuple
from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextFragment, TerminalTextProjection, TerminalTextFragmentsBuilder

class Split(
    namedtuple("Split", "projection terminal_texts width height"),
    TerminalTextProjection
):

    @staticmethod
    def project(terminal_texts, width=0, height=0):
        """
        >>> Split.project([
        ...     TerminalText(fragments=SuperTuple([
        ...         TerminalTextFragment(0, 0, "one")
        ...     ]), cursors=SuperTuple([])),
        ...     TerminalText(fragments=SuperTuple([
        ...         TerminalTextFragment(0, 0, "two")
        ...     ]), cursors=SuperTuple([])),
        ... ], width=10, height=3).projection.print_fragments_and_cursors()
        TerminalTextFragment(x=0, y=0, text='one', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=0, y=1, text='----------', bold=None, bg='FOREGROUND', fg='BACKGROUND')
        TerminalTextFragment(x=0, y=2, text='two', bold=None, bg=None, fg=None)
        """
        builder = TerminalTextFragmentsBuilder()
        cursors = []
        step = max(1, height // len(terminal_texts))
        dy = 0
        for terminal_text in terminal_texts:
            if dy > 0:
                builder.add(TerminalTextFragment(0, dy, "-"*width, bg="FOREGROUND", fg="BACKGROUND"))
                dy += 1
            for fragment in terminal_text.fragments:
                if fragment.y < step:
                    builder.add(fragment.move(dy=dy))
            cursors.extend(terminal_text.cursors.map(lambda x: x.move(dy=dy)))
            dy += step
        return Split(
            projection=TerminalText(
                fragments=builder.to_immutable(),
                cursors=SuperTuple(cursors)
            ),
            terminal_texts=terminal_texts,
            width=width,
            height=height
        )

    def keyboard_event(self, event):
        return Split.project(
            terminal_texts=[x.keyboard_event(event) for x in self.terminal_texts],
            width=self.width,
            height=self.height
        )

    def size_event(self, event):
        return Split.project(
            terminal_texts=self.terminal_texts,
            width=event.width,
            height=event.height
        )
