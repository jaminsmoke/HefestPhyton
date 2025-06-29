# 🍽️ tpv_avanzado - TPV Avanzado Modularizado

Componente modular para Terminal Punto de Venta con funcionalidades avanzadas de gestión de pedidos, productos y pagos.

---

## 📋 Índice de Contenidos

| Sección                                             | Descripción                              |
| --------------------------------------------------- | ---------------------------------------- |
| [🗂️ Estructura](#estructura)                         | Organización interna y tipos de archivos |
| [📁 Políticas y Estándares](#políticas-y-estándares) | Qué se permite y qué no                  |
| [🚀 Uso e Integración](#uso-e-integración)           | Cómo se usa el componente                |
| [📖 Información relevante](#información-relevante)   | Enlaces y notas                          |

---

## 🗂️ Estructura

```
tpv_avanzado/
├── __init__.py                    # Configuración del paquete
├── tpv_avanzado_main.py          # Componente principal TPV
├── tpv_avanzado_header.py        # Header modularizado
├── tpv_avanzado_productos.py     # Panel de productos y categorías
├── tpv_avanzado_pedido.py        # Panel de pedido y pago
└── README.md                     # Este archivo
```

- **tpv_avanzado_main.py**: Clase principal TPVAvanzado que coordina todos los subcomponentes
- **tpv_avanzado_header.py**: Header con información de mesa y acciones rápidas
- **tpv_avanzado_productos.py**: Panel de productos organizados por categorías
- **tpv_avanzado_pedido.py**: Panel de gestión de pedidos y procesamiento de pagos

---

## 📁 Políticas y Estándares

- Solo se permite código fuente modular del TPV avanzado
- Nomenclatura: `tpv_avanzado_[componente].py`
- Cada archivo debe tener una responsabilidad específica y bien definida
- Prohibido incluir lógica de negocio compleja en archivos de UI
- Separación clara entre presentación y lógica de datos
- Referencia a la política general en el README raíz

---

## 🚀 Uso e Integración

### Importación básica:
```python
from .components.tpv_avanzado import TPVAvanzado

# Crear instancia
tpv_widget = TPVAvanzado(mesa, tpv_service, parent)
```

### Señales disponibles:
- `pedido_completado(mesa_id: int, total: float)`: Emitida al completar un pedido

### Métodos principales:
- `set_mesa(mesa: Mesa)`: Establece la mesa activa
- `nuevo_pedido()`: Inicia un nuevo pedido
- `procesar_pago()`: Procesa el pago del pedido actual

---

## 📖 Información relevante

- Reemplaza al archivo `advanced_tpv_component.py` (respaldado en backups/)
- Integrado con el servicio TPVService para gestión de datos
- Diseño responsive y moderno con gradientes y efectos visuales
- Soporte para múltiples categorías de productos
- Cálculo automático de IVA y totales

---

> **Nota:** Este componente sigue el patrón modular establecido en `mesas_area/` para mantener consistencia en el proyecto.

---

**Cumple con la política de estandarización y organización definida en el README raíz.**