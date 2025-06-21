"""
Servicio de gestión del inventario.
"""

import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, date

logger = logging.getLogger(__name__)

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
    tipo: str  # entrada, salida
    cantidad: int
    fecha: datetime
    motivo: str
    usuario_id: Optional[int] = None
    usuario_nombre: Optional[str] = None
    
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

class InventarioService:
    """Servicio para la gestión del inventario"""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        logger.info("InventarioService inicializado con base de datos real" if db_manager else "InventarioService inicializado sin base de datos")
        
    def _convert_db_row_to_producto(self, row: dict) -> Producto:
        """Convierte una fila de la base de datos a un objeto Producto"""
        return Producto(
            id=row.get('id'),
            nombre=row.get('nombre', ''),
            categoria=row.get('categoria', 'General'),
            precio=float(row.get('precio', 0.0)),
            stock_actual=int(row.get('stock', 0)),
            stock_minimo=int(row.get('stock_minimo', 0)),  # Asumiendo que se agregará esta columna
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
    
    def get_proveedores(self) -> List[Proveedor]:
        """Retorna todos los proveedores"""
        return self._proveedores_cache.copy()
    
    def get_proveedor_by_id(self, proveedor_id: int) -> Optional[Proveedor]:
        """Retorna un proveedor por su ID"""
        for p in self._proveedores_cache:
            if p.id == proveedor_id:
                return p
        return None
    
    def get_movimientos(self, limit: int = 50) -> List[MovimientoStock]:
        """Retorna los últimos movimientos de stock"""
        return sorted(self._movimientos_cache, key=lambda m: m.fecha, reverse=True)[:limit]
    
    def get_pedidos(self, estado: str = "") -> List[Pedido]:
        """Retorna los pedidos, opcionalmente filtrados por estado"""
        if not estado:
            return self._pedidos_cache.copy()
            
        return [p for p in self._pedidos_cache if p.estado == estado]
    
    def get_categorias(self) -> List[str]:
        """Retorna las categorías disponibles"""
        categorias = set(p.categoria for p in self._productos_cache)
        return sorted(list(categorias))
    
    def get_productos_bajo_minimo(self) -> List[Producto]:
        """Retorna productos con stock bajo el mínimo"""
        return [p for p in self._productos_cache if p.necesita_reposicion]
    
    def buscar_productos(self, termino: str = "") -> List[Producto]:
        """Busca productos por nombre, categoria o cualquier campo de texto"""
        if not termino:
            return self._productos_cache.copy()
            
        termino = termino.lower()
        resultado = []
        
        for producto in self._productos_cache:
            # Buscar en nombre, categoria y proveedor
            if (termino in producto.nombre.lower() or 
                termino in producto.categoria.lower() or 
                (producto.proveedor_nombre and termino in producto.proveedor_nombre.lower())):
                resultado.append(producto)
                
        return resultado
    
    def get_productos_stock_bajo(self, umbral_multiplicador: float = 1.0) -> List[Producto]:
        """Retorna productos con stock por debajo del mínimo multiplicado por el umbral"""
        productos_stock_bajo = []
        
        for producto in self._productos_cache:
            umbral = producto.stock_minimo * umbral_multiplicador
            if producto.stock_actual <= umbral:
                productos_stock_bajo.append(producto)
                
        return productos_stock_bajo

    # === MÉTODOS DE NEGOCIO ===
    
    def crear_producto(self, producto: Producto) -> Producto:
        """Crea un nuevo producto en el inventario"""
        # Generar ID para el nuevo producto
        if not producto.id:
            max_id = max([p.id or 0 for p in self._productos_cache], default=0)
            producto.id = max_id + 1
            
        # Añadir a la caché
        self._productos_cache.append(producto)
        
        # TODO: Persistir en BD
        
        logger.info(f"Producto creado: {producto.nombre}")
        return producto
    
    def actualizar_producto(self, producto: Producto) -> bool:
        """Actualiza un producto existente"""
        for i, p in enumerate(self._productos_cache):
            if p.id == producto.id:
                self._productos_cache[i] = producto
                
                # TODO: Persistir en BD
                
                logger.info(f"Producto actualizado: {producto.nombre}")
                return True
                
        return False
    
    def eliminar_producto(self, producto_id: int) -> bool:
        """Elimina un producto del inventario"""
        for i, p in enumerate(self._productos_cache):
            if p.id == producto_id:
                del self._productos_cache[i]
                
                # TODO: Persistir en BD
                
                logger.info(f"Producto eliminado: ID {producto_id}")
                return True
                
        return False
    
    def registrar_movimiento(self, movimiento: MovimientoStock) -> MovimientoStock:
        """Registra un movimiento de stock"""
        # Validar que el producto existe
        producto = self.get_producto_by_id(movimiento.producto_id)
        if not producto:
            raise ValueError(f"No existe producto con ID {movimiento.producto_id}")
            
        # Generar ID para el movimiento
        if not movimiento.id:
            max_id = max([m.id or 0 for m in self._movimientos_cache], default=0)
            movimiento.id = max_id + 1
            
        # Actualizar stock del producto
        if movimiento.tipo == "entrada":
            producto.stock_actual += movimiento.cantidad
            if movimiento.motivo.startswith("Pedido"):
                producto.fecha_ultima_entrada = movimiento.fecha.date()
        elif movimiento.tipo == "salida":
            if producto.stock_actual < movimiento.cantidad:
                raise ValueError(f"Stock insuficiente para {producto.nombre}")
            producto.stock_actual -= movimiento.cantidad
        else:
            raise ValueError("Tipo de movimiento no válido")
            
        # Actualizar producto
        self.actualizar_producto(producto)
        
        # Añadir el movimiento a la caché
        self._movimientos_cache.append(movimiento)
        
        # TODO: Persistir en BD
        
        logger.info(f"Movimiento registrado: {movimiento.tipo} de {movimiento.cantidad} {movimiento.producto_nombre}")
        return movimiento
    
    def crear_pedido(self, pedido: Pedido) -> Pedido:
        """Crea un nuevo pedido a proveedor"""
        # Validar que el proveedor existe
        proveedor = self.get_proveedor_by_id(pedido.proveedor_id)
        if not proveedor:
            raise ValueError(f"No existe proveedor con ID {pedido.proveedor_id}")
            
        # Generar ID para el pedido
        if not pedido.id:
            max_id = max([p.id or 0 for p in self._pedidos_cache], default=0)
            pedido.id = max_id + 1
            
        # Añadir a la caché
        self._pedidos_cache.append(pedido)
        
        # TODO: Persistir en BD
        
        logger.info(f"Pedido creado: {pedido.id} a {pedido.proveedor_nombre}")
        return pedido
    
    def recibir_pedido(self, pedido_id: int) -> bool:
        """Marca un pedido como recibido y actualiza el stock"""
        for i, p in enumerate(self._pedidos_cache):
            if p.id == pedido_id and p.estado == "pendiente":
                p.estado = "recibido"
                p.fecha_recepcion = datetime.now()
                
                # Registrar entradas de stock para cada línea
                if p.lineas:
                    for producto_id, nombre, cantidad, _ in p.lineas:
                        movimiento = MovimientoStock(
                            id=None,
                            producto_id=producto_id,
                            producto_nombre=nombre,
                            tipo="entrada",
                            cantidad=cantidad,
                            fecha=datetime.now(),
                            motivo=f"Pedido #{pedido_id}"
                        )
                        self.registrar_movimiento(movimiento)
                  # TODO: Persistir en BD
                
                logger.info(f"Pedido recibido: {pedido_id}")
                return True
                
        return False
    
    def generar_pedido_automatico(self) -> List[Pedido]:
        """Genera un pedido automático para productos bajo mínimo"""
        productos_bajo_minimo = self.get_productos_bajo_minimo()
        if not productos_bajo_minimo:
            return []
            
        # Agrupar por proveedor
        por_proveedor = {}
        for p in productos_bajo_minimo:
            if not p.proveedor_id:
                continue
                
            if p.proveedor_id not in por_proveedor:
                por_proveedor[p.proveedor_id] = []
                
            # Calcular cantidad a pedir (mínimo * 2 - stock_actual)
            cantidad = (p.stock_minimo * 2) - p.stock_actual
            if cantidad <= 0:
                continue
                
            por_proveedor[p.proveedor_id].append((p.id, p.nombre, cantidad, p.precio * 0.7))  # Precio de coste estimado
        
        # Crear pedidos
        pedidos_creados = []
        for proveedor_id, lineas in por_proveedor.items():
            if not lineas:
                continue
                
            proveedor = self.get_proveedor_by_id(proveedor_id)
            if not proveedor:
                continue
                
            pedido = Pedido(
                id=None,
                proveedor_id=proveedor_id,
                proveedor_nombre=proveedor.nombre,
                fecha_pedido=datetime.now(),
                fecha_recepcion=None,
                estado="pendiente",
                lineas=lineas
            )
            
            pedido_creado = self.crear_pedido(pedido)
            pedidos_creados.append(pedido_creado)
            
        logger.info(f"Pedidos automáticos generados: {len(pedidos_creados)}")
        return pedidos_creados
    
    def crear_proveedor(self, proveedor: Proveedor) -> Proveedor:
        """Crea un nuevo proveedor"""
        # Generar ID para el proveedor
        if not proveedor.id:
            max_id = max([p.id or 0 for p in self._proveedores_cache], default=0)
            proveedor.id = max_id + 1
            
        # Añadir a la caché
        self._proveedores_cache.append(proveedor)
        
        # TODO: Persistir en BD
        
        logger.info(f"Proveedor creado: {proveedor.nombre}")
        return proveedor
