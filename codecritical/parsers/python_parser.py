import ast
from codecritical.metrics.complexity import get_function_complexity

def parse_python_file(filepath):
    """
    Parses a Python file to extract code metrics.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()

    total_lines = len(lines)
    code_lines = 0
    comment_lines = 0
    blank_lines = 0

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            blank_lines += 1
        elif stripped_line.startswith('#'):
            comment_lines += 1
        else:
            code_lines += 1

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return {
            'filepath': filepath,
            'error': 'SyntaxError: could not parse file'
        }

    functions = []
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            complexity = get_function_complexity(node)
            functions.append({
                'name': node.name,
                'lineno': node.lineno,
                'complexity': complexity
            })
        elif isinstance(node, ast.ClassDef):
            classes.append({
                'name': node.name,
                'lineno': node.lineno
            })

    avg_complexity = 0
    if functions:
        avg_complexity = sum(f['complexity'] for f in functions) / len(functions)


    return {
        'filepath': filepath,
        'lines': {
            'total': total_lines,
            'code': code_lines,
            'comment': comment_lines,
            'blank': blank_lines,
        },
        'functions': functions,
        'classes': classes,
        'function_count': len(functions),
        'class_count': len(classes),
        'avg_complexity': avg_complexity,
    }
