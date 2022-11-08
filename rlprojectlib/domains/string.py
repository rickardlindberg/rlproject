from collections import namedtuple

class String(
    namedtuple("String", "string selections")
):

    @staticmethod
    def from_file(path):
        with open(path) as f:
            return String(string=f.read(), selections=[Selection(0, 0)])

    def keyboard_event(self, event):
        if event.unicode_character == "\x06": # Ctrl-F
            return self.move_cursor_forward()
        elif event.unicode_character == "\x02": # Ctrl-B
            return self.move_cursor_back()
        elif event.unicode_character == "\x0e": # Ctrl-N
            return self.select_next_word()
        elif event.unicode_character and ord(event.unicode_character) >= 32:
            return self.replace(event.unicode_character)
        else:
            return self

    def replace(self, text):
        """
        >>> String("hello", [Selection(0, 1)]).replace("1").string
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
            selections=selections
        )

    def move_cursor_back(self):
        return String(
            string=self.string,
            selections=[self.selections[-1].move_cursor_back()]
        )

    def move_cursor_forward(self):
        return String(
            string=self.string,
            selections=[self.selections[-1].move_cursor_forward()]
        )

    def select_next_word(self):
        """
        >>> String("hello there", [Selection(0, 0)]).select_next_word()
        String(string='hello there', selections=[Selection(start=5, length=-5)])
        """
        if abs(self.selections[-1].length) > 0:
            return self._replace(selections=self.selections+[self.selections[-1].move_forward(abs(self.selections[-1].length))])
        else:
            return self._replace(selections=[Selection(
                start=self.selections[-1].start+5,
                length=-5
            )])

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
