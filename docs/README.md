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

- `logs/`: Carpeta para logs y reportes de pruebas.

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



## [v0.0.14] Versión en desarrollo (desde 07/07/2025)

- **Contexto:**
  - Se inicia la fase de desarrollo 0.0.14 tras el cierre de la versión 0.0.13.
  - Todos los cambios y fixes nuevos deben documentarse como parte de la versión 0.0.14.
  - Para información histórica de la v0.0.13, consultar el changelog y fixes de esa versión.

---
### 🛡️ Gestión de usuarios y autenticación en TPV avanzado (v0.0.14)

- **Cambio de usuario en TPV avanzado:**
  - Al intentar cambiar de usuario desde el ComboBox del header, se solicita el PIN del usuario destino.
  - Si el PIN es incorrecto o el usuario no tiene ID válido, se muestra un mensaje de error y se mantiene el usuario original.
  - Todos los intentos fallidos de autenticación quedan registrados en los logs para auditoría y seguridad.
  - El usuario activo se resalta visualmente en el selector.
  - No se bloquean acciones adicionales: cada usuario solo puede realizar las operaciones permitidas por sus permisos.
  - Lógica unificada: ahora todas las operaciones usan únicamente el modelo de usuario (`usuarios`).

**EXCEPCIÓN FUNCIONAL ELIMINADA:**
> Desde v0.0.14, la tabla `empleados` ha sido eliminada y todas las referencias a empleados/empleado_id han sido migradas a usuarios/usuario_id. El sistema de autenticación, permisos y registro de comandas es ahora completamente consistente y unificado.

**Recomendaciones implementadas:**
- Feedback visual claro del usuario activo.
- Registro de intentos fallidos de cambio de usuario.

Para detalles técnicos y flujo completo, ver el roadmap de progreso de v0.0.14.

---
Para información histórica de la v0.0.12, consultar el changelog y fixes de esa versión.

---
Para más información, ver README completo si es necesario.
