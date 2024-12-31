"""
exceptions.py - Custom exceptions for BetterJava.
"""

class BetterJavaError(Exception):
    pass


class BetterJavaSyntaxError(BetterJavaError):
    def __init__(self, message: str, line: int = None):
        if line is not None:
            message = f"Line {line}: {message}"
        super().__init__(message)


class BetterJavaTranslationError(BetterJavaError):
    def __init__(self, message: str):
        super().__init__(f"Translation Error: {message}")