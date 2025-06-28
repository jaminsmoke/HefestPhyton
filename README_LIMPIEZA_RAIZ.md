# Limpieza y organización de archivos raíz (v0.0.13)

**Actualización:** 2025-06-28

Se ha realizado una limpieza de archivos sueltos en la raíz del proyecto, moviendo logs y scripts experimentales a carpetas especializadas bajo las políticas de estandarización.

- Se movieron los scripts `debug_creacion_tarjetas.py` y `debug_profundo_tarjetas.py` desde la raíz a `scripts/analysis/` (cumpliendo política de organización, v0.0.13).
- Ver detalles y justificación en `docs/logs/[v0.0.13]_REGISTRO_LIMPIEZA_ARCHIVOS_RAIZ.md`.
- Para cualquier excepción funcional, consultar el plan en `docs/development/planning/[v0.0.13]_PLAN_LIMPIEZA_ORGANIZACION_PROYECTO.md`.

**Estructura recomendada tras la limpieza:**
- `docs/logs/` → Logs, salidas de pruebas, reportes históricos
- `scripts/analysis/` → Scripts de análisis, fixes, investigación
- `scripts/testing/` → Scripts de pruebas manuales o experimentales

Cumple con la política de organización y facilita el mantenimiento futuro.
