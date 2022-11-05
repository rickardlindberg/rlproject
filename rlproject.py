import wx
from collections import namedtuple

class Canvas(wx.Panel):

    THEME = {
        "font_size": 17,
        "colors": {
            "BACKGROUND": (0, 43, 54),
            "FOREGROUND": (101, 123, 131),
            "BLACK": (7, 54, 66),
            "BLUE": (38, 139, 210),
            "CYAN": (42, 161, 152),
            "GREEN": (133, 153, 0),
            "MAGENTA": (211, 54, 130),
            "RED": (220, 50, 47),
            "WHITE": (238, 232, 213),
            "YELLOW": (181, 137, 0),
        },
    }

    def __init__(self, parent, document):
        wx.Panel.__init__(self, parent, style=wx.NO_BORDER|wx.WANTS_CHARS)
        self.document = document
        self.cursor_blink_timer = wx.Timer(self)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.Bind(wx.EVT_SET_FOCUS, self.on_set_focus)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)
        self.repaint_bitmap()

    def on_size(self, evt):
        self.repaint_bitmap()

    def on_char(self, evt):
        new_document = self.document.keyboard_event(KeyboardEvent(
            unicode_character=chr(evt.GetUnicodeKey())
        ))
        if new_document != self.document:
            self.document = new_document
            self.repaint_bitmap()

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0, True)
        if self.show_cursors:
            dc.SetPen(wx.Pen((0, 0, 0), 0))
            dc.SetBrush(wx.Brush(self.THEME["colors"]["FOREGROUND"]))
            for cursor_rect in self.cursor_rects:
                dc.DrawRectangle(cursor_rect)

    def on_timer(self, event):
        self.show_cursors = not self.show_cursors
        self.force_repaint_window()

    def on_set_focus(self, event):
        self.reset_cursor_blink()
        self.force_repaint_window()

    def on_kill_focus(self, event):
        self.cursor_blink_timer.Stop()
        self.show_cursors = True
        self.force_repaint_window()

    def repaint_bitmap(self):
        font = wx.Font(
            self.THEME["font_size"],
            wx.FONTFAMILY_TELETYPE,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL
        )
        font_bold = font.Bold()
        width, height = self.GetSize()
        self.bitmap = wx.Bitmap(width, height)
        memdc = wx.MemoryDC()
        memdc.SelectObject(self.bitmap)
        memdc.SetBackground(wx.Brush(self.THEME["colors"]["BACKGROUND"], wx.SOLID))
        memdc.SetBackgroundMode(wx.PENSTYLE_SOLID)
        memdc.Clear()
        memdc.SetFont(font)
        char_width, char_height = memdc.GetTextExtent(".")
        for string in self.document.strings:
            if string.bold:
                memdc.SetFont(font_bold)
            else:
                memdc.SetFont(font)
            memdc.SetTextBackground(self.THEME["colors"].get(string.bg, self.THEME["colors"]["BACKGROUND"]))
            memdc.SetTextForeground(self.THEME["colors"].get(string.fg, self.THEME["colors"]["FOREGROUND"]))
            memdc.DrawText(string.text, string.x*char_width, string.y*char_height)
        del memdc
        self.cursor_rects = []
        for cursor in self.document.cursors:
            self.cursor_rects.append(wx.Rect(
                cursor.x*char_width-1,
                cursor.y*char_height,
                3,
                char_height
            ))
        self.reset_cursor_blink()
        self.force_repaint_window()

    def reset_cursor_blink(self):
        self.show_cursors = True
        self.cursor_blink_timer.Start(500)

    def force_repaint_window(self):
        self.Refresh()
        self.Update()

class TerminalText:

    def __init__(self, cursors, strings):
        self.cursors = cursors
        self.strings = strings

class Coordinate:

    def move(self, dy):
        return self._replace(y=self.y+dy)

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
    pass

class KeyboardEvent(
    namedtuple("KeyboardEvent", "unicode_character")
):
    pass

