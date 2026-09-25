from __future__ import annotations
import json

def mission_summary(sections):
    warnings = []
    for section, values in sections.items():
        if isinstance(values, dict):
            for key, value in values.items():
                if key.endswith('_ok') and value is False:
                    warnings.append(f'{section}:{key}')
    return {'sections': sections, 'warning_count': len(warnings), 'warnings': warnings}

def markdown_report(summary):
    lines = ['# OrbitForge Mission Analysis', '']
    for name, values in summary['sections'].items():
        lines.append(f'## {name}')
        if isinstance(values, dict):
            for key, value in values.items():
                lines.append(f'- {key}: {value}')
        else:
            lines.append(f'- {values}')
        lines.append('')
    if summary['warnings']:
        lines.append('## Warnings')
        lines.extend((f'- {w}' for w in summary['warnings']))
    return '\n'.join(lines) + '\n'

def json_report(summary):
    return json.dumps(summary, sort_keys=True, indent=2)
