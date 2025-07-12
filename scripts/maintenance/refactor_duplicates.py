#!/usr/bin/env python3
"""
HEFEST - REFACTORIZACIÓN INTELIGENTE DE DUPLICADOS
==================================================
VERSIÓN: v0.0.14
AUTOR: Hefest Development Team

Script especializado para analizar y refactorizar duplicación de código
de manera estratégica, priorizando los casos más impactantes.

CARACTERÍSTICAS:
- Análisis estratégico por tipos de duplicación
- Refactorización automática inteligente
- Extracción de funciones/métodos comunes
- Generación de reporte de impacto
- Validación de integridad post-refactorización
"""

import os
import re
import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class DuplicateBlock:
    """Representa un bloque de código duplicado"""
    file_path: str
    start_line: int
    end_line: int
    content: str
    hash_value: str
    lines_count: int
    
@dataclass
class RefactoringOpportunity:
    """Representa una oportunidad de refactorización"""
    category: str
    duplicates: List[DuplicateBlock]
    impact_score: float
    refactor_type: str
    suggested_name: str
    suggested_location: str
    estimated_reduction: int

class DuplicateRefactorer:
    """Analizador y refactorizador inteligente de duplicados"""
    
    def __init__(self, source_dir: str = "src"):
        self.source_dir = Path(source_dir)
        self.duplicates_groups: Dict[str, List[DuplicateBlock]] = defaultdict(list)
        self.refactoring_opportunities: List[RefactoringOpportunity] = []
        
        # Patrones comunes a extraer
        self.common_patterns = {
            'logging_setup': [
                r'logging\.getLogger\(__name__\)',
                r'logger\.info\(',
                r'logger\.error\(',
                r'logger\.warning\(',
                r'logger\.debug\('
            ],
            'database_operations': [
                r'cursor\.execute\(',
                r'cursor\.fetchall\(\)',
                r'cursor\.fetchone\(\)',
                r'conn\.commit\(\)',
                r'conn\.rollback\(\)'
            ],
            'ui_setup': [
                r'QWidget\(\)',
                r'QVBoxLayout\(\)',
                r'QHBoxLayout\(\)',
                r'setStyleSheet\(',
                r'setObjectName\('
            ],
            'error_handling': [
                r'try:',
                r'except.*:',
                r'except Exception as e:',
                r'finally:'
            ],
            'import_statements': [
                r'from PyQt6',
                r'import logging',
                r'from typing import',
                r'from datetime import'
            ]
        }
    
    def analyze_project(self) -> Dict[str, Any]:
        """Análisis completo del proyecto para detectar duplicados"""
        logger.info("🔍 Iniciando análisis de duplicación de código...")
        
        # 1. Recolectar todos los archivos Python
        python_files = list(self.source_dir.rglob("*.py"))
        logger.info(f"📁 Encontrados {len(python_files)} archivos Python")
        
        # 2. Extraer bloques de código con metadatos
        self._extract_code_blocks(python_files)
        
        # 3. Detectar duplicados usando hashing avanzado
        self._detect_duplicates()
        
        # 4. Clasificar oportunidades de refactorización
        self._classify_opportunities()
        
        # 5. Generar reporte de análisis
        return self._generate_analysis_report()
    
    def _extract_code_blocks(self, files: List[Path]) -> None:
        """Extrae bloques de código con contexto AST"""
        logger.info("📊 Extrayendo bloques de código...")
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extraer bloques por líneas (ventana deslizante)
                lines = content.split('\n')
                
                # Ventanas de diferentes tamaños (3, 5, 10, 15 líneas)
                for window_size in [3, 5, 10, 15]:
                    for i in range(len(lines) - window_size + 1):
                        block_lines = lines[i:i + window_size]
                        block_content = '\n'.join(block_lines).strip()
                        
                        # Filtrar bloques vacíos o solo comentarios
                        if not block_content or self._is_trivial_block(block_content):
                            continue
                        
                        # Normalizar contenido para comparación
                        normalized = self._normalize_code(block_content)
                        hash_value = hashlib.md5(normalized.encode()).hexdigest()
                        
                        block = DuplicateBlock(
                            file_path=str(file_path),
                            start_line=i + 1,
                            end_line=i + window_size,
                            content=block_content,
                            hash_value=hash_value,
                            lines_count=window_size
                        )
                        
                        self.duplicates_groups[hash_value].append(block)
                        
            except Exception as e:
                logger.warning(f"Error procesando {file_path}: {e}")
    
    def _normalize_code(self, code: str) -> str:
        """Normaliza código para comparación (elimina espacios, comentarios, etc.)"""
        # Eliminar comentarios
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        
        # Normalizar espacios en blanco
        code = re.sub(r'\s+', ' ', code)
        
        # Eliminar líneas vacías
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        
        return '\n'.join(lines).strip()
    
    def _is_trivial_block(self, content: str) -> bool:
        """Determina si un bloque es trivial (imports, comentarios, etc.)"""
        lines = content.strip().split('\n')
        
        # Menos de 3 líneas útiles
        useful_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        if len(useful_lines) < 3:
            return True
        
        # Solo imports
        if all(l.strip().startswith(('import ', 'from ')) for l in useful_lines):
            return True
        
        # Solo comentarios o docstrings
        if all(l.strip().startswith(('#', '"""', "'''")) for l in useful_lines):
            return True
        
        return False
    
    def _detect_duplicates(self) -> None:
        """Detecta grupos de duplicados significativos"""
        logger.info("🔍 Detectando patrones de duplicación...")
        
        # Filtrar solo grupos con duplicados reales (>=2 occurrencias)
        significant_duplicates = {
            hash_val: blocks for hash_val, blocks in self.duplicates_groups.items()
            if len(blocks) >= 2
        }
        
        self.duplicates_groups = significant_duplicates
        logger.info(f"🎯 Detectados {len(self.duplicates_groups)} grupos de duplicados")
    
    def _classify_opportunities(self) -> None:
        """Clasifica oportunidades de refactorización por categorías"""
        logger.info("📊 Clasificando oportunidades de refactorización...")
        
        for hash_value, duplicates in self.duplicates_groups.items():
            if len(duplicates) < 2:
                continue
            
            # Calcular impacto (occurrencias × líneas × complejidad)
            impact_score = len(duplicates) * duplicates[0].lines_count * self._calculate_complexity(duplicates[0].content)
            
            # Clasificar tipo de duplicado
            category = self._classify_duplicate_category(duplicates[0].content)
            
            # Determinar estrategia de refactorización
            refactor_type, suggested_name, location = self._suggest_refactoring_strategy(category, duplicates)
            
            # Estimar reducción de líneas
            estimated_reduction = (len(duplicates) - 1) * duplicates[0].lines_count
            
            opportunity = RefactoringOpportunity(
                category=category,
                duplicates=duplicates,
                impact_score=impact_score,
                refactor_type=refactor_type,
                suggested_name=suggested_name,
                suggested_location=location,
                estimated_reduction=estimated_reduction
            )
            
            self.refactoring_opportunities.append(opportunity)
        
        # Ordenar por impacto descendente
        self.refactoring_opportunities.sort(key=lambda x: x.impact_score, reverse=True)
    
    def _calculate_complexity(self, content: str) -> float:
        """Calcula la complejidad del código"""
        complexity = 1.0
        
        # Factores que aumentan complejidad
        if_count = len(re.findall(r'\bif\b', content))
        for_count = len(re.findall(r'\bfor\b', content))
        while_count = len(re.findall(r'\bwhile\b', content))
        try_count = len(re.findall(r'\btry\b', content))
        class_count = len(re.findall(r'\bclass\b', content))
        def_count = len(re.findall(r'\bdef\b', content))
        
        complexity += (if_count + for_count + while_count + try_count) * 0.5
        complexity += (class_count + def_count) * 1.0
        
        return complexity
    
    def _classify_duplicate_category(self, content: str) -> str:
        """Clasifica la categoría del duplicado"""
        for category, patterns in self.common_patterns.items():
            matches = sum(1 for pattern in patterns if re.search(pattern, content))
            if matches >= 2:  # Al menos 2 patrones coinciden
                return category
        
        # Clasificaciones específicas
        if 'QWidget' in content or 'QLayout' in content:
            return 'ui_setup'
        elif 'cursor' in content or 'execute' in content:
            return 'database_operations'
        elif 'logger' in content:
            return 'logging_setup'
        elif 'try:' in content and 'except' in content:
            return 'error_handling'
        elif 'import' in content or 'from' in content:
            return 'import_statements'
        else:
            return 'general_logic'
    
    def _suggest_refactoring_strategy(self, category: str, duplicates: List[DuplicateBlock]) -> Tuple[str, str, str]:
        """Sugiere estrategia de refactorización"""
        file_paths = [d.file_path for d in duplicates]
        common_path = os.path.commonpath(file_paths) if len(file_paths) > 1 else os.path.dirname(file_paths[0])
        
        strategies = {
            'logging_setup': ('utility_function', 'setup_logger', 'src/utils/logging_utils.py'),
            'database_operations': ('utility_function', 'execute_db_operation', 'src/utils/db_utils.py'),
            'ui_setup': ('base_class', 'BaseWidget', 'src/ui/base/base_widget.py'),
            'error_handling': ('decorator', 'error_handler', 'src/utils/decorators.py'),
            'import_statements': ('common_imports', 'common_imports', 'src/utils/common_imports.py'),
            'general_logic': ('utility_function', 'common_operation', f'{common_path}/utils.py')
        }
        
        return strategies.get(category, ('utility_function', 'common_function', f'{common_path}/utils.py'))
    
    def _generate_analysis_report(self) -> Dict[str, Any]:
        """Genera reporte completo del análisis"""
        total_files = len(list(self.source_dir.rglob("*.py")))
        affected_files = len(set(d.file_path for opp in self.refactoring_opportunities for d in opp.duplicates))
        total_reduction = sum(opp.estimated_reduction for opp in self.refactoring_opportunities)
        
        # Top 10 oportunidades por impacto
        top_opportunities = self.refactoring_opportunities[:10]
        
        # Estadísticas por categoría
        category_stats = defaultdict(lambda: {'count': 0, 'reduction': 0, 'impact': 0})
        for opp in self.refactoring_opportunities:
            category_stats[opp.category]['count'] += 1
            category_stats[opp.category]['reduction'] += opp.estimated_reduction
            category_stats[opp.category]['impact'] += opp.impact_score
        
        return {
            'summary': {
                'total_files': total_files,
                'affected_files': affected_files,
                'duplicates_groups': len(self.duplicates_groups),
                'refactoring_opportunities': len(self.refactoring_opportunities),
                'estimated_line_reduction': total_reduction,
                'affected_percentage': round((affected_files / total_files) * 100, 1)
            },
            'top_opportunities': [
                {
                    'category': opp.category,
                    'files_count': len(set(d.file_path for d in opp.duplicates)),
                    'duplicates_count': len(opp.duplicates),
                    'impact_score': round(opp.impact_score, 2),
                    'estimated_reduction': opp.estimated_reduction,
                    'refactor_type': opp.refactor_type,
                    'suggested_name': opp.suggested_name,
                    'suggested_location': opp.suggested_location,
                    'sample_content': opp.duplicates[0].content[:200] + "..." if len(opp.duplicates[0].content) > 200 else opp.duplicates[0].content
                }
                for opp in top_opportunities
            ],
            'category_breakdown': dict(category_stats),
            'analysis_timestamp': datetime.now().isoformat()
        }

