# Guía Rápida de Migración a PySide6

Esta guía proporciona instrucciones paso a paso para migrar de PyQt6 a PySide6 en el proyecto Hefest.

## Preparación

### 1. Crear Rama de Desarrollo

```bash
git checkout -b feature/pyside6-migration
```

### 2. Instalar Dependencias

```bash
# Desinstalar PyQt6
pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip

# Instalar PySide6
pip install PySide6

# Actualizar requirements.txt
sed -i 's/PyQt6==.*/PySide6>=6.5.0/g' requirements.txt
```

## Migración Automática

### 1. Ejecutar Script de Migración en Modo Simulación

```bash
python scripts/migration/pyqt_to_pyside_migrator.py src --dry-run --verbose
```

### 2. Ejecutar Migración Real

```bash
python scripts/migration/pyqt_to_pyside_migrator.py src
```

### 3. Verificar Migración

```bash
python scripts/migration/verify_migration.py src --verbose
```

## Ajustes Manuales Comunes

### Diferencias en Señales y Slots

**PyQt6:**
```python
self.button.clicked.connect(self.on_click)  # type: ignore
```

**PySide6:**
```python
self.button.clicked.connect(self.on_click)
```

### Enumeraciones

**PyQt6:**
```python
Qt.AlignmentFlag.AlignRight
QDialog.DialogCode.Accepted
QMessageBox.Icon.Critical
```

**PySide6:**
```python
Qt.AlignRight
QDialog.Accepted
QMessageBox.Critical
```

### Contexto de Mensajes

**PyQt6:**
```python
def handler(_type: QtMsgType, _context: QMessageLogContext, message: str):
    pass
```

**PySide6:**
```python
def handler(_type: QtMsgType, _context: QtMessageLogContext, message: str):
    pass
```

## Pruebas

### 1. Pruebas Unitarias

```bash
python -m unittest discover tests
```

### 2. Pruebas Manuales

Verificar visualmente los siguientes componentes:
- Ventana principal
- Diálogos
- Tablas y vistas
- Menús y barras de herramientas

## Solución de Problemas Comunes

### Error: "No module named 'PySide6'"

**Solución:** Verificar instalación de PySide6
```bash
pip install PySide6
```

### Error: "AttributeError: module 'PySide6.QtCore' has no attribute 'pyqtSignal'"

**Solución:** Reemplazar `pyqtSignal` por `Signal`
```python
from PySide6.QtCore import Signal  # En lugar de pyqtSignal
```

### Error: "TypeError: 'PySide6.QtWidgets.QDialog.DialogCode' object is not callable"

**Solución:** Usar constantes directamente
```python
if dialog.exec() == QDialog.Accepted:  # En lugar de QDialog.DialogCode.Accepted
```

## Finalización

### 1. Actualizar Documentación

```bash
# Actualizar README.md con información sobre PySide6
sed -i 's/PyQt6/PySide6/g' README.md
```

### 2. Commit y Push

```bash
git add .
git commit -m "Migración de PyQt6 a PySide6"
git push origin feature/pyside6-migration
```

### 3. Crear Pull Request

Crear un Pull Request en GitHub para revisar los cambios antes de fusionar con la rama principal.

---

Para más detalles, consultar el [Plan de Migración Completo](plan_migracion_pyside6.md).