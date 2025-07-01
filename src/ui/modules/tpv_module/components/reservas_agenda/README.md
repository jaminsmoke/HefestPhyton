# 📅 reservas_agenda - Agenda y gestión de reservas TPV

Carpeta para componentes, modelos y servicios relacionados con la agenda de reservas del TPV. Cumple la política de modularidad y persistencia centralizada.

---

## 📋 Índice de Contenidos

| Sección                    | Descripción                                 |
|----------------------------|---------------------------------------------|
| [🗂️ Estructura](#estructura) | Organización interna y tipos de archivos    |
| [📁 Políticas](#políticas)   | Qué se permite y qué no                     |
| [🚀 Integración](#integración) | Cómo se usa la carpeta (opcional)           |

---

## 🗂️ Estructura

```
reservas_agenda/
├── reserva_model.py    # Modelo de datos Reserva
├── reserva_service.py  # Servicio centralizado de reservas
├── README.md           # Este archivo
```

---

## 📁 Políticas

- Solo se permite código fuente modular relacionado con reservas.
- Prohibido incluir documentación de progreso, migraciones o detalles de implementación aquí.
- Nomenclatura: snake_case para archivos, PascalCase para clases.
- Cumplir la plantilla oficial de README de carpeta.

---

## 🚀 Integración

- Usar `ReservaService` para toda gestión de reservas.
- Integrar visualización y edición de reservas desde la UI TPV.

---

## Estado

- [v0.0.13] Estructura y servicios implementados. Pendiente UI visual y conexión con widgets de mesa.
