from collections import namedtuple

from rlprojectlib.domains.string import String
from rlprojectlib.domains.terminal import Cursor
from rlprojectlib.domains.terminal import KeyboardEvent
from rlprojectlib.domains.terminal import MeasurementEvent
from rlprojectlib.domains.terminal import SizeEvent
from rlprojectlib.domains.terminal import Terminal
from rlprojectlib.domains.terminal import TextFragment
from rlprojectlib.drivers.wxterminal import DocumentProjectionDriver
from rlprojectlib.projections.lines_to_terminal import LinesToTerminal
from rlprojectlib.projections.string_to_lines import StringToLines
from rlprojectlib.projections.string_to_terminal import StringToTerminal
from rlprojectlib.projections.terminal.clipscroll import ClipScroll
from rlprojectlib.projections.terminal.split import Options
from rlprojectlib.projections.terminal.split import VSplit

class ProjectionState(
    namedtuple("ProjectionState", "terminal popup_terminal document")
):
    pass

class EditorState(
    namedtuple("EditorState", "width height popup event measurement_event")
):
    pass

class Editor(Terminal):

    """
    I can edit an example document without crashing:

    Some basic assumptions about types:

    >>> driver = Editor.create_driver("rlproject.py")

    >>> isinstance(driver.document, String)
    True

    >>> isinstance(driver.document.meta, EditorState)
    True

    >>> isinstance(driver.terminal, Terminal)
    True

    A size event changes the editor state:

    >>> _ = driver.size_event(SizeEvent(20, 10))
    >>> driver.document.meta.width
    20
    >>> driver.document.meta.height
    10

    A Ctrl-G opens the popup:

    >>> driver.document.meta.popup is None
    True

    >>> _ = driver.keyboard_event(KeyboardEvent(unicode_character="\x07"))
    >>> driver.document.meta.popup
    String(meta=None, string='', selections=Selections(Selection(start=0, length=0)))

    >>> _ = driver.keyboard_event(KeyboardEvent(unicode_character="\x07"))
    >>> driver.document.meta.popup is None
    True

    >>> _ = driver.keyboard_event(KeyboardEvent(unicode_character="k"))
    >>> driver.document.string[driver.document.selections[-1].start-1]
    'k'
    """

    @staticmethod
    def create_driver(path):
        return DocumentProjectionDriver(
            String.from_file(path).replace_meta(EditorState(
                width=10,
                height=10,
                popup=None,
                event=None,
                measurement_event=MeasurementEvent(0, 0)
            )),
            Editor.project
        )

    @staticmethod
    def project(document):
        """
        >>> document = String.from_string("hello").replace_meta(EditorState(
        ...     width=10,
        ...     height=10,
        ...     popup=None,
        ...     event=None,
        ...     measurement_event=MeasurementEvent(0, 0)
        ... ))
        >>> Editor.project(document).print_fragments_and_cursors()
        TextFragment(x=0, y=1, text='1', bold=None, bg=None, fg='YELLOW')
        TextFragment(x=2, y=1, text='hello', bold=None, bg=None, fg=None)
        TextFragment(x=0, y=5, text='----------', bold=None, bg='FOREGROUND', fg='BACKGROUND')
        TextFragment(x=0, y=6, text='hello', bold=None, bg=None, fg=None)
        TextFragment(x=0, y=0, text='None 0ms 0ms', bold=None, bg='MAGENTA', fg='WHITE')
        Cursor(x=2, y=1)
        """
        if document.meta.popup:
            popup_terminal = StringToTerminal.project(
                document.meta.popup,
                x=0,
                y=0
            )
        else:
            popup_terminal = None
        split = VSplit.project(
            [
                Options(
                    LinesToTerminal.project(
                        StringToLines.project(
                            document
                        )
                    ),
                    1,
                    True
                ),
                Options(
                    Terminal.create(
                        fragments=[TextFragment(
                            x=0,
                            y=0,
                            bg="FOREGROUND",
                            fg="BACKGROUND",
                            text="-"*document.meta.width
                        )]
                    ),
                    0,
                    False
                ),
                Options(
                    StringToTerminal.project(
                        document,
                        x=0,
                        y=0
                    ),
                    1,
                    False
                ),
            ],
            height=document.meta.height,
            width=document.meta.width
        )
        terminal = split
        status_fragment = TextFragment(
            text=f"{document.meta.event} {document.meta.measurement_event.ms_project}ms {document.meta.measurement_event.ms_repaint}ms".ljust(document.meta.width),
            x=0,
            y=0,
            bg="MAGENTA",
            fg="WHITE"
        )
        if popup_terminal:
            projection = terminal.clear_cursors(
            ).translate(
                dy=2
            ).add_fragment(
                status_fragment
            ).add_fragment(TextFragment(
                text=f"Filter:".ljust(document.meta.width),
                x=0,
                y=1,
                bg="GREEN",
                fg="WHITE",
                bold=True
            )).merge(popup_terminal.style(bg="GREEN", fg="WHITE").translate(dy=1, dx=8))
        else:
            projection = terminal.translate(
                dy=1
            ).add_fragment(
                status_fragment
            )
        return Editor(
            *projection.replace_meta(ProjectionState(
                terminal=terminal,
                popup_terminal=popup_terminal,
                document=document
            ))
        )

    def size_event(self, event):
        return self.document.with_meta(
            width=event.width,
            height=event.height,
            event=event
        )

    def keyboard_event(self, event):
        if event.unicode_character == "\x07": # Ctrl-G
            if self.editor_state.popup:
                return self.document.with_meta(
                    popup=None,
                    event=event
                )
            else:
                return self.document.with_meta(
                    popup=String.from_string(''),
                    event=event
                )
        elif self.editor_state.popup:
            return self.document.with_meta(
                popup=self.projection_state.popup_terminal.keyboard_event(event),
                event=event
            )
        else:
            return self.projection_state.terminal.keyboard_event(event).with_meta(
                event=event
            )

    def measurement_event(self, event):
        return self.document.with_meta(
            measurement_event=event
        )

    @property
    def editor_state(self):
        return self.document.meta

    @property
    def document(self):
        return self.projection_state.document

    @property
    def projection_state(self):
        return self.meta
