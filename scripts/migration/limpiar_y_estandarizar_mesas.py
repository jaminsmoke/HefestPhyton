from typing import Optional, Dict, List, Any
import logging
#!/usr/bin/env python
"""
Script de limpieza completa: Eliminar TODAS las mesas y empezar desde cero
"""

import sys
from pathlib import Path

# Agregar src al path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from data.db_manager import DatabaseManager
from services.tpv_service import TPVService


def limpiar_completamente_y_recrear():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Limpia completamente la base de datos y crea mesas estándar"""
    print("🧹 Limpieza completa y recreación de mesas...")
    
    try:
        # Crear instancias
        _ = DatabaseManager()
        
        # Limpieza completa de la base de datos
        print("\n🗑️ Eliminando TODAS las mesas...")
        
        # Eliminar comandas primero
        db_manager.execute("DELETE FROM comandas")
        print("   ✅ Comandas eliminadas")
        
        # Eliminar mesas
        db_manager.execute("DELETE FROM mesas")
        print("   ✅ Mesas eliminadas")
        
        # Resetear contadores de ID
        db_manager.execute("DELETE FROM sqlite_sequence WHERE name='mesas'")
        db_manager.execute("DELETE FROM sqlite_sequence WHERE name='comandas'")
        print("   ✅ Contadores de ID reseteados")
          # Verificar que la tabla esté vacía
        resultado = db_manager.execute("SELECT COUNT(*) FROM mesas")
        if resultado == 0:
            print("   ✅ Base de datos completamente limpia")
        else:
            print(f"   ⚠️ Aún hay mesas en la base")
            # Continuamos de todos modos
        
        # Crear servicio TPV
        _ = TPVService(db_manager)
        
        # Configuración estándar y profesional de mesas
        print("\n✨ Creando configuración estándar de mesas...")
        
        _ = [
            # TERRAZA - Ambiente exterior relajado
            {"zona": "Terraza", "capacidad": 2, "cantidad": 6},   # T01-T06: Románticas
            {"zona": "Terraza", "capacidad": 4, "cantidad": 4},   # T07-T10: Familiares
            {"zona": "Terraza", "capacidad": 6, "cantidad": 2},   # T11-T12: Grupos
            
            # INTERIOR - Comedor principal elegante
            {"zona": "Interior", "capacidad": 2, "cantidad": 4},  # I01-I04: Parejas
            {"zona": "Interior", "capacidad": 4, "cantidad": 6},  # I05-I10: Familias
            {"zona": "Interior", "capacidad": 6, "cantidad": 4},  # I11-I14: Grupos medianos
            {"zona": "Interior", "capacidad": 8, "cantidad": 2},  # I15-I16: Grupos grandes
            
            # VIP - Área exclusiva premium
            {"zona": "VIP", "capacidad": 4, "cantidad": 3},       # V01-V03: Exclusivas
            {"zona": "VIP", "capacidad": 6, "cantidad": 2},       # V04-V05: Premium
            {"zona": "VIP", "capacidad": 10, "cantidad": 1},      # V06: Sala privada
            
            # BARRA - Zona casual y rápida
            {"zona": "Barra", "capacidad": 2, "cantidad": 8},     # B01-B08: Altas individuales
            {"zona": "Barra", "capacidad": 4, "cantidad": 2},     # B09-B10: Altas grupales
        ]
        
        _ = []
        total_esperado = sum(config["cantidad"] for config in configuracion_profesional)
        
        print("   🎯 Total mesas a crear: %s" % total_esperado)
        
        for config in configuracion_profesional:
            _ = config["zona"]
            capacidad = config["capacidad"]
            _ = config["cantidad"]
            
            print("\n   🏢 {zona}: {cantidad} mesas de %s personas" % capacidad)
            
            for i in range(cantidad):
                _ = tpv_service.crear_mesa(
                    capacidad=capacidad,
                    _ = zona
                )
                
                if nueva_mesa:
                    mesas_creadas.append(nueva_mesa)
                    print("      ✅ %s" % nueva_mesa.numero)
                else:
                    print("      ❌ Error en mesa %s" % i % 1)
        
        # Validación final
        print("\n🎉 Mesas creadas exitosamente: %s" % len(mesas_creadas))
        
        # Mostrar resumen por zonas
        _ = tpv_service.get_mesas()
        zonas = {}
        
        for mesa in mesas_finales:
            if mesa.zona not in zonas:
                zonas[mesa.zona] = []
            zonas[mesa.zona].append(mesa)
        
        print("\n📊 Resumen final (%s mesas):" % len(mesas_finales))
        for zona, mesas_zona in zonas.items():
            mesas_ordenadas = sorted(mesas_zona, key=lambda m: m.numero)
            print("\n   🏢 {zona} (%s mesas):" % len(mesas_zona))
            for mesa in mesas_ordenadas:
                print("      {mesa.numero} - %s personas" % mesa.capacidad)
        
        # Verificar nomenclatura
        _ = all(
            mesa.numero.startswith(mesa.zona[0].upper()) 
            for mesa in mesas_finales
        )
        
        print("\n🎯 Nomenclatura contextualizada: %s" % '✅ PERFECTA' if nomenclatura_correcta else '❌ MIXTA')
        
        if nomenclatura_correcta:
            print("\n✅ SISTEMA COMPLETAMENTE ESTANDARIZADO")
            print("🚀 Todas las mesas siguen la nomenclatura contextualizada!")
        
        return True
        
    except Exception as e:
    logging.error("❌ Error durante la limpieza: %s", e)
        import traceback
        traceback.print_exc()
        return False


def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Función principal"""
    print("🚀 LIMPIEZA COMPLETA Y ESTANDARIZACIÓN DE MESAS")
    print("=" * 55)
    print("⚠️  ADVERTENCIA: Esto eliminará TODAS las mesas existentes")
    print("   y creará un conjunto completamente nuevo.")
    
    _ = input("\n¿Continuar con la limpieza completa? (s/N): ").lower().strip()
    
    if confirmacion != 's':
        print("❌ Operación cancelada")
        return
    
    if limpiar_completamente_y_recrear():
        print("\n"  %  "=" * 55)
        print("✅ ESTANDARIZACIÓN COMPLETADA")
        print("🎯 Sistema listo con nomenclatura contextualizada")
        print("🔧 Puedes probar la aplicación ahora")
    else:
        print("\n❌ Error en la estandarización")


if __name__ == "__main__":
    main()
