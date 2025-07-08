
# 📑 dialogs - Diálogos del módulo TPV

Breve descripción del propósito de la carpeta y su rol en la estructura del módulo TPV.

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
dialogs/
├── reserva_dialog.py      # Diálogo de reservas
├── mesa_dialog.py         # Diálogo de gestión de mesa (sincronización y persistencia real)
├── ...
```

- Explica brevemente la función de los principales archivos y subcarpetas.

---

## 📁 Políticas y Estándares

- Solo se permite código fuente de diálogos modales del TPV.
- Nomenclatura clara y descriptiva.
- Prohibido incluir detalles de progreso, métricas o implementaciones específicas.
- Referencia a la política general en el README raíz.

---

## ⚠️ Excepción funcional registrada: Sincronización y persistencia real de estado de mesa y reservas

**Fecha:** 2025-07-08  
**Archivo:** `mesa_dialog.py`  
**Motivo:** Para garantizar la sincronización y persistencia real del estado de la mesa y sus reservas tras reinicio o cambios externos, se fuerza la consulta directa al servicio/base de datos al inicializar el diálogo, sobrescribiendo cualquier estado temporal en memoria.  
**Protocolo aplicado:**
1. Se documenta aquí la excepción técnica y en el encabezado del archivo.
2. Se refuerza la llamada a refrescar_mesa_desde_bd y obtener_reservas_activas_por_mesa en el constructor.
3. Se añade TODO para refactorización futura si la arquitectura permite una sincronización 100% reactiva solo por eventos.
4. Se mantiene la trazabilidad en changelog y fixes.

---
