# 🛠️ services - Servicios del Sistema

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
services/
├── nombre_service.py   # Servicio específico
└── ...
```

- Explica brevemente la función de los principales archivos y subcarpetas.

---

## 📁 Políticas y Estándares

- Solo se permiten archivos de servicios del sistema.
- Nomenclatura: `nombre_service.py`.
- Prohibido incluir código fuente de lógica de negocio fuera de servicios, ni documentación de progreso.
- Referencia a la política general en el README raíz.

---

## 🚀 Uso e Integración (opcional)

- Documenta cada servicio en su docstring.
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

### ⚠️ Excepción funcional registrada (v0.0.12)

- **Archivo:** `tpv_service.py`
- **Motivo:** Se eliminó la emisión redundante de `comanda_actualizada` en `persistir_comanda` para evitar dobles recargas y efectos visuales en la UI. Ahora solo los métodos de alto nivel emiten el evento.
- **Plan de cumplimiento:** Refactorizar para que ningún método de persistencia emita señales globales, solo devuelvan estado. Programar refactorización para versión >= v0.0.13.
- **TODO en código:** Añadido comentario y registro de excepción según protocolo.
- **Documentación:** Ver `docs/development/fixes/[v0.0.12]_FIX_SERVICES_DobleEmisionComandaActualizada_RESUELTO.md`
