from token import TType
from lexer import Lexer


class Interpreter:
    def __init__(self):
        self.mode = 'INFIX'
        self.lexer = None
        self.current_token = None
        self.vars = {}

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
        elif token.type == TType.VAR:
            self.eat(TType.VAR)
            if self.current_token.type == TType.ASSIGN:
                self.eat(TType.ASSIGN)
                result = self.expr()
                self.vars[token.value] = result
                return result
            else:
                if token.value not in self.vars:
                    self.vars[token.value] = 0
                return self.vars[token.value]
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

        return round(result)

    def multi_expr(self):
        is_multi_expr = False
        result = True
        left_expr = self.expr()

        while self.current_token.type in (TType.GT, TType.GTE, TType.LT, TType.LTE):
            is_multi_expr = True
            token = self.current_token

            if token.type == TType.GT:
                self.eat(TType.GT)
                right_expr = self.expr()
                result &= (left_expr > right_expr)
            elif token.type == TType.GTE:
                self.eat(TType.GTE)
                right_expr = self.expr()
                result &= (left_expr >= right_expr)
            elif token.type == TType.LT:
                self.eat(TType.LT)
                right_expr = self.expr()
                result &= (left_expr < right_expr)
            elif token.type == TType.LTE:
                self.eat(TType.LTE)
                right_expr = self.expr()
                result &= (left_expr <= right_expr)
            else:
                self.error()

            left_expr = right_expr

        return result if is_multi_expr else left_expr

    def eval_infix(self, text):
        print(text)
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()
        return self.multi_expr()

    def eval(self, text, mode):
        if mode == 'INFIX':
            return self.eval_infix(text)
        elif mode == 'POSTFIX':
            return self.eval_infix(self.postfix_to_infix(text))
        elif mode == 'PREFIX':
            return self.eval_infix(self.prefix_to_infix(text))
        else:
            self.error()

    def postfix_to_infix(self, text):
        return self.convert_to_infix(text, True)

    def prefix_to_infix(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()
        tokens = []
        while self.current_token.type != TType.EOF:
            tokens.append(self.current_token.value)
            self.eat(self.current_token.type)

        reverse_text = ' '.join(str(token) for token in reversed(tokens))
        return self.convert_to_infix(reverse_text, False)

    def convert_to_infix(self, text, is_postfix):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()
        operands = []

        while self.current_token.type != TType.EOF:
            token = self.current_token
            if token.type in [TType.INTEGER, TType.VAR]:
                operands.append(token.value)
                self.eat(token.type)
            elif token.type in [TType.PLUS, TType.MINUS, TType.MUL, TType.DIV, TType.ASSIGN]:
                left = operands.pop()
                right = operands.pop()
                if is_postfix:
                    left, right = right, left
                operands.append('({}{}{})'.format(left, token.value, right))
                self.eat(token.type)
            else:
                self.error()

        return operands.pop()
