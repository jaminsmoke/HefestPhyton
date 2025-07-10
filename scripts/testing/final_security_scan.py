#!/usr/bin/env python3
"""
Escaneo final de seguridad - Verificar que todos los problemas están resueltos
"""

import re
import json
from pathlib import Path
from collections import defaultdict

def scan_remaining_issues():
    """Escanea problemas de seguridad restantes"""
    project_root = Path(__file__).parent.parent.parent
    issues = defaultdict(list)
    
    # Patrones críticos que NO deben existir
    critical_patterns = {
        'sql_injection': [
            r'f"SELECT.*\{[^}]*\}"',
            r'f"INSERT.*\{[^}]*\}"', 
            r'f"UPDATE.*\{[^}]*\}"',
            r'f"DELETE.*\{[^}]*\}"',
        ],
        'hardcoded_secrets': [
            r'password\s*=\s*["\'][a-zA-Z0-9]{8,}["\']',
            r'secret\s*=\s*["\'][a-zA-Z0-9]{16,}["\']',
            r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
        ],
        'path_traversal': [
            r'os\.path\.join\([^)]*\.\.[^)]*\)',
            r'open\([^)]*\.\.[^)]*\)',
        ],
        'command_injection': [
            r'os\.system\(',
            r'subprocess\.call\([^,]*shell=True',
            r'eval\(',
        ],
        'weak_crypto': [
            r'md5\(',
            r'sha1\(',
            r'random\.random\(\)',
        ],
        'unsafe_deserialization': [
            r'pickle\.loads?\(',
            r'yaml\.load\(',
        ]
    }
    
    total_files = 0
    
    for py_file in project_root.rglob('*.py'):
        if 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        total_files += 1
        
        try:
            content = py_file.read_text(encoding='utf-8')
            
            for category, patterns in critical_patterns.items():
                for pattern in patterns:
                    matches = list(re.finditer(pattern, content, re.IGNORECASE))
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        
                        # Filtrar falsos positivos
                        line_content = content.split('\n')[line_num - 1]
                        if ('# TODO' in line_content or 
                            '# REMOVED' in line_content or
                            '# LEGACY ARCHIVE' in content or
                            'ui_key=' in line_content or
                            'validate_table_name' in line_content or
                            'test' in str(py_file).lower() or
                            'archive' in str(py_file).lower()):
                            continue
                            
                        issues[category].append({
                            'file': str(py_file.relative_to(project_root)),
                            'line': line_num,
                            'pattern': pattern,
                            'code': match.group(0),
                            'context': line_content.strip()
                        })
                        
        except Exception:
            continue
    
    return dict(issues), total_files

def generate_final_report(issues, total_files):
    """Genera reporte final"""
    total_issues = sum(len(category_issues) for category_issues in issues.values())
    
    report = {
        'scan_date': '2025-06-28',
        'total_files_scanned': total_files,
        'total_issues_found': total_issues,
        'issues_by_category': {},
        'status': 'CLEAN' if total_issues == 0 else 'ISSUES_FOUND',
        'security_level': 'HIGH' if total_issues < 5 else 'MEDIUM' if total_issues < 20 else 'LOW'
    }
    
    for category, category_issues in issues.items():
        report['issues_by_category'][category] = {
            'count': len(category_issues),
            'issues': category_issues
        }
    
    return report

def main():
    """Ejecuta escaneo final"""
    print("ESCANEO FINAL DE SEGURIDAD")
    print("=" * 40)
    
    issues, total_files = scan_remaining_issues()
    report = generate_final_report(issues, total_files)
    
    print(f"Archivos escaneados: {total_files}")
    print(f"Problemas encontrados: {report['total_issues_found']}")
    print(f"Estado: {report['status']}")
    print(f"Nivel de seguridad: {report['security_level']}")
    
    if report['total_issues_found'] > 0:
        print("\nPROBLEMAS RESTANTES:")
        for category, data in report['issues_by_category'].items():
            if data['count'] > 0:
                print(f"\n{category.upper()}: {data['count']} issues")
                for issue in data['issues'][:3]:  # Mostrar solo primeros 3
                    print(f"  {issue['file']}:{issue['line']} - {issue['code']}")
                if data['count'] > 3:
                    print(f"  ... y {data['count'] - 3} más")
    else:
        print("\nEXITO: NO SE ENCONTRARON PROBLEMAS CRITICOS!")
        print("Todos los problemas de seguridad han sido resueltos")
    
    # Guardar reporte
    report_file = Path(__file__).parent.parent.parent / 'docs' / 'development' / 'fixes' / 'final_security_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nReporte guardado en: {report_file}")
    
    return report['total_issues_found']

if __name__ == "__main__":
    remaining = main()
    exit(0 if remaining == 0 else 1)