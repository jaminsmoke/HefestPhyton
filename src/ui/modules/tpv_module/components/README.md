# 🧩 components - Componentes Reutilizables TPV

Carpeta que agrupa todos los componentes reutilizables, visuales y lógicos del módulo TPV (Terminal Punto de Venta) de Hefest. Su propósito es centralizar, organizar y estandarizar los elementos modulares que conforman la interfaz y lógica avanzada del TPV.

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
components/
├── mesa_widget.py         # Widget visual individual de mesa
├── tpv_dashboard.py       # Dashboard principal del TPV
├── tpv_avanzado/          # Componentes avanzados del TPV (ver README propio)
├── mesas_area/            # Componentes de gestión de áreas y mesas (ver README propio)
├── __init__.py            # Inicialización del módulo
└── README.md              # Este archivo
```

- Cada subcarpeta contiene su propio README siguiendo la plantilla oficial.
- Los archivos principales implementan widgets, paneles o utilidades reutilizables en la UI TPV.

---

## 📁 Políticas y Estándares

- Solo se permite código fuente modular, widgets y utilidades del TPV.
- Prohibido incluir documentación de progreso, migraciones o detalles de implementación aquí.
- Nomenclatura: snake_case para archivos, PascalCase para clases.
- Cada subcarpeta debe tener README propio y cumplir la plantilla oficial.
- No se permite duplicar componentes ni archivos.
- Cumplimiento estricto de la política general del proyecto (ver README raíz).

---

## 🚀 Uso e Integración (opcional)

- Los componentes aquí definidos se importan desde los módulos principales del TPV.
- Ejemplo de importación:
  ```python
  from src.ui.modules.tpv_module.components.mesa_widget import MesaWidget
  ```

---

## 📖 Información relevante (opcional)

- Para detalles de implementación, migraciones o decisiones técnicas, consultar la documentación en `docs/`.
- Para políticas completas, ver README raíz y `.copilot-instructions.md`.

---

> **Nota:** No incluir aquí detalles de progreso, migraciones ni implementaciones específicas. Toda esa información debe estar en `docs/`.

---

**Cumple con la política de estandarización y organización definida en el README raíz.**

---

> Última actualización: 2025-07-07  
> Versión: v0.0.14 (EN DESARROLLO)  
> Responsable: GitHub Copilot
