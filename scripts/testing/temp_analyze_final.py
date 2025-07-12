#!/usr/bin/env python3
"""
Final analysis of Pyright warnings after optimization session.
"""

import json
from pathlib import Path
from collections import Counter


def main():
    # Read the JSON file
    try:
        with open("pyright_final_analysis.json", "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except (UnicodeDecodeError, json.JSONDecodeError):
        with open("pyright_final_analysis.json", "r", encoding="utf-8") as f:
            data = json.load(f)

    # Count warnings by file
    warnings_by_file = Counter()
    warnings_by_rule = Counter()

    for diagnostic in data.get("generalDiagnostics", []):
        file_path = diagnostic.get("file", "")
        rule = diagnostic.get("rule", "unknown")

        # Extract filename only
        file_name = Path(file_path).name
        warnings_by_file[file_name] += 1
        warnings_by_rule[rule] += 1

    # Display results
    print("🎯 ANÁLISIS FINAL DE PYRIGHT - SESIÓN DE OPTIMIZACIÓN 11 JULIO 2025")
    print("=" * 80)
    print(f"Total warnings: {sum(warnings_by_file.values())}")
    print(f"Archivos afectados: {len(warnings_by_file)}")
    if len(warnings_by_file) > 0:
        print(
            f"Promedio por archivo: {sum(warnings_by_file.values()) / len(warnings_by_file):.1f}"
        )
    print(f"Tipos de warning únicos: {len(warnings_by_rule)}")

    print(f"\n📊 TOP 15 ARCHIVOS CON MÁS WARNINGS:")
    print("=" * 70)
    for i, (file_name, count) in enumerate(warnings_by_file.most_common(15), 1):
        print(f"{i:2d}. {file_name:45s} | {count:3d} warnings")

    print(f"\n📊 TOP 10 TIPOS DE WARNINGS MÁS COMUNES:")
    print("=" * 70)
    for i, (rule, count) in enumerate(warnings_by_rule.most_common(10), 1):
        print(f"{i:2d}. {rule:45s} | {count:3d} ocurrencias")


if __name__ == "__main__":
    main()
