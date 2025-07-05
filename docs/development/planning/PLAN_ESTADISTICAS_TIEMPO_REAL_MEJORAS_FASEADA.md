# [v0.0.13]_PLAN_ESTADISTICAS_TIEMPO_REAL_MEJORAS_FASEADA_PENDIENTE.md

## Objetivo

Rediseñar y mejorar la sección de “Estadísticas en Tiempo Real” del TPV, enfocándonos en claridad visual, experiencia de usuario, interactividad y extensibilidad futura.

---

## Fase 1: Rediseño Visual y UX Básica
- [ ] Tarjetas KPI más grandes y jerarquizadas (icono, valor, etiqueta)
- [ ] Colores diferenciados por estado (verde, rojo, amarillo, azul)
- [ ] Bordes/sombras para jerarquía visual
- [ ] Contraste alto y fuentes legibles
- [ ] Tooltips enriquecidos con explicación/desglose

## Fase 2: Interactividad y Feedback
- [ ] Animación de actualización (pulse/highlight al cambiar valor)
- [ ] Transición suave de números
- [ ] Indicador de tendencia (flecha o mini-icono)
- [ ] Badge de alerta en métricas críticas
- [ ] Estado de actualización visible (fecha/hora último refresh)

## Fase 3: Funcionalidad Avanzada
- [ ] Refresco manual y automático (botón y temporizador)
- [ ] Drill-down: clic en tarjeta muestra detalle o gráfico
- [ ] Configuración de métricas visibles por usuario
- [ ] Soporte para nuevas métricas (ej: % ocupación, tiempo medio, etc.)
- [ ] Mini-gráfica sparkline en la tarjeta



## Fase 3.5: Rediseño Visual Avanzado de Tarjetas KPI

**IMPORTANTE: Refactor y unificación obligatoria antes de continuar**

> **Diagnóstico técnico (julio 2025):**
>
> Se detectó una duplicidad de widgets para las tarjetas KPI de estadísticas en tiempo real: existen dos implementaciones de `create_ultra_premium_stat` y `create_subcontenedor_metric_cards` (una en `mesas_area_stats.py` y otra en `mesas_area_header.py`). La versión avanzada con microinteracciones, glassmorphism y accesibilidad solo se aplica en TPV si se usa la de `mesas_area_stats.py`. Por compatibilidad histórica, el dashboard administrativo seguía usando la versión antigua, lo que impedía la unificación visual y funcional.
>
> **Plan de cumplimiento:**
> - Unificar el uso de la versión avanzada en ambos contextos.
> - Eliminar la duplicidad y migrar todo a la versión de `mesas_area_stats.py`.
> - Registrar este cambio en el changelog y planificar refactor para v0.0.14.
> - No marcar tareas como completadas hasta que el refactor esté hecho y validado en ambos contextos.
> - Una vez hecho el refactor, revisar qué tareas visuales y de interacción realmente se cumplen y cuáles requieren iteración.

**Tareas visuales a implementar (todas pendientes hasta refactor):**
- [ ] Layout jerárquico y compacto
    - [ ] Definir estructura base de la tarjeta (zonas para icono, valor, tendencia, badge, sparkline, etiqueta, tooltip, estado de actualización)
    - [ ] Probar alineaciones verticales/horizontales y separación clara de secciones
    - [ ] Validar visibilidad y legibilidad de todos los elementos
- [ ] Uso de gradientes, glassmorphism o fondos translúcidos
    - [ ] Prototipar fondo con gradiente suave
    - [ ] Prototipar fondo con efecto glassmorphism
    - [ ] Probar sombras difusas y profundidad visual
- [ ] Iconografía grande y clara
    - [ ] Seleccionar iconos SVG/vectoriales de alta calidad
    - [ ] Ajustar tamaño y contraste del icono principal
    - [ ] Validar nitidez y accesibilidad del icono
- [ ] Separación visual de secciones
    - [ ] Delimitar áreas para valor principal, tendencia, sparkline y badge
    - [ ] Usar líneas sutiles, tarjetas internas o bloques de color
- [ ] Microinteracciones visuales
    - [ ] Animaciones sutiles al pasar el mouse (hover)
    - [ ] Animaciones al actualizar valores
    - [ ] Animaciones al mostrar tooltips
- [ ] Contraste y accesibilidad mejorados
    - [ ] Revisar contraste de textos y símbolos
    - [ ] Realizar pruebas de accesibilidad (WCAG AA/AAA)
- [ ] Animaciones y transiciones suaves
    - [ ] Transiciones para cambios de estado
    - [ ] Transiciones para aparición/desaparición de badges
    - [ ] Transiciones para actualización de la sparkline
- [ ] Integración de mini-gráfica sparkline
    - [ ] Definir fondo propio o destacado para la sparkline
    - [ ] Asegurar que no reste protagonismo al valor principal
- [ ] Tooltip enriquecido y contextual
    - [ ] Diseñar tooltip visualmente destacado
    - [ ] Fondo translúcido y sombra
    - [ ] Mostrar desglose y ayuda contextual
- [ ] Estado de actualización visible pero discreto
    - [ ] Ubicación fija y legible
    - [ ] Añadir icono de reloj o similar

**Notas:**
- Esta fase es solo de diseño visual/UX. No implica cambios funcionales ni de lógica.
- No avanzar ni marcar tareas como completadas hasta que el refactor esté validado en ambos contextos.

---
## Fase 4: Refactor y Accesibilidad
- [ ] Refactorizar cada tarjeta como widget reutilizable/configurable
- [ ] Accesibilidad total: navegación teclado, lectores de pantalla
- [ ] Documentar API interna de los widgets de métricas
- [ ] Tests unitarios y de integración para los componentes

---

## Seguimiento y actualización

- Este documento se irá actualizando y marcando tareas conforme se implementen.
- Añadir comentarios, fechas y responsables en cada fase según avance el desarrollo.
- Notas/contexto relevante se añadirán junto a cada ítem si aplica.

---

**Responsable inicial:** Equipo de UI/UX y Frontend
**Estado:** PENDIENTE/EN PROGRESO
**Versión:** v0.0.13
