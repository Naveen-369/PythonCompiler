import re
from typing import List
from enum import Enum
from file_reader import FileObject
import keyword

# CONSTANTS:
# Keywords
CONDITIONALS = {c: "CONDITIONAL" for c in ["if", "elif", "else"]}
# Operators
OPERATORS = {op: "OPERATOR" for op in ["+", "-", "*", "/", "=", "**", "//", "%"]}
# Relational Operators
RELOP = {relop: "RELOP" for relop in ['==', '!=', '<', '<=', '>', '>=']}
# Loops
LOOPS = {loop: "LOOP" for loop in ['for', 'while']}


class TokenType(Enum):
    CONDITIONAL = "CONDITIONAL"
    OPERATOR = "OPERATOR"
    INDENTATION = "INDENTATION"
    RELOP = "RELOP"
    LOOP = "LOOP"
    IDENTIFIER = "IDENTIFIER"
    CONSTANT = "CONSTANT"
    FUNCTION = "FUNCTION"
    SYMBOL = "SYMBOL"
    SEMICOLON = "SEMICOLON"
    BLOCK_BEGIN = "BLOCK BEGIN"
    BLOCK_END = "BLOCK END"
    NEWLINE = "NEWLINE"
    EOF = "EOF"


class Token:
    """
    the token class classifies the words in the program into tokens like identifier, constants, etc
    and stores a value of it.
    """

    def __init__(self, tokenType: TokenType, atr: str = None, lineNo: int = None, colNo: int = None) -> None:
        self.tokenType = tokenType
        self.atr = atr
        self.lineNo = lineNo
        self.colNo = colNo

    def __repr__(self, indent=0) -> str:
        return "\t"*indent + f"{self.tokenType.name}: {self.atr}"
        # return f"('{self.tokenType.name}', '{self.atr}', line={self.lineNo}, col={self.colNo})"


def make_token(tType: TokenType, value: str, line: int = None, col: int = None) -> Token:
    return Token(tType, value, line, col)


def token_giver(word: str, line: int = None, col: int = None) -> Token:
    """
    Takes a word from the code and returns a Token object with its type and attribute.
    :param word:
    :return Token:
    """
    # Keyword
    if word in CONDITIONALS:
        return make_token(TokenType.CONDITIONAL, word, line, col)

    # Loops
    if word in LOOPS:
        return Token(TokenType.LOOP, word, line, col)

    # Indentation
    elif not word:
        return make_token(TokenType.INDENTATION, '\\t', line, col)

    # Operator
    elif word in OPERATORS:
        return make_token(TokenType.OPERATOR, word, line, col)

    # Relational Operator
    elif word in RELOP:
        return make_token(TokenType.RELOP, word, line, col)

    # Semicolon
    elif word == ":":
        return make_token(TokenType.SEMICOLON, word, line, col)

    # def function
    elif word == "def":
        return make_token(TokenType.FUNCTION, word, line, col)

    # Identifier
    elif bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', word)) and not keyword.iskeyword(word):
        return make_token(TokenType.IDENTIFIER, word, line, col)

    # Constant (Update later to work for float and exponential numbers)
    elif word[0].isdigit():
        return make_token(TokenType.CONSTANT, word, line, col)

    # Default to symbol if none of the above match
    else:
        return make_token(TokenType.SYMBOL, word, line, col)


def lexical_analyzer(inp: FileObject) -> List[Token]:
    """
    maps the list of words in the file to a list of Tokens
    :param inp: content of the file in a list
    :return: list of tokens
    """
    listOfTokens = []
    indent_stack = [0]
    lineNo = 0
    colNo = 0
    for lineNo in range(len(inp)):
        colNo = 0
        line = inp.at(lineNo)
        indent_level = len(line) - len(line.lstrip())
        stripped_line = line.strip()

        # Skip empty lines
        if not stripped_line:
            continue

        # Handle indentation changes
        if indent_level > indent_stack[-1]:
            # Indentation increased - add BLOCK BEGIN
            indent_stack.append(indent_level)
            listOfTokens.append(Token(TokenType.BLOCK_BEGIN, "begin", lineNo))
        elif indent_level < indent_stack[-1]:
            # Indentation decreased - add BLOCK END tokens
            while indent_stack and indent_level < indent_stack[-1]:
                indent_stack.pop()
                listOfTokens.append(Token(TokenType.BLOCK_END, "end", lineNo - 1))

            if indent_level != indent_stack[-1]:
                raise IndentationError(f"unexpected indent at Line {lineNo}, {line.strip()}\n ")
        # Process the actual line content
        for word in re.split(r'\s+', stripped_line):
            listOfTokens.append(token_giver(word, lineNo, colNo))
            colNo += 1
        listOfTokens.append(Token(TokenType.NEWLINE, "\\n", lineNo, colNo))
        colNo += 1

    # Add remaining BLOCK END tokens at EOF
    while len(indent_stack) > 1:
        indent_stack.pop()
        listOfTokens.append(Token(TokenType.BLOCK_END, "end", lineNo, colNo))
        colNo += 1

    listOfTokens.append(Token(TokenType.EOF, '$', lineNo + 1))
    return listOfTokens
