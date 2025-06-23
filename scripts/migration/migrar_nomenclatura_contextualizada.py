#!/usr/bin/env python
"""
Script de migración: Recrear mesas con nomenclatura contextualizada
Elimina mesas existentes y crea un set estándar con la nueva nomenclatura
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Agregar src al path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from data.db_manager import DatabaseManager
from services.tpv_service import TPVService


def respaldar_mesas_existentes(tpv_service: TPVService) -> dict:
    """Crea un respaldo de las mesas existentes"""
    print("📦 Creando respaldo de mesas existentes...")
    
    mesas_actuales = tpv_service.get_mesas()
    respaldo = {
        "fecha_respaldo": datetime.now().isoformat(),
        "total_mesas": len(mesas_actuales),
        "mesas": []
    }
    
    for mesa in mesas_actuales:
        respaldo["mesas"].append({
            "id": mesa.id,
            "numero": mesa.numero,
            "zona": mesa.zona,
            "capacidad": mesa.capacidad,
            "estado": mesa.estado
        })
    
    # Guardar respaldo en archivo
    backup_file = Path("backup_mesas_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(respaldo, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Respaldo guardado en: {backup_file}")
    print(f"   📊 Mesas respaldadas: {len(mesas_actuales)}")
    
    return respaldo


def limpiar_mesas_existentes(db_manager: DatabaseManager) -> bool:
    """Elimina todas las mesas existentes de la base de datos"""
    print("\n🧹 Limpiando mesas existentes de la base de datos...")
    
    try:
        # Eliminar comandas asociadas primero (integridad referencial)
        comandas_eliminadas = db_manager.execute("DELETE FROM comandas")
        print(f"   🗑️ Comandas eliminadas: {comandas_eliminadas}")
        
        # Eliminar mesas
        mesas_eliminadas = db_manager.execute("DELETE FROM mesas")
        print(f"   🗑️ Mesas eliminadas: {mesas_eliminadas}")
        
        # Resetear secuencia de IDs (SQLite)
        db_manager.execute("DELETE FROM sqlite_sequence WHERE name='mesas'")
        db_manager.execute("DELETE FROM sqlite_sequence WHERE name='comandas'")
        
        print("   ✅ Base de datos limpiada correctamente")
        return True
        
    except Exception as e:
        print(f"   ❌ Error limpiando base de datos: {e}")
        return False


def crear_mesas_estandar(tpv_service: TPVService) -> list:
    """Crea un conjunto estándar de mesas con nomenclatura contextualizada"""
    print("\n✨ Creando mesas estándar con nomenclatura contextualizada...")
    
    # Configuración estándar de mesas para restaurante
    configuracion_mesas = [
        # Terraza - Ambiente exterior
        {"zona": "Terraza", "capacidad": 2, "cantidad": 4},  # T01-T04: Mesas pequeñas
        {"zona": "Terraza", "capacidad": 4, "cantidad": 3},  # T05-T07: Mesas medianas
        {"zona": "Terraza", "capacidad": 6, "cantidad": 2},  # T08-T09: Mesas grandes
        
        # Interior - Comedor principal
        {"zona": "Interior", "capacidad": 2, "cantidad": 3},  # I01-I03: Parejas
        {"zona": "Interior", "capacidad": 4, "cantidad": 5},  # I04-I08: Familias pequeñas
        {"zona": "Interior", "capacidad": 6, "cantidad": 3},  # I09-I11: Familias grandes
        {"zona": "Interior", "capacidad": 8, "cantidad": 2},  # I12-I13: Grupos grandes
        
        # VIP - Área premium
        {"zona": "VIP", "capacidad": 4, "cantidad": 2},      # V01-V02: Exclusivas medianas
        {"zona": "VIP", "capacidad": 6, "cantidad": 2},      # V03-V04: Exclusivas grandes
        {"zona": "VIP", "capacidad": 10, "cantidad": 1},     # V05: Mesa de lujo
        
        # Barra - Zona casual
        {"zona": "Barra", "capacidad": 2, "cantidad": 6},    # B01-B06: Altas individuales
        {"zona": "Barra", "capacidad": 4, "cantidad": 2},    # B07-B08: Altas grupales
        
        # Principal - Área central
        {"zona": "Principal", "capacidad": 4, "cantidad": 4}, # P01-P04: Centrales medianas
        {"zona": "Principal", "capacidad": 6, "cantidad": 2}, # P05-P06: Centrales grandes
    ]
    
    mesas_creadas = []
    total_configuracion = sum(config["cantidad"] for config in configuracion_mesas)
    
    print(f"   📋 Configuración: {len(configuracion_mesas)} tipos de mesa")
    print(f"   🎯 Total mesas a crear: {total_configuracion}")
    
    for config in configuracion_mesas:
        zona = config["zona"]
        capacidad = config["capacidad"]
        cantidad = config["cantidad"]
        
        print(f"\n   🏢 Creando en {zona}:")
        print(f"      Capacidad: {capacidad} personas, Cantidad: {cantidad}")
        
        for i in range(cantidad):
            nueva_mesa = tpv_service.crear_mesa(
                capacidad=capacidad,
                zona=zona
            )
            
            if nueva_mesa:
                mesas_creadas.append(nueva_mesa)
                print(f"      ✅ Mesa {nueva_mesa.numero} creada")
            else:
                print(f"      ❌ Error creando mesa {i+1}")
    
    print(f"\n   🎉 Total mesas creadas: {len(mesas_creadas)}")
    return mesas_creadas


def validar_resultado(tpv_service: TPVService) -> dict:
    """Valida el resultado final de la migración"""
    print("\n🔍 Validando resultado de la migración...")
    
    mesas_finales = tpv_service.get_mesas()
    zonas_stats = {}
    
    for mesa in mesas_finales:
        if mesa.zona not in zonas_stats:
            zonas_stats[mesa.zona] = {"mesas": [], "total": 0}
        
        zonas_stats[mesa.zona]["mesas"].append(mesa)
        zonas_stats[mesa.zona]["total"] += 1
    
    print(f"\n   📊 Resumen final por zonas:")
    total_final = 0
    
    for zona, stats in zonas_stats.items():
        mesas_zona = sorted(stats["mesas"], key=lambda m: m.numero)
        print(f"\n   🏢 {zona} ({stats['total']} mesas):")
        
        for mesa in mesas_zona:
            print(f"      Mesa {mesa.numero} - {mesa.capacidad} personas - {mesa.estado}")
        
        total_final += stats["total"]
    
    print(f"\n   🎯 Total mesas en sistema: {total_final}")
    
    return {
        "total_mesas": total_final,
        "zonas": list(zonas_stats.keys()),
        "nomenclatura_correcta": all(
            mesa.numero.startswith(mesa.zona[0].upper()) 
            for mesa in mesas_finales
        )
    }


def main():
    """Función principal de migración"""
    print("🚀 Iniciando migración: Nomenclatura Contextualizada de Mesas")
    print("=" * 60)
    
    try:
        # Crear instancias
        db_manager = DatabaseManager()
        tpv_service = TPVService(db_manager)
        
        # Paso 1: Respaldar mesas existentes
        respaldo = respaldar_mesas_existentes(tpv_service)
        
        # Confirmación del usuario
        print(f"\n⚠️  ATENCIÓN: Se van a eliminar {respaldo['total_mesas']} mesas existentes")
        print("   y crear un nuevo conjunto con nomenclatura contextualizada.")
        
        confirmacion = input("\n¿Continuar con la migración? (s/N): ").lower().strip()
        
        if confirmacion != 's':
            print("❌ Migración cancelada por el usuario")
            return
        
        # Paso 2: Limpiar base de datos
        if not limpiar_mesas_existentes(db_manager):
            print("❌ Error en la limpieza. Migración abortada.")
            return
        
        # Paso 3: Crear mesas estándar
        mesas_creadas = crear_mesas_estandar(tpv_service)
        
        if not mesas_creadas:
            print("❌ No se pudieron crear las mesas. Verificar configuración.")
            return
        
        # Paso 4: Validar resultado
        resultado = validar_resultado(tpv_service)
        
        # Resumen final
        print("\n" + "=" * 60)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print(f"📦 Mesas respaldadas: {respaldo['total_mesas']}")
        print(f"✨ Mesas creadas: {resultado['total_mesas']}")
        print(f"🏢 Zonas configuradas: {', '.join(resultado['zonas'])}")
        print(f"🎯 Nomenclatura correcta: {'✅ Sí' if resultado['nomenclatura_correcta'] else '❌ No'}")
        
        print("\n🎉 El sistema ahora tiene nomenclatura contextualizada completa!")
        print("🔧 Puedes probar la aplicación para ver los resultados.")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
