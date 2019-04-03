from enum import Enum


class TType(Enum):
    INTEGER = 0
    PLUS = 1
    MINUS = 2
    MUL = 3
    DIV = 4
    EOF = 5
    LPAREN = 6
    RPAREN = 7
    VAR = 8
    ASSIGN = 9
    GT = 10
    LT = 11
    GTE = 12
    LTE = 13


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return "<{}, {}>".format(self.type, self.value)
