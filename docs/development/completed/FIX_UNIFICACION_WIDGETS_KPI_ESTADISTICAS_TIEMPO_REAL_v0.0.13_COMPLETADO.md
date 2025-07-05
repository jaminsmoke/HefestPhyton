# Plan de refactor para unificación total de widgets KPI (julio 2025)

1. Analizar y listar todas las diferencias funcionales y visuales entre las tarjetas KPI de TPV y dashboard (tooltips, badges, animaciones, API, etc.).
2. Diseñar una API centralizada y flexible para widgets KPI avanzados, que permita:
   - Tooltips enriquecidos y accesibles
   - Badges y estados visuales configurables
   - Microinteracciones y animaciones equivalentes
   - Personalización de métricas y layout
3. Extraer componentes reutilizables (tooltips, badges, animaciones) en funciones o clases independientes.
4. Refactorizar ambos contextos (TPV y dashboard) para usar la nueva API centralizada, eliminando cualquier lógica o estilo duplicado.
5. Validar visual y funcionalmente en ambos contextos, asegurando consistencia y accesibilidad.
6. Documentar la nueva API y actualizar el fix, el plan y el changelog.

> Este plan debe ejecutarse antes de marcar como completada la unificación real de widgets KPI.

---

# [v0.0.13]_FIX_UNIFICACION_WIDGETS_KPI_ESTADISTICAS_TIEMPO_REAL_PENDIENTE.md

## Título
Unificación y refactor de widgets KPI de estadísticas en tiempo real (TPV y dashboard)

## Contexto y diagnóstico
- Se detectó una duplicidad de widgets para las tarjetas KPI de estadísticas en tiempo real: existen dos implementaciones de `create_ultra_premium_stat` y `create_subcontenedor_metric_cards` (una en `mesas_area_stats.py` y otra en `mesas_area_header.py`).
- La versión avanzada (con microinteracciones, glassmorphism, accesibilidad, etc.) solo se aplica en TPV si se usa la de `mesas_area_stats.py`.
- Por compatibilidad histórica, el dashboard administrativo seguía usando la versión antigua, lo que impide la unificación visual y funcional.

## Excepción funcional detectada (julio 2025)
Aunque se eliminó la duplicidad de funciones a nivel de import y uso, persisten diferencias funcionales:
- Los tooltips avanzados solo están implementados en el dashboard, mientras que en TPV siguen siendo simples.
- Algunas microinteracciones, badges y animaciones difieren entre contextos.
- No todas las funciones de las tarjetas KPI del dashboard existen en la versión TPV.
Por lo tanto, la unificación es parcial y se mantiene deuda técnica.

### Checklist de microfuncionalidades pendientes de unificar
- [ ] Tooltips avanzados en ambos contextos
- [ ] Microinteracciones y animaciones equivalentes
- [ ] Badges y estados visuales consistentes
- [ ] API y lógica de tarjetas KPI centralizada y reutilizable

> **TODO:** Documentar y programar el refactor para lograr una unificación total en la siguiente iteración.

## Plan de acción
1. Refactorizar para que ambos contextos (TPV y dashboard) usen la versión avanzada de los widgets desde `mesas_area_stats.py`.
2. Eliminar la duplicidad de código y migrar toda la lógica y estilos a la versión avanzada.
3. Validar visual y funcionalmente en ambos contextos antes de marcar cualquier tarea de mejora como completada.
4. Registrar el cambio en el changelog y actualizar el plan de mejoras.
5. Documentar cualquier excepción funcional temporal si surge durante el refactor.

## TODO
- [x] Unificar imports y uso de widgets en ambos contextos (AVANZADO)
- [x] Eliminar código duplicado
- [ ] Validar visualmente en TPV y dashboard
- [ ] Actualizar changelog y plan
- [ ] Marcar tareas como completadas solo tras validación real

## Notas
- No avanzar en nuevas mejoras visuales o de interacción hasta que el refactor esté finalizado y validado.
- Este fix es obligatorio para cumplir las políticas de estandarización y evitar deuda técnica.

---

## Análisis de diferencias funcionales y visuales (TPV vs Dashboard)

**Tooltips:**
- TPV: Tooltips simples, solo en botones de refresco/configuración.
- Dashboard: Tooltips avanzados, enriquecidos y contextuales en las tarjetas KPI.

