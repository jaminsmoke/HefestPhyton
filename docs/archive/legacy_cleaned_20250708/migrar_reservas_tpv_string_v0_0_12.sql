-- [v0.0.12]_MIGRACION_RESERVAS_TPV_STRING.sql
-- Script SQL para migrar la tabla reservas a un modelo TPV puro, eliminando campos de hospedería y añadiendo los de TPV.

-- 1. Renombrar tabla antigua
ALTER TABLE reservas RENAME TO reservas_old;

-- 2. Crear nueva tabla reservas (modelo TPV)

CREATE TABLE reservas (
    id INTEGER PRIMARY KEY,
    mesa_id TEXT,
    cliente TEXT,
    fecha_hora TEXT,
    duracion_min INTEGER,
    estado TEXT,
    notas TEXT,
    telefono TEXT,
    personas INTEGER,
    cliente_id INTEGER,
    fecha_entrada TEXT,
    fecha_salida TEXT
);

-- 3. Migrar datos antiguos (solo mesa_id y estado si existen, el resto queda NULL)

INSERT INTO reservas (
    id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas, cliente_id, fecha_entrada, fecha_salida
)
SELECT
    id,
    CAST(mesa_id AS TEXT),
    cliente,
    fecha_hora,
    duracion_min,
    estado,
    notas,
    telefono,
    personas,
    cliente_id,
    fecha_entrada,
    fecha_salida
FROM reservas_old;

-- 4. Eliminar tabla temporal
DROP TABLE reservas_old;
