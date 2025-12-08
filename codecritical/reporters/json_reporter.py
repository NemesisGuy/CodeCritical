import json
import datetime

def generate_report(results, repo_path):
    """
    Generates a JSON report from the analysis results.
    """
    summary = {
        'files_scanned': len(results),
        'languages': [],
        'total_lines': 0
    }

    languages = {}

    for result in results:
        if 'error' in result:
            continue

        lang = 'python' # Hardcoded for now
        if lang not in languages:
            languages[lang] = {
                'files': 0,
                'lines': 0,
                'functions': 0,
                'avg_complexity': 0,
                'top_complex_files': []
            }
            summary['languages'].append(lang)

        languages[lang]['files'] += 1
        languages[lang]['lines'] += result['lines']['total']
        languages[lang]['functions'] += result['function_count']

        # This is a simple sum for now, will be averaged later
        languages[lang]['avg_complexity'] += result['avg_complexity']

        if result['avg_complexity'] > 0:
             languages[lang]['top_complex_files'].append({
                'path': result['filepath'],
                'complexity': result['avg_complexity']
            })

    # Calculate average complexity
    for lang in languages:
        if languages[lang]['files'] > 0:
            languages[lang]['avg_complexity'] /= languages[lang]['files']

        # Sort top complex files
        languages[lang]['top_complex_files'].sort(key=lambda x: x['complexity'], reverse=True)
        languages[lang]['top_complex_files'] = languages[lang]['top_complex_files'][:5]


    report = {
        'repo': repo_path,
        'date': datetime.datetime.utcnow().isoformat(),
        'summary': summary,
        'languages': languages
    }

    return json.dumps(report, indent=2)
