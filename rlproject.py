#!/usr/bin/env python3

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
                if "__pycache__" in dirs:
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
        import os
        path = "rlproject.py"
        for arg in sys.argv[1:]:
            if os.path.exists(arg):
                path = arg
        from rlprojectlib.drivers.wxterminal import WxTerminalDriver
        from rlprojectlib.projections.terminal.editor import Editor
        WxTerminalDriver.run(Editor.create_driver(path))
