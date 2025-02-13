import sys
import re


'''
classes camelCase
Variable camelCase
functions snake_case
constants UPPERCASE
'''

"""
TODO:
 Make change to indentation like if 'a' < '5' : \n (indent,4) 'a' = '7' \n 'b' = '10' (dedent,0) eof
 
FUTURE:
 make the CFG automatic by using text file
 implement lalr parser instead of backtracking
"""

# CONSTANTS:
# Keywords
CONDITIONALS = {c: "CONDITIONAL" for c in ["if", "else", "then"]}
# Operators
OPERATORS = {op: "OPERATOR" for op in ["+", "-", "*", "/", "="]}
# Relational Operators
RELOP = {relop: "RELOP" for relop in ['==', '!=', '<', '<=', '>', '>=']}
# Loops
LOOPS = {loop: "LOOP" for loop in ['for', 'while']}

class GrammarError(Exception):
    def __init__(self, message, token=None, expected=None):
        self.token = token
        self.expected = expected
        error_message = f"Grammar Error: {message}"
        if token:
            error_message += f" | Found: '{token}'"
        if expected:
            error_message += f" | Expected: {expected}"
        super().__init__(error_message)


# Grammar
class Parser:
    """
    <statement>      -> <if_statement>
                     | <while_loop>
                     | <for_loop>
                     | <function_def>
                     | <function_call>
                     | <return_statement>
    <assignment>     -> IDENTIFIER '=' <expression>
    <expression>     -> <expression> '+' <term>
                     | <expression> '-' <term>
                     | <term>
    <term>           -> <term> '*' <factor>
                     | <term> '/' <factor>
                     | <factor>
    <factor>         -> '(' <expression> ')'
                     | NUMBER
                     | IDENTIFIER
    <while_loop>     -> 'while' '(' <condition> ')' '{' <statement_list> '}'
    <for_loop>       -> 'for' '(' IDENTIFIER 'in' 'range' '(' NUMBER ',' NUMBER ')' ')' '{' <statement_list> '}'
    <function_def>   -> 'def' IDENTIFIER '(' <param_list> ')' '{' <statement_list> '}'
    <param_list>     -> IDENTIFIER ',' <param_list> | IDENTIFIER | ε
    <function_call>  -> IDENTIFIER '(' <arg_list> ')'
    <arg_list>       -> <expression> ',' <arg_list> | <expression> | ε
    <return_statement> -> 'return' <expression>
    <condition>      -> <expression> <relop> <expression>
    <relop>          -> '==' | '!=' | '<' | '<=' | '>' | '>='

    In the future, try to implement this grammar by reading a text file and if possible try to eliminate left
    recursion and use that grammar
    """

    def __init__(self, lTokens):
        self.tokens = lTokens
        self.pos = 0
        self.lookahead: Token = self.tokens[self.pos]
        self.program()

    def consume(self, **kwargs):
        """
        Improved consume method with better error handling and return values
        """
        if not kwargs:
            self.match()
            return True

        key, value = list(kwargs.items())[0]
        if not self.check(**kwargs):
            # self.error_grammar(expected=value)
            return False
        else:
            print(self.lookahead)
            self.match()
        return True

    def consume_error(self, **kwargs):
        key, value = list(kwargs.items())[0]
        if len(kwargs.items()) == 2:
            message = kwargs['message']
        else:
            message = value
        if not self.consume(**{key:value}):
            self.error_grammar(expected=message)
    def program(self):
        self.statement_list()

    def statement_list(self):
        self.statement()
        self.consume(tokenType='NEWLINE')
        if ((not self.consume(tokenType='EOF')) and (not self.consume(atr='end'))):
            self.statement_list()

    def statement(self):
        """
        Improved statement handling with proper returns
        """
        if self.check(tokenType='IDENTIFIER'):
            self.assignment()
        elif self.check(atr='if'):
            self.if_statement()
        elif self.check(atr='for'):
            self.for_loop()
        elif self.check(atr='while'):
            self.while_loop()
        elif self.check(atr='def'):
            self.function_def()
        else:
            return


    # <assignment>     -> IDENTIFIER '=' <expression>
    def assignment(self):
        self.consume_error(tokenType='IDENTIFIER')
        self.consume_error(atr='=')
        self.expression()

    # < expression >     -> < term > <expression_1>
    def expression(self):
        self.term()
        self.expression_1()

    # E' -> '+' T E' | '-' T E' | None
    def expression_1(self):
        if self.consume(atr='+'):
            # consumed '+'
            self.term()
            self.expression_1()
            return
        elif self.consume(atr='-'):
            self.term()
            self.expression_1()
            return

    # T  -> F T'
    def term(self):
        self.factor()
        self.term_1()

    # T' -> '*' F T' | '/' F T' | None
    def term_1(self):
        if self.consume(atr='*'):
            self.factor()
            self.term_1()
            return
        elif self.consume(atr='/'):
            self.factor()
            self.term_1()
            return

    # F  -> '(' E ')' | CONSTANT | IDENTIFIER
    def factor(self):
        if self.consume(atr='('):
            # consumed '('
            self.expression()
            self.consume(atr=')')
            return

        elif self.consume(tokenType='CONSTANT'):
            # consumed 'CONSTANT'
            return

        elif self.consume(tokenType='IDENTIFIER'):
            # consumed 'IDENTIFIER'
            return

        self.error_grammar(expected="CONSTANT, IDENTIFIER, expression")

    # < if_statement >   -> 'if' '(' < condition > ')' ':' \n 'begin' < statment_list > 'end'
    # | 'if' '(' < condiiton > ')' ':' \n 'begin' < statement_list > 'end' \n 'elif' '(' condition ')' ':' \n 'begin' < statement_list > 'end'
    # | 'if' '(' < condition > ')' ':' \n 'begin' < statement_list > 'end' \n 'else' ':' 'begin' < statement_list > 'end'
    def if_statement(self):
        self.consume_error(atr='if')
        if self.consume(atr='('):
            # consumed '('
            self.condition()
            self.consume_error(atr=')')
        else:
            self.condition()
        self.consume_error(atr=':')
        self.consume(tokenType='NEWLINE')
        self.consume_error(tokenType='BLOCK BEGIN', message='INDENTATION')
        self.statement_list()

        while(self.consume(atr='elif')):
            if self.consume(atr='('):
                # consumed '('
                self.condition()
                self.consume_error(atr=')')
            else:
                self.condition()
            self.consume_error(atr=':')
            self.consume(tokenType='NEWLINE')
            self.consume_error(tokenType='BLOCK BEGIN', message='INDENTATION')
            self.statement_list()

        if self.consume(atr='else'):
            # consumed 'else'
            self.consume_error(atr=':')
            self.consume(tokenType='NEWLINE')
            self.consume_error(tokenType='BLOCK BEGIN', message='INDENTATION')
            self.statement_list()

    # <condition>      -> <expression> <relop> <expression>
    def condition(self):
        self.expression()
        self.relop()
        self.expression()

    # <relop>          -> '==' | '!=' | '<' | '<=' | '>' | '>='
    def relop(self):
        self.consume(tokenType='RELOP')

    # < for_loop >       -> 'for' '(' IDENTIFIER 'in' 'range' '(' NUMBER ',' NUMBER ')' ')' ':' \n 'begin' < statement_list > 'end'
    def for_loop(self):
        pass

    # <while_loop>     -> 'while' '(' <condition> ')' ':' \n 'begin' <statement_list> 'end'
    def while_loop(self):
        if not self.consume(atr='while'):
            self.error_grammar(expected='while')
        if self.consume(atr='('):
            # consumed '('
            self.condition()
            if not self.consume(atr=')'):
                self.error_grammar(expected=')')
        else:
            self.condition()
        if not self.consume(atr=':'):
            self.error_grammar(expected=':')
        self.consume(tokenType='NEWLINE')
        if not self.consume(tokenType='BLOCK BEGIN'):
            self.error_grammar(expected='INDENTATION')
        self.statement_list()

    # <function_def>   -> 'def' IDENTIFIER '(' <param_list> ')' '{' <statement_list> '}'
    def function_def(self):
        self.consume_error(atr='def')
        self.consume_error(tokenType='IDENTIFIER')
        self.consume_error(atr='(')
        self.param_list()
        self.consume_error(atr=')')
        self.consume_error(tokenType='SEMICOLON')
        self.consume_error(tokenType='NEWLINE')
        self.consume_error(tokenType='BLOCK BEGIN', message='INDENTATION')
        self.statement_list()

    # <param_list>     -> IDENTIFIER ',' <param_list> | IDENTIFIER | ε
    def param_list(self):
        if not self.consume(tokenType='IDENTIFIER'):
            return
        if not self.consume(atr=','):
            return
        # consumed ','
        if self.check(tokenType='IDENTIFIER'):
            self.param_list()


    def match(self):
        """
        Improved match method with better bounds checking
        """
        if self.pos + 1 < len(self.tokens):
            self.pos += 1
            self.lookahead = self.tokens[self.pos]
        else:
            self.lookahead = None  # Explicitly handle end of input

    def check(self, **kwargs):
        """
        Improved check method with null safety
        """
        if self.lookahead is None:
            return False

        for key, value in kwargs.items():
            if key == 'tokenType':
                return self.lookahead.tokenType == value
            elif key == 'atr':
                return self.lookahead.atr == value
        return False

    def error_grammar(self, expected=None):
        raise GrammarError("Invalid syntax", self.lookahead, expected)


