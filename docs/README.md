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
