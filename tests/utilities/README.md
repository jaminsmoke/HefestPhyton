# 🔧 Test Utilities

Herramientas de verificación y diagnóstico para el sistema de tests.

## 📁 Contenido

### Verificación de Base de Datos
- `check_db_status.py` - Verificar estado de la BD
- `check_db_structure.py` - Verificar estructura de tablas
- `verify_db.py` - Verificación general de BD

### Uso

```bash
# Verificar estado de BD
python tests/utilities/check_db_status.py

# Verificar estructura
python tests/utilities/check_db_structure.py
```

## 📝 Nota

Estas utilidades no son tests unitarios sino herramientas de diagnóstico.
Se mantienen separadas de los tests automatizados.