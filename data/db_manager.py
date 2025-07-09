import sqlite3
from contextlib import contextmanager
import os

class DatabaseManager:
    def descontar_stock_y_registrar(self, producto_id, cantidad, usuario_id=None, observaciones=None):
        """Descuenta stock de un producto y registra el movimiento en movimientos_stock."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Obtener stock actual
            cursor.execute("SELECT stock FROM productos WHERE id = ?", (producto_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Producto con id {producto_id} no encontrado")
            stock_anterior = row[0] if row[0] is not None else 0
            if stock_anterior < cantidad:
                raise ValueError(f"Stock insuficiente para producto {producto_id}")
            stock_nuevo = stock_anterior - cantidad
            # Actualizar stock
            cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (stock_nuevo, producto_id))
            # Registrar movimiento
            cursor.execute(
                """
                INSERT INTO movimientos_stock (producto_id, tipo, cantidad, stock_anterior, stock_nuevo, fecha, observaciones, usuario_id)
                VALUES (?, ?, ?, ?, ?, datetime('now'), ?, ?)
                """,
                (producto_id, 'salida', cantidad, stock_anterior, stock_nuevo, observaciones, usuario_id)
            )
            conn.commit()
            return stock_nuevo
    def update_zona_nombre(self, zona_id, nuevo_nombre):
        """Actualiza el nombre de una zona y todas las mesas asociadas a esa zona."""
        # Obtener el nombre actual de la zona
        zona = self.get_by_id('zonas', zona_id)
        if not zona:
            return False
        nombre_anterior = zona['nombre']
        # Actualizar el nombre en la tabla zonas
        self.execute("UPDATE zonas SET nombre = ? WHERE id = ?", (nuevo_nombre, zona_id))
        # Actualizar todas las mesas que tengan esa zona
        self.execute("UPDATE mesas SET zona = ? WHERE zona = ?", (nuevo_nombre, nombre_anterior))
        return True
    def sync_zonas_from_mesas(self):
        """Sincroniza la tabla zonas con los valores únicos de la columna zona de mesas (ignora nulos y 'Todas')."""
        zonas_mesas = self.query("SELECT DISTINCT zona FROM mesas WHERE zona IS NOT NULL AND zona != '' AND zona != 'Todas'")
        zonas_db = set(z['nombre'] for z in self.get_zonas())
        nuevas_zonas = [z['zona'] for z in zonas_mesas if z['zona'] and z['zona'] not in zonas_db]
        for nombre in nuevas_zonas:
            self.create_zona(nombre)
    # Métodos para gestión de zonas (persistencia real)
    def get_zonas(self):
        """Obtiene todas las zonas ordenadas por nombre ASC"""
        return self.query("SELECT * FROM zonas ORDER BY nombre ASC")

    def create_zona(self, nombre):
        """Crea una nueva zona (si no existe)"""
        return self.execute("INSERT INTO zonas (nombre) VALUES (?)", (nombre,))

    def delete_zona(self, zona_id):
        """Elimina una zona por id"""
        return self.execute("DELETE FROM zonas WHERE id = ?", (zona_id,))

    def get_zona_by_nombre(self, nombre):
        """Obtiene una zona por nombre"""
        result = self.query("SELECT * FROM zonas WHERE nombre = ?", (nombre,))
        return result[0] if result else None
    def __init__(self, path=None):
        if path is None:
            # Calcular la ruta absoluta a la base de datos
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, 'hefest.db')
        else:
            self.db_path = path
        self._init_db()
        # Sincronizar zonas históricas de mesas al inicializar
        self.sync_zonas_from_mesas()

    def _init_db(self):
        with self._get_connection() as conn:
            # Tabla de usuarios
            conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                role TEXT NOT NULL,
                pin TEXT NOT NULL,
                email TEXT,
                telefono TEXT,
                fecha_creacion TEXT,
                is_active BOOLEAN DEFAULT 1,
                ultimo_acceso TEXT
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL,
                stock INTEGER,
                categoria TEXT
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS mesas (
                id INTEGER PRIMARY KEY,
                numero TEXT NOT NULL,
                zona TEXT,
                estado TEXT,
                capacidad INTEGER
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellidos TEXT,
                dni TEXT UNIQUE,
                telefono TEXT,
                email TEXT
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS habitaciones (
                id INTEGER PRIMARY KEY,
                numero TEXT NOT NULL,
                tipo TEXT,
                estado TEXT,
                precio_base REAL
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY,
                cliente_id INTEGER,
                habitacion_id INTEGER,
                mesa_id TEXT,
                fecha_entrada TEXT,
                fecha_salida TEXT,
                estado TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (habitacion_id) REFERENCES habitaciones (id)
            )''')



            conn.execute('''CREATE TABLE IF NOT EXISTS comandas (
                id INTEGER PRIMARY KEY,
                mesa_id TEXT,
                usuario_id INTEGER,
                fecha_hora TEXT,
                estado TEXT,
                total REAL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS comanda_detalles (
                id INTEGER PRIMARY KEY,
                comanda_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER,
                precio_unitario REAL,
                notas TEXT,
                FOREIGN KEY (comanda_id) REFERENCES comandas (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )''')

            # Tablas de inventario avanzado
            conn.execute('''CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                fecha_creacion TEXT,
                activa BOOLEAN DEFAULT 1
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                contacto TEXT,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                fecha_registro TEXT,
                activo BOOLEAN DEFAULT 1,
                notas TEXT
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS movimientos_stock (
                id INTEGER PRIMARY KEY,
                producto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                stock_anterior INTEGER,
                stock_nuevo INTEGER,
                fecha TEXT NOT NULL,
                observaciones TEXT,
                usuario_id INTEGER,
                FOREIGN KEY (producto_id) REFERENCES productos (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )''')

            # Insertar usuarios predeterminados si no existen
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            if cursor.fetchone()[0] == 0:
                usuarios_default = [
                    (1, "Administrador", "ADMIN", "admin123", "admin@hefest.com", "+34-600-000-001",
                     "2025-06-10", 1, None),
                    (2, "Manager", "MANAGER", "manager123", "manager@hefest.com", "+34-600-000-002",
                     "2025-06-10", 1, None),                (3, "Empleado", "EMPLOYEE", "employee123", "empleado@hefest.com", "+34-600-000-003",
                     "2025-06-10", 1, None)
                ]
                conn.executemany("""
                    INSERT INTO usuarios (id, nombre, role, pin, email, telefono, fecha_creacion, is_active, ultimo_acceso)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, usuarios_default)
                conn.commit()  # ¡Importante! Hacer commit de los usuarios por defecto

    @contextmanager
    def _get_connection(self):
        # Añadimos timeout para evitar bloqueos inmediatos y activamos WAL para concurrencia
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            # Activar WAL solo la primera vez por conexión
            conn.execute('PRAGMA journal_mode=WAL;')
            yield conn
        finally:
            conn.close()

    # TODO: Si se detecta uso multihilo, migrar a una única conexión compartida o pool de conexiones.
    #       Documentar y refactorizar para evitar bloqueos en escenarios concurrentes.

    def query(self, sql, params=()):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()

    def execute(self, sql, params=()):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid

    def execute_many(self, sql, params_list):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(sql, params_list)
            conn.commit()

    def get_by_id(self, table, id):
        sql = f"SELECT * FROM {table} WHERE id = ?"
        result = self.query(sql, (id,))
        return result[0] if result else None

    def insert(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.execute(sql, values)

    def update(self, table, id, data):
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values()) + (id,)

        sql = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0  # Retorna True si se actualizó alguna fila

    def delete(self, table, id):
        sql = f"DELETE FROM {table} WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id,))
            conn.commit()
            return cursor.rowcount > 0  # Retorna True si se eliminó alguna fila

    # Métodos para gestión de usuarios
    def get_usuarios(self):
        """Obtiene todos los usuarios"""
        return self.query("SELECT * FROM usuarios WHERE is_active = 1")

    def get_usuario_by_id(self, user_id):
        """Obtiene un usuario por ID"""
        result = self.query("SELECT * FROM usuarios WHERE id = ? AND is_active = 1", (user_id,))
        return result[0] if result else None

    def validate_user_login(self, user_id, pin):
        """Valida las credenciales de usuario"""
        result = self.query(
            "SELECT * FROM usuarios WHERE id = ? AND pin = ? AND is_active = 1",
            (user_id, pin)
        )
        return result[0] if result else None

    def update_ultimo_acceso(self, user_id, timestamp):
        """Actualiza el último acceso del usuario"""
        self.execute(
            "UPDATE usuarios SET ultimo_acceso = ? WHERE id = ?",
            (timestamp, user_id)
        )

    def create_usuario(self, nombre, role, pin, email=None, telefono=None):
        """Crea un nuevo usuario"""
        from datetime import datetime
        fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return self.execute("""
            INSERT INTO usuarios (nombre, role, pin, email, telefono, fecha_creacion, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (nombre, role, pin, email, telefono, fecha_creacion))
    def update_usuario(self, user_id, **kwargs):
        """Actualiza campos de un usuario"""
        fields = []
        values = []

        for field, value in kwargs.items():
            if field in ['nombre', 'role', 'pin', 'email', 'telefono', 'is_active']:
                fields.append(f"{field} = ?")
                values.append(value)

        if fields:
            values.append(user_id)
            sql = f"UPDATE usuarios SET {', '.join(fields)} WHERE id = ?"
            self.execute(sql, values)

    def delete_usuario(self, user_id):
        """Desactiva un usuario (soft delete)"""
        self.execute("UPDATE usuarios SET is_active = 0 WHERE id = ?", (user_id,))

    # Métodos para gestión de habitaciones
    def get_habitaciones(self):
        """Obtiene todas las habitaciones"""
        return self.query("SELECT * FROM habitaciones")

    def update_estado_habitacion(self, habitacion_id, estado):
        """Actualiza el estado de una habitación"""
        self.execute(
            "UPDATE habitaciones SET estado = ? WHERE id = ?",
            (estado, habitacion_id)
        )

    # Métodos para gestión de reservas
    def get_reservas(self):
        """Obtiene todas las reservas con información del cliente"""
        return self.query("""
            SELECT r.*, c.nombre as cliente_nombre, c.telefono as cliente_telefono,
                   h.numero as habitacion_numero
            FROM reservas r
            JOIN clientes c ON r.cliente_id = c.id
            JOIN habitaciones h ON r.habitacion_id = h.id
            ORDER BY r.fecha_entrada
        """)

    def create_reserva(self, cliente_id, habitacion_id, fecha_entrada, fecha_salida, estado='pendiente'):
        """Crea una nueva reserva"""
        return self.execute("""
            INSERT INTO reservas (cliente_id, habitacion_id, fecha_entrada, fecha_salida, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (cliente_id, habitacion_id, fecha_entrada, fecha_salida, estado))

    # Métodos para obtener métricas administrativas reales
    def get_admin_metrics(self):
        """
        Obtiene métricas administrativas reales del negocio
        Retorna diccionario con métricas clave
        """
        try:
            metrics = {}

            # Métricas de ventas (desde comandas)
            ventas_result = self.query("""
                SELECT
                    COALESCE(SUM(total), 0) as ventas_totales,
                    COUNT(*) as num_comandas,
                    COALESCE(AVG(total), 0) as ticket_promedio
                FROM comandas
                WHERE DATE(fecha_hora) = DATE('now')
            """)

            if ventas_result:
                ventas_data = ventas_result[0]
                metrics['ventas'] = float(ventas_data['ventas_totales'])
                metrics['ticket_promedio'] = float(ventas_data['ticket_promedio'])
                metrics['ordenes_activas'] = int(ventas_data['num_comandas'])
            else:
                metrics['ventas'] = 0.0
                metrics['ticket_promedio'] = 0.0
                metrics['ordenes_activas'] = 0

            # Métricas de ocupación hotelera
            ocupacion_result = self.query("""
                SELECT
                    COUNT(*) as total_habitaciones,
                    SUM(CASE WHEN estado = 'ocupada' THEN 1 ELSE 0 END) as habitaciones_ocupadas
                FROM habitaciones
            """)

            if ocupacion_result and ocupacion_result[0]['total_habitaciones'] > 0:
                ocupacion_data = ocupacion_result[0]
                ocupacion_porcentaje = (ocupacion_data['habitaciones_ocupadas'] / ocupacion_data['total_habitaciones']) * 100
                metrics['ocupacion'] = float(ocupacion_porcentaje)
            else:
                metrics['ocupacion'] = 0.0

            # Métricas de tiempo de servicio (estimado desde comandas)
            tiempo_result = self.query("""
                SELECT
                    COUNT(*) as comandas_completadas,
                    COALESCE(AVG(julianday('now') - julianday(fecha_hora)) * 24 * 60, 0) as tiempo_promedio_minutos
                FROM comandas
                WHERE estado = 'completada' AND DATE(fecha_hora) = DATE('now')
            """)

            if tiempo_result:
                tiempo_data = tiempo_result[0]
                metrics['tiempo_servicio'] = float(tiempo_data['tiempo_promedio_minutos'])
            else:
                metrics['tiempo_servicio'] = 0.0

            # Satisfacción por defecto (hasta tener sistema de reviews)
            metrics['satisfaccion'] = 0.0

            return metrics

        except Exception as e:
            import logging
            logging.error(f"Error al obtener métricas administrativas: {e}")
            # Retornar métricas vacías en caso de error
            return {
                'ventas': 0.0,
                'ocupacion': 0.0,
                'tiempo_servicio': 0.0,
                'satisfaccion': 0.0,
                'ordenes_activas': 0,
                'ticket_promedio': 0.0
            }

    def get_inventory_metrics(self):
        """Obtiene métricas de inventario reales"""
        try:
            result = self.query("""
                SELECT
                    COUNT(*) as total_productos,
                    SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) as productos_sin_stock,
                    SUM(CASE WHEN stock < 5 THEN 1 ELSE 0 END) as productos_stock_bajo,
                    COALESCE(AVG(precio), 0) as precio_promedio,
                    COALESCE(SUM(stock * precio), 0) as valor_total_inventario
                FROM productos
            """)

            if result:
                data = result[0]
                return {
                    'total_productos': int(data['total_productos']),
                    'productos_sin_stock': int(data['productos_sin_stock']),
                    'productos_stock_bajo': int(data['productos_stock_bajo']),
                    'precio_promedio': float(data['precio_promedio']),
                    'valor_total_inventario': float(data['valor_total_inventario'])
                }
            else:
                return {
                    'total_productos': 0,
                    'productos_sin_stock': 0,
                    'productos_stock_bajo': 0,
                    'precio_promedio': 0.0,
                    'valor_total_inventario': 0.0
                }

        except Exception as e:
            import logging
            logging.error(f"Error al obtener métricas de inventario: {e}")
            return {
                'total_productos': 0,
                'productos_sin_stock': 0,
                'productos_stock_bajo': 0,
                'precio_promedio': 0.0,
                'valor_total_inventario': 0.0
            }

    def get_hospitality_metrics(self):
        """Obtiene métricas de hospedería reales"""
        try:
            # Métricas de reservas
            reservas_result = self.query("""
                SELECT
                    COUNT(*) as total_reservas,
                    SUM(CASE WHEN estado = 'confirmada' THEN 1 ELSE 0 END) as reservas_confirmadas,
                    SUM(CASE WHEN DATE(fecha_entrada) = DATE('now') THEN 1 ELSE 0 END) as check_ins_hoy,
                    SUM(CASE WHEN DATE(fecha_salida) = DATE('now') THEN 1 ELSE 0 END) as check_outs_hoy
                FROM reservas
                WHERE fecha_entrada >= DATE('now', '-30 days')
            """)

            # Métricas de habitaciones
            habitaciones_result = self.query("""
                SELECT
                    COUNT(*) as total_habitaciones,
                    SUM(CASE WHEN estado = 'ocupada' THEN 1 ELSE 0 END) as habitaciones_ocupadas,
                    SUM(CASE WHEN estado = 'disponible' THEN 1 ELSE 0 END) as habitaciones_disponibles,
                    SUM(CASE WHEN estado = 'mantenimiento' THEN 1 ELSE 0 END) as habitaciones_mantenimiento,
                    COALESCE(AVG(precio_base), 0) as precio_promedio_noche
                FROM habitaciones
            """)

            metrics = {}

            if reservas_result:
                reservas_data = reservas_result[0]
                metrics.update({
                    'total_reservas': int(reservas_data['total_reservas']),
                    'reservas_confirmadas': int(reservas_data['reservas_confirmadas']),
                    'check_ins_hoy': int(reservas_data['check_ins_hoy']),
                    'check_outs_hoy': int(reservas_data['check_outs_hoy'])
                })

            if habitaciones_result:
                habitaciones_data = habitaciones_result[0]
                metrics.update({
                    'total_habitaciones': int(habitaciones_data['total_habitaciones']),
                    'habitaciones_ocupadas': int(habitaciones_data['habitaciones_ocupadas']),
                    'habitaciones_disponibles': int(habitaciones_data['habitaciones_disponibles']),
                    'habitaciones_mantenimiento': int(habitaciones_data['habitaciones_mantenimiento']),
                    'precio_promedio_noche': float(habitaciones_data['precio_promedio_noche'])
                })

            # Calcular ocupación si hay habitaciones
            if metrics.get('total_habitaciones', 0) > 0:
                ocupacion_porcentaje = (metrics['habitaciones_ocupadas'] / metrics['total_habitaciones']) * 100
                metrics['ocupacion_porcentaje'] = round(ocupacion_porcentaje, 1)
            else:
                metrics['ocupacion_porcentaje'] = 0.0

            return metrics

        except Exception as e:
            import logging
            logging.error(f"Error al obtener métricas de hospedería: {e}")
            return {
                'total_reservas': 0,
                'reservas_confirmadas': 0,
                'check_ins_hoy': 0,
                'check_outs_hoy': 0,
                'total_habitaciones': 0,
                'habitaciones_ocupadas': 0,
                'habitaciones_disponibles': 0,
                'habitaciones_mantenimiento': 0,
                'precio_promedio_noche': 0.0,
                'ocupacion_porcentaje': 0.0
            }
