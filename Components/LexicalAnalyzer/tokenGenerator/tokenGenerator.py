from ...constants import CONDITIONALS,RELOP,LOOPS,OPERATORS
from token import Token


def TokenGenerator(word:str)->Token:
    """Assigns types to the Tokens

    Args:
        word (str): A word from the set of words that are synthesised from the code 

    Returns:
        Token (Token): The word(Token) is mapped with its respective Token type
    """
    
    # Check if the word is empty or None
    if not word:
        return Token("INDENTATION", '\\t')
    
    # Check if the word is a conditional keyword
    elif word in CONDITIONALS:
        return Token("CONDITIONALS", word)
    
    # Check if the word is a loop keyword
    elif word in LOOPS:
        return Token("LOOPS", word)
    
    # Check if the word is an operator
    elif word in OPERATORS:
        return Token("OPERATORS", word)
    
    # Check if the word is a relational operator
    elif word in RELOP:
        return Token("RELOP", word)
    
    # Check if the word is a semicolon
    elif word == ";":
        return Token("SEMICOLON", word)
    
    # Check if the word is the function definition keyword
    elif word == "def":
        return Token("FUNCTION", word)
    
    # Check if the word starts with an alphabet or underscore (identifier)
    elif word[0].isalpha() or word[0] == "_":
        return Token("IDENTIFIER", word)
    
    # Check if the word starts with a digit (constant)
    elif word[0].isdigit():
        return Token("CONSTANTS", word)
    
    # If none of the above, classify the word as a symbol
    else:
        return Token("SYMBOL", word)