class Token:
    """
    the token class classifies the words in the program into tokens like identifier, constants, etc
    and stores a value of it.
    """

    def __init__(self, tokenType: str, atr: str = None) -> None:
        self.tokenType = tokenType
        self.atr = atr

    def __repr__(self) -> str:
        return f"('{self.tokenType}', '{self.atr}')"


def token_giver(word: str) -> Token:
    """
    Takes a word from the code and returns a Token object with its type and attribute.
    :param word:
    :return Token:
    """
    # Keyword
    if word in CONDITIONALS:
        return Token("CONDITIONAL", word)

    # Loops
    if word in LOOPS:
        return Token("LOOPS", word)

    # Indentation
    elif not word:
        return Token("INDENTATION", '\\t')

    # Operator
    elif word in OPERATORS:
        return Token("OPERATOR", word)

    # Relational Operator
    elif word in RELOP:
        return Token("RELOP", word)

    # Semicolon
    elif word == ":":
        return Token("SEMICOLON", word)

    # def function
    elif word == "def":
        return Token("FUNCTION", word)

    # Identifier
    elif word[0].isalpha() or word[0] == '_':
        return Token("IDENTIFIER", word)

    # Constant (Update later to work for float and exponential numbers)
    elif word[0].isdigit():
        return Token("CONSTANT", word)

    # Default to symbol if none of the above match
    else:
        return Token("SYMBOL", word)


