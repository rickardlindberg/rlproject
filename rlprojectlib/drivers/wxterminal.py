import time

import wx

from rlprojectlib.domains.terminal import KeyboardEvent
from rlprojectlib.domains.terminal import MeasurementEvent
from rlprojectlib.domains.terminal import SizeEvent

class WxTerminalDriver(wx.Panel):

    @staticmethod
    def run(driver):
        app = wx.App()
        main_frame = wx.Frame(None)
        WxTerminalDriver(main_frame, driver)
        main_frame.Show()
        app.MainLoop()

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

    def __init__(self, parent, driver):
        wx.Panel.__init__(self, parent, style=wx.NO_BORDER|wx.WANTS_CHARS)
        self.driver = driver
        self.terminal = driver.terminal
        self.cursor_blink_timer = wx.Timer(self)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.Bind(wx.EVT_SET_FOCUS, self.on_set_focus)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)
        self.setup_font()
        self.repaint_bitmap()

    def on_size(self, evt):
        def project():
            self.terminal = self.driver.size_event(SizeEvent(
                width=evt.Size.Width // self.char_width,
                height=evt.Size.Height // self.char_height
            ))
        self._measure(project)

    def on_char(self, evt):
        def project():
            self.terminal = self.driver.keyboard_event(KeyboardEvent(
                unicode_character=chr(evt.GetUnicodeKey())
            ))
        self._measure(project)

    def _measure(self, fn):
        _, ms_project = measure_ms(fn)
        _, ms_repaint = measure_ms(self.repaint_bitmap)
        self.terminal = self.driver.measurement_event(MeasurementEvent(
            ms_project=ms_project,
            ms_repaint=ms_repaint,
        ))
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

    def setup_font(self):
        self.font = wx.Font(
            self.THEME["font_size"],
            wx.FONTFAMILY_TELETYPE,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL
        )
        self.font_bold = self.font.Bold()
        self.bitmap = wx.Bitmap(10, 10)
        memdc = wx.MemoryDC()
        memdc.SelectObject(self.bitmap)
        memdc.SetFont(self.font)
        self.char_width, self.char_height = memdc.GetTextExtent(".")
        del memdc

    def repaint_bitmap(self):
        self.bitmap = wx.Bitmap(self.GetSize())
        memdc = wx.MemoryDC()
        memdc.SelectObject(self.bitmap)
        memdc.SetBackground(wx.Brush(self.THEME["colors"]["BACKGROUND"], wx.SOLID))
        memdc.SetBackgroundMode(wx.PENSTYLE_SOLID)
        memdc.Clear()
        for fragment in self.terminal.fragments:
            if fragment.bold:
                memdc.SetFont(self.font_bold)
            else:
                memdc.SetFont(self.font)
            memdc.SetTextBackground(self.THEME["colors"].get(fragment.bg, self.THEME["colors"]["BACKGROUND"]))
            memdc.SetTextForeground(self.THEME["colors"].get(fragment.fg, self.THEME["colors"]["FOREGROUND"]))
            memdc.DrawText(fragment.text, fragment.x*self.char_width, fragment.y*self.char_height)
        del memdc
        self.cursor_rects = []
        for cursor in self.terminal.cursors:
            self.cursor_rects.append(wx.Rect(
                cursor.x*self.char_width-1,
                cursor.y*self.char_height,
                3,
                self.char_height
            ))
        self.reset_cursor_blink()
        self.force_repaint_window()

    def reset_cursor_blink(self):
        self.show_cursors = True
        self.cursor_blink_timer.Start(500)

    def force_repaint_window(self):
        self.Refresh()
        self.Update()

class DocumentProjectionDriver:

    def __init__(self, document, projection_fn):
        self.document = document
        self.projection_fn = projection_fn
        self._project()

    def size_event(self, event):
        self.document = self.terminal.size_event(event)
        return self._project()

    def keyboard_event(self, event):
        self.document = self.terminal.keyboard_event(event)
        return self._project()

    def measurement_event(self, event):
        self.document = self.terminal.measurement_event(event)
        return self._project()

    def _project(self):
        self.terminal = self.projection_fn(self.document)
        return self.terminal

def measure_ms(fn):
    t1 = time.perf_counter()
    return_value = fn()
    t2 = time.perf_counter()
    return (return_value, int((t2-t1)*1000))
