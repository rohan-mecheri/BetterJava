"""
translator.py - Translates BetterJava (.bjava) syntax into standard Java (.java) syntax.
"""

from betterjava.logger import setup_logger
from betterjava.exceptions import BetterJavaTranslationError

logger = setup_logger("translator", "translator.log")

def translate_to_java(bjava_code: str) -> str:

    logger.info("Starting translation of BetterJava code.")
    try:
        lines = bjava_code.splitlines()
        java_code = []
        indent_stack = []

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()

            if not stripped:
                java_code.append("")
                logger.debug(f"Line {line_num}: Skipping empty line.")
                continue

            # if line ends with a colon, it's a block start
            if stripped.endswith(":"):
                java_code.append(stripped[:-1] + " {")
                indent_stack.append(len(line) - len(stripped))
                logger.debug(f"Line {line_num}: Block started.")
            else:
                # close blocks if indentation decreases
                while indent_stack and (len(line) - len(stripped)) < indent_stack[-1]:
                    java_code.append(" " * indent_stack.pop() + "}")
                    logger.debug(f"Line {line_num}: Block closed.")
                java_code.append(line)

        # close remaining blocks
        while indent_stack:
            java_code.append(" " * indent_stack.pop() + "}")
            logger.debug("Closing remaining block.")

        logger.info("Translation completed successfully.")
        return "\n".join(java_code)

    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise BetterJavaTranslationError(f"Unexpected error during translation: {e}")