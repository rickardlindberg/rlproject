import wx

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

    def __init__(self, parent, domain):
        wx.Panel.__init__(self, parent, style=wx.NO_BORDER|wx.WANTS_CHARS)
        self.domain = domain
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
        new_domain = self.domain.keyboard_event(KeyboardEvent(
            unicode_character=chr(evt.GetUnicodeKey())
        ))
        if new_domain is not self.domain:
            self.domain = new_domain
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
        for string in self.domain.get_strings():
            if string.bold:
                memdc.SetFont(font_bold)
            else:
                memdc.SetFont(font)
            memdc.SetTextBackground(self.THEME["colors"].get(string.bg, self.THEME["colors"]["BACKGROUND"]))
            memdc.SetTextForeground(self.THEME["colors"].get(string.fg, self.THEME["colors"]["FOREGROUND"]))
            memdc.DrawText(string.text, string.x*char_width, string.y*char_height)
        del memdc
        x, y = self.domain.get_cursor()
        self.cursor_rect = wx.Rect(x*char_width, y*char_height, char_width, char_height)
        self.reset_cursor()
        self.force_repaint_window()

    def reset_cursor(self):
        self.show_cursor = True
        self.cursor_timer.Start(500)

    def force_repaint_window(self):
        self.Refresh()
        self.Update()

class StyledTextTerminalDomain:

    """
    In the styled text terminal domain

    * a document is a list if styled text at a given (x, y)
    * a cursor position is a position (x, y)
    * keyboard events are accepted as input
    """

    def __init__(self, cursor_position=(4, 3)):
        self.cursor_position = cursor_position

    def get_cursor(self):
        return self.cursor_position

    def get_strings(self):
        return [
            StyledTerminalText(0, 0, "hello"),
            StyledTerminalText(4, 1, "world!", bold=True),
            StyledTerminalText(3, 3, "styled 1", fg="GREEN"),
            StyledTerminalText(5, 4, "styled 2", bg="GREEN", fg="WHITE"),
        ]

    def keyboard_event(self, event):
        x, y = self.cursor_position
        if event.unicode_character == "j":
            return StyledTextTerminalDomain((x, y+1))
        elif event.unicode_character == "k":
            return StyledTextTerminalDomain((x, y-1))
        elif event.unicode_character == "h":
            return StyledTextTerminalDomain((x-1, y))
        elif event.unicode_character == "l":
            return StyledTextTerminalDomain((x+1, y))
        else:
            return self

class StyledTerminalText:

    def __init__(self, x, y, text, bold=False, bg=None, fg=None):
        self.x = x
        self.y = y
        self.text = text
        self.bold = bold
        self.bg = bg
        self.fg = fg

class KeyboardEvent:

    def __init__(self, unicode_character):
        self.unicode_character = unicode_character

if __name__ == "__main__":
    app = wx.App()
    main_frame = wx.Frame(None)
    Canvas(main_frame, StyledTextTerminalDomain())
    main_frame.Show()
    app.MainLoop()
