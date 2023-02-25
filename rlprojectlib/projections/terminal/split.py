from collections import namedtuple

from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.domains.terminal import TextFragmentsBuilder
from rlprojectlib.projections.terminal.clipscroll import ClipScroll

class Meta(
    namedtuple("Meta", "active_terminal")
):
    pass

class Options(
    namedtuple("Options", "terminal,proportion,active")
):
    pass

class Split(Terminal):

    @classmethod
    def project(cls, options, height, width):
        builder = TextFragmentsBuilder()
        offset = 0
        active = None
        size_left = cls.get_start_size(width, height)
        proportion_total = 0
        for option in options:
            if option.proportion == 0:
                size_left -= cls.get_size(option)
            else:
                proportion_total += option.proportion
        for option in options:
            if option.proportion == 0:
                terminal_size = cls.get_size(option)
            else:
                terminal_size = int(size_left * (option.proportion/proportion_total))
            terminal = ClipScroll.project(
                option.terminal,
                **cls.get_child_size(width, height, terminal_size)
            ).translate(**cls.get_dx_xy(offset))
            builder.extend(terminal.fragments)
            offset += terminal_size
            if option.active:
                active = terminal
        return SplitIntoRows(*Terminal.create(
            fragments=builder.get(),
            cursors=active.cursors
        )).replace_meta(Meta(active_terminal=active))

    def size_event(self, event):
        return self.meta.active_terminal.size_event(event)

    def keyboard_event(self, event):
        return self.meta.active_terminal.keyboard_event(event)

class SplitIntoRows(Split):

    """
    >>> terminal1 = Terminal.create(fragments=[
    ...     TextFragment(x=0, y=0, text="one one"),
    ...     TextFragment(x=0, y=1, text="one two"),
    ... ], cursors=[Cursor(x=0, y=0)])
    >>> terminal2 = Terminal.create(fragments=[
    ...     TextFragment(x=0, y=0, text="two one"),
    ...     TextFragment(x=0, y=1, text="two two"),
    ... ], cursors=[Cursor(x=0, y=0)])

    I lay out terminal windows vertically:

    >>> SplitIntoRows.project([
    ...     Options(terminal1, 1, True),
    ...     Options(terminal2, 1, False),
    ... ], 6, 10).print_fragments_and_cursors()
    TextFragment(x=0, y=0, text='one one', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=1, text='one two', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=3, text='two one', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=4, text='two two', bold=None, bg=None, fg=None)
    Cursor(x=0, y=0)

    >>> SplitIntoRows.project([
    ...     Options(terminal1, 0, True),
    ...     Options(terminal2, 1, False),
    ... ], 5, 10).print_fragments_and_cursors()
    TextFragment(x=0, y=0, text='one one', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=1, text='one two', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=2, text='two one', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=3, text='two two', bold=None, bg=None, fg=None)
    Cursor(x=0, y=0)

    I clip terminals that do not fit:

    >>> SplitIntoRows.project([
    ...     Options(terminal1, 1, True),
    ...     Options(terminal2, 1, False),
    ... ], 2, 10).print_fragments_and_cursors()
    TextFragment(x=0, y=0, text='one one', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=1, text='two one', bold=None, bg=None, fg=None)
    Cursor(x=0, y=0)

    Only cursors from the active terminal is shown:

    >>> SplitIntoRows.project([
    ...     Options(terminal1, 1, True),
    ...     Options(terminal2, 1, False),
    ... ], 4, 10).print_fragments_and_cursors()
    TextFragment(x=0, y=0, text='one one', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=1, text='one two', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=2, text='two one', bold=None, bg=None, fg=None)
    TextFragment(x=0, y=3, text='two two', bold=None, bg=None, fg=None)
    Cursor(x=0, y=0)
    """

    @staticmethod
    def get_size(option):
        return option.terminal.get_height()

    @staticmethod
    def get_start_size(width, height):
        return height

    @staticmethod
    def get_child_size(width, height, size):
        return {"width": width, "height": size}

    @staticmethod
    def get_dx_xy(offset):
        return {"dy": offset}
