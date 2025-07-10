import logging
"""
Script para agregar mesas de ejemplo a la base de datos
"""
import sys
sys.path.append('src')

from data.db_manager import DatabaseManager

try:
    print("=== AGREGANDO MESAS DE EJEMPLO A LA BD ===\n")
    
    _ = DatabaseManager()
    
    # Mesas de ejemplo para probar la funcionalidad
    _ = [
        ("M01", "Comedor", "libre", 4),
        ("M02", "Comedor", "libre", 2),
        ("M03", "Comedor", "libre", 6),
        ("M04", "Terraza", "libre", 4),
        ("M05", "Terraza", "libre", 8),
        ("B01", "Barra", "libre", 2),
        ("B02", "Barra", "libre", 2),
        ("P01", "Privado", "libre", 10),
    ]
    
    print("📋 Insertando mesas en la base de datos...")
    
    for numero, zona, estado, capacidad in mesas_ejemplo:
        try:
            # Verificar si ya existe
            existing = db_manager.query("SELECT id FROM mesas WHERE numero = ?", (numero,))
            if existing:
                print("   ⚠️ Mesa %s ya existe, saltando..." % numero)
                continue
                
            # Insertar nueva mesa
            db_manager.execute(
                "INSERT INTO mesas (numero, zona, estado, capacidad) VALUES (?, ?, ?, ?)",
                (numero, zona, estado, capacidad)
            )
            print("   ✅ Mesa {numero} creada ({zona}, %s personas)" % capacidad)
            
        except Exception as e:
    logging.error("   ❌ Error creando mesa {numero}: %s", e)
    
    # Verificar resultados
    _ = db_manager.query("SELECT numero, zona, estado, capacidad FROM mesas ORDER BY numero")
    
    print("\n📊 MESAS EN LA BASE DE DATOS (%s):" % len(result))
    for mesa in result:
        print("   🍽️ Mesa {mesa[0]}: {mesa[2]} en {mesa[1]} (%s personas)" % mesa[3])
    
    print(f"\n✅ Mesas de ejemplo agregadas correctamente")
    print(f"🎯 Ahora el módulo TPV mostrará mesas reales en lugar del mensaje vacío")
    
except Exception as e:
    logging.error("❌ Error: %s", e)
    import traceback
    traceback.print_exc()