class String(
    namedtuple("String", "string selections")
):

    def replace(self, text):
        """
        >>> String("hello", [StringSelection(0, 1)]).replace("1").string
        '1ello'
        """
        return String(
            string="".join([
                self.string[:self.selections[-1].start],
                text,
                self.string[self.selections[-1].start+self.selections[-1].length:],
            ]),
            selections=[self.selections[-1].move_cursor_forward()]
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
        >>> String("hello there", [StringSelection(0, 0)]).select_next_word()
        String(string='hello there', selections=[StringSelection(start=5, length=-5)])
        """
        if abs(self.selections[-1].length) > 0:
            return self._replace(selections=self.selections+[self.selections[-1].move_forward(abs(self.selections[-1].length))])
        else:
            return self._replace(selections=[StringSelection(
                start=self.selections[-1].start+5,
                length=-5
            )])

class StringSelection(
    namedtuple("StringSelection", "start length")
):

    def move_cursor_back(self, steps=1):
        return self._replace(start=self.start-steps, length=0)

    def move_cursor_forward(self, steps=1):
        return self._replace(start=self.start+steps, length=0)

    def move_forward(self, steps=1):
        return self._replace(start=self.start+steps)

class StringToTerminalText(TerminalText):

    """
    I project a String to a TerminalText.

    I project keyboard events back to the String.

    >>> terminal_text = StringToTerminalText(String("hello", [StringSelection(1, 3)]))
    >>> print("\\n".join(repr(x) for x in terminal_text.strings))
    TerminalTextFragment(x=0, y=0, text='h', bold=None, bg=None, fg=None)
    TerminalTextFragment(x=1, y=0, text='ell', bold=None, bg='YELLOW', fg=None)
    TerminalTextFragment(x=4, y=0, text='o', bold=None, bg=None, fg=None)
    """

    def __init__(self, string):
        self.string = string
        string = self.string.string
        start = self.string.selections[0].start
        length = self.string.selections[0].length
        TerminalText.__init__(self,
            strings=[
                TerminalTextFragment(
                    text=string[:start],
                    y=0,
                    x=0
                ),
                TerminalTextFragment(
                    text=string[start:start+length],
                    y=0,
                    x=start,
                    bg="YELLOW"
                ),
                TerminalTextFragment(
                    text=string[start+length:],
                    y=0,
                    x=start+length
                ),
            ],
            cursors=[
                TerminalCursor(x=selection.start, y=0)
                for selection
                in self.string.selections
            ]
        )

    def keyboard_event(self, event):
        if event.unicode_character == "\x06": # Ctrl-F
            return StringToTerminalText(
                self.string.move_cursor_forward()
            )
        elif event.unicode_character == "\x02": # Ctrl-B
            return StringToTerminalText(
                self.string.move_cursor_back()
            )
        elif event.unicode_character == "\x0e": # Ctrl-N
            return StringToTerminalText(
                self.string.select_next_word()
            )
        elif event.unicode_character and ord(event.unicode_character) >= 32:
            return StringToTerminalText(
                self.string.replace(event.unicode_character)
            )
        else:
            return self

class Editor(TerminalText):

    def __init__(self, terminal_text, unicode_character=None):
        self.terminal_text = terminal_text
        TerminalText.__init__(self,
            strings=[
                TerminalTextFragment(
                    text=f"STATUS: {repr(unicode_character)}",
                    x=0,
                    y=0,
                    bg="MAGENTA",
                    fg="WHITE"
                )
            ]+[x.move(dy=1) for x in self.terminal_text.strings],
            cursors=[x.move(dy=1) for x in self.terminal_text.cursors]
        )

    def keyboard_event(self, event):
        return Editor(
            terminal_text=self.terminal_text.keyboard_event(event),
            unicode_character=event.unicode_character
        )

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv[1:]:
        import doctest
        if doctest.testmod().failed > 0:
            sys.exit(1)
        print("ok")
    else:
        app = wx.App()
        main_frame = wx.Frame(None)
        Canvas(
            main_frame,
            Editor(
                StringToTerminalText(
                    String("hello world, hello world!", [StringSelection(0, 0)])
                )
            )
        )
        main_frame.Show()
        app.MainLoop()
