# 🔍 analysis - Scripts de Análisis

Breve descripción del propósito de la carpeta y su rol en la estructura del proyecto.

---

## 📋 Índice de Contenidos

| Sección                                             | Descripción                              |
| --------------------------------------------------- | ---------------------------------------- |
| [🗂️ Estructura](#estructura)                         | Organización interna y tipos de archivos |
| [📁 Políticas y Estándares](#políticas-y-estándares) | Qué se permite y qué no                  |
| [🚀 Uso e Integración](#uso-e-integración)           | Cómo se usa la carpeta (opcional)        |
| [📖 Información relevante](#información-relevante)   | Enlaces y notas (opcional)               |

---

## 🗂️ Estructura

```
scripts/analysis/
├── root_cleanup_analysis.py   # Análisis de archivos en raíz
├── utils_cleanup_analysis.py  # Análisis de utilidades
├── debug_creacion_tarjetas.py # Debug de creación de tarjetas (migrado desde raíz)
├── debug_profundo_tarjetas.py # Diagnóstico profundo de tarjetas (migrado desde raíz)
└── ...
```

- Explica brevemente la función de los principales archivos y subcarpetas.
- Los scripts `debug_creacion_tarjetas.py` y `debug_profundo_tarjetas.py` fueron movidos desde la raíz en la limpieza v0.0.13 (histórico). A partir de la versión 0.0.14, toda reubicación o limpieza se documenta bajo la nueva versión activa.

---

## 📁 Políticas y Estándares

- Solo se permiten scripts de análisis, depuración y generación de reportes.
- Nomenclatura esperada según el tipo de análisis.
- Prohibido incluir código fuente principal, documentación de progreso o detalles de implementación.
- Referencia a la política general en el README raíz.

---

## 🚀 Uso e Integración (opcional)

- Ejecuta los scripts desde la raíz del proyecto según las instrucciones de cada archivo.
- Consulta los README de cada subcarpeta para detalles y comandos específicos.

---

## 📖 Información relevante (opcional)

- Para plantillas y políticas, consulta el README raíz del proyecto.
- Notas y advertencias visuales pueden incluirse aquí si es necesario.

---

> **Nota:** No incluir aquí detalles de progreso, migraciones, ni implementaciones específicas. Toda esa información debe estar en los documentos internos de `docs/`.

---

**Cumple con la política de estandarización y organización definida en el README raíz.**

---
