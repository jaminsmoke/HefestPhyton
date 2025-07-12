#!/usr/bin/env python3
"""
Script para corregir el PIN del usuario administrador
====================================================

Este script actualiza el PIN del usuario administrador desde "9999" a "1234"
para mantener compatibilidad con las expectativas del usuario.
"""

import sys
import os
import sqlite3
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def fix_admin_pin():
    """Corrige el PIN del usuario administrador"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'hefest.db')
    
    print("🔧 CORRIGIENDO PIN DEL ADMINISTRADOR")
    print("=" * 40)
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar usuario admin actual
        cursor.execute('SELECT id, username, name, password FROM empleados WHERE username = ?', ('admin',))
        admin_user = cursor.fetchone()
        
        if admin_user:
            print(f"✅ Usuario admin encontrado:")
            print(f"   ID: {admin_user[0]}")
            print(f"   Username: {admin_user[1]}")
            print(f"   Nombre: {admin_user[2]}")
            print(f"   PIN actual: {admin_user[3]}")
            
            # Actualizar PIN a 1234
            cursor.execute(
                'UPDATE empleados SET password = ? WHERE username = ?',
                ('1234', 'admin')
            )
            
            # Verificar la actualización
            cursor.execute('SELECT password FROM empleados WHERE username = ?', ('admin',))
            new_pin = cursor.fetchone()[0]
            
            if new_pin == '1234':
                print(f"✅ PIN actualizado correctamente a: {new_pin}")
                
                # Confirmar cambios
                conn.commit()
                print("✅ Cambios guardados en la base de datos")
                
                # Log del cambio
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"📝 Cambio registrado: {timestamp}")
                
            else:
                print(f"❌ Error: El PIN no se actualizó correctamente")
                return False
                
        else:
            print("❌ Usuario admin no encontrado en la base de datos")
            
            # Mostrar usuarios existentes
            cursor.execute('SELECT username, name FROM empleados')
            users = cursor.fetchall()
            print(f"\n📋 Usuarios existentes ({len(users)}):")
            for user in users:
                print(f"   - {user[0]} ({user[1]})")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_auth_service():
    """Verifica que el servicio de autenticación funcione con el nuevo PIN"""
    try:
        from services.auth_service import AuthService
        from data.db_manager import DBManager
        
        print("\n🔍 VERIFICANDO AUTENTICACIÓN")
        print("=" * 30)
        
        db = DBManager()
        auth = AuthService(db)
        
        # Probar autenticación con PIN 1234
        result = auth.authenticate_with_pin('admin', '1234')
        
        if result:
            print("✅ Autenticación con PIN 1234: EXITOSA")
            return True
        else:
            print("❌ Autenticación con PIN 1234: FALLIDA")
            
            # Probar con otros PINs para diagnóstico
            pins_to_test = ['9999', '0000', '1111']
            for pin in pins_to_test:
                test_result = auth.authenticate_with_pin('admin', pin)
                status = "✅" if test_result else "❌"
                print(f"   {status} PIN {pin}: {'EXITOSA' if test_result else 'FALLIDA'}")
            
            return False
            
    except Exception as e:
        print(f"❌ Error verificando autenticación: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO CORRECCIÓN DE PIN ADMINISTRADOR")
    print("=" * 50)
    
    # Paso 1: Corregir PIN en base de datos
    if fix_admin_pin():
        print("\n" + "=" * 50)
        
        # Paso 2: Verificar que funciona
        if verify_auth_service():
            print("\n🎉 ¡CORRECCIÓN COMPLETADA EXITOSAMENTE!")
            print("   El PIN del administrador ahora es: 1234")
        else:
            print("\n⚠️  PIN actualizado pero hay problemas con la autenticación")
    else:
        print("\n❌ FALLÓ LA CORRECCIÓN DEL PIN")
    
    print("\n" + "=" * 50)
