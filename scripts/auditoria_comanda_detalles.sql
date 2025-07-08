-- Auditoría de líneas de comanda en comanda_detalles
-- 1. Ver las últimas comandas creadas
SELECT * FROM comandas ORDER BY id DESC LIMIT 5;

-- 2. Consultar las líneas de la comanda más reciente (reemplaza <id_de_la_comanda> si es necesario)
SELECT * FROM comanda_detalles WHERE comanda_id = (SELECT id FROM comandas ORDER BY id DESC LIMIT 1);

-- 3. Consultar todas las líneas de comanda existentes
SELECT * FROM comanda_detalles ORDER BY comanda_id DESC, producto_id;
