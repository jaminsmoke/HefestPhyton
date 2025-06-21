#!/usr/bin/env python3
"""
Analizador de Calidad del Código para Hefest
===========================================

Ejecuta análisis completo de calidad:
- Cobertura de tests
- Complejidad ciclomática
- Duplicación de código
- Métricas de mantenibilidad
- Análisis de seguridad
"""

import subprocess
import sys
import json
import os
from pathlib import Path

class QualityAnalyzer:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.src_dir = self.project_root / "src"
        self.tests_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "reports"
        
        # Crear directorio de reportes
        self.reports_dir.mkdir(exist_ok=True)
        
    def run_tests_with_coverage(self):
        """Ejecuta tests con análisis de cobertura."""
        print("🧪 Ejecutando tests con cobertura...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            str(self.tests_dir),
            "--cov=src",
            "--cov-report=html:reports/coverage_html",
            "--cov-report=json:reports/coverage.json",
            "--cov-report=term",
            "-v"
        ]
        
        result = subprocess.run(cmd, cwd=self.project_root)
        return result.returncode == 0
        
    def analyze_complexity(self):
        """Analiza complejidad ciclomática."""
        print("📊 Analizando complejidad ciclomática...")
        
        try:
            # Instalar radon si no está disponible
            subprocess.run([sys.executable, "-m", "pip", "install", "radon"], 
                         capture_output=True)
            
            # Ejecutar análisis
            cmd = [
                sys.executable, "-m", "radon", "cc", 
                str(self.src_dir), 
                "--json",
                "--average"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                with open(self.reports_dir / "complexity.json", "w") as f:
                    f.write(result.stdout)
                print("✅ Análisis de complejidad completado")
                return True
            else:
                print(f"❌ Error en análisis de complejidad: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error instalando/ejecutando radon: {e}")
            return False
            
    def check_code_duplication(self):
        """Verifica duplicación de código."""
        print("🔍 Verificando duplicación de código...")
        
        try:
            # Instalar jscpd si no está disponible
            subprocess.run(["npm", "install", "-g", "jscpd"], 
                         capture_output=True)
            
            cmd = [
                "jscpd",
                str(self.src_dir),
                "--output", str(self.reports_dir),
                "--format", "json",
                "--min-lines", "5",
                "--languages", "python"
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0:
                print("✅ Análisis de duplicación completado")
                return True
            else:
                print("⚠️ jscpd no disponible, omitiendo análisis de duplicación")
                return False
                
        except Exception as e:
            print(f"⚠️ Error en análisis de duplicación: {e}")
            return False
            
    def analyze_maintainability(self):
        """Analiza índice de mantenibilidad."""
        print("🔧 Analizando mantenibilidad...")
        
        try:
            cmd = [
                sys.executable, "-m", "radon", "mi",
                str(self.src_dir),
                "--json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                with open(self.reports_dir / "maintainability.json", "w") as f:
                    f.write(result.stdout)
                print("✅ Análisis de mantenibilidad completado")
                return True
            else:
                print(f"❌ Error en análisis de mantenibilidad: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error en análisis de mantenibilidad: {e}")
            return False
            
    def security_scan(self):
        """Ejecuta análisis de seguridad."""
        print("🔒 Ejecutando análisis de seguridad...")
        
        try:
            # Instalar bandit si no está disponible
            subprocess.run([sys.executable, "-m", "pip", "install", "bandit"], 
                         capture_output=True)
            
            cmd = [
                sys.executable, "-m", "bandit",
                "-r", str(self.src_dir),
                "-f", "json",
                "-o", str(self.reports_dir / "security.json")
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0:
                print("✅ Análisis de seguridad completado")
                return True
            else:
                print("⚠️ Análisis de seguridad encontró problemas (ver reporte)")
                return False
                
        except Exception as e:
            print(f"❌ Error en análisis de seguridad: {e}")
            return False
            
    def generate_summary_report(self):
        """Genera reporte resumen."""
        print("📋 Generando reporte resumen...")
        
        summary = {
            "timestamp": str(subprocess.run(["date"], capture_output=True, text=True).stdout.strip()),
            "project": "Hefest v0.0.10",
            "analysis": {}
        }
        
        # Leer cobertura
        coverage_file = self.reports_dir / "coverage.json"
        if coverage_file.exists():
            with open(coverage_file) as f:
                coverage_data = json.load(f)
                summary["analysis"]["coverage"] = {
                    "total_coverage": coverage_data.get("totals", {}).get("percent_covered", 0),
                    "lines_covered": coverage_data.get("totals", {}).get("covered_lines", 0),
                    "total_lines": coverage_data.get("totals", {}).get("num_statements", 0)
                }
        
        # Leer complejidad
        complexity_file = self.reports_dir / "complexity.json"
        if complexity_file.exists():
            with open(complexity_file) as f:
                complexity_data = json.load(f)
                # Calcular promedio de complejidad
                total_complexity = 0
                total_functions = 0
                for file_data in complexity_data.values():
                    if isinstance(file_data, list):
                        for item in file_data:
                            if "complexity" in item:
                                total_complexity += item["complexity"]
                                total_functions += 1
                
                avg_complexity = total_complexity / total_functions if total_functions > 0 else 0
                summary["analysis"]["complexity"] = {
                    "average_complexity": round(avg_complexity, 2),
                    "total_functions": total_functions,
                    "quality_grade": self._complexity_grade(avg_complexity)
                }
        
        # Guardar resumen
        with open(self.reports_dir / "quality_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
            
        # Mostrar resumen en consola
        self._print_summary(summary)
        
    def _complexity_grade(self, avg_complexity):
        """Asigna grado basado en complejidad promedio."""
        if avg_complexity <= 5:
            return "A (Excelente)"
        elif avg_complexity <= 10:
            return "B (Bueno)"
        elif avg_complexity <= 20:
            return "C (Aceptable)"
        elif avg_complexity <= 30:
            return "D (Necesita mejora)"
        else:
            return "F (Crítico)"
            
    def _print_summary(self, summary):
        """Imprime resumen formateado."""
        print("\n" + "="*50)
        print("📊 REPORTE DE CALIDAD - HEFEST v0.0.10")
        print("="*50)
        
        if "coverage" in summary["analysis"]:
            cov = summary["analysis"]["coverage"]
            print(f"🧪 Cobertura de Tests: {cov['total_coverage']:.1f}%")
            print(f"   Líneas cubiertas: {cov['lines_covered']}/{cov['total_lines']}")
            
        if "complexity" in summary["analysis"]:
            comp = summary["analysis"]["complexity"]
            print(f"📊 Complejidad Promedio: {comp['average_complexity']}")
            print(f"   Grado de Calidad: {comp['quality_grade']}")
            print(f"   Total Funciones: {comp['total_functions']}")
            
        print(f"\n📁 Reportes detallados en: {self.reports_dir}")
        print("="*50)
        
    def run_full_analysis(self):
        """Ejecuta análisis completo."""
        print("🚀 Iniciando análisis completo de calidad...")
        
        results = {
            "tests_coverage": self.run_tests_with_coverage(),
            "complexity": self.analyze_complexity(),
            "duplication": self.check_code_duplication(),
            "maintainability": self.analyze_maintainability(),
            "security": self.security_scan()
        }
        
        # Generar reporte resumen
        self.generate_summary_report()
        
        # Mostrar resultados
        print("\n🎯 Resultados del Análisis:")
        for check, passed in results.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check.replace('_', ' ').title()}")
            
        all_passed = all(results.values())
        if all_passed:
            print("\n🎉 ¡Todos los análisis completados exitosamente!")
        else:
            print("\n⚠️ Algunos análisis requieren atención. Ver reportes detallados.")
            
        return all_passed

def main():
    analyzer = QualityAnalyzer()
    success = analyzer.run_full_analysis()
    
    # Código de salida para CI/CD
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
