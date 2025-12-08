import argparse
import os
from codecritical.parsers.python_parser import parse_python_file
from codecritical.reporters.json_reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="CodeCritical: A code analysis tool.")
    parser.add_argument('--path', type=str, default='.', help='Path to the repository or file to analyze.')
    parser.add_argument('--lang', type=str, help='Language to analyze (e.g., "python").')
    parser.add_argument('--detect', action='store_true', help='Automatically detect and analyze all supported languages.')
    parser.add_argument('--output', type=str, default='json', help='Output format (json, csv, md, html).')
    parser.add_argument('--report-file', type=str, help='File to write the report to.')

    args = parser.parse_args()

    results = []
    if os.path.isfile(args.path):
        if args.lang == 'python' or args.path.endswith('.py'):
            results.append(parse_python_file(args.path))
    elif os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for file in files:
                filepath = os.path.join(root, file)
                if args.lang == 'python' and file.endswith('.py'):
                    results.append(parse_python_file(filepath))
                elif args.detect and file.endswith('.py'): # Add other languages later
                    results.append(parse_python_file(filepath))

    if args.output == 'json':
        report = generate_report(results, args.path)
        if args.report_file:
            with open(args.report_file, 'w') as f:
                f.write(report)
        else:
            print(report)

if __name__ == '__main__':
    main()
