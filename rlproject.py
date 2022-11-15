#!/usr/bin/env python3

def example_document():
    """
    I can create an example document without crashing:

    >>> _ = example_document()
    """
    from rlprojectlib.projections.editor import Editor
    from rlprojectlib.projections.split import Split
    from rlprojectlib.projections.lines_to_terminal_text import LinesToTerminalText
    from rlprojectlib.projections.string_to_lines import StringToLines
    from rlprojectlib.projections.string_to_terminal_text import StringToTerminalText
    from rlprojectlib.domains.string import String
    return Editor.project(
        Split.project([
            LinesToTerminalText.project(
                StringToLines.project(
                    String.from_file("rlproject.py")
                )
            ),
            StringToTerminalText.project(
                String.from_file("rlproject.py")
            ),
        ])
    )

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv[1:]:
        import doctest
        import unittest
        import importlib
        suite = unittest.TestSuite()
        for module in [
            "rlproject",
            "rlprojectlib",
            "rlprojectlib.drivers",
            "rlprojectlib.drivers.wxterminaltext",
            "rlprojectlib.domains",
            "rlprojectlib.domains.generic",
            "rlprojectlib.domains.lines",
            "rlprojectlib.domains.string",
            "rlprojectlib.domains.terminaltext",
            "rlprojectlib.projections",
            "rlprojectlib.projections.editor",
            "rlprojectlib.projections.split",
            "rlprojectlib.projections.lines_to_terminal_text",
            "rlprojectlib.projections.string_to_lines",
            "rlprojectlib.projections.string_to_terminal_text",
        ]:
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
