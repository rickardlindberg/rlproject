from collections import namedtuple

from rlprojectlib.domains.generic import Coordinate, SuperTuple

class TerminalText(
    namedtuple("TerminalText", "fragments cursors"),
):

    def print_fragments_and_cursors(self):
        self.fragments.print()
        self.cursors.print()

class TerminalTextProjection:

    @property
    def fragments(self):
        return self.projection.fragments

    @property
    def cursors(self):
        return self.projection.cursors

    def print_fragments_and_cursors(self):
        self.projection.print_fragments_and_cursors()

class TerminalCursor(
    namedtuple("TerminalCursor", "x y"),
    Coordinate
):
    pass

class TerminalTextFragment(
    namedtuple(
        "TerminalTextFragment",
        "x y text bold bg fg",
        defaults=[None, None, None]
    ),
    Coordinate
):

    def replace_newlines(self, **styling_kwargs):
        return self.split("\n", text="\\n", **styling_kwargs)

    def split(self, separator, **styling_kwargs):
        """
        >>> TerminalTextFragment(0, 0, "hello").split("ll", text="||", fg="YELLOW").print()
        TerminalTextFragment(x=0, y=0, text='he', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=2, y=0, text='||', bold=None, bg=None, fg='YELLOW')
        TerminalTextFragment(x=4, y=0, text='o', bold=None, bg=None, fg=None)

        >>> TerminalTextFragment(0, 0, "n2").split("n", text="N").print()
        TerminalTextFragment(x=0, y=0, text='N', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=1, y=0, text='2', bold=None, bg=None, fg=None)
        """
        fragments = TerminalTextFragmentsBuilder()
        next_x = self.x
        for index, subtext in enumerate(self.text.split(separator)):
            if index > 0:
                next_x += fragments.add(self._replace(x=next_x, **styling_kwargs))
            next_x += fragments.add(self._replace(x=next_x, text=subtext))
        return fragments.to_immutable()

class TerminalTextFragmentsBuilder:

    def __init__(self):
        self.fragments = []

    def add(self, fragment):
        if fragment.text:
            self.fragments.append(fragment)
        return len(fragment.text)

    def extend(self, fragments):
        return sum(self.add(x) for x in fragments)

    def to_immutable(self):
        return SuperTuple(self.fragments)

class KeyboardEvent(
    namedtuple("KeyboardEvent", "unicode_character")
):
    pass
