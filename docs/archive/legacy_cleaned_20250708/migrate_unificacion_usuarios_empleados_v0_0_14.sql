-- MIGRACIÓN v0.0.14: Unificación de usuarios y empleados
-- Elimina la tabla empleados y actualiza comandas para usar usuario_id
-- 1. Renombrar columna empleado_id a usuario_id en comandas
ALTER TABLE comandas
RENAME TO comandas_old;

CREATE TABLE comandas (
    id INTEGER PRIMARY KEY,
    mesa_id INTEGER,
    usuario_id INTEGER,
    fecha_hora TEXT,
    estado TEXT,
    total REAL,
    FOREIGN KEY (mesa_id) REFERENCES mesas (id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

INSERT INTO
    comandas (
        id,
        mesa_id,
        usuario_id,
        fecha_hora,
        estado,
        total
    )
SELECT
    id,
    mesa_id,
    empleado_id,
    fecha_hora,
    estado,
    total
FROM
    comandas_old;

DROP TABLE comandas_old;

-- 2. Eliminar tabla empleados
DROP TABLE IF EXISTS empleados;

-- 3. (Opcional) Limpiar referencias legacy en otras tablas si existen
-- (No se detectaron otras referencias directas en el análisis actual)
-- Fin de migración
