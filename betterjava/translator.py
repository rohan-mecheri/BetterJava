"""
translator.py - Translates BetterJava (.bjava) syntax into standard Java (.java) syntax.
"""

def translate_to_java(bjava_code: str) -> str:
    """
    Converts BetterJava code (indentation-based) to Java code (bracket-based).
    """
    lines = bjava_code.splitlines()
    java_code = []
    indent_stack = []

    for line in lines:
        stripped = line.strip()

        # empty lines
        if not stripped:
            java_code.append("")
            continue

        # if line ends with a colon, it's a block start
        if stripped.endswith(":"):
            java_code.append(stripped[:-1] + " {")
            indent_stack.append(len(line) - len(stripped))
        else:
            # close blocks if indentation decreases
            while indent_stack and (len(line) - len(stripped)) < indent_stack[-1]:
                java_code.append(" " * indent_stack.pop() + "}")
            java_code.append(line)

    # close remaining blocks
    while indent_stack:
        java_code.append(" " * indent_stack.pop() + "}")

    return "\n".join(java_code)