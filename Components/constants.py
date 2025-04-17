"""
This module defines essential constants used in the PythonCompiler project.

Attributes:
    CONDITIONALS (dict): Mapping of conditional keywords (e.g., "if", "else", "then") to their token type "CONDITIONAL".
    OPERATORS (dict): Mapping of arithmetic and assignment operators (e.g., "+", "-", "*", "/", "=") to their token type "OPERATOR".
    RELOP (dict): Mapping of relational operators (e.g., "==", "!=", "<", "<=", ">", ">=") to their token type "RELOP".
    LOOPS (dict): Mapping of loop keywords (e.g., "for", "while") to their token type "LOOP".
"""
# Keywords
CONDITIONALS = {c: "CONDITIONAL" for c in ["if", "else", "then"]}
# Operators
OPERATORS = {op: "OPERATOR" for op in ["+", "-", "*", "/", "="]}
# Relational Operators
RELOP = {relop: "RELOP" for relop in ['==', '!=', '<', '<=', '>', '>=']}
# Loops
LOOPS = {loop: "LOOP" for loop in ['for', 'while']}
