#!/usr/bin/env python3
import json
from collections import Counter, defaultdict


def analyze_pylint_results():
    try:
        with open('pylint-results.json', 'r', encoding='utf-16') as f:
            data = json.load(f)
        
        print("="*50)
        print("🔍 PYLINT CODE QUALITY ANALYSIS - RAMA ACTUAL")
        print("="*50)
        
        print(f"📊 Total Issues Encontrados: {len(data)}")
        
        # Contar por tipo de issue
        issue_types = Counter(item['type'] for item in data)
        
        print("\n📈 DISTRIBUCIÓN POR TIPO:")
        for issue_type, count in issue_types.items():
            emoji = {
                'error': '🔴',
                'warning': '🟡', 
                'convention': '🔵',
                'refactor': '🟢',
                'info': 'ℹ️'
            }.get(issue_type, '⚪')
            print(f"  {emoji} {issue_type.upper()}: {count}")
        
        # Top issues más frecuentes
        message_ids = Counter(item['symbol'] for item in data)
        
        print("\n🎯 TOP 10 TIPOS DE ISSUES MÁS FRECUENTES:")
        for symbol, count in message_ids.most_common(10):
            print(f"  • {symbol}: {count} ocurrencias")
        
        # Issues por archivo
        files = defaultdict(int)
        for item in data:
            files[item['path']] += 1
        
        print("\n📂 TOP 10 ARCHIVOS CON MÁS ISSUES:")
        sorted_files = sorted(files.items(), key=lambda x: x[1], reverse=True)
        for filepath, count in sorted_files[:10]:
            filename = filepath.replace('src\\', '').replace('\\', '/')
            print(f"  • {filename}: {count} issues")
        
        # Issues críticos (errores)
        errors = [item for item in data if item['type'] == 'error']
        if errors:
            print(f"\n🚨 ERRORES CRÍTICOS ({len(errors)}):")
            for i, error in enumerate(errors[:5], 1):
                filepath = error['path'].replace('src\\', '').replace('\\', '/')
                print(f"  {i}. {filepath}:{error['line']}")
                print(f"     {error['symbol']}: {error['message']}")
        
        # Warnings importantes
        warnings = [item for item in data if item['type'] == 'warning']
        if warnings:
            print(f"\n⚠️  WARNINGS IMPORTANTES ({len(warnings)}):")
            for i, warning in enumerate(warnings[:5], 1):
                filepath = warning['path'].replace('src\\', '').replace('\\', '/')
                print(f"  {i}. {filepath}:{warning['line']}")
                print(f"     {warning['symbol']}: {warning['message']}")
        
        # Calcular puntuación aproximada
        score = 10 - (len(errors) * 0.1 + len(warnings) * 0.05)
        score = max(0, score)
        
        print(f"\n🏆 PUNTUACIÓN ESTIMADA: {score:.1f}/10")
        
        # Recomendaciones
        print("\n💡 RECOMENDACIONES PRINCIPALES:")
        if 'line-too-long' in [item['symbol'] for item in data]:
            print("  • Configurar límite de línea a 88-100 caracteres")
        if 'unused-import' in [item['symbol'] for item in data]:
            print("  • Limpiar imports no utilizados")
        if 'too-many-locals' in [item['symbol'] for item in data]:
            print("  • Refactorizar funciones con muchas variables locales")
        
    except FileNotFoundError:
        print("❌ No se encontró el archivo pylint-results.json")
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el JSON: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    analyze_pylint_results()
