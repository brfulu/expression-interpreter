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


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return "<{}, {}>".format(self.type, self.value)


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

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()

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

        return Token(TType.EOF, None)


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Greska u parsiranju')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token

        if token.type == TType.INTEGER:
            self.eat(TType.INTEGER)
            return token.value
        elif token.type == TType.LPAREN:
            self.eat(TType.LPAREN)
            result = self.expr()
            self.eat(TType.RPAREN)
            return result

    def term(self):
        # 2 * (9) / 6 * 8 * 5

        result = self.factor()

        while self.current_token.type in (TType.MUL, TType.DIV):
            token = self.current_token
            if token.type == TType.MUL:
                self.eat(TType.MUL)
                result = result * self.factor()
            elif token.type == TType.DIV:
                self.eat(TType.DIV)
                result = result / self.factor()
            else:
                self.error()

        return result

    def expr(self):
        # 1 + 3 * 8 / 3 + 9 - 9

        result = self.term()

        while self.current_token.type in (TType.PLUS, TType.MINUS):
            token = self.current_token
            if token.type == TType.PLUS:
                self.eat(TType.PLUS)
                result = result + self.term()
            elif token.type == TType.MINUS:
                self.eat(TType.MINUS)
                result = result - self.term()
            else:
                self.error()

        return result


def main():
    while True:
        try:
            text = input('--> ')
        except EOFError:
            break

        if not text:
            continue

        if text == 'exit':
            break

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
