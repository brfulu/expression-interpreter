from token import Token, TType


class Lexer:
    def __init__(self, text):
        self.pos = 0
        self.text = text
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Neocekivani karakter {}'.format(self.current_char))

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        number = ''
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return Token(TType.INTEGER, int(number))

    def variable_or_rim(self):
        temp = ''
        while self.current_char is not None and (
                self.current_char.isdigit() or self.current_char.isalpha() or self.current_char == '_'):
            temp += self.current_char
            self.advance()

        if temp == 'RIM' and self.current_char == '(':
            value = ''
            self.advance()
            while self.current_char != ')':
                value += self.current_char
                self.advance()
            self.advance()
            return Token(TType.RIM, 'RIM({})'.format(value.upper()))

        else:
            return Token(TType.VAR, temp)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()

            if self.current_char.isalpha():
                return self.variable_or_rim()

            if self.current_char.isdigit():
                return self.integer()

            if self.current_char == '+':
                self.advance()
                return Token(TType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TType.MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TType.DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TType.RPAREN, ')')

            if self.current_char == '=':
                self.advance()
                return Token(TType.ASSIGN, '=')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TType.GTE, '>=')
                else:
                    return Token(TType.GT, '>')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TType.LTE, '<=')
                else:
                    return Token(TType.LT, '<')

        return Token(TType.EOF, None)
