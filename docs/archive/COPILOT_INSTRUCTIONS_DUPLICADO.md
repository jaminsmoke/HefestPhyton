# Instrucciones para Copilot - Políticas de Documentación Hefest

## 🎯 INSTRUCCIÓN PRINCIPAL
**ANTES de crear, mover o modificar cualquier archivo en el proyecto Hefest, SIEMPRE leer primero:**
1. **README raíz** del área correspondiente (ej: `docs/README.md`, `src/README.md`)
2. **README específico** de la carpeta de destino (ej: `docs/development/README.md`)

## 📂 Estructura de Documentación Obligatoria

### docs/ - Directorio Principal
```
docs/
├── README.md                    # 🎯 LEER PRIMERO - Políticas generales
├── changelog/                   # 📝 Cambios por versión
├── development/                 # 🔧 Procesos técnicos y desarrollo
├── analysis/                    # 🔍 Análisis y investigación  
└── archive/                     # 📦 Documentos archivados
```

### src/ - Código Fuente
```
src/
├── README.md                    # 🎯 LEER PRIMERO - Arquitectura del código
├── services/                    # 🛠️ Servicios de negocio
├── ui/                          # 🖥️ Interfaz de usuario
├── utils/                       # 🔧 Utilidades y helpers
└── core/                        # ⚡ Funcionalidades centrales
```

## 📝 Políticas de Nomenclatura OBLIGATORIAS

### Formato Universal con Versionado
```
[v{VERSION}]_[TIPO]_[ÁREA]_[DESCRIPCIÓN]_[ESTADO].md
```

**Ejemplos Correctos**:
- `[v0.0.13]_MIGRACION_DATOS_REALES_COMPLETADA.md`
- `[v0.0.14]_FIX_INVENTARIO_SERVICE_DUPLICACIÓN.md`
- `[v0.0.14]_PLAN_REFACTORIZACION_UI_COMPONENTS.md`

### Tipos de Documento por Carpeta

#### docs/development/
- `[v{VERSION}]_IMPLEMENTACION_` - Procesos de implementación
- `[v{VERSION}]_PLAN_` - Documentos de planificación  
- `[v{VERSION}]_FIX_` - Correcciones específicas
- `[v{VERSION}]_DEPURACION_` - Procesos de debug
- `[v{VERSION}]_PROGRESO_` - Seguimiento de progreso
- `[v{VERSION}]_ESTANDARIZACION_` - Procesos de estandarización
- `[v{VERSION}]_LIMPIEZA_` - Procesos de limpieza

#### docs/analysis/
- `[v{VERSION}]_cleanup_analysis_` - Análisis de limpieza
- `[v{VERSION}]_performance_analysis_` - Análisis de rendimiento
- `[v{VERSION}]_code_review_` - Revisiones de código

#### docs/changelog/
- `vX.X.X.md` - Formato estándar de versiones

## 🗂️ Ubicación por Tipo de Documento

### ✅ docs/development/completed/
**Criterio**: Tareas, procesos o implementaciones **finalizadas exitosamente**
**Ejemplos**: 
- Implementaciones completadas
- Migraciones finalizadas  
- Estandarizaciones completadas
- Limpiezas finalizadas

### 📋 docs/development/planning/
**Criterio**: Documentos de **planificación y estrategia**
**Ejemplos**:
- Planes de estandarización
- Roadmaps técnicos
- Estrategias de migración

### 🔧 docs/development/fixes/
**Criterio**: **Correcciones específicas** y hotfixes
**Ejemplos**:
- Unificación de servicios
- Corrección de duplicados
- Fixes de bugs específicos

### 📊 docs/development/progress/
**Criterio**: **Seguimiento activo** de tareas en curso
**Ejemplos**:
- Estado de proyectos en progreso
- Métricas de avance
- Reportes de estado

### 🔍 docs/analysis/
**Criterio**: **Análisis, investigación y estudios**
**Ejemplos**:
- Estado del sistema
- Análisis de rendimiento
- Investigación técnica

### 📦 docs/archive/
**Criterio**: Documentos **obsoletos o archivados**
**Ejemplos**:
- Documentación obsoleta
- Procesos deprecados
- Referencias históricas

## 🧹 POLÍTICA DE LIMPIEZA AUTOMÁTICA OBLIGATORIA

### 🔥 REGLA CRÍTICA: LIMPIEZA INMEDIATA
**SIEMPRE que se cree un archivo nuevo para reemplazar otro existente, la acción INMEDIATA siguiente debe ser:**

#### Opción A: Backup + Eliminación
1. ✅ **Crear backup** del archivo original en la carpeta de backup correspondiente
2. ✅ **Eliminar archivo original** de la ubicación actual
3. ✅ **Verificar** que no quedan referencias rotas

#### Opción B: Eliminación Directa
1. ✅ **Eliminar archivo original** directamente
2. ✅ **Verificar** que no quedan referencias rotas
3. ✅ **Documentar** la eliminación en el commit/changelog

### 📁 Carpetas de Backup por Área
```
version-backups/
├── v{VERSION}/
│   ├── src/               # Código fuente original
│   ├── docs/              # Documentación original  
│   ├── config/            # Configuraciones originales
│   └── scripts/           # Scripts originales
└── archive/
    ├── deprecated/        # Archivos obsoletos
    ├── replaced/          # Archivos reemplazados
    └── temp/              # Archivos temporales
```

### 🔧 Protocolo de Limpieza
1. **Identificar archivo a reemplazar**
2. **Crear archivo nuevo** con mejoras
3. **INMEDIATAMENTE** después:
   - Hacer backup del original (si es valioso)
   - O eliminar directamente (si no es necesario)
