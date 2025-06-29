# 📦 backups - Backups Temporales

Carpeta para almacenamiento temporal de archivos de código o recursos que requieren resguardo durante procesos de refactorización, migración o cambios mayores.

---

## 📋 Índice de Contenidos

| Sección                                             | Descripción                              |
| --------------------------------------------------- | ---------------------------------------- |
| [🗂️ Estructura](#estructura)                         | Organización interna y tipos de archivos |
| [📁 Políticas y Estándares](#políticas-y-estándares) | Qué se permite y qué no                  |
| [🚀 Proceso de Backup](#proceso-de-backup)           | Cómo realizar y registrar un backup      |
| [📖 Información relevante](#información-relevante)   | Enlaces y notas (opcional)               |

---

## 🗂️ Estructura

```
backups/
├── YYYYMMDD_nombreArchivo_Backup.py   # Backup temporal de archivo
├── ...
├── README.md                         # Este archivo
```

- Cada archivo es una copia exacta del original, con nombre estandarizado.

---

## 📁 Políticas y Estándares

- Solo se permite almacenamiento temporal de archivos de código o recursos.
- Prohibido almacenar documentación definitiva, código fuente activo o archivos de desarrollo final.
- No debe usarse como fuente de imports ni ejecutarse desde aquí.
- Todos los archivos aquí deben ser eliminados o migrados a la documentación oficial (`docs/`) una vez completado el proceso correspondiente.
- Nomenclatura obligatoria: `YYYYMMDD_nombreArchivo_Backup.py` (fecha + nombre original + Backup).
- Registrar cada backup en este README (ver sección siguiente).
- Referencia a la política general en el README raíz.

---

## 🚀 Proceso de Backup

1. Copiar el archivo a respaldar en esta carpeta usando el nombre: `YYYYMMDD_nombreArchivo_Backup.py`.
2. Registrar el backup en la tabla siguiente:

| Fecha      | Archivo original      | Backup generado                       | Motivo/resguardo breve                      |
| ---------- | --------------------- | ------------------------------------- | ------------------------------------------- |
| 2025-06-28 | mesa_widget_simple.py | 20250628_mesa_widget_simple_Backup.py | Refactorización y cumplimiento de políticas |

3. Eliminar el backup cuando ya no sea necesario o migrarlo a `docs/` si requiere trazabilidad histórica.

---

## 📖 Información relevante

- Para políticas completas, ver README raíz y `docs/README.md`.
- Esta carpeta es solo para uso temporal y debe mantenerse limpia y organizada.

---

> **Nota:** No incluir aquí detalles de progreso, migraciones ni implementaciones específicas. Toda esa información debe estar en `docs/`.

---

**Cumple con la política de estandarización y organización definida en el README raíz.**
