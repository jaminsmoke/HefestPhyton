# 📦 data/ - Base de datos y backups

Esta carpeta almacena la base de datos principal, backups y scripts de inicialización de datos para el sistema Hefest.

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
data/
├── hefest.db         # Base de datos principal
├── backups/          # Backups
├── init_db.py        # Script de inicialización
└── README.md         # Este archivo
```

- Base de datos principal (`hefest.db`)
- Backups de la base de datos (`backups/`)
- Scripts de inicialización y migración (`init_db.py`, etc)

---

## 📁 Políticas y Estándares

- Solo se permiten archivos de datos, backups y scripts de inicialización.
- No almacenar aquí código fuente de lógica de negocio ni documentación de progreso.
- Nomenclatura clara y descriptiva.
- Cumple la política general del proyecto (ver README raíz).

---

## 📖 Información relevante

- Los scripts aquí permiten inicializar o migrar la base de datos.
- Para detalles de uso y estructura, ver la documentación técnica en `docs/`.

---

> **Nota:** No incluir aquí detalles de progreso, migraciones ni implementaciones específicas. Toda esa información debe estar en `docs/`.

---

**Cumple con la política de estandarización y organización definida en el README raíz.**