def file_reader(inp: str) -> list:
    """
    reads the inp file and return the list of list about the contents / text of the file
    :param inp:
    :return:
    """
    text = []
    try:
        with open(inp, "r") as f:
            for line in f:
                text.append(line.rstrip('\n'))
    except FileNotFoundError:
        print("Error: The file was not found.")
    print(text)
    return text


def lexical_analyzer(inp: list) -> list:
    """
    maps the list of words in the file to a list of Tokens
    :param inp:
    :return:
    """
    lTokens = []
    indent_stack = [0]

    for line in inp:
        # Count leading spaces
        indent_level = len(line) - len(line.lstrip())
        stripped_line = line.strip()

        # Skip empty lines
        if not stripped_line:
            continue

        # Handle indentation changes
        if indent_level > indent_stack[-1]:
            # Indentation increased - add BLOCK BEGIN
            indent_stack.append(indent_level)
            lTokens.append(Token("BLOCK BEGIN", "begin"))
        elif indent_level < indent_stack[-1]:
            # Indentation decreased - add BLOCK END tokens
            while indent_stack and indent_level < indent_stack[-1]:
                indent_stack.pop()
                lTokens.append(Token("BLOCK END", "end"))

            if indent_level != indent_stack[-1]:
                raise IndentationError(f"Invalid indentation level: {indent_level}")

        # Process the actual line content
        for word in re.split(r'\s+', stripped_line):
            lTokens.append(token_giver(word))

        lTokens.append(Token("NEWLINE", "\\n"))

        # Add remaining BLOCK END tokens at EOF
    while len(indent_stack) > 1:
        indent_stack.pop()
        lTokens.append(Token("BLOCK END", "end"))

    lTokens.append(Token('EOF', '$'))
    return lTokens

    # Ensure all opened blocks are closed before EOF
    while block_stack:
        lTokens.append(Token("BLOCK END", ""))
        block_stack.pop()

    lTokens.append(Token('EOF', '$'))
    return lTokens

if __name__ == '__main__':
    # Reading the program

    file = file_reader(sys.argv[1])

    print(file)
    # Token Parsing
    tokens = lexical_analyzer(file)

    print(tokens)
    # NOW MAP OUT A GRAMMER THAT THIS PROGRAMMING LANGUAGE FOLLOWS
    # AFTER THAT CODE THE LALR PARSER BUT BEFORE THAT YOU NEED FIRST AND FOLLOW COMPUTE TO USE

    # for token in tokens:
    #     print(token)
    Parser(tokens)
    print("Parsing done")
