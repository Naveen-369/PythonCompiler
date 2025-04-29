import sys
from enum import Enum
from typing import List, Union
from file_reader import *
from lexical_analyzer import *
from Parser import *
'''
classes camelCase
Variable camelCase
functions snake_case
constants UPPERCASE
'''

"""
TODO:
 refactor lexer using FileObject class
 Implement String literals? Comments? Floats?
 Implement Decimals and exponents for CONSTANTS
FUTURE:
 make the CFG automatic by using text file
 implement lalr parser instead of backtracking
"""

def main():
    # Reading the program

    file = file_reader(sys.argv[1])
    # print(file.lines)
    # print(lexical_analyzer(FileObject(["a = 5"])))

    # Token Parsing
    tokens = lexical_analyzer(file)
    # for t in tokens:
    #     print(t)
    # print("[" + ", ".join(f"TokenType.{tt.tokenType.name}" for tt in tokens) + "]")
    # print([t.atr for t in tokens])

    # NOW MAP OUT A GRAMMER THAT THIS PROGRAMMING LANGUAGE FOLLOWS
    # AFTER THAT CODE THE LALR PARSER BUT BEFORE THAT YOU NEED FIRST AND FOLLOW COMPUTE TO USE

    parser = Parser(tokens)
    print(parser.tree)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        sys.exit(1)
    main()