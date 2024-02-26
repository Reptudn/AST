class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Shunting yard algorithm
# in: ['1', '+', '2', '*', '4']
# out: ['1', '2', '+', '4', '*']
def shunting_yard(tokens):
    output = []
    operators = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    for token in tokens:
        if token in '1234567890':
            output.append(token)
        elif token in '+-*/':
            while (operators and operators[-1] in '+-*/' and
                   precedence[token] <= precedence[operators[-1]]):
                output.append(operators.pop())
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Discard the '('
    while operators:
        output.append(operators.pop())
    return output

# Build the AST from the postfix tokens
# in: ['1', '2', '+', '4', '*']
# out: Node('*')
def build_ast(postfix_tokens):
    stack = []
    for token in postfix_tokens:
        if token in '1234567890':
            stack.append(Node(token))
        elif token in '+-*/':
            node = Node(token)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    return stack[0] if stack else None

# Tokenize the input string
# in: 1 + 2 * 4
# out: ['1', '+', '2', '*', '4']
def tokenize(line: str):
    tokens = []
    number = ''
    for char in line:
        if char in '1234567890':
            number += char
        elif char in '+-*/()':
            if number != '':
                tokens.append(number)
                number = ''
            tokens.append(char)
        elif char in ' ':
            if number != '':
                tokens.append(number)
                number = ''
        else:
            print(f"Invalid character: {char}")
            return None
    if number != '':
        tokens.append(number)
    return tokens

# actual recursive calucaltion
def calculate(node):
    if node.value in '1234567890':
        return int(node.value)
    left = calculate(node.left)
    right = calculate(node.right)
    if node.value == '+':
        return left + right
    elif node.value == '-':
        return left - right
    elif node.value == '*':
        return left * right
    elif node.value == '/':
        return left / right

def main():
    print("Calculator")
    while True:
        line = str(input("calc> "))
        if line == "exit":
            break
        tokens = tokenize(line)
        if tokens == None:
            continue
        print("Tokens: ", str(tokens))
        output = shunting_yard(tokens)
        print("Postfix: " + str(output))
        ast = build_ast(output)
        if ast is None:
            print("ast err")
            continue
        print(ast.value)
        print("Solution: " + str(calculate(ast)))


if __name__ == "__main__":
    main()