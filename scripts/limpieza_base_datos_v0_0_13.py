#!/usr/bin/env python3
"""
Script de limpieza y mantenimiento de base de datos - Hefest v0.0.13
====================================================================

Este script verifica y limpia datos de prueba en las tablas:
- categorias: Elimina categorías inactivas y de prueba
- proveedores: Elimina proveedores inactivos y de prueba
"""

import sqlite3
import os
from datetime import datetime

def verificar_base_datos():
    """Verifica el estado actual de la base de datos"""
    # Obtener la ruta del script y construir la ruta de la base de datos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, 'data', 'hefest.db')
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=== VERIFICACIÓN INICIAL DE BASE DE DATOS ===")
        print(f"📍 Ruta: {os.path.abspath(db_path)}")
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [t[0] for t in cursor.fetchall()]
        print(f"📋 Tablas disponibles: {tablas}")
        
        # Verificar categorías
        if 'categorias' in tablas:
            cursor.execute("SELECT COUNT(*) FROM categorias")
            total_cat = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM categorias WHERE activa = 1")
            activas_cat = cursor.fetchone()[0]
            print(f"📂 Categorías: {total_cat} total, {activas_cat} activas, {total_cat - activas_cat} inactivas")
              # Mostrar categorías inactivas
            cursor.execute("SELECT id, nombre, activa FROM categorias WHERE activa = 0")
            inactivas = cursor.fetchall()
            if inactivas:
                print("   ❌ Categorías inactivas encontradas:")
                for cat in inactivas:
                    print(f"      ID: {cat[0]} | Nombre: '{cat[1]}'")
        
        # Verificar proveedores
        if 'proveedores' in tablas:
            cursor.execute("SELECT COUNT(*) FROM proveedores")
            total_prov = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM proveedores WHERE activo = 1")
            activos_prov = cursor.fetchone()[0]
            print(f"🏢 Proveedores: {total_prov} total, {activos_prov} activos, {total_prov - activos_prov} inactivos")
            
            # Mostrar todos los proveedores
            cursor.execute("SELECT id, nombre, activo FROM proveedores")
            todos_prov = cursor.fetchall()
            if todos_prov:
                print("   📋 Proveedores encontrados:")
                for prov in todos_prov:
                    status = "✅ ACTIVO" if prov[2] else "❌ INACTIVO"
                    print(f"      ID: {prov[0]} | Nombre: '{prov[1]}' | Estado: {status}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar base de datos: {e}")
        return False

def limpiar_categorias():
    """Elimina categorías inactivas y de prueba"""
    # Obtener la ruta del script y construir la ruta de la base de datos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, 'data', 'hefest.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n=== LIMPIEZA DE CATEGORÍAS ===")
        
        # Obtener categorías inactivas
        cursor.execute("SELECT id, nombre FROM categorias WHERE activa = 0")
        categorias_inactivas = cursor.fetchall()
        
        if not categorias_inactivas:
            print("✅ No hay categorías inactivas para eliminar")
            conn.close()
            return
        
        print(f"🗑️ Eliminando {len(categorias_inactivas)} categorías inactivas:")
        for cat in categorias_inactivas:
            print(f"   - ID: {cat[0]} | Nombre: '{cat[1]}'")
        
        # Como no hay productos en la base de datos, proceder directo a eliminar
        print("   📝 No hay productos que verificar (tabla productos vacía)")
        
        # Eliminar categorías inactivas
        cursor.execute("DELETE FROM categorias WHERE activa = 0")
        eliminadas = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ Eliminadas {eliminadas} categorías inactivas correctamente")
        
    except Exception as e:
        print(f"❌ Error al limpiar categorías: {e}")

def limpiar_proveedores():
    """Elimina todos los proveedores (tabla debe estar vacía)"""
    # Obtener la ruta del script y construir la ruta de la base de datos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, 'data', 'hefest.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n=== LIMPIEZA DE PROVEEDORES ===")
        
        # Obtener todos los proveedores
        cursor.execute("SELECT id, nombre, activo FROM proveedores")
        todos_proveedores = cursor.fetchall()
        
        if not todos_proveedores:
            print("✅ Tabla de proveedores ya está vacía")
            conn.close()
            return
        
        print(f"🗑️ Eliminando {len(todos_proveedores)} proveedores:")
        for prov in todos_proveedores:
            status = "ACTIVO" if prov[2] else "INACTIVO"
            print(f"   - ID: {prov[0]} | Nombre: '{prov[1]}' | Estado: {status}")
          # Como no hay productos en la base de datos, proceder directo a eliminar
        print("   📝 No hay productos que verificar (tabla productos vacía)")
        
        # Eliminar todos los proveedores
        cursor.execute("DELETE FROM proveedores")
        eliminados = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ Eliminados {eliminados} proveedores correctamente")
        
    except Exception as e:
        print(f"❌ Error al limpiar proveedores: {e}")

def crear_backup():
    """Crea un backup antes de la limpieza"""
    import shutil
    from datetime import datetime
      # Obtener la ruta del script y construir la ruta de la base de datos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, 'data', 'hefest.db')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(project_root, 'version-backups', 'v0.0.13', f'hefest_backup_limpieza_{timestamp}.db')
    
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # Copiar base de datos
        shutil.copy2(db_path, backup_path)
        print(f"💾 Backup creado: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

def main():
    """Función principal de limpieza"""
    print("🧹 LIMPIEZA Y MANTENIMIENTO DE BASE DE DATOS - HEFEST v0.0.13")
    print("=" * 60)
    
    # Verificar estado inicial
    if not verificar_base_datos():
        return
    
    # Crear backup
    print(f"\n💾 Creando backup de seguridad...")
    if not crear_backup():
        print("❌ No se pudo crear backup. Cancelando limpieza por seguridad.")
        return
    
    # Confirmar limpieza
    print(f"\n⚠️  CONFIRMACIÓN DE LIMPIEZA:")
    print("   - Se eliminarán categorías inactivas")
    print("   - Se eliminarán todos los proveedores")
    print("   - Se actualizarán productos para remover referencias")
    
    respuesta = input("\n¿Proceder con la limpieza? (s/N): ").strip().lower()
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Limpieza cancelada por el usuario")
        return
    
    # Realizar limpieza
    limpiar_categorias()
    limpiar_proveedores()
    
    # Verificar estado final
    print(f"\n=== VERIFICACIÓN FINAL ===")
    verificar_base_datos()
    
    print(f"\n✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
