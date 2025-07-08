# README - controllers

## Excepción funcional temporal (v0.0.14)

Se ha modificado el constructor de `TPVController` para requerir explícitamente un `db_manager` y así garantizar la persistencia y consistencia de datos en el TPV avanzado. Esta decisión responde a la necesidad crítica de evitar errores de conexión a base de datos y warnings de inicialización sin contexto real de persistencia.

### Detalles de la excepción
- **Razón técnica:** El constructor anterior permitía instanciar `TPVService` sin `db_manager`, lo que generaba errores de persistencia y warnings en el log.
- **Plan de cumplimiento:**
  1. Se ha actualizado el constructor de `TPVController` para requerir `db_manager`.
  2. Se debe revisar y actualizar cualquier instancia de `TPVController` en el futuro para asegurar que reciba el `db_manager` real desde el flujo principal (ej: desde MainWindow).
  3. Se ha dejado un TODO en el código para detectar y corregir cualquier uso sin `db_manager`.
- **Registro:** Esta excepción queda documentada aquí y debe eliminarse en cuanto todo el flujo garantice la inyección de dependencias correctamente.

> TODO: Si se detecta alguna instancia de `TPVController` sin `db_manager`, refactorizar inmediatamente y registrar el cambio aquí.

---

**Versión:** v0.0.14
**Fecha:** 2025-07-07
