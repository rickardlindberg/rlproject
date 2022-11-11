from collections import namedtuple

from rlprojectlib.domains.terminaltext import TerminalText, TerminalTextProjection, TerminalTextFragment

class Editor(
    namedtuple("Editor", "projection terminal_text"),
    TerminalTextProjection
):

    @staticmethod
    def project(terminal_text, unicode_character=None):
        return Editor(
            projection=TerminalText(
                fragments=[
                    TerminalTextFragment(
                        text=f"STATUS: {repr(unicode_character)}",
                        x=0,
                        y=0,
                        bg="MAGENTA",
                        fg="WHITE"
                    )
                ]+[x.move(dy=1) for x in terminal_text.fragments],
                cursors=[x.move(dy=1) for x in terminal_text.cursors]
            ),
            terminal_text=terminal_text,
        )

    def keyboard_event(self, event):
        return Editor.project(
            terminal_text=self.terminal_text.keyboard_event(event),
            unicode_character=event.unicode_character
        )
