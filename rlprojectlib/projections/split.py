from collections import namedtuple

from rlprojectlib.domains.generic import SuperTuple
from rlprojectlib.domains.terminaltext import SizeEvent
from rlprojectlib.domains.terminaltext import TerminalText
from rlprojectlib.domains.terminaltext import TerminalTextFragment
from rlprojectlib.domains.terminaltext import TerminalTextFragmentsBuilder
from rlprojectlib.domains.terminaltext import TerminalTextProjection

class Split(
    namedtuple("Split", "projection terminal_texts width split_height"),
    TerminalTextProjection
):

    @staticmethod
    def project(terminal_texts, width=0, split_height=0):
        """
        >>> Split.project([
        ...     TerminalText(fragments=SuperTuple([
        ...         TerminalTextFragment(0, 0, "one")
        ...     ]), cursors=SuperTuple([])),
        ...     TerminalText(fragments=SuperTuple([
        ...         TerminalTextFragment(0, 0, "two")
        ...     ]), cursors=SuperTuple([])),
        ... ], width=10, split_height=1).projection.print_fragments_and_cursors()
        TerminalTextFragment(x=0, y=0, text='one', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=0, y=1, text='----------', bold=None, bg='FOREGROUND', fg='BACKGROUND')
        TerminalTextFragment(x=0, y=2, text='two', bold=None, bg=None, fg=None)
        """
        builder = TerminalTextFragmentsBuilder()
        cursors = []
        dy = 0
        for terminal_text in terminal_texts:
            if dy > 0:
                builder.add(TerminalTextFragment(0, dy, "-"*width, bg="FOREGROUND", fg="BACKGROUND"))
                dy += 1
            for fragment in terminal_text.fragments:
                builder.add(fragment.move(dy=dy))
            cursors.extend(terminal_text.cursors.map(lambda x: x.move(dy=dy)))
            dy += split_height
        return Split(
            projection=TerminalText(
                fragments=builder.to_immutable(),
                cursors=SuperTuple(cursors)
            ),
            terminal_texts=terminal_texts,
            width=width,
            split_height=split_height
        )

    def keyboard_event(self, event):
        return Split.project(
            terminal_texts=[x.keyboard_event(event) for x in self.terminal_texts],
            width=self.width,
            split_height=self.split_height,
        )

    def size_event(self, event):
        number_of_bars = len(self.terminal_texts) - 1
        split_height = max(
            1,
            (event.height - number_of_bars) // len(self.terminal_texts)
        )
        sized_terminal_texts = []
        for terminal_text in self.terminal_texts:
            sized_terminal_texts.append(terminal_text.size_event(SizeEvent(
                width=event.width,
                height=split_height
            )))
        return Split.project(
            terminal_texts=sized_terminal_texts,
            width=event.width,
            split_height=split_height
        )
