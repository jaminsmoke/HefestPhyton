-- Corrige la foreign key de comanda_detalles para que apunte a comandas
PRAGMA foreign_keys=off;

CREATE TABLE IF NOT EXISTS comanda_detalles_tmp (
    id INTEGER PRIMARY KEY,
    comanda_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    precio_unitario REAL(10),
    notas TEXT,
    FOREIGN KEY (comanda_id) REFERENCES comandas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

INSERT INTO comanda_detalles_tmp (id, comanda_id, producto_id, cantidad, precio_unitario, notas)
SELECT id, comanda_id, producto_id, cantidad, precio_unitario, notas FROM comanda_detalles;

DROP TABLE comanda_detalles;
ALTER TABLE comanda_detalles_tmp RENAME TO comanda_detalles;

PRAGMA foreign_keys=on;
