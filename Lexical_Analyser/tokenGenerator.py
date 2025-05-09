from Components.Constants import *
from Lexical_Components.TokenType import TokenType
from Lexical_Components.Token import Token
import re,keyword



def token_gen(word: str, line: int = None, col: int = None) -> Token:
    """This methods determines the type of the token with respect to the work given to it in form of string. 

    Args:
        word (str): The parsed set of words
        line (int, optional): The horizontal posistion of the word. Defaults to None.
        col (int, optional): The vertical posistion of the word. Defaults to None.

    Returns:
        Token: Set containing the tokenType, tokenValue and pair of Token Position
    """
    
    # Keyword
    if word in CONDITIONALS:
        return Token(TokenType.CONDITIONAL, word, line, col)

    # Loops
    if word in LOOPS:
        return Token(TokenType.LOOP, word, line, col)

    # Indentation
    elif not word:
        return Token(TokenType.INDENTATION, '\\t', line, col)

    # Operator
    elif word in OPERATORS:
        return Token(TokenType.OPERATOR, word, line, col)

    # Relational Operator
    elif word in RELOP:
        return Token(TokenType.RELOP, word, line, col)

    # Semicolon
    elif word == ":":
        return Token(TokenType.SEMICOLON, word, line, col)

    # def function
    elif word == "def":
        return Token(TokenType.FUNCTION, word, line, col)

    # Identifier
    elif bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', word)) and not keyword.iskeyword(word):
        return Token(TokenType.IDENTIFIER, word, line, col)

    # Constant (Update later to work for float and exponential numbers)
    elif word[0].isdigit():
        return Token(TokenType.CONSTANT, word, line, col)

    # Default to symbol if none of the above match
    else:
        return Token(TokenType.SYMBOL, word, line, col)
