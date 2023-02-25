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
    namedtuple("Options", "fn_or_terminal,proportion,active")
):

    def calculate_terminal(self, width, height):
        if isinstance(self.fn_or_terminal, Terminal):
            return self.fn_or_terminal
        else:
            return self.fn_or_terminal(width, height)

class Split(Terminal):

    """
    >>> terminal1 = Terminal.create(fragments=[
    ...     TextFragment(x=0, y=0, text="1111111111"),
    ...     TextFragment(x=0, y=1, text="1111111111"),
    ... ])
    >>> terminal2 = Terminal.create(fragments=[
    ...     TextFragment(x=0, y=0, text="2222222222"),
    ...     TextFragment(x=0, y=1, text="2222222222"),
    ... ])
    >>> terminal3 = Terminal.create(fragments=[
    ...     TextFragment(x=0, y=0, text="3333333333"),
    ...     TextFragment(x=0, y=1, text="3333333333"),
    ... ])

    >>> SplitIntoRows.project([
    ...     Options(lambda width, height: SplitIntoColumns.project([
    ...         Options(terminal1, 1, True),
    ...         Options(terminal2, 1, False),
    ...     ], width=width, height=height), 1, True),
    ...     Options(terminal3, 1, False),
    ... ], width=6, height=2).print_ascii_layout()
    111222
    333333

    >>> SplitIntoRows.project([
    ...     Options(lambda width, height: SplitIntoRows.project([
    ...         Options(terminal1, 1, True),
    ...         Options(terminal2, 1, False),
    ...     ], width=width, height=height), 1, True),
    ...     Options(terminal3, 1, False),
    ... ], width=4, height=4).print_ascii_layout()
    1111
    2222
    3333
    3333

    >>> SplitIntoRows.project([
    ...     Options(lambda width, height: SplitIntoColumns.project([
    ...         Options(terminal1, 1, True),
    ...         Options(terminal2, 1, False),
    ...     ], width=width, height=height), 1, True),
    ...     Options(terminal3, 1, False),
    ... ], width=4, height=6).print_ascii_layout()
    1122
    1122
    <BLANKLINE>
    3333
    3333

    >>> SplitIntoRows.project([
    ...     Options(lambda width, height: SplitIntoColumns.project([
    ...         Options(terminal1, 1, True),
    ...         Options(terminal2, 1, False),
    ...     ], width=width, height=height), 0, True),
    ...     Options(terminal3, 1, False),
    ... ], width=4, height=6).print_ascii_layout()
    1122
    1122
    3333
    3333

    >>> SplitIntoRows.project([
    ...     Options(terminal1, 0, True),
    ...     Options(terminal2, 0, False),
    ... ], width=3, height=3).print_ascii_layout()
    111
    111
    222
    222

    >>> one_space_two = lambda width, height: SplitIntoColumns.project([
    ...     Options(
    ...         Terminal.create(fragments=[TextFragment(x=0, y=0, text="1")]),
    ...         0,
    ...         True
    ...     ),
    ...     Options(
    ...         lambda width, height: Terminal.create(fragments=[TextFragment(x=0, y=0, text="*"*width)]),
    ...         1,
    ...         True
    ...     ),
    ...     Options(
    ...         Terminal.create(fragments=[TextFragment(x=0, y=0, text="2")]),
    ...         0,
    ...         False
    ...     ),
    ... ], width=width, height=height)

    >>> one_space_two(5, 5).print_ascii_layout()
    1***2

    >>> SplitIntoColumns.project([
    ...     Options(
    ...         one_space_two,
    ...         1,
    ...         True
    ...     ),
    ...     Options(
    ...         Terminal.create(fragments=[TextFragment(x=0, y=0, text="x")]),
    ...         1,
    ...         False
    ...     ),
    ... ], width=10, height=10).print_ascii_layout()
    1***2x

    >>> SplitIntoRows.project([
    ...     Options(
    ...         one_space_two,
    ...         0,
    ...         True
    ...     ),
    ...     Options(
    ...         Terminal.create(fragments=[TextFragment(x=0, y=0, text="x")]),
    ...         1,
    ...         False
    ...     ),
    ...     Options(
    ...         Terminal.create(fragments=[TextFragment(x=0, y=0, text="y")]),
    ...         1,
    ...         False
    ...     ),
    ... ], width=5, height=5).print_ascii_layout()
    1***2
    x
    <BLANKLINE>
    y
    """

    @classmethod
    def project(cls, options, height, width):
        builder = TextFragmentsBuilder()
        offset = 0
        active = None
        size_left = cls.get_start_size(width, height)
        proportion_total = 0
        for option in options:
            if option.proportion == 0:
                size_left -= cls.get_size(width, height, option)
            else:
                proportion_total += option.proportion
        for option in options:
            if option.proportion == 0:
                terminal_size = cls.get_size(width, height, option)
            else:
                terminal_size = int(size_left * (option.proportion/proportion_total))
            child_size = cls.get_child_size(width, height, terminal_size)
            terminal = ClipScroll.project(
                option.calculate_terminal(**child_size),
                **child_size
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
    def get_size(width, height, option):
        return option.calculate_terminal(width, height).get_height()

    @staticmethod
    def get_start_size(width, height):
        return height

    @staticmethod
    def get_child_size(width, height, size):
        return {"width": width, "height": size}

    @staticmethod
    def get_dx_xy(offset):
        return {"dy": offset}

class SplitIntoColumns(Split):

    """
    >>> terminal1 = Terminal.create(fragments=[
    ...     TextFragment(x=0, y=0, text="111"),
    ... ])
    >>> terminal2 = Terminal.create(fragments=[
    ...     TextFragment(x=0, y=0, text="222"),
    ... ])

    I lay out terminal windows in columns:

    >>> SplitIntoColumns.project([
    ...     Options(terminal1, 0, True),
    ...     Options(terminal2, 0, False),
    ... ], 6, 1).print_fragments_and_cursors()
    TextFragment(x=0, y=0, text='111', bold=None, bg=None, fg=None)
    TextFragment(x=3, y=0, text='222', bold=None, bg=None, fg=None)
    """

    @staticmethod
    def get_size(width, height, option):
        return option.calculate_terminal(width, height).get_width()

    @staticmethod
    def get_start_size(width, height):
        return width

    @staticmethod
    def get_child_size(width, height, size):
        return {"width": size, "height": height}

    @staticmethod
    def get_dx_xy(offset):
        return {"dx": offset}
