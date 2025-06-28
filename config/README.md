# ⚙️ config/ - Configuración del sistema

Archivos de configuración por entorno para el sistema Hefest, incluyendo configuraciones de base de datos, UI, logging y servicios.

---

## 📋 Índice de Contenidos

| Sección                                             | Descripción                              |
| --------------------------------------------------- | ---------------------------------------- |
| [🗂️ Estructura](#estructura)                         | Organización interna y tipos de archivos |
| [📁 Políticas y Estándares](#políticas-y-estándares) | Qué se permite y qué no                  |
| [📖 Información relevante](#información-relevante)   | Enlaces y notas                          |

---

## 🗂️ Estructura

```
config/
├── default.json      # Configuración por defecto
├── development.json  # Configuración para desarrollo
├── production.json   # Configuración para producción
└── README.md         # Este archivo
```

- `default.json`: Configuración base
- `development.json`: Configuración para desarrollo
- `production.json`: Configuración para producción

---

## 📁 Políticas y Estándares

- Solo se permiten archivos de configuración por entorno.
- Nomenclatura clara y descriptiva.
- No almacenar aquí código fuente, datos ni documentación de progreso.
- Cumple la política general del proyecto (ver README raíz).

---

## 📖 Información relevante

- Para detalles de uso y estructura de configuración, ver la documentación técnica en `docs/`.
- Si se agregan nuevos entornos, actualizar este README y la estructura.

---

> **Nota:** No incluir aquí detalles de progreso, migraciones ni implementaciones específicas. Toda esa información debe estar en `docs/`.

---

**Cumple con la política de estandarización y organización definida en el README raíz.**
