from betterjava.logger import setup_logger
from betterjava.exceptions import BetterJavaSyntaxError

logger = setup_logger("parser", "parser.log")

def parse_bjava(bjava_code: str) -> None:
    logger.info("Starting syntax validation.")
    lines = bjava_code.splitlines()
    indent_stack = []

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        logger.debug(f"Processing line {line_num}: '{line}' (stripped: '{stripped}')")

        if not stripped:
            logger.debug(f"Line {line_num}: Skipping empty line.")
            continue

        current_indent = len(line) - len(stripped)
        logger.debug(f"Indentation level: {current_indent} | Current stack: {indent_stack}")

        # Handle unexpected large indentation
        if indent_stack and current_indent > indent_stack[-1] + 4:
            logger.error(f"Line {line_num}: Unexpected indentation level.")
            raise BetterJavaSyntaxError("Unexpected indentation level.", line_num)

        # Handle block starters (lines ending with a colon)
        if stripped.endswith(":"):
            if not stripped[:-1].strip():  # Check if there's content before the colon
                logger.error(f"Line {line_num}: Missing block definition before ':'.")
                raise BetterJavaSyntaxError("Missing block definition before ':'.", line_num)
            indent_stack.append(current_indent)
            logger.debug(f"Line {line_num}: Block started. Updated stack: {indent_stack}")

        # Handle inline code (matches current block indentation)
        elif indent_stack and current_indent == indent_stack[-1]:
            logger.debug(f"Line {line_num}: Valid inline code.")

        # Handle closing blocks (indentation decreases)
        elif indent_stack and current_indent < indent_stack[-1]:
            while indent_stack and current_indent < indent_stack[-1]:
                logger.debug(f"Line {line_num}: Closing block at indent level {indent_stack[-1]}.")
                indent_stack.pop()

            if current_indent == (indent_stack[-1] if indent_stack else 0):
                logger.debug(f"Line {line_num}: Valid inline code after block closure.")
            else:
                logger.error(f"Line {line_num}: Misaligned indentation.")
                raise BetterJavaSyntaxError("Misaligned indentation.", line_num)

        # Handle invalid indentation within blocks
        elif indent_stack and current_indent > indent_stack[-1]:
            logger.error(f"Line {line_num}: Missing ':' at the end of block-starting line.")
            raise BetterJavaSyntaxError("Missing ':' at the end of block-starting line.", line_num)

        # Handle unexpected characters or structure
        elif "{" in stripped or "}" in stripped:
            logger.error(f"Line {line_num}: Unexpected '{{' or '}}' in BetterJava code.")
            raise BetterJavaSyntaxError("Unexpected '{' or '}' in BetterJava code.", line_num)

    # Ensure all blocks are properly closed
    if indent_stack:
        logger.error("Unclosed blocks detected at the end of the file.")
        raise BetterJavaSyntaxError("Unclosed blocks detected.")

    logger.info("Syntax validation completed successfully.")
