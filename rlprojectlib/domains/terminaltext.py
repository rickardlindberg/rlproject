from collections import namedtuple

from rlprojectlib.domains.generic import Coordinate

class TerminalText(
    namedtuple("TerminalText", "fragments cursors"),
):

    def print_fragments_and_cursors(self):
        for fragment in self.fragments:
            print(fragment)
        for cursor in self.cursors:
            print(cursor)

class TerminalTextProjection:

    @property
    def fragments(self):
        return self.terminal_text.fragments

    @property
    def cursors(self):
        return self.terminal_text.cursors

    def print_fragments_and_cursors(self):
        self.terminal_text.print_fragments_and_cursors()

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
        >>> print_namedtuples(TerminalTextFragment(0, 0, "hello").split("ll", text="||", fg="YELLOW"))
        TerminalTextFragment(x=0, y=0, text='he', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=2, y=0, text='||', bold=None, bg=None, fg='YELLOW')
        TerminalTextFragment(x=4, y=0, text='o', bold=None, bg=None, fg=None)

        >>> print_namedtuples(TerminalTextFragment(0, 0, "n2").split("n", text="N"))
        TerminalTextFragment(x=0, y=0, text='N', bold=None, bg=None, fg=None)
        TerminalTextFragment(x=1, y=0, text='2', bold=None, bg=None, fg=None)
        """
        fragments = TerminalTextFragmentsBuilder()
        next_x = self.x
        for index, subtext in enumerate(self.text.split(separator)):
            if index > 0:
                next_x += fragments.add(self._replace(x=next_x, **styling_kwargs))
            next_x += fragments.add(self._replace(x=next_x, text=subtext))
        return fragments.to_tuple()

class TerminalTextFragmentsBuilder:

    def __init__(self):
        self.fragments = []

    def add(self, fragment):
        if fragment.text:
            self.fragments.append(fragment)
        return len(fragment.text)

    def extend(self, fragments):
        return sum(self.add(x) for x in fragments)

    def to_tuple(self):
        return tuple(self.fragments)

class KeyboardEvent(
    namedtuple("KeyboardEvent", "unicode_character")
):
    pass

def print_namedtuples(namedtuples):
    print("\n".join(repr(x) for x in namedtuples))
