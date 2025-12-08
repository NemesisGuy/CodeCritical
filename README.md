# 📊 CodeCritical

### 🚀 A Comprehensive Code Analysis Tool

Welcome to **CodeCritical**, a powerful and flexible tool designed to give you in-depth insights into your codebase. Track important metrics like lines of code, functions, classes, and cyclomatic complexity. This tool is designed for developers and teams aiming to measure and improve the quality, maintainability, and readability of their code.

## 🔥 Key Features

- **Multi-Language Support**: Analyze Python code out of the box, with a modular design for easily adding more languages.
- **Core Metrics**: Get a clear picture of your codebase with metrics like:
    - **Lines of Code**: Total, code, comment, and blank lines.
    - **Function & Class Counts**: Understand the structure of your code.
    - **Cyclomatic Complexity**: Measure the complexity of your functions to identify areas for refactoring.
- **CLI Interface**: A simple and powerful command-line interface for running analysis.
- **Structured Reports**: Generate machine-readable JSON reports.
- **CI/CD Integration**: Easily integrate with your CI/CD pipelines to track code quality over time.

## 🛠️ Usage

### Installation

\`\`\`bash
pip install -e .
\`\`\`

### Running Analysis

Analyze a single file:
\`\`\`bash
python -m codecritical.cli --path path/to/your/file.py --lang python
\`\`\`

Analyze a whole directory:
\`\`\`bash
python -m codecritical.cli --path path/to/your/repo --detect
\`\`\`

Generate a JSON report:
\`\`\`bash
python -m codecritical.cli --path . --detect --output json --report-file report.json
\`\`\`

## JSON Report Schema

The tool generates a `codecritical-report.json` file with the following schema:

\`\`\`json
{
  "repo": "name/or/path",
  "date": "2025-12-08T00:00:00Z",
  "summary": {
    "files_scanned": 123,
    "languages": ["python"],
    "total_lines": 45678
  },
  "languages": {
    "python": {
      "files": 12,
      "lines": 3000,
      "functions": 210,
      "avg_complexity": 3.4,
      "top_complex_files": [
        {"path":"app/foo.py","complexity":18}
      ]
    }
  }
}
\`\`\`

## 👨‍💻 Contributing
Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## 👥 Authors

- **Peter Buckingham** - [NemesisGuy](https://github.com/NemesisGuy)
- **Jules** - AI Software Engineer

## 📄 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
