# 🍽️ mesas_area - Submódulo de Gestión de Mesas (TPV)

Breve descripción: Este submódulo contiene la implementación modularizada del área de gestión de mesas para el Terminal Punto de Venta (TPV), siguiendo las políticas de estandarización y organización del proyecto Hefest.

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
mesas_area/
├── mesas_area_main.py     # Clase principal y coordinador
├── mesas_area_header.py   # Header, filtros y estadísticas compactas
├── mesas_area_grid.py     # Grid de mesas y lógica de renderizado
├── mesas_area_stats.py    # KPIs y lógica de estadísticas
├── mesas_area_utils.py    # Utilidades y helpers internos
├── __init__.py           # Importación de submódulo
└── README.md              # Este archivo
```

- Cada archivo implementa una responsabilidad clara y modular.
- La clase principal importa y coordina los subcomponentes.

---

## 📁 Políticas y Estándares

- Cumple con las políticas de estandarización y organización del proyecto (ver README raíz y de cada área).
- Nomenclatura clara, modular y versionada.
- Prohibido duplicar código o romper imports existentes.
- Documentar cualquier excepción funcional en el plan y en este README.
- Mantener trazabilidad de cambios y refactorizaciones.

---

## 🚀 Uso e Integración (opcional)

- Importa la clase principal desde `mesas_area_main.py` para integrar el área de mesas en el TPV.
- Cada submódulo puede ser testeado y extendido de forma independiente.

---

## 📖 Información relevante (opcional)

- Refactorización en progreso (v0.0.13)
- Mejoras UI v0.0.13: chips rápidos, breadcrumb, toggle grid/lista, KPIs compactos con barra de progreso visual.
- Consulta el plan de refactorización: `docs/development/planning/[v0.0.13]_PLAN_REFACTORIZACION_MESAS_AREA_COMPONENTS_EN_PROGRESO.md`
- Para políticas generales, ver README raíz del proyecto.

---

> **Nota:** Si se requiere una excepción funcional, debe documentarse aquí y en el plan correspondiente.
