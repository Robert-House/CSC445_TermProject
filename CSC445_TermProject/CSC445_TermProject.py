#!/usr/bin/env python
"""
Parsing Arithmetic Expressions
"""
import sys
from spark_parser import GenericParser, GenericASTTraversal
from spark_parser import AST
from spark_parser.scanner import GenericScanner, GenericToken

class ExprScanner(GenericScanner):
    # A simple integer expression Parser.
    

    def __init__(self):
        GenericScanner.__init__(self)

    def tokenize(self, input):
        self.rv = []
        GenericScanner.tokenize(self, input)
        return self.rv

    def add_token(self, name, s):
        t = GenericToken(kind=name, attr=s)
        self.rv.append(t)

    # Strip Whitespace
    def t_whitespace(self, s):
        r' \s+ '
        pass

    # Recognize binary operators.
    # The routines for '+' and '-' are separated from '*' and '/'
    # keep operator precidence separate.
    def t_add_op(self, s):
        r'[+-]'
        self.add_token('ADD_OP', s)

    def t_mult_op(self, s):
        r'[/*]'
        self.add_token('MULT_OP', s)

    # Recognize integers
    def t_integer(self, s):
        r'\d+'
        self.add_token('INTEGER', s)

# Some kinds of SPARK parsing you might want to consider
DEFAULT_DEBUG = {'rules': False, 'transition': False, 'reduce': False, 'dups': True}

class ExprParser(GenericParser):
    # A simple expression parser for numbers and arithmetic operators: +, , *, and /.

    def __init__(self, start='expr', debug=DEFAULT_DEBUG):
        GenericParser.__init__(self, start, debug)

    # Below are methods for the grammar rules and the AST tree-building
    # action to take

    def p_expr_add_term(self, args):
        ' expr ::= expr ADD_OP term '
        op = 'add' if args[1].attr == '+' else 'subtract'
        return AST(op, [args[0], args[2]])

    def p_expr2term2(self, args):
        ' expr ::= term '
        return AST('single', [args[0]])

    def p_term_mult_factor(self, args):
        ' term ::= term MULT_OP factor '
        op = 'multiply' if args[1].attr == '*' else 'divide'
        return AST(op, [args[0], args[2]])

    def p_term2single(self, args):
        ' term ::= factor '
        return AST('single', [args[0]])

    def p_factor2integer(self, args):
        ' factor ::= INTEGER '
        return AST('single', [args[0]])

class Interpret(GenericASTTraversal):

    def __init__(self, ast):
        GenericASTTraversal.__init__(self, ast)
        self.postorder(ast)
        self.attr = int(ast.attr)

    # Rules for interpreting nodes based on their AST node type
    def n_integer(self, node):
        node.attr = int(node.attr)

    def n_single(self, node):
        node.attr = node.data[0].attr

    def n_multiply(self, node):
        node.attr = int(node[0].attr) * int(node[1].attr)

    def n_divide(self, node):
        node.attr = int(node[0].attr) / int(node[1].attr)

    def n_add(self, node):
        node.attr = int(node[0].attr) + int(node[1].attr)

    def n_subtract(self, node):
        node.attr = int(node[0].attr) - int(node[1].attr)

    def default(self, node):
        pass

def scan_expression(data):
    """
    Tokenize *filename* into integers, numbers, and operators
    """
    scanner = ExprScanner()
    return scanner.tokenize(data)

def parse_expression(tokens):
    parser = ExprParser()
    return parser.parse(tokens)


# MAIN
if __name__ == '__main__':
    a = input("Please Enter an expression: ")

    data = a
    while (data != "n"):
        print(data)
        tokens = scan_expression(data)
        print(tokens)
        tree = parse_expression(tokens)
        print(tree)
        i = Interpret(tree)
        print("Final value is: %d" % i.attr)
        a = input("Please Enter an expression(n to quit): ")
        data = a