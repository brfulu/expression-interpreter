from lexer import Lexer
from interpreter import Interpreter


def main():
    mode = 'INFIX'
    interpreter = Interpreter()

    while True:
        try:
            text = input(mode + ' -> ')
        except EOFError:
            break

        if not text:
            continue

        if text.strip() == 'exit':
            break

        if text.strip().upper() in ['INFIX', 'POSTFIX', 'PREFIX']:
            mode = text.strip().upper()
            continue

        result = interpreter.eval(text, mode)
        print(result)


if __name__ == "__main__":
    main()
