from collections import namedtuple

from rlprojectlib.domains.generic import Selections

class String(
    namedtuple("String", "string selections")
):

    @staticmethod
    def from_file(path):
        with open(path) as f:
            return String.from_string(f.read())

    @staticmethod
    def from_string(string, selection_start=0, selection_length=0):
        return String(
            string=string,
            selections=Selections([Selection(selection_start, selection_length)])
        )

    def replace(self, text):
        """
        >>> String.from_string("hello", selection_length=1).replace("1").string
        '1ello'
        """
        parts = []
        selections = []
        last_pos = 0
        for selection in self.selections:
            parts.append(self.string[last_pos:selection.pos_start])
            last_pos = selection.pos_end
            parts.append(text)
            selections.append(Selection(start=len("".join(parts)), length=0))
        parts.append(self.string[last_pos:])
        return String(
            string="".join(parts),
            selections=Selections(selections)
        )

    def move_cursor_back(self):
        return String(
            string=self.string,
            selections=Selections([self.selections[-1].move_cursor_back()])
        )

    def move_cursor_forward(self):
        return String(
            string=self.string,
            selections=Selections([self.selections[-1].move_cursor_forward()])
        )

    def select_next_word(self):
        """
        >>> String.from_string("hello there").select_next_word()
        String(string='hello there', selections=Selections(Selection(start=5, length=-5)))
        """
        if abs(self.selections[-1].length) > 0:
            return self._replace(selections=Selections(
                list(self.selections)+[self.selections[-1].move_forward(abs(self.selections[-1].length)+3)]
            ))
        else:
            return self._replace(selections=Selections([Selection(
                start=self.selections[-1].start+5,
                length=-5
            )]))

    def delete_back(self):
        """
        >>> String.from_string("hello", 1).delete_back()
        String(string='ello', selections=Selections(Selection(start=0, length=0)))
        """
        return self._replace(selections=self.selections.map(lambda x:
            x.delete_back()
        )).replace("")

class Selection(
    namedtuple("Selection", "start length")
):

    @property
    def abs_lenght(self):
        return abs(self.length)

    @property
    def pos_start(self):
        if self.length < 0:
            return self.start + self.length
        else:
            return self.start

    @property
    def pos_end(self):
        if self.length > 0:
            return self.start + self.length
        else:
            return self.start

    def move_cursor_back(self, steps=1):
        return self._replace(start=self.start-steps, length=0)

    def move_cursor_forward(self, steps=1):
        return self._replace(start=self.start+steps, length=0)

    def move_forward(self, steps=1):
        return self._replace(start=self.start+steps)

    def delete_back(self):
        if self.start <= 0:
            return self
        else:
            return self._replace(start=self.start-1, length=1)
