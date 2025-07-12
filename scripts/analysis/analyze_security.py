#!/usr/bin/env python3
import json

def analyze_bandit_results():
    try:
        with open('bandit-results.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("="*50)
        print("🔍 BANDIT SECURITY ANALYSIS - RAMA ACTUAL")
        print("="*50)
        
        metrics = data['metrics']['_totals']
        results = data['results']
        
        print(f"📊 Total Issues Encontrados: {len(results)}")
        print(f"📏 Líneas de Código Analizadas: {metrics['loc']:,}")
        print(f"🔴 Alta Confianza: {metrics['CONFIDENCE.HIGH']}")
        print(f"🟡 Media Confianza: {metrics['CONFIDENCE.MEDIUM']}")
        print(f"🟢 Baja Confianza: {metrics['CONFIDENCE.LOW']}")
        print(f"🚨 Severidad Media: {metrics['SEVERITY.MEDIUM']}")
        print(f"⚠️  Severidad Baja: {metrics['SEVERITY.LOW']}")
        
        print("\n" + "="*50)
        print("🎯 TOP 10 ISSUES DE SEGURIDAD")
        print("="*50)
        
        for i, issue in enumerate(results[:10], 1):
            severity = issue['issue_severity']
            confidence = issue['issue_confidence']
            test_name = issue['test_name']
            filename = issue['filename'].replace('\\', '/')
            line_number = issue['line_number']
            
            # Emojis según severidad
            severity_emoji = "🔴" if severity == "HIGH" else "🟡" if severity == "MEDIUM" else "🟢"
            
            print(f"{i:2d}. {severity_emoji} {test_name}")
            print(f"    📁 {filename}:{line_number}")
            print(f"    🎯 Severidad: {severity} | Confianza: {confidence}")
            print(f"    💬 {issue['issue_text'][:100]}...")
            print()
        
        # Agrupar por tipo de issue
        issue_types = {}
        for issue in results:
            test_name = issue['test_name']
            if test_name not in issue_types:
                issue_types[test_name] = 0
            issue_types[test_name] += 1
        
        print("="*50)
        print("📈 TIPOS DE ISSUES MÁS FRECUENTES")
        print("="*50)
        
        for test_name, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
            print(f"• {test_name}: {count} ocurrencias")
        
    except FileNotFoundError:
        print("❌ No se encontró el archivo bandit-results.json")
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el JSON: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    analyze_bandit_results()
