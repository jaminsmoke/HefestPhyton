# 📚 docs - Documentación y Registros

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
docs/
├── changelog/      # Cambios y versiones
├── development/    # Procesos técnicos y planificación
├── analysis/       # Análisis y revisiones
├── archive/        # Documentos históricos
├── logs/           # Logs y reportes de pruebas
└── ...
```

- Explica brevemente la función de los principales archivos y subcarpetas.

---

## 📁 Políticas y Estándares

- Solo se permite documentación, reportes, análisis y registros históricos.
- Nomenclatura obligatoria: `[vX.X.X]_TIPO_AREA_DESCRIPCION_ESTADO.md`
- Prohibido incluir código fuente, scripts o detalles de progreso/implementación.
- Referencia a la política general en el README raíz.

---

## 🚀 Uso e Integración (opcional)

- Utiliza esta carpeta para almacenar y consultar toda la documentación técnica y registros relevantes del proyecto.
- Consulta los README de cada subcarpeta para detalles específicos.

---

## 📖 Información relevante (opcional)

- Para plantillas y políticas, consulta el README raíz del proyecto.
- Notas y advertencias visuales pueden incluirse aquí si es necesario.

---

> **Nota:** No incluir aquí detalles de progreso, migraciones, ni implementaciones específicas. Toda esa información debe estar en los documentos internos de `docs/`.

---

**Cumple con la política de estandarización y organización definida en el README raíz.**

---

# Documentación Hefest (Sintetizada)

- `changelog/`: Cambios y versiones
- `development/`: Procesos técnicos
- `analysis/`: Análisis y revisiones
- `archive/`: Documentos históricos

## ¿Cómo documentar?
1. Elige la carpeta según el tipo de documento.
2. Sigue la nomenclatura: `[vX.X.X]_TIPO_AREA_DESCRIPCION_ESTADO.md`
3. Consulta el README de la subcarpeta para detalles.

## [v0.0.12] Excepción funcional registrada (28/06/2025)

- **Contexto:**
  - Los métodos de creación de categorías y proveedores no permiten recrear entidades inactivas (soft delete), lo que rompe la idempotencia de los tests y la experiencia de usuario.
- **Plan:**
  - Refactorizar para permitir recrear o reactivar entidades inactivas.
  - Documentado en `docs/development/progress/[v0.0.12]_MIGRACION_TESTS_SCRIPTS_DECISIONES_ESTADO_EN_PROGRESO.md` y marcado con TODO en el código fuente.

---
Para más información, ver README completo si es necesario.
