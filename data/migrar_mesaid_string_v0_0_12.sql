-- [v0.0.12]_MIGRACION_MESAID_STRING_COMPLETO.sql
-- Script SQL para migrar mesa_id a TEXT en todas las tablas y migrar los datos existentes.

-- 1. Renombrar tablas afectadas
ALTER TABLE comandas RENAME TO comandas_old;
ALTER TABLE reservas RENAME TO reservas_old;

-- 2. Crear nuevas tablas con mesa_id TEXT
CREATE TABLE comandas (
    id INTEGER PRIMARY KEY,
    mesa_id TEXT,
    usuario_id INTEGER,
    fecha_hora TEXT,
    estado TEXT,
    total REAL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE reservas (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER,
    habitacion_id INTEGER,
    mesa_id TEXT,
    fecha_entrada TEXT,
    fecha_salida TEXT,
    estado TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones (id)
);

-- 3. Copiar datos antiguos, convirtiendo mesa_id a string (ej: 1 -> 'T01')
INSERT INTO comandas (id, mesa_id, usuario_id, fecha_hora, estado, total)
SELECT id, 'T' || printf('%02d', mesa_id), usuario_id, fecha_hora, estado, total FROM comandas_old;

INSERT INTO reservas (id, cliente_id, habitacion_id, mesa_id, fecha_entrada, fecha_salida, estado)
SELECT id, cliente_id, habitacion_id, CASE WHEN mesa_id IS NOT NULL THEN 'T' || printf('%02d', mesa_id) ELSE NULL END, fecha_entrada, fecha_salida, estado FROM reservas_old;

-- 4. Eliminar tablas temporales
DROP TABLE comandas_old;
DROP TABLE reservas_old;
