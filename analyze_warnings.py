#!/usr/bin/env python3
"""
Script para analizar el reporte de pyright y encontrar archivos con más warnings
"""
import json
from collections import defaultdict

def analyze_pyright_report():
    try:        # Intentar diferentes codificaciones
        encodings = ['utf-8-sig', 'utf-8', 'utf-16', 'latin-1']
        data = None

        for encoding in encodings:
            try:
                with open('pyright_after_tpv_avanzado.json', 'r', encoding=encoding) as f:
                    data = json.load(f)
                break
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue

        if data is None:
            print("❌ Error: No se pudo leer el archivo con ninguna codificación")
            return

        # Contador de warnings por archivo
        file_warnings = defaultdict(int)

        # Procesar diagnósticos generales
        for diagnostic in data.get('generalDiagnostics', []):
            if diagnostic.get('severity') == 'warning':
                file_path = diagnostic.get('file', '')
                # Extraer solo el nombre del archivo
                file_name = file_path.split('\\')[-1] if '\\' in file_path else file_path.split('/')[-1]
                file_warnings[file_name] += 1

        # Ordenar por número de warnings (descendente)
        sorted_files = sorted(file_warnings.items(), key=lambda x: x[1], reverse=True)

        print("🎯 ANÁLISIS DE WARNINGS POR ARCHIVO")
        print("=" * 50)
        print(f"Total de archivos con warnings: {len(sorted_files)}")
        print(f"Total de warnings: {sum(file_warnings.values())}")
        print()

        print("📊 TOP 15 ARCHIVOS CON MÁS WARNINGS:")
        print("-" * 50)

        for i, (file_name, count) in enumerate(sorted_files[:15], 1):
            print(f"{i:2d}. {file_name:<40} {count:3d} warnings")

        print()
        print("✅ PRÓXIMOS CANDIDATOS PARA OPTIMIZACIÓN:")
        print("-" * 50)

        # Mostrar los próximos 5 archivos más problemáticos
        for i, (file_name, count) in enumerate(sorted_files[:5], 1):
            print(f"🎯 {i}. {file_name} ({count} warnings)")

    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo pyright_current_analysis.json")
    except json.JSONDecodeError:
        print("❌ Error: El archivo JSON está malformado")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    analyze_pyright_report()
