import ast

class ComplexityVisitor(ast.NodeVisitor):
    """
    A visitor to calculate cyclomatic complexity of a Python function.
    """
    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        if node.orelse:
            # Each 'elif' branch adds complexity, but the final 'else' does not.
            # An 'elif' is just another If node in the orelse block.
            pass
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        # Each 'except' block adds one to complexity
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Assert(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        # For 'and' and 'or', each value is a branch
        if isinstance(node.op, (ast.And, ast.Or)):
            self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_comprehension(self, node):
        # For list/dict/set comprehensions
        self.complexity += 1  # For the 'for' loop
        self.complexity += len(node.ifs)  # For each 'if' condition
        self.generic_visit(node)


def get_function_complexity(func_node):
    """
    Calculates the cyclomatic complexity of a single function AST node.
    """
    visitor = ComplexityVisitor()
    visitor.visit(func_node)
    return visitor.complexity
