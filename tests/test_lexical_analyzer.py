import pytest
from lexical_analyzer import *


def list_asserter(lexer, l_tt, l_atr):
    for index in range(len(lexer)):
        asserter(lexer[index], l_tt[index], l_atr[index])


def asserter(word: Token, tt: TokenType, atr: str):
    assert word.tokenType == tt
    assert word.atr == atr


def test_lexer_simple_assignment():
    lexer = lexical_analyzer(FileObject(["a = 5"]))
    l_TokenTypes = [TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.CONSTANT, TokenType.NEWLINE,
                    TokenType.EOF]
    l_attributes = ['a', '=', '5', '\\n', '$']
    list_asserter(lexer, l_TokenTypes, l_attributes)


def test_lexer_if_elif_else():
    lexer = lexical_analyzer(
        FileObject(['if ( a == 5 ) :', '    a = 1', 'elif ( a == 6 ) :', '    a = 2', 'else :', '    a = 3']))
    l_tokenTypes = [TokenType.CONDITIONAL, TokenType.SYMBOL, TokenType.IDENTIFIER, TokenType.RELOP, TokenType.CONSTANT,
                    TokenType.SYMBOL, TokenType.SEMICOLON, TokenType.NEWLINE,
                    TokenType.BLOCK_BEGIN, TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.CONSTANT,
                    TokenType.NEWLINE, TokenType.BLOCK_END,
                    TokenType.CONDITIONAL, TokenType.SYMBOL, TokenType.IDENTIFIER, TokenType.RELOP, TokenType.CONSTANT,
                    TokenType.SYMBOL, TokenType.SEMICOLON, TokenType.NEWLINE,
                    TokenType.BLOCK_BEGIN, TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.CONSTANT,
                    TokenType.NEWLINE, TokenType.BLOCK_END,
                    TokenType.CONDITIONAL, TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.BLOCK_BEGIN,
                    TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.CONSTANT, TokenType.NEWLINE,
                    TokenType.BLOCK_END,
                    TokenType.EOF]
    l_attributes = ['if', '(', 'a', '==', '5', ')', ':', '\\n', 'begin', 'a', '=', '1', '\\n', 'end', 'elif', '(', 'a',
                    '==', '6', ')', ':', '\\n', 'begin', 'a', '=', '2', '\\n', 'end', 'else', ':', '\\n', 'begin', 'a',
                    '=', '3', '\\n', 'end', '$']
    list_asserter(lexer, l_tokenTypes, l_attributes)


def test_lexer_function():
    lexer = lexical_analyzer(FileObject(['def func ( a , b , c ) :', '    a = a * 1 - 2', '    b = b / 2 + 3', '    c = c ** 4 // 5 % 2']))
    l_tokenTypes = [TokenType.FUNCTION, TokenType.IDENTIFIER, TokenType.SYMBOL, TokenType.IDENTIFIER, TokenType.SYMBOL, TokenType.IDENTIFIER, TokenType.SYMBOL, TokenType.IDENTIFIER, TokenType.SYMBOL, TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.BLOCK_BEGIN, TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.CONSTANT, TokenType.OPERATOR, TokenType.CONSTANT, TokenType.NEWLINE, TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.CONSTANT, TokenType.OPERATOR, TokenType.CONSTANT, TokenType.NEWLINE, TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.CONSTANT, TokenType.OPERATOR, TokenType.CONSTANT, TokenType.OPERATOR, TokenType.CONSTANT, TokenType.NEWLINE, TokenType.BLOCK_END, TokenType.EOF]
    l_attributes = ['def', 'func', '(', 'a', ',', 'b', ',', 'c', ')', ':', '\\n', 'begin', 'a', '=', 'a', '*', '1', '-', '2', '\\n', 'b', '=', 'b', '/', '2', '+', '3', '\\n', 'c', '=', 'c', '**', '4', '//', '5', '%', '2', '\\n', 'end', '$']
