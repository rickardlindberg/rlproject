from collections import namedtuple

from rlprojectlib.domains.generic import Coordinate
from rlprojectlib.domains.generic import ImmutableList

class Terminal(
    namedtuple("Terminal", "meta fragments cursors"),
):

    @classmethod
    def create(cls, fragments=[], cursors=[], meta=None):
        return cls(
            meta=meta,
            fragments=ImmutableList(fragments),
            cursors=ImmutableList(cursors)
        )

    def with_meta(self, meta):
        return self._replace(meta=meta)

    def print_fragments_and_cursors(self):
        self.fragments.print()
        self.cursors.print()

    def translate(self, dx=0, dy=0):
        return self._replace(
            fragments=self.fragments.map(lambda x: x.move(dx=dx, dy=dy)),
            cursors=self.cursors.map(lambda x: x.move(dx=dx, dy=dy))
        )

    def clip(self, width, height):
        return self._replace(
            fragments=self.fragments.filter(lambda fragment:
                fragment.y < height
            ).map(lambda fragment: fragment.clip(width)),
            cursors=self.cursors.filter(lambda cursor:
                cursor.x >= 0 and cursor.x < width and
                cursor.y >= 0 and cursor.y < height
            )
        )

    def add_fragment(self, fragment):
        return self._replace(
            fragments=self.fragments.add(fragment)
        )

    def clear_cursors(self):
        return self._replace(cursors=ImmutableList())

    def merge(self, terminal):
        return Terminal.create(
            fragments=self.fragments.merge(terminal.fragments),
            cursors=self.cursors.merge(terminal.cursors),
        )

    def style(self, **kwargs):
        return self._replace(fragments=self.fragments.map(lambda x: x._replace(**kwargs)))

    def keyboard_event(self, event):
        raise NotImplementedError()

    def size_event(self, event):
        raise NotImplementedError()

class Cursor(
    namedtuple("Cursor", "x y"),
    Coordinate
):
    pass

class TextFragment(
    namedtuple(
        "TextFragment",
        "x y text bold bg fg",
        defaults=[None, None, None]
    ),
    Coordinate
):

    def clip(self, width):
        """
        >>> TextFragment(0, 0, "hello").clip(2)
        TextFragment(x=0, y=0, text='he', bold=None, bg=None, fg=None)

        >>> TextFragment(-2, 0, "hello").clip(2)
        TextFragment(x=0, y=0, text='ll', bold=None, bg=None, fg=None)

        >>> TextFragment(1, 0, "hello").clip(2)
        TextFragment(x=1, y=0, text='h', bold=None, bg=None, fg=None)
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
        >>> TextFragment(0, 0, "hello").split("ll", text="||", fg="YELLOW").print()
        TextFragment(x=0, y=0, text='he', bold=None, bg=None, fg=None)
        TextFragment(x=2, y=0, text='||', bold=None, bg=None, fg='YELLOW')
        TextFragment(x=4, y=0, text='o', bold=None, bg=None, fg=None)

        >>> TextFragment(0, 0, "n2").split("n", text="N").print()
        TextFragment(x=0, y=0, text='N', bold=None, bg=None, fg=None)
        TextFragment(x=1, y=0, text='2', bold=None, bg=None, fg=None)
        """
        fragments = TextFragmentsBuilder()
        next_x = self.x
        for index, subtext in enumerate(self.text.split(separator)):
            if index > 0:
                next_x += fragments.add(self._replace(x=next_x, **styling_kwargs))
            next_x += fragments.add(self._replace(x=next_x, text=subtext))
        return fragments.get()

class TextFragmentsBuilder:

    def __init__(self):
        self.fragments = []

    def add(self, fragment):
        if fragment.text:
            self.fragments.append(fragment)
        return len(fragment.text)

    def extend(self, fragments):
        return sum(self.add(x) for x in fragments)

    def get(self):
        return ImmutableList(self.fragments)

class KeyboardEvent(
    namedtuple("KeyboardEvent", "unicode_character")
):
    pass

class SizeEvent(
    namedtuple("SizeEvent", "width height")
):

    def resize(self, height=None, dh=0):
        return self._replace(
            height=(self.height if height is None else height)+dh
        )
