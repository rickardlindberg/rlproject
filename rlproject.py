#!/usr/bin/env python3

def example_document(path="rlproject.py"):
    """
    I can create an example document without crashing:

    >>> from rlprojectlib.domains.terminaltext import SizeEvent
    >>> from rlprojectlib.domains.terminaltext import KeyboardEvent
    >>> terminal_text = example_document()
    >>> _ = terminal_text.size_event(SizeEvent(10, 10))
    >>> _ = terminal_text.keyboard_event(KeyboardEvent('a'))
    """
    from rlprojectlib.domains.string import String
    from rlprojectlib.projections.clipscroll import ClipScroll
    from rlprojectlib.projections.editor import Editor
    from rlprojectlib.projections.lines_to_terminal_text import LinesToTerminalText
    from rlprojectlib.projections.split import Split
    from rlprojectlib.projections.string_to_lines import StringToLines
    from rlprojectlib.projections.string_to_terminal_text import StringToTerminalText
    return Editor.project(
        Split.project([
            ClipScroll.project(
                LinesToTerminalText.project(
                    StringToLines.project(
                        String.from_file(path)
                    )
                ),
            ),
            ClipScroll.project(
                StringToTerminalText.project(
                    String.from_file(path)
                ),
            ),
        ])
    )

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv[1:]:
        import doctest
        import unittest
        import importlib
        import os
        def find_modules():
            yield "rlproject"
            for root, dirs, files in os.walk("rlprojectlib"):
                dirs.remove("__pycache__")
                if "__init__.py" in files:
                    files.remove("__init__.py")
                    yield root.replace("/", ".")
                    for file in files:
                        if file.endswith(".py"):
                            yield os.path.join(root, file).replace("/", ".")[:-3]
                else:
                    dirs.clear()
        suite = unittest.TestSuite()
        for module in find_modules():
            suite.addTest(doctest.DocTestSuite(
                importlib.import_module(module),
                optionflags=doctest.REPORT_NDIFF|doctest.FAIL_FAST
            ))
        result = unittest.TextTestRunner().run(suite)
        if not result.wasSuccessful():
            sys.exit(1)
    else:
        from rlprojectlib.drivers.wxterminaltext import WxTerminalTextDriver
        WxTerminalTextDriver.run(example_document())
