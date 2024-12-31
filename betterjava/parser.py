"""
parser.py - Validates BetterJava (.bjava) syntax for correctness.
"""

from betterjava.logger import setup_logger
from betterjava.exceptions import BetterJavaSyntaxError

logger = setup_logger("parser", "parser.log")


def parse_bjava(bjava_code: str) -> None:

    logger.info("Starting syntax validation.")
    lines = bjava_code.splitlines()
    indent_stack = []

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped:
            logger.debug(f"Line {line_num}: Skipping empty line.")
            continue

        current_indent = len(line) - len(stripped)
        if indent_stack and current_indent > indent_stack[-1] + 4:
            logger.error(f"Line {line_num}: Unexpected indentation level.")
            raise BetterJavaSyntaxError("Unexpected indentation level.", line_num)

        # if line ends with colon, it's a block starter
        if stripped.endswith(":"):
            if not stripped[:-1].strip():
                logger.error(f"Line {line_num}: Missing block definition before ':'.")
                raise BetterJavaSyntaxError("Missing block definition before ':'.", line_num)
            indent_stack.append(current_indent)
            logger.debug(f"Line {line_num}: Block started.")

        # close blocks when indentation decreases
        while indent_stack and current_indent < indent_stack[-1]:
            logger.debug(f"Line {line_num}: Closing block at indent level {indent_stack[-1]}.")
            indent_stack.pop()

        # check for valid syntax 
        if not stripped.endswith(":") and "{" in stripped:
            logger.error(f"Line {line_num}: Unexpected '{{' in BetterJava code.")
            raise BetterJavaSyntaxError("Unexpected '{' in BetterJava code.", line_num)

    # ensure all indentation levels are closed
    if indent_stack:
        logger.error("Unclosed blocks detected at the end of the file.")
        raise BetterJavaSyntaxError("Unclosed blocks detected.")

    logger.info("Syntax validation completed successfully.")
    return None