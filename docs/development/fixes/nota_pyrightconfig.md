# Nota sobre pyrightconfig.json

## Configuración Duplicada

El archivo `pyrightconfig.json` se mantiene en dos ubicaciones:

1. **Raíz del proyecto**: `pyrightconfig.json` - Archivo activo utilizado por VS Code
2. **Carpeta de configuración**: `development-config/pyrightconfig.json` - Copia de referencia

## Justificación

Esta duplicación es intencional y necesaria por las siguientes razones:

1. **Requisito de VS Code**: VS Code/Pylance busca el archivo `pyrightconfig.json` en la raíz del proyecto y no reconoce configuraciones en subdirectorios.

2. **Política del Proyecto**: Según las políticas del proyecto, todas las configuraciones de herramientas deben estar documentadas en `development-config/`.

## Mantenimiento

Para mantener la coherencia:

1. Cualquier cambio en la configuración debe realizarse en ambos archivos.
2. El archivo en `development-config/` incluye un comentario que indica que es una copia de referencia.

## Configuración Actual

La configuración actual incluye:

- Ignorar errores de importación
- Ignorar errores de redefinición de constantes
- Configuración para Python 3.10
- Rutas adicionales para incluir `src`

---

**Nota**: Esta es una excepción a la regla general de centralización de configuraciones, justificada por requisitos técnicos de VS Code.