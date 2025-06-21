# Instrucciones para Copilot - Proyecto Hefest

## 🎯 INSTRUCCIÓN PRINCIPAL
**ANTES de crear, mover o modificar cualquier archivo, SIEMPRE leer:**
1. **README raíz** del área (`docs/README.md`, `src/README.md`)
2. **README específico** de la carpeta de destino

## � POLÍTICA DE CUMPLIMIENTO RÍGIDO
**Las políticas de estandarización y organización son OBLIGATORIAS y deben aplicarse con RIGOR MÁXIMO.**

### ⚖️ EXCEPCIONES FUNCIONALES PERMITIDAS
**ÚNICAMENTE** se permiten excepciones cuando el cumplimiento estricto compromete la funcionalidad:

#### 🔥 Criterios para Excepciones Críticas:
1. **Imports y Referencias**: Mover/renombrar archivos rompería imports existentes
2. **Funcionalidad Crítica**: Aplicar políticas detendría el sistema productivo
3. **Dependencias Técnicas**: Restricciones de frameworks, librerías o herramientas
4. **Compatibilidad**: Cambios causarían incompatibilidades con código existente

#### 📋 Protocolo de Excepción:
**Cuando sea ABSOLUTAMENTE necesario hacer una excepción:**
1. ✅ **Documentar la razón técnica específica**
2. ✅ **Crear un plan de cumplimiento futuro**  
3. ✅ **Registrar la excepción en el README correspondiente**
4. ✅ **Añadir TODO comment en el código afectado**
5. ✅ **Programar refactorización para cumplir políticas**

## �📝 Nomenclatura Obligatoria
**Formato**: `[v{VERSION}]_TIPO_ÁREA_DESCRIPCIÓN_ESTADO.md`

## 📂 Estructura de docs/
- `changelog/` - Cambios por versión
- `development/` - Procesos técnicos (completed/, planning/, fixes/, progress/)
- `analysis/` - Análisis e investigación  
- `archive/` - Documentos obsoletos

## ⚠️ VALIDACIONES OBLIGATORIAS
1. ✅ Leer README antes de actuar - **SIN EXCEPCIONES**
2. ✅ Verificar nomenclatura con versionado - **OBLIGATORIO**
3. ✅ Confirmar ubicación correcta - **RIGUROSO**
4. ✅ No crear duplicados - **VERIFICACIÓN EXHAUSTIVA**
5. ✅ Documentar excepciones funcionales - **MANDATORIO**

## 🔥 TOLERANCIA CERO
- **NO** hay excepciones por conveniencia
- **NO** hay excepciones por desconocimiento  
- **NO** hay excepciones por falta de tiempo
- **SÍ** hay excepciones por riesgo funcional técnico (documentadas)

**Versión actual**: v0.0.12

Ver `.copilot-instructions.md` para instrucciones completas.