**Microinteracciones y animaciones:**
- TPV: Hover y animación básica en el widget principal.
- Dashboard: Microinteracciones más ricas (badges animados, transiciones, tooltips animados).

**Badges y estados visuales:**
- TPV: Badges básicos o ausentes.
- Dashboard: Badges con lógica visual y estados diferenciados.

**API y lógica:**
- TPV: Lógica centralizada en `mesas_area_stats.py`, pero limitada a métricas predefinidas.
- Dashboard: Puede tener lógica extendida, más métricas, y mayor personalización.

**Accesibilidad y glassmorphism:**
- Ambos tienen glassmorphism, pero la accesibilidad avanzada (por ejemplo, tooltips accesibles, navegación teclado) parece más desarrollada en dashboard.

> Este análisis servirá de base para el diseño de la nueva API centralizada y la integración real del fix.

---

## Propuesta de API centralizada para widgets KPI avanzados

```python
class KPIWidget(QFrame):
    def __init__(self, icon, label, value, color, bg_color, tooltip=None, badge=None, trend=None, sparkline=None, 
                 on_click=None, accessible_label=None, animation=None, layout_opts=None, parent=None):
        super().__init__(parent)
        # icon: str o QIcon
        # label: str
        # value: str/int/float
        # color, bg_color: str (hex)
        # tooltip: str o QWidget avanzado
        # badge: dict (texto, color, animación, etc.)
        # trend: dict (valor, icono, color)
        # sparkline: datos para mini-gráfica
        # on_click: callback
        # accessible_label: str (para lectores de pantalla)
        # animation: dict (tipo, duración, etc.)
        # layout_opts: dict (personalización de layout)
        # ...
        # Implementar construcción visual y lógica aquí
```

**Características clave:**
- Tooltips enriquecidos y accesibles (acepta texto o widget personalizado)
- Badges configurables (texto, color, animación)
- Microinteracciones y animaciones equivalentes (hover, click, actualización)
- Personalización de layout y métricas
- Soporte para sparkline y tendencia
- Accesibilidad: label accesible, navegación teclado
- Callback para drill-down o detalles

> Esta API servirá como base para refactorizar ambos contextos y eliminar duplicidad.

---

## Componentes reutilizables a extraer para la nueva arquitectura KPI

- **TooltipAvanzado**: Widget o función para tooltips enriquecidos, accesibles y con soporte de animación.
- **BadgeKPI**: Componente visual para badges configurables (texto, color, animación, icono).
- **AnimacionKPI**: Utilidades para animaciones de hover, actualización de valor, aparición/desaparición de badges, etc.
- **SparklineKPI**: Mini-gráfica integrada en la tarjeta, reutilizable para cualquier métrica.
- **AccesibilidadKPI**: Funciones para navegación por teclado, labels accesibles y soporte para lectores de pantalla.
- **LayoutKPI**: Opciones de layout flexibles para adaptar la tarjeta a distintos contextos (TPV, dashboard, mobile, etc.).

> Cada componente debe ser desacoplado y probado de forma independiente antes de integrarse en la nueva API centralizada.

---

## Estrategia de migración y refactor

1. Crear los componentes reutilizables en un módulo común (`kpi_components.py` o similar).
2. Refactorizar la nueva clase `KPIWidget` para usar estos componentes y exponer una API flexible.
3. Migrar el uso de widgets KPI en TPV y dashboard a la nueva API, eliminando cualquier lógica o estilo duplicado.
4. Validar visual y funcionalmente en ambos contextos.
5. Documentar el uso de la nueva API y los componentes en el README y en este fix.

---

## Consideraciones de compatibilidad y pruebas

- Mantener compatibilidad visual y funcional con las métricas y estilos actuales.
- Probar exhaustivamente en ambos contextos (TPV y dashboard) y en distintos tamaños de pantalla.
- Validar accesibilidad (teclado, lectores de pantalla, contraste, etc.).
- Documentar cualquier excepción funcional temporal que surja durante la migración.

---

> Una vez completada la documentación y el diseño, se procederá a la implementación siguiendo este plan y checklist.

---
**Responsable:** Equipo de UI/UX y Frontend
**Estado:** PENDIENTE
**Fecha:** 2025-07-05
