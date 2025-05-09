from file_reader import FileObject
from typing import List
import re
from .tokenGenerator import token_gen
from .Lexical_Components.Token import Token
from .Lexical_Components.TokenType import TokenType

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
            listOfTokens.append(token_gen(word, lineNo, colNo))
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
