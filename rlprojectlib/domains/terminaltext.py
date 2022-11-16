from collections import namedtuple

from rlprojectlib.domains.generic import Coordinate, SuperTuple

class TerminalText(
    namedtuple("TerminalText", "fragments cursors"),
):

    def print_fragments_and_cursors(self):
        self.fragments.print()
        self.cursors.print()

    def translate(self, dx=0, dy=0):
        return self._replace(
            fragments=self.fragments.map(lambda x: x.move(dx=dx, dy=dy)),
            cursors=self.cursors.map(lambda x: x.move(dx=dx, dy=dy))
        )

    def clip(self, width, height):
        fragments = TerminalTextFragmentsBuilder()
        for fragment in self.fragments:
            if fragment.y < height:
                fragments.add(fragment.clip(width))
        cursors = []
        for cursor in self.cursors:
            if cursor.x <= width and cursor.y < height:
                cursors.append(cursor)
        return TerminalText(
            fragments=fragments.to_immutable(),
            cursors=SuperTuple(cursors)
        )

    def add_fragment(self, fragment):
        return self._replace(
            fragments=self.fragments.add(fragment)
        )

class TerminalTextProjection:

    @property
    def fragments(self):
        return self.projection.fragments

    @property
    def cursors(self):
        return self.projection.cursors

    def print_fragments_and_cursors(self):
        self.projection.print_fragments_and_cursors()

    def translate(self, *args, **kwargs):
        return self.projection.translate(*args, **kwargs)

    def clip(self, *args, **kwargs):
        return self.projection.clip(*args, **kwargs)

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

    def clip(self, width):
        """
        >>> TerminalTextFragment(0, 0, "hello").clip(2)
        TerminalTextFragment(x=0, y=0, text='he', bold=None, bg=None, fg=None)

        >>> TerminalTextFragment(-2, 0, "hello").clip(2)
        TerminalTextFragment(x=0, y=0, text='ll', bold=None, bg=None, fg=None)

        >>> TerminalTextFragment(1, 0, "hello").clip(2)
        TerminalTextFragment(x=1, y=0, text='h', bold=None, bg=None, fg=None)
        """
        if self.x < 0:
            start = -self.x
            end = start + width
            x = 0
        else:
            start = 0
            end = width - self.x
            x = self.x
        return self._replace(text=self.text[start:end], x=x)

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

class SizeEvent(
    namedtuple("SizeEvent", "width height")
):
    pass
