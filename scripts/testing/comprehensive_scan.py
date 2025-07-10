#!/usr/bin/env python3
"""
Escaneo comprensivo de todos los tipos de problemas: medium, low, info
"""

import re
import json
from pathlib import Path
from collections import defaultdict

def scan_all_issues():
    """Escanea todos los tipos de problemas restantes"""
    project_root = Path(__file__).parent.parent.parent
    issues = defaultdict(list)
    
    # Patrones por severidad
    patterns = {
        'medium': {
            'unused_imports': [
                r'^import\s+(\w+)(?:\s+as\s+\w+)?$',
                r'^from\s+[\w.]+\s+import\s+[\w,\s]+$'
            ],
            'unused_variables': [
                r'(\w+)\s*=\s*[^=\n]+\n(?!.*\1)',
            ],
            'broad_exceptions': [
                r'except\s*:',
                r'except\s+Exception\s*:',
            ],
            'missing_docstrings': [
                r'def\s+\w+\([^)]*\):\s*\n\s*(?!""")',
                r'class\s+\w+[^:]*:\s*\n\s*(?!""")',
            ]
        },
        'low': {
            'line_too_long': [],  # Se detectará por longitud
            'trailing_whitespace': [
                r'\s+$',
            ],
            'multiple_statements': [
                r';.*\w',
            ],
            'naming_conventions': [
                r'def\s+[A-Z]\w*\(',  # función con mayúscula
                r'class\s+[a-z]\w*:',  # clase con minúscula
            ]
        },
        'info': {
            'todo_comments': [
                r'#\s*TODO',
                r'#\s*FIXME',
                r'#\s*HACK',
            ],
            'debug_prints': [
                r'print\s*\(',
            ],
            'commented_code': [
                r'^\s*#\s*[a-zA-Z_]\w*\s*=',
                r'^\s*#\s*def\s+',
                r'^\s*#\s*if\s+',
            ]
        }
    }
    
    total_files = 0
    
    for py_file in project_root.rglob('*.py'):
        if ('venv' in str(py_file) or 
            '__pycache__' in str(py_file) or
            'archive' in str(py_file).lower()):
            continue
            
        total_files += 1
        
        try:
            content = py_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Detectar líneas muy largas
            for i, line in enumerate(lines, 1):
                if len(line) > 120:
                    issues['low'].append({
                        'type': 'line_too_long',
                        'file': str(py_file.relative_to(project_root)),
                        'line': i,
                        'message': f'Line too long ({len(line)} > 120 characters)'
                    })
            
            # Detectar otros patrones
            for severity, categories in patterns.items():
                for category, pattern_list in categories.items():
                    for pattern in pattern_list:
                        matches = list(re.finditer(pattern, content, re.MULTILINE))
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            
                            # Filtrar falsos positivos
                            if ('test' in str(py_file).lower() or
                                'demo' in str(py_file).lower()):
                                continue
                            
                            issues[severity].append({
                                'type': category,
                                'file': str(py_file.relative_to(project_root)),
                                'line': line_num,
                                'pattern': pattern,
                                'match': match.group(0)[:50]
                            })
                            
        except Exception:
            continue
    
    return dict(issues), total_files

def analyze_unused_imports(project_root):
    """Análisis específico de imports no utilizados"""
    unused_imports = []
    
    for py_file in project_root.rglob('*.py'):
        if ('venv' in str(py_file) or 
            '__pycache__' in str(py_file) or
            'archive' in str(py_file).lower()):
            continue
            
        try:
            content = py_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            imports = []
            code_lines = []
            
            for line in lines:
                if (line.strip().startswith('import ') or 
                    line.strip().startswith('from ')):
                    imports.append(line.strip())
                else:
                    code_lines.append(line)
            
            code_content = '\n'.join(code_lines)
            
            for import_line in imports:
                # Extraer módulo importado
                if 'import ' in import_line:
                    parts = import_line.split('import ')[-1].split(' as ')
                    module = parts[0].strip().split('.')[0]
                    
                    # Verificar si se usa
                    if (module not in code_content and 
                        module not in ['os', 'sys', 'logging', 'json', 're']):  # Comunes
                        unused_imports.append({
                            'file': str(py_file.relative_to(project_root)),
                            'import': import_line,
                            'module': module
                        })
                        
        except Exception:
            continue
    
    return unused_imports

def main():
    """Ejecuta escaneo comprensivo"""
    print("ESCANEO COMPRENSIVO - MEDIUM/LOW/INFO")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent.parent
    issues, total_files = scan_all_issues()
    unused_imports = analyze_unused_imports(project_root)
    
    print(f"Archivos escaneados: {total_files}")
    
    # Resumen por severidad
    for severity in ['medium', 'low', 'info']:
        count = len(issues.get(severity, []))
        print(f"{severity.upper()}: {count} issues")
        
        if count > 0:
            # Agrupar por tipo
            by_type = defaultdict(int)
            for issue in issues[severity]:
                by_type[issue['type']] += 1
            
            for issue_type, type_count in by_type.items():
                print(f"  {issue_type}: {type_count}")
    
    print(f"\nUNUSED IMPORTS: {len(unused_imports)}")
    if unused_imports:
        files_with_unused = set(item['file'] for item in unused_imports)
        print(f"  Archivos afectados: {len(files_with_unused)}")
    
    # Guardar reporte detallado
    report = {
        'scan_date': '2025-06-28',
        'total_files': total_files,
        'issues_by_severity': {
            severity: len(issues.get(severity, []))
            for severity in ['medium', 'low', 'info']
        },
        'unused_imports_count': len(unused_imports),
        'detailed_issues': issues,
        'unused_imports': unused_imports[:50]  # Primeros 50
    }
    
    report_file = project_root / 'docs' / 'development' / 'fixes' / 'comprehensive_scan_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nReporte guardado en: {report_file}")
    
    total_issues = sum(len(issues.get(s, [])) for s in ['medium', 'low', 'info']) + len(unused_imports)
    print(f"\nTOTAL ISSUES ENCONTRADOS: {total_issues}")
    
    return total_issues

if __name__ == "__main__":
    total = main()
    exit(0 if total < 100 else 1)  # Aceptable si < 100 issues menores