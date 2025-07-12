#!/usr/bin/env python3
"""
Detector de duplicación de código para Hefest
Analiza la rama actual y detecta código duplicado
"""
import os
import hashlib
from collections import defaultdict, Counter
import ast
import difflib


class CodeDuplicationDetector:
    def __init__(self, min_lines=6, similarity_threshold=0.8):
        self.min_lines = min_lines
        self.similarity_threshold = similarity_threshold
        self.duplications = []
        self.file_stats = {}
        
    def get_python_files(self, directory):
        """Obtiene todos los archivos Python del directorio"""
        python_files = []
        for root, dirs, files in os.walk(directory):
            # Ignorar directorios de cache y tests
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'htmlcov']]
            
            for file in files:
                if file.endswith('.py') and not file.startswith('temp_'):
                    python_files.append(os.path.join(root, file))
        return python_files
    
    def extract_code_blocks(self, filepath):
        """Extrae bloques de código de un archivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    lines = f.readlines()
            except Exception:
                return []
        except Exception:
            return []
        
        blocks = []
        for i in range(len(lines) - self.min_lines + 1):
            block = ''.join(lines[i:i + self.min_lines])
            # Normalizar el bloque (eliminar espacios extra, comentarios básicos)
            normalized = self.normalize_code(block)
            if len(normalized.strip()) > 50:  # Solo bloques significativos
                blocks.append({
                    'content': normalized,
                    'original': block,
                    'file': filepath,
                    'start_line': i + 1,
                    'end_line': i + self.min_lines,
                    'hash': hashlib.md5(normalized.encode()).hexdigest()
                })
        return blocks
    
    def normalize_code(self, code):
        """Normaliza el código para comparación"""
        # Eliminar comentarios de línea completa
        lines = code.split('\n')
        normalized_lines = []
        
        for line in lines:
            # Mantener líneas que no son solo comentarios o espacios
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                # Normalizar espacios pero mantener estructura
                normalized_lines.append(' '.join(stripped.split()))
        
        return '\n'.join(normalized_lines)
    
    def find_exact_duplicates(self, all_blocks):
        """Encuentra duplicados exactos por hash"""
        hash_groups = defaultdict(list)
        
        for block in all_blocks:
            hash_groups[block['hash']].append(block)
        
        duplicates = []
        for hash_key, blocks in hash_groups.items():
            if len(blocks) > 1:
                duplicates.append({
                    'type': 'exact',
                    'blocks': blocks,
                    'hash': hash_key,
                    'similarity': 1.0
                })
        
        return duplicates
    
    def find_similar_blocks(self, all_blocks):
        """Encuentra bloques similares usando difflib"""
        similar_groups = []
        
        # Comparar todos los bloques entre sí
        for i, block1 in enumerate(all_blocks):
            for j, block2 in enumerate(all_blocks[i+1:], i+1):
                if block1['file'] != block2['file']:  # Solo comparar entre archivos diferentes
                    similarity = difflib.SequenceMatcher(
                        None, 
                        block1['content'], 
                        block2['content']
                    ).ratio()
                    
                    if similarity >= self.similarity_threshold:
                        similar_groups.append({
                            'type': 'similar',
                            'blocks': [block1, block2],
                            'similarity': similarity
                        })
        
        return similar_groups
    
    def analyze_directory(self, directory):
        """Analiza un directorio completo"""
        print(f"🔍 Analizando directorio: {directory}")
        
        python_files = self.get_python_files(directory)
        print(f"📁 Encontrados {len(python_files)} archivos Python")
        
        all_blocks = []
        file_block_counts = {}
        
        for filepath in python_files:
            blocks = self.extract_code_blocks(filepath)
            all_blocks.extend(blocks)
            
            rel_path = os.path.relpath(filepath, directory)
            file_block_counts[rel_path] = len(blocks)
            
            # Estadísticas del archivo
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
            except:
                lines = 0
            
            self.file_stats[rel_path] = {
                'lines': lines,
                'blocks': len(blocks)
            }
        
        print(f"📊 Extraídos {len(all_blocks)} bloques de código")
        
        # Encontrar duplicados exactos
        exact_duplicates = self.find_exact_duplicates(all_blocks)
        
        # Encontrar similares (más computacionalmente costoso)
        print("🔍 Buscando similitudes...")
        similar_blocks = self.find_similar_blocks(all_blocks[:1000])  # Limitar para performance
        
        return exact_duplicates, similar_blocks
    
    def generate_report(self, exact_duplicates, similar_blocks):
        """Genera reporte de duplicación"""
        print("="*60)
        print("🔍 REPORTE DE DUPLICACIÓN DE CÓDIGO - RAMA ACTUAL")
        print("="*60)
        
        total_duplicated_lines = 0
        affected_files = set()
        
        print(f"\n📊 RESUMEN:")
        print(f"🎯 Duplicados exactos: {len(exact_duplicates)} grupos")
        print(f"🔍 Similares encontrados: {len(similar_blocks)} pares")
        
        if exact_duplicates:
            print(f"\n🚨 DUPLICADOS EXACTOS ({len(exact_duplicates)} grupos):")
            
            for i, dup in enumerate(exact_duplicates, 1):
                blocks = dup['blocks']
                print(f"\n{i}. Grupo de {len(blocks)} duplicados:")
                
                for block in blocks:
                    rel_path = os.path.relpath(block['file'])
                    print(f"   📁 {rel_path}:{block['start_line']}-{block['end_line']}")
                    affected_files.add(rel_path)
                    total_duplicated_lines += (block['end_line'] - block['start_line'])
                
                # Mostrar una muestra del código duplicado
                sample = blocks[0]['original'][:200].replace('\n', '\\n')
                print(f"   💬 Muestra: {sample}...")
        
        if similar_blocks:
            print(f"\n🔍 BLOQUES SIMILARES ({len(similar_blocks)} pares):")
            
            for i, sim in enumerate(similar_blocks[:10], 1):  # Solo top 10
                similarity = sim['similarity']
                blocks = sim['blocks']
                
                print(f"\n{i}. Similitud {similarity:.1%}:")
                for block in blocks:
                    rel_path = os.path.relpath(block['file'])
                    print(f"   📁 {rel_path}:{block['start_line']}-{block['end_line']}")
        
        # Estadísticas por archivo
        print(f"\n📂 ARCHIVOS MÁS AFECTADOS:")
        file_dup_count = Counter()
        
        for dup in exact_duplicates:
            for block in dup['blocks']:
                rel_path = os.path.relpath(block['file'])
                file_dup_count[rel_path] += 1
        
        for filepath, count in file_dup_count.most_common(10):
            lines = self.file_stats.get(filepath, {}).get('lines', 0)
            print(f"   📄 {filepath}: {count} duplicaciones ({lines} líneas)")
        
        # Métricas finales
        total_files = len(self.file_stats)
        affected_file_count = len(affected_files)
        duplication_percentage = (affected_file_count / total_files) * 100 if total_files > 0 else 0
        
        print(f"\n🎯 MÉTRICAS FINALES:")
        print(f"   📊 Archivos afectados: {affected_file_count}/{total_files} ({duplication_percentage:.1f}%)")
        print(f"   📏 Líneas duplicadas estimadas: {total_duplicated_lines}")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        if len(exact_duplicates) > 10:
            print("   🔴 Alta duplicación detectada - refactorización urgente")
        elif len(exact_duplicates) > 5:
            print("   🟡 Duplicación moderada - considerar refactorización")
        else:
            print("   🟢 Duplicación bajo control")
        
        if affected_file_count > 0:
            print("   🛠️  Crear funciones/clases comunes para código duplicado")
            print("   📦 Considerar extraer utilidades compartidas")
            print("   🔧 Implementar pre-commit hooks para prevenir duplicación")


def main():
    detector = CodeDuplicationDetector(min_lines=6, similarity_threshold=0.85)
    
    # Analizar directorio src
    src_directory = "src"
    if os.path.exists(src_directory):
        exact_duplicates, similar_blocks = detector.analyze_directory(src_directory)
        detector.generate_report(exact_duplicates, similar_blocks)
    else:
        print("❌ Directorio 'src' no encontrado")


if __name__ == "__main__":
    main()
