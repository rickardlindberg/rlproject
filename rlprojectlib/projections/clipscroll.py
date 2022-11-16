from collections import namedtuple

from rlprojectlib.domains.generic import SuperTuple
from rlprojectlib.domains.terminaltext import TerminalText
from rlprojectlib.domains.terminaltext import TerminalTextFragment
from rlprojectlib.domains.terminaltext import TerminalTextFragmentsBuilder
from rlprojectlib.domains.terminaltext import TerminalTextProjection

class ClipScroll(
    namedtuple("ClipScroll", "projection terminal_text width height"),
    TerminalTextProjection
):

    @staticmethod
    def project(terminal_text, width=0, height=0):
        """
        """
        return ClipScroll(
            projection=terminal_text.clip(width, height),
            terminal_text=terminal_text,
            width=width,
            height=height
        )

    def keyboard_event(self, event):
        return ClipScroll.project(
            terminal_text=self.terminal_text.keyboard_event(event),
            width=self.width,
            height=self.height
        )

    def size_event(self, event):
        return ClipScroll.project(
            terminal_text=self.terminal_text.size_event(event),
            width=event.width,
            height=event.height
        )
