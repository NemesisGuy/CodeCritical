import pytest
import subprocess
import json

@pytest.fixture
def sample_python_file(tmp_path):
    content = """
def hello(name):
    print(f"Hello, {name}!")
"""
    p = tmp_path / "sample.py"
    p.write_text(content)
    return str(p)

def test_cli_with_file(sample_python_file):
    result = subprocess.run(
        ['python', '-m', 'codecritical.cli', '--path', sample_python_file, '--lang', 'python', '--output', 'json'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    report = json.loads(result.stdout)

    assert report['repo'] == sample_python_file
    assert report['summary']['files_scanned'] == 1
    assert report['languages']['python']['files'] == 1
    assert report['languages']['python']['functions'] == 1
    assert report['languages']['python']['avg_complexity'] == 1.0