4. **Verificar** que no hay referencias rotas
5. **Actualizar** imports/referencias si es necesario
6. **Documentar** la acción en el changelog

### 🚨 TOLERANCIA CERO A ARCHIVOS HUÉRFANOS
- **NO** dejar archivos duplicados en el sistema
- **NO** crear archivos temporales sin limpieza posterior
- **NO** acumular versiones obsoletas sin archivar
- **SÍ** mantener solo la versión activa y funcional

## ⚠️ VALIDACIONES OBLIGATORIAS

### Antes de Crear un Archivo:
1. ✅ **Leer README raíz** del área (`docs/README.md`, `src/README.md`)
2. ✅ **Leer README específico** de la carpeta de destino
3. ✅ **Verificar nomenclatura** sigue el formato `[v{VERSION}]_TIPO_ÁREA_DESCRIPCIÓN_ESTADO.md`
4. ✅ **Confirmar ubicación** según criterios de cada carpeta
5. ✅ **Verificar que no existe** archivo similar que debería actualizarse
6. ✅ **Planificar limpieza** del archivo que será reemplazado

### Antes de Mover un Archivo:
1. ✅ **Leer políticas** de la carpeta de origen y destino
2. ✅ **Verificar criterios** de ubicación en ambas carpetas
3. ✅ **Confirmar que cumple** con la nomenclatura de destino
4. ✅ **Actualizar referencias** si es necesario
5. ✅ **Limpiar ubicación original** tras mover exitosamente

### Antes de Modificar Estructura:
1. ✅ **Consultar README** de nivel superior
2. ✅ **Verificar impacto** en otros archivos y referencias
3. ✅ **Seguir convenciones** establecidas
4. ✅ **Actualizar documentación** afectada
5. ✅ **Limpiar archivos obsoletos** generados por el cambio

## 🔄 Flujo de Trabajo Recomendado

### Para Nuevos Documentos:
```
1. Identificar tipo de documento
2. Leer README raíz → Leer README específico  
3. Determinar ubicación según criterios
4. Aplicar nomenclatura con versionado
5. Crear archivo en ubicación correcta
6. INMEDIATAMENTE: Limpiar archivo reemplazado (backup + eliminación)
7. Verificar referencias y actualizar si es necesario
8. Actualizar README si es necesario
```

### Para Modificaciones:
```
1. Leer políticas de la carpeta actual
2. Verificar si la modificación afecta la ubicación
3. Si cambia la ubicación: seguir flujo de reubicación
4. Si permanece: aplicar cambios manteniendo coherencia
5. INMEDIATAMENTE: Limpiar archivos obsoletos generados
6. Actualizar documentación relacionada
```

### Para Reemplazos de Archivos:
```
1. Crear nuevo archivo mejorado
2. INMEDIATAMENTE: Aplicar limpieza automática
   - Opción A: Backup + Eliminación del original
   - Opción B: Eliminación directa del original
3. Verificar que no hay referencias rotas
4. Actualizar imports/referencias si es necesario
5. Documentar el cambio en changelog
```

## 📚 Referencias Rápidas

### READMEs Críticos a Consultar:
- `docs/README.md` - **Políticas generales de documentación**
- `docs/development/README.md` - **Procesos técnicos y desarrollo**
- `docs/analysis/README.md` - **Análisis e investigación**
- `src/README.md` - **Arquitectura y estructura del código**
- `src/services/README.md` - **Servicios de negocio**
- `src/ui/README.md` - **Componentes de interfaz**

### Versiones del Proyecto:
- **Actual**: v0.0.13 (usar para documentos nuevos)
- **Formato**: v{MAJOR}.{MINOR}.{PATCH}
- **Ubicación**: Verificar en `package.json` o `src/__version__.py`

## ❌ ERRORES COMUNES A EVITAR

1. **No leer README** antes de crear archivos
2. **Ubicación incorrecta** según tipo de documento  
3. **Nomenclatura inconsistente** sin versionado
4. **Crear archivos en raíz** de docs/ cuando deberían ir en subcarpetas
5. **No verificar duplicados** o archivos similares existentes
6. **No actualizar documentación** relacionada tras cambios
7. **🚨 CRÍTICO: Dejar archivos huérfanos** sin limpiar tras reemplazos
8. **🚨 CRÍTICO: No hacer backup** de archivos importantes antes de eliminar
9. **🚨 CRÍTICO: Acumular versiones obsoletas** sin archivar correctamente

## ✅ CHECKLIST DE VALIDACIÓN

Antes de cualquier acción con archivos:
- [ ] ¿Leí el README raíz del área?
- [ ] ¿Leí el README específico de la carpeta?
- [ ] ¿El nombre sigue el formato `[v{VERSION}]_TIPO_ÁREA_DESCRIPCIÓN_ESTADO.md`?
- [ ] ¿La ubicación es correcta según los criterios?
- [ ] ¿Verifiqué que no existe archivo similar?
- [ ] ¿Actualicé documentación relacionada si es necesario?

### 🧹 CHECKLIST DE LIMPIEZA AUTOMÁTICA

Tras crear archivo de reemplazo:
- [ ] ¿Identifiqué el archivo original a limpiar?
- [ ] ¿Decidí si necesita backup o eliminación directa?
- [ ] ¿Ejecuté la limpieza INMEDIATAMENTE tras crear el nuevo?
- [ ] ¿Verifiqué que no hay referencias rotas?
- [ ] ¿Actualicé imports/referencias si era necesario?
- [ ] ¿Documenté la acción en el changelog?

---

**🎯 RECORDATORIO**: La coherencia y organización del proyecto depende del cumplimiento estricto de estas políticas. Siempre consultar README antes de actuar.
