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
    """Limpia completamente la base de datos y crea mesas estándar"""
    print("🧹 Limpieza completa y recreación de mesas...")
    
    try:
        # Crear instancias
        db_manager = DatabaseManager()
        
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
        tpv_service = TPVService(db_manager)
        
        # Configuración estándar y profesional de mesas
        print("\n✨ Creando configuración estándar de mesas...")
        
        configuracion_profesional = [
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
        
        mesas_creadas = []
        total_esperado = sum(config["cantidad"] for config in configuracion_profesional)
        
        print(f"   🎯 Total mesas a crear: {total_esperado}")
        
        for config in configuracion_profesional:
            zona = config["zona"]
            capacidad = config["capacidad"]
            cantidad = config["cantidad"]
            
            print(f"\n   🏢 {zona}: {cantidad} mesas de {capacidad} personas")
            
            for i in range(cantidad):
                nueva_mesa = tpv_service.crear_mesa(
                    capacidad=capacidad,
                    zona=zona
                )
                
                if nueva_mesa:
                    mesas_creadas.append(nueva_mesa)
                    print(f"      ✅ {nueva_mesa.numero}")
                else:
                    print(f"      ❌ Error en mesa {i+1}")
        
        # Validación final
        print(f"\n🎉 Mesas creadas exitosamente: {len(mesas_creadas)}")
        
        # Mostrar resumen por zonas
        mesas_finales = tpv_service.get_mesas()
        zonas = {}
        
        for mesa in mesas_finales:
            if mesa.zona not in zonas:
                zonas[mesa.zona] = []
            zonas[mesa.zona].append(mesa)
        
        print(f"\n📊 Resumen final ({len(mesas_finales)} mesas):")
        for zona, mesas_zona in zonas.items():
            mesas_ordenadas = sorted(mesas_zona, key=lambda m: m.numero)
            print(f"\n   🏢 {zona} ({len(mesas_zona)} mesas):")
            for mesa in mesas_ordenadas:
                print(f"      {mesa.numero} - {mesa.capacidad} personas")
        
        # Verificar nomenclatura
        nomenclatura_correcta = all(
            mesa.numero.startswith(mesa.zona[0].upper()) 
            for mesa in mesas_finales
        )
        
        print(f"\n🎯 Nomenclatura contextualizada: {'✅ PERFECTA' if nomenclatura_correcta else '❌ MIXTA'}")
        
        if nomenclatura_correcta:
            print("\n✅ SISTEMA COMPLETAMENTE ESTANDARIZADO")
            print("🚀 Todas las mesas siguen la nomenclatura contextualizada!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal"""
    print("🚀 LIMPIEZA COMPLETA Y ESTANDARIZACIÓN DE MESAS")
    print("=" * 55)
    print("⚠️  ADVERTENCIA: Esto eliminará TODAS las mesas existentes")
    print("   y creará un conjunto completamente nuevo.")
    
    confirmacion = input("\n¿Continuar con la limpieza completa? (s/N): ").lower().strip()
    
    if confirmacion != 's':
        print("❌ Operación cancelada")
        return
    
    if limpiar_completamente_y_recrear():
        print("\n" + "=" * 55)
        print("✅ ESTANDARIZACIÓN COMPLETADA")
        print("🎯 Sistema listo con nomenclatura contextualizada")
        print("🔧 Puedes probar la aplicación ahora")
    else:
        print("\n❌ Error en la estandarización")


if __name__ == "__main__":
    main()
