import pytest
from codecritical.parsers.python_parser import parse_python_file

@pytest.fixture
def sample_python_file(tmp_path):
    content = """
def hello(name):
    print(f"Hello, {name}!")

class Greeter:
    def __init__(self, greeting):
        self.greeting = greeting

    def greet(self, name):
        if self.greeting == "Hello":
            print(f"Hello, {name}!")
        else:
            print(f"{self.greeting}, {name}!")
"""
    p = tmp_path / "sample.py"
    p.write_text(content)
    return str(p)

def test_parse_python_file(sample_python_file):
    result = parse_python_file(sample_python_file)

    assert result['filepath'] == sample_python_file
    assert result['lines']['total'] == 13
    assert result['function_count'] == 3
    assert result['class_count'] == 1

    # hello complexity = 1
    # __init__ complexity = 1
    # greet complexity = 2 (1 for if)
    assert result['avg_complexity'] == (1 + 1 + 2) / 3

    func_complexities = {f['name']: f['complexity'] for f in result['functions']}
    assert func_complexities['hello'] == 1
    assert func_complexities['__init__'] == 1
    assert func_complexities['greet'] == 2

def test_parse_python_file_with_syntax_error(tmp_path):
    content = """
def hello(name)
    print(f"Hello, {name}!")
"""
    p = tmp_path / "sample.py"
    p.write_text(content)
    result = parse_python_file(str(p))
    assert 'error' in result
