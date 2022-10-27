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
        self.cursor_timer = wx.Timer(self)
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
        if self.show_cursor:
            r, g, b = self.THEME["colors"]["FOREGROUND"]
            dc.SetPen(wx.Pen((r, g, b), 1))
            dc.SetBrush(wx.Brush((r, g, b, 150)))
            dc.DrawRectangle(self.cursor_rect)

    def on_timer(self, event):
        self.show_cursor = not self.show_cursor
        self.force_repaint_window()

    def on_set_focus(self, event):
        self.reset_cursor()
        self.force_repaint_window()

    def on_kill_focus(self, event):
        self.cursor_timer.Stop()
        self.show_cursor = True
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
        for string in self.document.get_strings():
            if string.bold:
                memdc.SetFont(font_bold)
            else:
                memdc.SetFont(font)
            memdc.SetTextBackground(self.THEME["colors"].get(string.bg, self.THEME["colors"]["BACKGROUND"]))
            memdc.SetTextForeground(self.THEME["colors"].get(string.fg, self.THEME["colors"]["FOREGROUND"]))
            memdc.DrawText(string.text, string.x*char_width, string.y*char_height)
        del memdc
        x, y = self.document.get_cursor()
        self.cursor_rect = wx.Rect(x*char_width, y*char_height, char_width, char_height)
        self.reset_cursor()
        self.force_repaint_window()

    def reset_cursor(self):
        self.show_cursor = True
        self.cursor_timer.Start(500)

    def force_repaint_window(self):
        self.Refresh()
        self.Update()

class TerminalText:

    """
    In the styled text terminal domain

    * a document is a list if styled text at a given (x, y)
    * a cursor position is a position (x, y)
    * keyboard events are accepted as input
    """

    def __init__(self, cursor_position, strings):
        self.cursor_position = cursor_position
        self.strings = strings

    def get_cursor(self):
        return self.cursor_position

    def get_strings(self):
        return self.strings

class TerminalTextFragment(namedtuple(
    "TerminalTextFragment",
    ["x", "y", "text", "bold", "bg", "fg"],
    defaults=[None, None, None]
)):

    def move(self, dy=0):
        return self._replace(y=self.y+dy)

class KeyboardEvent:

    def __init__(self, unicode_character):
        self.unicode_character = unicode_character

class String:

    """
    >>> String("hello", 0, 1).replace("1").string
    '1ello'
    """

    def __init__(self, string, selection_start, selection_length):
        self.string = string
        self.selection_start = selection_start
        self.selection_length = selection_length

    def replace(self, text):
        return String(
            string="".join([
                self.string[:self.selection_start],
                text,
                self.string[self.selection_start+self.selection_length:],
            ]),
            selection_start=self.selection_start+1,
            selection_length=0
        )

class StringToTerminalText(TerminalText):

    """
    I project a String to a TerminalText.

    I project keyboard events back to the String.

    >>> terminal_text = StringToTerminalText(String("hello", 1, 3))
    >>> print("\\n".join(repr(x) for x in terminal_text.get_strings()))
    TerminalTextFragment(x=0, y=0, text='h', bold=None, bg=None, fg=None)
    TerminalTextFragment(x=1, y=0, text='ell', bold=None, bg='YELLOW', fg=None)
    TerminalTextFragment(x=4, y=0, text='o', bold=None, bg=None, fg=None)
    """

    def __init__(self, string):
        self.string = string
        string = self.string.string
        start = self.string.selection_start
        length = self.string.selection_length
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
            cursor_position=(start, 0)
        )

    def keyboard_event(self, event):
        if event.unicode_character:
            return StringToTerminalText(
                self.string.replace(event.unicode_character)
            )
        else:
            return self

class Editor(TerminalText):

    def __init__(self, terminal_text, unicode_character=None):
        self.terminal_text = terminal_text
        (x, y) = self.terminal_text.get_cursor()
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
            cursor_position=(x, y+1)
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
                    String("hello world", 2, 2)
                )
            )
        )
        main_frame.Show()
        app.MainLoop()
