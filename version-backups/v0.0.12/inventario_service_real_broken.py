"""
Servicio de gestión del inventario - Versión con datos reales.
"""

import logging
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum

from .base_service import BaseService

logger = logging.getLogger(__name__)

class TipoAlerta(Enum):
    """Tipos de alertas del inventario"""
    STOCK_AGOTADO = "stock_agotado"
    STOCK_BAJO = "stock_bajo"
    STOCK_CRITICO = "stock_critico"
    PRODUCTO_VENCIDO = "producto_vencido"
    PRODUCTO_POR_VENCER = "producto_por_vencer"

class PrioridadAlerta(Enum):
    """Prioridades de alertas"""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

@dataclass
class AlertaInventario:
    """Clase de datos para una alerta de inventario"""
    id: Optional[int]
    producto_id: int
    producto_nombre: str
    tipo: TipoAlerta
    prioridad: PrioridadAlerta
    titulo: str
    mensaje: str
    fecha_creacion: datetime
    fecha_resolucion: Optional[datetime] = None
    resuelta: bool = False
    datos_adicionales: Optional[Dict[str, Any]] = None
    
    @property
    def es_activa(self) -> bool:
        """Indica si la alerta está activa"""
        return not self.resuelta and self.fecha_resolucion is None
    
    @property
    def color_prioridad(self) -> str:
        """Retorna el color asociado a la prioridad"""
        colors = {
            PrioridadAlerta.BAJA: "#10b981",
            PrioridadAlerta.MEDIA: "#f59e0b", 
            PrioridadAlerta.ALTA: "#ef4444",
            PrioridadAlerta.CRITICA: "#dc2626"
        }
        return colors.get(self.prioridad, "#6b7280")

@dataclass
class Producto:
    """Clase de datos para un producto del inventario"""
    id: Optional[int]
    nombre: str
    categoria: str
    precio: float
    stock_actual: int
    stock_minimo: int
    proveedor_id: Optional[int] = None
    proveedor_nombre: Optional[str] = None
    fecha_ultima_entrada: Optional[date] = None
    
    @property
    def necesita_reposicion(self) -> bool:
        """Indica si el producto necesita reposición"""
        return self.stock_actual <= self.stock_minimo
        
    @property
    def nivel_stock_porcentaje(self) -> float:
        """Retorna el nivel de stock como porcentaje del mínimo"""
        if self.stock_minimo == 0:
            return 100.0
        return (self.stock_actual / self.stock_minimo) * 100
        
@dataclass
class Proveedor:
    """Clase de datos para un proveedor"""
    id: Optional[int]
    nombre: str
    contacto: str
    telefono: str
    email: str
    direccion: Optional[str] = None

@dataclass
class MovimientoStock:
    """Clase de datos para un movimiento de stock"""
    id: Optional[int]
    producto_id: int
    producto_nombre: str
    tipo: str  # "entrada" o "salida"
    cantidad: int
    fecha: datetime
    observaciones: Optional[str] = None

@dataclass
class Pedido:
    """Clase de datos para un pedido a proveedor"""
    id: Optional[int]
    proveedor_id: int
    proveedor_nombre: str
    fecha_pedido: datetime
    estado: str  # pendiente, recibido, cancelado
    lineas: Optional[List[Tuple]] = None  # [(producto_id, nombre, cantidad, precio)]
    fecha_recepcion: Optional[datetime] = None
    
    @property
    def total(self) -> float:
        """Retorna el total del pedido"""
        if not self.lineas:
            return 0.0
        return sum(precio * cantidad for _, _, cantidad, precio in self.lineas)