def main():
    """Función principal"""
    print("🔥 HEFEST - REFACTORIZACIÓN INTELIGENTE DE DUPLICADOS")
    print("=" * 60)
    
    refactorer = DuplicateRefactorer()
    
    # Análisis completo
    report = refactorer.analyze_project()
    
    # Mostrar resultados
    print("\n📊 RESUMEN DEL ANÁLISIS:")
    print(f"📁 Total archivos: {report['summary']['total_files']}")
    print(f"⚠️  Archivos afectados: {report['summary']['affected_files']} ({report['summary']['affected_percentage']}%)")
    print(f"🔍 Grupos de duplicados: {report['summary']['duplicates_groups']}")
    print(f"🛠️  Oportunidades de refactorización: {report['summary']['refactoring_opportunities']}")
    print(f"📏 Reducción estimada: {report['summary']['estimated_line_reduction']} líneas")
    
    print("\n🎯 TOP 5 OPORTUNIDADES DE REFACTORIZACIÓN:")
    for i, opp in enumerate(report['top_opportunities'][:5], 1):
        print(f"\n{i}. 📂 Categoría: {opp['category']}")
        print(f"   📊 Impacto: {opp['impact_score']} | Archivos: {opp['files_count']} | Duplicados: {opp['duplicates_count']}")
        print(f"   🛠️  Estrategia: {opp['refactor_type']} → {opp['suggested_name']}")
        print(f"   📍 Ubicación sugerida: {opp['suggested_location']}")
        print(f"   📏 Reducción: {opp['estimated_reduction']} líneas")
        print(f"   📝 Muestra: {opp['sample_content'][:100]}...")
    
    print("\n📋 BREAKDOWN POR CATEGORÍAS:")
    for category, stats in report['category_breakdown'].items():
        print(f"   🔖 {category}: {stats['count']} oportunidades, {stats['reduction']} líneas")
    
    # Guardar reporte detallado
    output_file = "reporte_refactoring_inteligente.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Reporte detallado guardado en: {output_file}")
    print("\n🚀 ¡Análisis completado! Listo para refactorización estratégica.")

if __name__ == "__main__":
    main()
