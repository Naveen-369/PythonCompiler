# Grammar
from enum import Enum
from Lexical_Analyser.Lexical_Components.Token import Token
from Lexical_Analyser.Lexical_Components.TokenType import TokenType
from Lexical_Analyser.Lexical_Components.GrammarErrorException import GrammarError


class Parser:
    """
    <statement>      -> <if_statement>
                     | <while_loop>
                     | <for_loop>
                     | <function_def>
                     | <function_call>
                     | <return_statement>
    <assignment>     -> IDENTIFIER '=' <expression>
    <expression>     -> <term> <expression_1>
    <expression_1>   -> '+' <term> <expression_1>
                     | '-' <term> <expression_1>
                     | None
    <term>           -> <factor> <term_1>
    <term_1>         -> '*' <factor> <term_1>
                     | '/' <factor> <term_1>
                     | None
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

    def __init__(self, listOfTokens):
        self.tokens = listOfTokens
        self.pos = 0
        self.lookahead: Token = self.tokens[self.pos]
        self.listOfExpressions = []
        self.tree = None
        self.program()

    def consume(self, **kwargs):
        if not kwargs:
            token = self.lookahead
            self.match()
            return token  # Return the token, still advances the parser
        if not self.check(**kwargs):
            return None
        else:
            token = self.lookahead
            self.match()
            return token

    def consume_error(self, **kwargs):
        key, value = list(kwargs.items())[0]
        if len(kwargs.items()) == 2:
            message = kwargs['message']
        else:
            message = value
        temp = self.consume(**{key: value})
        if not temp:
            self.error_grammar(expected=message)
        else:
            return temp

    def program(self):
        self.tree = ASTNode(AST.PROGRAM)
        self.tree.add(self.statement_list())

    def statement_list(self):
        stmnt_list = ASTNode(AST.STATEMENT_LIST)
        while not self.check(tokenType=TokenType.EOF) and not self.check(atr='end'):
            stmt = self.statement()
            if stmt:
                stmnt_list.add(stmt)
            self.consume(tokenType=TokenType.NEWLINE)
        return stmnt_list

    def statement(self):
        stmnt = ASTNode(AST.STATEMENT)
        if self.check(tokenType=TokenType.IDENTIFIER):
            if self.tokens[self.pos + 1].atr == '=':
                stmnt.add(self.assignment())
                return stmnt
            elif self.tokens[self.pos + 1].atr == '(':
                func_call = ASTNode(AST.FUNC_CALL)
                stmnt.add(func_call)
                func_call.add(self.function_call())
                return stmnt
            else:
                # NameError: name 'a' is not defined
                self.error_grammar()
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
        self.consume_error(tokenType=TokenType.BLOCK_END)

    # <assignment>     -> IDENTIFIER '=' <expression>

    def assignment(self):
        left = self.consume_error(tokenType=TokenType.IDENTIFIER)
        self.consume_error(atr='=')
        right = self.expression()  # This should return an ASTNode
        # parent = self.add(parent, root)
        node = ExpressionNode('=')
        node.left = left
        node.right = right
        root = ASTNode(AST.ASSIGNMENT)
        root.add(node)
        return root
        # node.add(right)
        # return node
        # self.listOfExpressions.append(root)

    # < expression >     -> < term > <expression_1>
    def expression(self):
        root = self.term()
        while self.lookahead.atr in ('+', '-'):
            op = self.consume().atr
            right = self.term()
            root = expression_tree_builder(op, root, right)
        return root

    # T  -> F T'
    def term(self):
        root = self.factor()
        while self.lookahead.atr in ('*', '/'):
            op = self.consume().atr  # Get operator (* or /)
            right = self.factor()  # Parse next factor
            root = expression_tree_builder(op, root, right)
        return root

    # F  -> '(' E ')' | CONSTANT | IDENTIFIER
    def factor(self):
        temp = self.consume()
        if temp.atr == '(':
            # consumed '('
            temp = self.expression()
            self.consume(atr=')')
            return temp
        elif temp.tokenType == TokenType.CONSTANT:
            # consumed 'CONSTANT'
            return temp
        elif temp.tokenType == TokenType.IDENTIFIER:
            val = temp.atr
            # consumed 'IDENTIFIER'
            return val
        else:
            self.error_grammar(expected="CONSTANT, IDENTIFIER, expression")

    # < if_statement >   -> 'if' '(' < condition > ')' ':' \n 'begin' < statement_list > 'end'
    # |'if''('<condition>')'':'\n\'begin'<statement_list>'end'\n\'elif''('condition')'':'\n\'begin'<statement_list>'end'
    # |'if''('<condition>')'':'\n\'begin'<statement_list>'end'\n\'else'':''begin'< statement_list >'end'
    def if_statement(self):
        self.consume_error(atr='if')
        # if_stmnt = ASTNode(AST.IF_COND)
        if self.consume(atr='('):
            # consumed '('
            self.condition()
            self.consume_error(atr=')')
        else:
            self.condition()
        self.consume_error(atr=':')
        self.consume(tokenType=TokenType.NEWLINE)
        self.consume_error(tokenType=TokenType.BLOCK_BEGIN, message='INDENTATION')
        self.statement_list()

        while self.consume(atr='elif'):
            if self.consume(atr='('):
                # consumed '('
                self.condition()
                self.consume_error(atr=')')
            else:
                self.condition()
            self.consume_error(atr=':')
            self.consume(tokenType=TokenType.NEWLINE)
            self.consume_error(tokenType=TokenType.BLOCK_BEGIN, message='INDENTATION')
            self.statement_list()

        if self.consume(atr='else'):
            # consumed 'else'
            self.consume_error(atr=':')
            self.consume(tokenType=TokenType.NEWLINE)
            self.consume_error(tokenType=TokenType.BLOCK_BEGIN, message='INDENTATION')
            self.statement_list()

    # <condition>      -> <expression> <relop> <expression>
    def condition(self):
        self.expression()
        self.relop()
        self.expression()

    # <relop>          -> '==' | '!=' | '<' | '<=' | '>' | '>='
    def relop(self):
        self.consume(tokenType=TokenType.RELOP)

    # < for_loop > -> 'for' '(' IDENTIFIER 'in' 'range' '(' NUMBER ',' NUMBER ')' ')' ':' \n
    #                 'begin' < statement_list > 'end'
    def for_loop(self):
        self.consume_error(atr='for')
        bracket_bool = False
        if self.consume(atr='('):
            bracket_bool = True
        self.consume_error(tokenType=TokenType.IDENTIFIER)
        self.consume_error(atr='in')
        self.function_call()
        if bracket_bool:
            self.consume_error(atr=')')
        del bracket_bool
        self.consume_error(atr=':')
        self.consume(tokenType=TokenType.NEWLINE)
        self.consume_error(tokenType=TokenType.BLOCK_BEGIN)
        self.statement_list()

    # <while_loop>     -> 'while' '(' <condition> ')' ':' \n 'begin' <statement_list> 'end'
    def while_loop(self):
        self.consume_error(atr='while')
        if self.consume(atr='('):
            # consumed '('
            self.condition()
            self.consume_error(atr=')')
        else:
            self.condition()
        self.consume_error(atr=':')
        self.consume(tokenType=TokenType.NEWLINE)
        self.consume_error(tokenType=TokenType.BLOCK_BEGIN, message='INDENTATION')
        self.statement_list()

    # <function_def>   -> 'def' IDENTIFIER '(' <param_list> ')' '{' <statement_list> '}'
    def function_def(self):
        self.consume_error(atr='def')
        self.consume_error(tokenType=TokenType.IDENTIFIER)
        self.consume_error(atr='(')
        self.param_list()
        self.consume_error(atr=')')
        self.consume_error(tokenType=TokenType.SEMICOLON)
        self.consume_error(tokenType=TokenType.NEWLINE)
        self.consume_error(tokenType=TokenType.BLOCK_BEGIN, message='INDENTATION')
        self.statement_list()

    # < function_call >  -> IDENTIFIER '(' < arg_list > ')'

    def function_call(self):
        # self.consume_error(tokenType=TokenType.IDENTIFIER)
        iden = ASTNode(AST.FUNC_CALL)
        iden.add(self.consume_error(tokenType=TokenType.IDENTIFIER))
        self.consume_error(atr='(')
        arg = self.arg_list()
        self.consume_error(atr=')')
        if arg:
            return [iden, arg]
        else:
            return iden

    # < arg_list >       -> < factor > ',' < arg_list > | < factor > | ε
    def arg_list(self):
        arg = None
        if self.check(tokenType=TokenType.IDENTIFIER):
            arg = ASTNode(AST.ARG_LIST)
            arg.add(self.factor())
        while self.consume(atr=','):
            if self.check(tokenType=TokenType.IDENTIFIER):
                arg.add(self.factor())
        return arg

    # < return_statement > -> 'return' < expression >
    def return_statement(self):
        self.consume_error(atr='return')
        self.expression()

    # <param_list>     -> IDENTIFIER ',' <param_list> | IDENTIFIER | ε
    def param_list(self):
        if not self.consume(tokenType=TokenType.IDENTIFIER):
            return
        if not self.consume(atr=','):
            return
        # consumed ','
        if self.check(tokenType=TokenType.IDENTIFIER):
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


class AST(Enum):
    PROGRAM = "PROGRAM"
    STATEMENT_LIST = "STATEMENT_LIST"
    STATEMENT = "STATEMENT"
    ASSIGNMENT = "ASSIGNMENT"
    EXPRESSION = "EXPRESSION"
    TERM = "TERM"
    FACTOR = "FACTOR"
    IF_COND = "IF_COND"
    WHILE_LOOP = "WHILE_LOOP"
    FOR_LOOP = "FOR_LOOP"
    FUNC_DEF = "FUNC_DEF"
    PARAM = "PARAM"
    FUNC_CALL = "FUNC_CALL"
    ARG_LIST = "ARG_LIST"
    RETURN = "RETURN"
    CONDITION = "CONDITION"
    RELOP = "RELOP"


class ASTNode:

    def __init__(self, nodeType: AST, value=None):
        self.nodeType = nodeType  # e.g., "ASSIGNMENT", "IF", "LOOP"
        self.value = value  # e.g., variable name or operator
        self.children = []  # For nested expressions/statements

    def add(self, child):
        if child is not None:
            self.children.append(child)

    def __repr__(self, indent=0):
        prefix = "  " * indent
        repr_str = f"{prefix}{self.nodeType.name}"  # or str(self.nodeType) if not enum
        if self.value is not None:
            repr_str += f": {self.value}"
        repr_str += "\n"
        for child in self.children:
            if isinstance(child, ASTNode):
                repr_str += child.__repr__(indent + 1)
            else:
                repr_str += f"{'  ' * (indent + 1)}{str(child)}\n"
        return repr_str


class ExpressionNode(ASTNode):
    def __init__(self, operator: str | int):
        super().__init__(AST.EXPRESSION)
        self.nodeType = "OPERATORS" if (type(operator) == str and not operator.isdigit()) else "CONSTANT"
        self.value = operator
        self.left = None
        self.right = None

    def __repr__(self, level=0):
        indent = '\t' * level
        result = f"{indent}{self.nodeType}: {self.value}\n"

        child_level = level + 1
        if self.left:
            left_repr = self.left.__repr__(child_level).rstrip('\n')
            result += f"{left_repr}\n"

        if self.right:
            right_repr = self.right.__repr__(child_level).rstrip('\n')
            result += f"{right_repr}\n"

        return result


def expression_tree_builder(operator: Token | str, left: Token | str | ExpressionNode,
                            right: Token | str | ExpressionNode):
    root = ExpressionNode(operator.atr) if type(operator) == Token else ExpressionNode(operator)
    root.left = ExpressionNode(left.atr) if type(left) == Token else ExpressionNode(left) if type(
        left) == str else left
    root.right = ExpressionNode(right.atr) if type(right) == Token else ExpressionNode(right) if type(
        right) == str else right
    return root


class IfNode(ASTNode):
    def __init__(self):
        self.condition = None
        self.if_block = None
        self.else_block = None