class InventarioService(BaseService):
    """Servicio para la gestión del inventario con datos reales"""
    
    def __init__(self, db_manager=None):
        super().__init__(db_manager)
        self.logger.info("InventarioService inicializado con base de datos real" if db_manager else "InventarioService inicializado sin base de datos")
        
    def get_service_name(self) -> str:
        """Retorna el nombre de este servicio"""
        return "InventarioService"
        
    def _convert_db_row_to_producto(self, row: dict) -> Producto:
        """Convierte una fila de la base de datos a un objeto Producto"""
        return Producto(
            id=row.get('id'),
            nombre=row.get('nombre', ''),
            categoria=row.get('categoria', 'General'),
            precio=float(row.get('precio', 0.0)),
            stock_actual=int(row.get('stock', 0)),
            stock_minimo=int(row.get('stock_minimo', 5)),  # Valor por defecto de 5
            proveedor_id=row.get('proveedor_id'),
            proveedor_nombre=row.get('proveedor_nombre'),
            fecha_ultima_entrada=None  # TODO: Implementar cuando se agregue la tabla de movimientos
        )
        
    def get_productos(self, texto_busqueda: str = "", categoria: str = "") -> List[Producto]:
        """Retorna productos filtrados por texto y/o categoría"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos, retornando lista vacía")
            return []
            
        try:
            # Construir consulta SQL con filtros
            where_clauses = []
            params = []
            
            if categoria:
                where_clauses.append("categoria = ?")
                params.append(categoria)
                
            if texto_busqueda:
                where_clauses.append("nombre LIKE ?")
                params.append(f"%{texto_busqueda}%")
            
            where_sql = ""
            if where_clauses:
                where_sql = "WHERE " + " AND ".join(where_clauses)
            
            sql = f"SELECT * FROM productos {where_sql} ORDER BY nombre"
            
            rows = self.db_manager.query(sql, params)
            productos = []
            
            for row in rows:
                try:
                    producto = self._convert_db_row_to_producto(row)
                    productos.append(producto)
                except Exception as e:
                    logger.error(f"Error al convertir producto {row.get('id', 'unknown')}: {e}")
                    
            logger.debug(f"Obtenidos {len(productos)} productos de la base de datos")
            return productos
            
        except Exception as e:
            logger.error(f"Error al obtener productos: {e}")
            return []
    
    def get_producto_by_id(self, producto_id: int) -> Optional[Producto]:
        """Retorna un producto por su ID"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos")
            return None
            
        try:
            rows = self.db_manager.query("SELECT * FROM productos WHERE id = ?", (producto_id,))
            if rows:
                return self._convert_db_row_to_producto(rows[0])
            return None
            
        except Exception as e:
            logger.error(f"Error al obtener producto {producto_id}: {e}")
            return None

    def get_categorias(self) -> List[str]:
        """Retorna las categorías únicas de productos"""
        if not self.db_manager:
            return []
            
        try:
            rows = self.db_manager.query("SELECT DISTINCT categoria FROM productos WHERE categoria IS NOT NULL ORDER BY categoria")
            return [row['categoria'] for row in rows if row['categoria']]
        except Exception as e:
            logger.error(f"Error al obtener categorías: {e}")
            return []

    def get_productos_bajo_minimo(self) -> List[Producto]:
        """Retorna productos que necesitan reposición"""
        if not self.db_manager:
            return []
            
        try:
            # Productos donde stock actual <= stock mínimo
            rows = self.db_manager.query("""
                SELECT * FROM productos 
                WHERE stock <= COALESCE(stock_minimo, 5)
                ORDER BY (stock::float / COALESCE(stock_minimo, 5)) ASC
            """)
            
            productos = []
            for row in rows:
                try:
                    producto = self._convert_db_row_to_producto(row)
                    productos.append(producto)
                except Exception as e:
                    logger.error(f"Error al convertir producto bajo mínimo {row.get('id', 'unknown')}: {e}")
                    
            return productos
            
        except Exception as e:
            logger.error(f"Error al obtener productos bajo mínimo: {e}")
            return []

    def get_productos_stock_bajo(self, umbral_multiplicador: float = 1.5) -> List[Producto]:
        """Retorna productos con stock bajo (por encima del mínimo pero cerca)"""
        if not self.db_manager:
            return []
            
        try:
            # Productos donde stock > stock_minimo pero < stock_minimo * umbral_multiplicador
            rows = self.db_manager.query("""
                SELECT * FROM productos 
                WHERE stock > COALESCE(stock_minimo, 5) 
                AND stock <= (COALESCE(stock_minimo, 5) * ?)
                ORDER BY (stock::float / COALESCE(stock_minimo, 5)) ASC
            """, (umbral_multiplicador,))
            
            productos = []
            for row in rows:
                try:
                    producto = self._convert_db_row_to_producto(row)
                    productos.append(producto)
                except Exception as e:
                    logger.error(f"Error al convertir producto stock bajo {row.get('id', 'unknown')}: {e}")
                    
            return productos
            
        except Exception as e:
            logger.error(f"Error al obtener productos con stock bajo: {e}")
            return []

    def crear_producto(self, nombre: str, categoria: str, precio: float, 
                      stock_inicial: int = 0, stock_minimo: int = 5) -> Optional[Producto]:
        """Crear un nuevo producto en el inventario"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos")
            return None
            
        try:
            # Validar datos de entrada
            if not nombre.strip():
                logger.error("Nombre del producto no puede estar vacío")
                return None
                
            if precio < 0:
                logger.error("El precio no puede ser negativo")
                return None
                
            if stock_inicial < 0:
                logger.error("El stock inicial no puede ser negativo")
                return None
                
            if stock_minimo < 0:
                logger.error("El stock mínimo no puede ser negativo")
                return None
            
            # Insertar el producto
            sql = """
                INSERT INTO productos (nombre, categoria, precio, stock, stock_minimo) 
                VALUES (?, ?, ?, ?, ?)
            """
            result = self.db_manager.execute_query(sql, (
                nombre.strip(),
                categoria.strip(),
                precio,
                stock_inicial,
                stock_minimo
            ))
            
            if result:
                # Obtener el ID del producto creado
                last_id = self.db_manager.get_last_insert_id()
                if last_id:
                    # Retornar el producto creado
                    nuevo_producto = Producto(
                        id=last_id,
                        nombre=nombre.strip(),
                        categoria=categoria.strip(),
                        precio=precio,
                        stock_actual=stock_inicial,
                        stock_minimo=stock_minimo
                    )
                    logger.info(f"Producto creado exitosamente: {nombre} (ID: {last_id})")
                    return nuevo_producto
            
            logger.error("No se pudo crear el producto")
            return None
            
        except Exception as e:
            logger.error(f"Error creando producto: {e}")
            return None

    def actualizar_stock(self, producto_id: int, nueva_cantidad: int, 
                        tipo_movimiento: str = "ajuste", observaciones: str = "") -> bool:
        """Actualiza el stock de un producto y registra el movimiento"""
        if not self.db_manager:
            logger.error("No se puede actualizar stock sin conexión a base de datos")
            return False
            
        try:
            # Obtener stock actual
            producto = self.get_producto_by_id(producto_id)
            if not producto:
                logger.error(f"Producto {producto_id} no encontrado")
                return False
            
            # Actualizar stock en la base de datos
            self.db_manager.execute("""
                UPDATE productos SET stock = ? WHERE id = ?
            """, (nueva_cantidad, producto_id))
            
            # TODO: Registrar movimiento en tabla de movimientos cuando se implemente
            logger.info(f"Stock actualizado para producto {producto_id}: {producto.stock_actual} -> {nueva_cantidad}")
            return True
            
        except Exception as e:
            logger.error(f"Error al actualizar stock del producto {producto_id}: {e}")
            return False

    def get_estadisticas_inventario(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales del inventario"""
        if not self.db_manager:
            return {}
            
        try:
            # Usar las métricas de inventario del db_manager
            return self.db_manager.get_inventory_metrics()
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas de inventario: {e}")
            return {
                'total_productos': 0,
                'productos_sin_stock': 0,
                'productos_stock_bajo': 0,
                'precio_promedio': 0.0,
                'valor_total_inventario': 0.0
            }
      # === GESTIÓN DE CATEGORÍAS ===
    
    def crear_categoria(self, nombre: str, descripcion: str = "") -> Optional[int]:
        """Crear una nueva categoría"""
        if not self.db_manager or not nombre.strip():
            return None
            
        try:
            from datetime import datetime
            result = self.db_manager.execute(
                "INSERT INTO categorias (nombre, descripcion, fecha_creacion, activa) VALUES (?, ?, ?, ?)",
                (nombre.strip(), descripcion.strip(), datetime.now(), True)
            )
            
            if result:
                categoria_id = self.db_manager.get_last_insert_id()
                logger.info(f"Categoría creada exitosamente: {nombre} (ID: {categoria_id})")
                return categoria_id
            return None
            
        except Exception as e:
            logger.error(f"Error creando categoría: {e}")
            return None
    
    def obtener_categorias(self) -> List[Dict[str, Any]]:
        """Obtener todas las categorías activas"""
        if not self.db_manager:
            return []
            
        try:
            rows = self.db_manager.fetch_all(
                "SELECT id, nombre, descripcion, fecha_creacion FROM categorias WHERE activa = ? ORDER BY nombre",
                (True,)
            )
            
            categorias = []
            for row in rows:
                categorias.append({
                    'id': row['id'],
                    'nombre': row['nombre'],
                    'descripcion': row['descripcion'] or '',
                    'fecha_creacion': row['fecha_creacion']
                })
            
            return categorias
            
        except Exception as e:
            logger.error(f"Error obteniendo categorías: {e}")
            return []
    
    def actualizar_categoria(self, categoria_id: int, nombre: str, descripcion: str = "") -> bool:
        """Actualizar una categoría existente"""
        if not self.db_manager or not nombre.strip():
            return False
            
        try:
            result = self.db_manager.execute(
                "UPDATE categorias SET nombre = ?, descripcion = ? WHERE id = ? AND activa = ?",
                (nombre.strip(), descripcion.strip(), categoria_id, True)
            )
            
            if result:
                logger.info(f"Categoría {categoria_id} actualizada exitosamente")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error actualizando categoría {categoria_id}: {e}")
            return False
    
    def eliminar_categoria(self, categoria_id: int) -> bool:
        """Eliminar (desactivar) una categoría"""
        if not self.db_manager:
            return False
            
        try:
            # Verificar si la categoría tiene productos asociados
            productos_count = self.db_manager.fetch_one(
                "SELECT COUNT(*) as count FROM productos WHERE categoria = (SELECT nombre FROM categorias WHERE id = ?)",
                (categoria_id,)
            )
            
            if productos_count and productos_count['count'] > 0:
                logger.warning(f"No se puede eliminar la categoría {categoria_id} porque tiene productos asociados")
                return False
            
            # Desactivar la categoría en lugar de eliminarla
            result = self.db_manager.execute(
                "UPDATE categorias SET activa = ? WHERE id = ?",
                (False, categoria_id)
            )
            
            if result:
                logger.info(f"Categoría {categoria_id} eliminada exitosamente")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error eliminando categoría {categoria_id}: {e}")
            return False

    # === GESTIÓN DE PROVEEDORES ===
    
    def crear_proveedor(self, nombre: str, contacto: str, telefono: str, 
                       email: str, direccion: str = "") -> Optional[int]:
        """Crear un nuevo proveedor"""
        if not self.db_manager or not nombre.strip():
            return None
            
        try:
            from datetime import datetime
            result = self.db_manager.execute(
                """INSERT INTO proveedores (nombre, contacto, telefono, email, direccion, fecha_creacion, activo) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (nombre.strip(), contacto.strip(), telefono.strip(), 
                 email.strip(), direccion.strip(), datetime.now(), True)
            )
            
            if result:
                proveedor_id = self.db_manager.get_last_insert_id()
                logger.info(f"Proveedor creado exitosamente: {nombre} (ID: {proveedor_id})")
                return proveedor_id
            return None
            
        except Exception as e:
            logger.error(f"Error creando proveedor: {e}")
            return None
    
    def obtener_proveedores(self) -> List[Dict[str, Any]]:
        """Obtener todos los proveedores activos"""
        if not self.db_manager:
            return []
            
        try:
            rows = self.db_manager.fetch_all(
                """SELECT id, nombre, contacto, telefono, email, direccion, fecha_creacion 
                   FROM proveedores WHERE activo = ? ORDER BY nombre""",
                (True,)
            )
            
            proveedores = []
            for row in rows:
                proveedores.append({
                    'id': row['id'],
                    'nombre': row['nombre'],
                    'contacto': row['contacto'],
                    'telefono': row['telefono'],
                    'email': row['email'],
                    'direccion': row['direccion'] or '',
                    'fecha_creacion': row['fecha_creacion']
                })
            
            return proveedores
            
        except Exception as e:
            logger.error(f"Error obteniendo proveedores: {e}")
            return []
    
    def actualizar_proveedor(self, proveedor_id: int, nombre: str, contacto: str, 
                           telefono: str, email: str, direccion: str = "") -> bool:
        """Actualizar un proveedor existente"""
        if not self.db_manager or not nombre.strip():
            return False
            
        try:
            result = self.db_manager.execute(
                """UPDATE proveedores SET nombre = ?, contacto = ?, telefono = ?, 
                   email = ?, direccion = ? WHERE id = ? AND activo = ?""",
                (nombre.strip(), contacto.strip(), telefono.strip(), 
                 email.strip(), direccion.strip(), proveedor_id, True)
            )
            
            if result:
                logger.info(f"Proveedor {proveedor_id} actualizado exitosamente")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error actualizando proveedor {proveedor_id}: {e}")
            return False
    
    def eliminar_proveedor(self, proveedor_id: int) -> bool:
        """Eliminar (desactivar) un proveedor"""
        if not self.db_manager:
            return False
            
        try:
            # Verificar si el proveedor tiene productos asociados
            productos_count = self.db_manager.fetch_one(
                "SELECT COUNT(*) as count FROM productos WHERE proveedor_id = ?",
                (proveedor_id,)
            )
            
            if productos_count and productos_count['count'] > 0:
                logger.warning(f"No se puede eliminar el proveedor {proveedor_id} porque tiene productos asociados")
                return False
            
            # Desactivar el proveedor en lugar de eliminarlo
            result = self.db_manager.execute(
                "UPDATE proveedores SET activo = ? WHERE id = ?",
                (False, proveedor_id)
            )
            
            if result:
                logger.info(f"Proveedor {proveedor_id} eliminado exitosamente")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error eliminando proveedor {proveedor_id}: {e}")
            return False

    def obtener_proveedor_por_id(self, proveedor_id: int) -> Optional[Dict[str, Any]]:
        """Obtener un proveedor específico por ID"""
        if not self.db_manager:
            return None
            
        try:
            row = self.db_manager.fetch_one(
                """SELECT id, nombre, contacto, telefono, email, direccion, fecha_creacion 
                   FROM proveedores WHERE id = ? AND activo = ?""",
                (proveedor_id, True)
            )
            
            if row:
                return {
                    'id': row['id'],
                    'nombre': row['nombre'],
                    'contacto': row['contacto'],
                    'telefono': row['telefono'],
                    'email': row['email'],
                    'direccion': row['direccion'] or '',
                    'fecha_creacion': row['fecha_creacion']
                }
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo proveedor {proveedor_id}: {e}")
            return None

    # === GESTIÓN DE MOVIMIENTOS DE STOCK ===
    
    def registrar_movimiento_stock(self, producto_id: int, tipo: str, cantidad: int, 
                                  observaciones: str = "") -> bool:
        """Registrar un movimiento de stock"""
        if not self.db_manager:
            return False
            
        try:
            from datetime import datetime
            
            # Obtener información del producto
            producto = self.get_producto_by_id(producto_id)
            if not producto:
                logger.error(f"Producto {producto_id} no encontrado para registrar movimiento")
                return False
            
            # Registrar el movimiento
            result = self.db_manager.execute(
                """INSERT INTO movimientos_stock (producto_id, tipo, cantidad, fecha, observaciones) 
                   VALUES (?, ?, ?, ?, ?)""",
                (producto_id, tipo.lower(), cantidad, datetime.now(), observaciones.strip())
            )
            
            if result:
                logger.info(f"Movimiento de stock registrado: {tipo} {cantidad} para producto {producto_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error registrando movimiento de stock: {e}")
            return False

    def obtener_movimientos_stock(self, producto_id: Optional[int] = None, 
                                 limite: int = 50) -> List[Dict[str, Any]]:
        """Obtener historial de movimientos de stock"""
        if not self.db_manager:
            return []
            
        try:
            if producto_id:
                query = """
                    SELECT ms.*, p.nombre as producto_nombre 
                    FROM movimientos_stock ms 
                    JOIN productos p ON ms.producto_id = p.id 
                    WHERE ms.producto_id = ? 
                    ORDER BY ms.fecha DESC 
                    LIMIT ?
                """
                params = (producto_id, limite)
            else:
                query = """
                    SELECT ms.*, p.nombre as producto_nombre 
                    FROM movimientos_stock ms 
                    JOIN productos p ON ms.producto_id = p.id 
                    ORDER BY ms.fecha DESC 
                    LIMIT ?
                """
                params = (limite,)
            
            rows = self.db_manager.fetch_all(query, params)
            
            movimientos = []
            for row in rows:
                movimientos.append({
                    'id': row['id'],
                    'producto_id': row['producto_id'],
                    'producto_nombre': row['producto_nombre'],
                    'tipo': row['tipo'],
                    'cantidad': row['cantidad'],
                    'fecha': row['fecha'],
                    'observaciones': row['observaciones'] or ''
                })
            
            return movimientos
            
        except Exception as e:
            logger.error(f"Error obteniendo movimientos de stock: {e}")
            return []

    def actualizar_producto(self, producto: Producto) -> bool:
        """Actualizar un producto existente"""
        if not self.db_manager:
            logger.error("No se puede actualizar producto sin conexión a base de datos")
            return False
            
        try:
            # Validar datos de entrada
            if not producto.nombre.strip():
                logger.error("Nombre del producto no puede estar vacío")
                return False
                
            if producto.precio < 0:
                logger.error("El precio no puede ser negativo")
                return False
                
            if producto.stock_actual < 0:
                logger.error("El stock no puede ser negativo")
                return False
                
            if producto.stock_minimo < 0:
                logger.error("El stock mínimo no puede ser negativo")
                return False
            
            # Actualizar producto en la base de datos
            sql = """
                UPDATE productos 
                SET nombre = ?, categoria = ?, precio = ?, stock = ?, stock_minimo = ?
                WHERE id = ?
            """
            result = self.db_manager.execute_query(sql, (
                producto.nombre.strip(),
                producto.categoria.strip(),
                producto.precio,
                producto.stock_actual,
                producto.stock_minimo,
                producto.id
            ))
            
            if result:
                logger.info(f"Producto actualizado exitosamente: {producto.nombre} (ID: {producto.id})")
                return True
            else:
                logger.error(f"No se pudo actualizar el producto {producto.id}")
                return False
                
        except Exception as e:
            logger.error(f"Error actualizando producto: {e}")
            return False

    def eliminar_producto(self, producto_id: int) -> bool:
        """Eliminar un producto del inventario"""
        if not self.db_manager:
            logger.error("No se puede eliminar producto sin conexión a base de datos")
            return False
            
        try:
            # Verificar que el producto existe
            producto = self.get_producto_by_id(producto_id)
            if not producto:
                logger.error(f"Producto {producto_id} no encontrado")
                return False
            
            # Eliminar movimientos de stock relacionados
            self.db_manager.execute_query(
                "DELETE FROM movimientos_stock WHERE producto_id = ?", 
                (producto_id,)
            )
            
            # Eliminar el producto
            result = self.db_manager.execute_query(
                "DELETE FROM productos WHERE id = ?", 
                (producto_id,)
            )
            
            if result:
                logger.info(f"Producto eliminado exitosamente: {producto.nombre} (ID: {producto_id})")
                return True
            else:
                logger.error(f"No se pudo eliminar el producto {producto_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error eliminando producto: {e}")
            return False

    def get_alertas_activas(self) -> List[Dict[str, Any]]:
        """Obtener alertas activas del inventario"""
        try:
            alertas = []
            
            # Obtener productos con stock bajo
            productos_bajo_minimo = self.get_productos_bajo_minimo()
            for producto in productos_bajo_minimo:
                alertas.append({
                    'tipo': 'stock_bajo',
                    'prioridad': 'alta' if producto.stock_actual == 0 else 'media',
                    'titulo': f'Stock Bajo: {producto.nombre}',
                    'mensaje': f'Stock actual: {producto.stock_actual}, Mínimo: {producto.stock_minimo}',
                    'producto_id': producto.id,
                    'fecha': datetime.now(),
                    'accion_sugerida': 'reponer_stock'
                })
            
            # Obtener productos agotados
            productos_agotados = [p for p in self.get_productos() if p.stock_actual == 0]
            for producto in productos_agotados:
                if not any(a['producto_id'] == producto.id for a in alertas):  # Evitar duplicados
                    alertas.append({
                        'tipo': 'agotado',
                        'prioridad': 'critica',
                        'titulo': f'Producto Agotado: {producto.nombre}',
                        'mensaje': f'Sin stock disponible',
                        'producto_id': producto.id,
                        'fecha': datetime.now(),
                        'accion_sugerida': 'reponer_urgente'
                    })
            
            # Ordenar por prioridad
            orden_prioridad = {'critica': 0, 'alta': 1, 'media': 2, 'baja': 3}
            alertas.sort(key=lambda x: orden_prioridad.get(x['prioridad'], 3))
              return alertas
            
        except Exception as e:
            logger.error(f"Error obteniendo alertas activas: {e}")
            return []

    # =================================================================
    # MÉTODOS ALIAS PARA COMPATIBILIDAD
    # =================================================================
    
    def obtener_productos(self, texto_busqueda: str = "", categoria: str = "") -> List[Producto]:
        """Alias de get_productos para compatibilidad"""
        return self.get_productos(texto_busqueda, categoria)
    
    def agregar_producto(self, nombre: str, categoria: str, precio: float, 
                        stock_inicial: int = 0, **kwargs) -> Optional[int]:
        """Alias de crear_producto para compatibilidad"""
        resultado = self.crear_producto(nombre, categoria, precio, stock_inicial, **kwargs)
        # crear_producto devuelve Producto o None, necesitamos int o None
        if resultado:
            return resultado.id if hasattr(resultado, 'id') else None
        return None
    
    def editar_producto(self, producto_id: int, **campos) -> bool:
        """Editar un producto existente"""
        try:
            if not self.db_manager:
                logger.error("No hay conexión a la base de datos")
                return False
            
            # Construir la consulta de actualización dinámicamente
            campos_validos = ['nombre', 'categoria', 'precio', 'stock', 'descripcion', 
                            'stock_minimo', 'stock_maximo', 'proveedor_id', 'codigo_barras']
            
            campos_actualizar = {k: v for k, v in campos.items() if k in campos_validos}
            
            if not campos_actualizar:
                logger.warning("No hay campos válidos para actualizar")
                return False
            
            # Construir SQL dinámico
            set_clause = ", ".join([f"{campo} = ?" for campo in campos_actualizar.keys()])
            valores = list(campos_actualizar.values()) + [producto_id]
            
            query = f"UPDATE productos SET {set_clause} WHERE id = ?"
            
            with self.db_manager._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, valores)
                conn.commit()
                
                if cursor.rowcount > 0:
                    logger.info(f"Producto {producto_id} actualizado correctamente")
                    return True
                else:
                    logger.warning(f"No se encontró producto con ID {producto_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error editando producto {producto_id}: {e}")
            return False
      def buscar_productos(self, termino: str) -> List[Producto]:
        """Búsqueda avanzada de productos"""
        try:
            if not self.db_manager:
                logger.error("No hay conexión a la base de datos")
                return []
            
            with self.db_manager._get_connection() as conn:
                cursor = conn.cursor()
                
                # Búsqueda en múltiples campos
                query = """
                    SELECT * FROM productos 
                    WHERE nombre LIKE ? 
                    OR categoria LIKE ? 
                    OR descripcion LIKE ?
                    OR codigo_barras LIKE ?
                    ORDER BY nombre
                """
                
                termino_busqueda = f"%{termino}%"
                cursor.execute(query, [termino_busqueda] * 4)
                
                productos = []
                for row in cursor.fetchall():
                    row_dict = dict(zip([col[0] for col in cursor.description], row))
                    productos.append(self._convert_db_row_to_producto(row_dict))
                
                logger.info(f"Búsqueda '{termino}': {len(productos)} productos encontrados")
                return productos
                
        except Exception as e:
            logger.error(f"Error buscando productos con término '{termino}': {e}")
            return []
