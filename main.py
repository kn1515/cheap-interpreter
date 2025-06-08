import re

# ===== トークンの定義 =====
TOKEN_REGEX = r"\s*(?:(\d+)|(.))"

def tokenize(expression):
    tokens = []
    for number, operator in re.findall(TOKEN_REGEX, expression):
        if number:
            tokens.append(('NUMBER', int(number)))
        else:
            tokens.append(('OP', operator))
    return tokens

# ===== パーサー =====
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, expected_type=None, expected_value=None):
        token = self.peek()
        if token is None:
            return None
        if expected_type and token[0] != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token}")
        if expected_value and token[1] != expected_value:
            raise SyntaxError(f"Expected {expected_value}, got {token}")
        self.pos += 1
        return token

    def parse_expression(self):
        return self.parse_add_sub()

    def parse_add_sub(self):
        node = self.parse_mul_div()
        while True:
            token = self.peek()
            if token and token[1] in ('+', '-'):
                self.eat('OP')
                right = self.parse_mul_div()
                node = (token[1], node, right)
            else:
                break
        return node

    def parse_mul_div(self):
        node = self.parse_atom()
        while True:
            token = self.peek()
            if token and token[1] in ('*', '/'):
                self.eat('OP')
                right = self.parse_atom()
                node = (token[1], node, right)
            else:
                break
        return node

    def parse_atom(self):
        token = self.peek()
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ('NUM', token[1])
        elif token[1] == '(':
            self.eat('OP', '(')
            node = self.parse_expression()
            self.eat('OP', ')')
            return node
        else:
            raise SyntaxError(f"Unexpected token: {token}")

# ===== 評価 =====
def evaluate(node):
    if node[0] == 'NUM':
        return node[1]
    op, left, right = node
    if op == '+':
        return evaluate(left) + evaluate(right)
    elif op == '-':
        return evaluate(left) - evaluate(right)
    elif op == '*':
        return evaluate(left) * evaluate(right)
    elif op == '/':
        return evaluate(left) / evaluate(right)
    else:
        raise ValueError(f"Unknown operator: {op}")

# ===== 実行 =====
def run_interpreter(expression):
    tokens = tokenize(expression)
    parser = Parser(tokens)
    ast = parser.parse_expression()
    return evaluate(ast)

# ===== テスト =====
if __name__ == "__main__":
    while True:
        try:
            expr = input(">>> ")
            if expr in ("exit", "quit"):
                break
            result = run_interpreter(expr)
            print(result)
        except Exception as e:
            print("Error:", e)
