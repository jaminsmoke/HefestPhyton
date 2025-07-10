# Servicio de gestión del Terminal Punto de Venta (TPV).

import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, date, time, timedelta
from threading import Lock

from core.hefest_data_models import Reserva, Mesa

# Import event bus at module level to avoid memory leaks
try:
    from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus
except ImportError:
    _ = None

logger = logging.getLogger(__name__)


# Mesa se importa del modelo central


@dataclass
class Producto:
    """Clase de datos para un producto"""

    id: int
    nombre: str
    precio: float
    categoria: str
    stock: Optional[int] = None


@dataclass
class LineaComanda:
    """Clase de datos para una línea de comanda"""

    producto_id: int
    producto_nombre: str
    precio_unidad: float
    cantidad: int

    @property
    def total(self) -> float:
        """TODO: Add docstring"""
        # TODO: Add input validation
        return self.precio_unidad * self.cantidad


@dataclass
class Comanda:
    """Clase de datos para una comanda"""

    id: Optional[int]
    mesa_id: str  # Cambiado a str
    fecha_apertura: datetime
    fecha_cierre: Optional[datetime]
    estado: str  # abierta, cerrada, pagada, cancelada
    lineas: List[LineaComanda]
    usuario_id: Optional[int] = (
        None  # ID del usuario/camarero/cajero que crea la comanda
    )

    @property
    def total(self) -> float:
        """TODO: Add docstring"""
        # TODO: Add input validation
        return sum(linea.total for linea in self.lineas)


@dataclass
class MetodoPago:
    """Clase de datos para métodos de pago"""

    tipo: str  # efectivo, tarjeta, transferencia, vales
    monto: float
    referencia: Optional[str] = None


@dataclass
class Descuento:
    """Clase de datos para descuentos"""

    tipo: str  # porcentaje, cantidad_fija
    valor: float
    descripcion: str


@dataclass
class Factura:
    """Clase de datos para una factura"""

    id: Optional[int]
    comanda_id: int
    fecha: datetime
    subtotal: float
    descuentos: List[Descuento]
    iva: float
    total: float
    metodos_pago: List[MetodoPago]
    estado: str  # pendiente, pagada, cancelada

    @property
    def total_descuentos(self) -> float:
        """TODO: Add docstring"""
        # TODO: Add input validation
        _ = 0
        for desc in self.descuentos:
            if desc.tipo == "porcentaje":
                total += self.subtotal * (desc.valor / 100)
            else:  # cantidad_fija
                total += desc.valor
        return total

    @property
    def total_pagado(self) -> float:
        """TODO: Add docstring"""
        # TODO: Add input validation
        return sum(pago.monto for pago in self.metodos_pago)

    @property
    def cambio(self) -> float:
        """TODO: Add docstring"""
        # TODO: Add input validation
        return max(0, self.total_pagado - self.total)


class TPVService:
    def eliminar_mesa_por_numero(self, numero: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Elimina una mesa de la base de datos usando el identificador string 'numero'"""
        # Input validation
        if not numero or not isinstance(numero, str):
            logger.error("Número de mesa inválido")
            return False
            
        try:
            if not self.db_manager:
                logger.warning("No hay conexión a base de datos para eliminar mesa")
                return False

            # Buscar la mesa por numero
            _ = None
            for mesa in self._mesas_cache:
                if mesa.numero == numero:
                    _ = mesa
                    break

            if not mesa_existente:
                logger.warning("No se encontró la mesa con numero %s", numero)
                return False

            # Verificar que la mesa no esté ocupada
            if mesa_existente.estado == "ocupada":
                logger.warning(
                    f"No se puede eliminar la mesa {mesa_existente.numero} porque está ocupada"
                )
                return False

            # Eliminar de la base de datos (ya parametrizada correctamente)
            self.db_manager.execute("DELETE FROM mesas WHERE numero = ?", (numero,))

            # Eliminar del cache
            self._mesas_cache = [
                mesa for mesa in self._mesas_cache if mesa.numero != numero
            ]

            logger.info(
                f"Mesa {mesa_existente.numero} eliminada correctamente de la base de datos (por numero)"
            )
            return True

        except ValueError as e:
            logger.error("Error de validación eliminando mesa {numero}: %s", e)
            return False
        except Exception as e:
            logger.error("Error crítico eliminando mesa {numero}: %s", e)
            # Intentar rollback si es necesario
            try:
                if self.db_manager:
                    self.db_manager.rollback()
            except Exception as e:
                logging.error("Error: %s", e)
                pass
            return False

    def persistir_comanda(self, comanda: Comanda) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Persiste la comanda y sus líneas en la base de datos.
        Refactorizado para separación de responsabilidades.
        """
        if not self._validate_comanda_for_persistence(comanda):
            return False
            
        try:
            success = self._persist_comanda_to_db(comanda)
            if success:
                self._update_mesa_state_from_comanda(comanda)
                self._update_comanda_cache(comanda)
            return success
        except ValueError as e:
            self.logger.error("Error de validación persistiendo comanda: %s", e)
            return False
        except Exception as e:
            self.logger.error("Error crítico persistiendo comanda {getattr(comanda, 'id', None)}: %s", e)
            self._handle_persistence_error()
            return False
    
    def _validate_comanda_for_persistence(self, comanda: Comanda) -> bool:
        """Valida que la comanda sea válida para persistir"""
        if not comanda or not isinstance(comanda, Comanda):
            self.logger.error("Comanda inválida para persistir")
            return False
            
        if not comanda.mesa_id or not isinstance(comanda.mesa_id, str):
            self.logger.error("Mesa ID inválido en comanda")
            return False
            
        if not self.db_manager:
            self.logger.error("No hay conexión a base de datos para persistir comanda")
            return False
            
        return True
    
    def _persist_comanda_to_db(self, comanda: Comanda) -> bool:
        """Persiste la comanda en la base de datos"""
        # Preparar datos para inserción/actualización
        _ = {
            "mesa_id": comanda.mesa_id,
            "usuario_id": comanda.usuario_id,
            "fecha_hora": comanda.fecha_apertura.strftime("%Y-%m-%d %H:%M:%S"),
            "estado": comanda.estado,
            "total": comanda.total,
        }
        
        if not self.db_manager:
            return False
            
        if comanda.id is not None:
            comanda_data["id"] = comanda.id
            _ = self.db_manager.update("comandas", comanda.id, comanda_data)
        else:
            updated = False

        if not updated:
            new_id = self.db_manager.insert("comandas", comanda_data)
            comanda.id = new_id

        return self._persist_comanda_details(comanda)
    
    def _persist_comanda_details(self, comanda: Comanda) -> bool:
        """Persiste los detalles de la comanda"""
        if comanda.id is None:
            return False
            
        if not self.db_manager:
            return False
            
        try:
            # Borrar líneas anteriores
            self.db_manager.execute(
                "DELETE FROM comanda_detalles WHERE comanda_id = ?", (comanda.id,)
            )
            
            # Insertar nuevas líneas
            for linea in comanda.lineas:
                _ = {
                    "comanda_id": comanda.id,
                    "producto_id": linea.producto_id,
                    "cantidad": linea.cantidad,
                    "precio_unitario": linea.precio_unidad,
                    "notas": getattr(linea, "notas", None)
                }
                if self.db_manager:
                    self.db_manager.insert("comanda_detalles", detalle_data)
            return True
        except Exception as e:
            self.logger.error("Error actualizando detalles de comanda {comanda.id}: %s", e)
            raise
    
    def _update_mesa_state_from_comanda(self, comanda: Comanda):
        """Actualiza el estado de la mesa basado en la comanda"""
        if not hasattr(comanda, 'mesa_id') or not comanda.mesa_id:
            return
            
        mesa_obj = next((m for m in self._mesas_cache if str(m.numero) == str(comanda.mesa_id)), None)
        if not mesa_obj or not mesa_obj.numero:
            return
            
        nuevo_estado = self._determine_mesa_state_from_comanda(comanda.estado)
        if nuevo_estado:
            mesa_obj.estado = nuevo_estado
            if self.db_manager:
                self.db_manager.execute(
                    "UPDATE mesas SET estado = ? WHERE numero = ?",
                    (nuevo_estado, mesa_obj.numero),
                )
            self.update_mesa(mesa_obj)
    
    def _determine_mesa_state_from_comanda(self, comanda_estado: str) -> Optional[str]:
        """Determina el estado de la mesa basado en el estado de la comanda"""
        if comanda_estado in ("abierta", "en_proceso"):
            return "ocupada"
        elif comanda_estado in ("cerrada", "pagada", "cancelada"):
            return "libre"
        return None
    
    def _update_comanda_cache(self, comanda: Comanda):
        """Actualiza el cache de comandas de forma thread-safe"""
        if hasattr(comanda, 'mesa_id') and comanda.mesa_id:
            with self._comanda_lock:
                self._comandas_cache[comanda.mesa_id] = comanda
    
    def _handle_persistence_error(self):
        """Maneja errores de persistencia con rollback"""
        try:
            if self.db_manager:
                self.db_manager.rollback()
        except Exception as e:
            logging.error("Error: %s", e)
            pass

    def update_mesa(self, mesa_actualizada: "Mesa") -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Actualiza una mesa en la base de datos y en el caché global.
        Emite eventos globales tras la persistencia para sincronización desacoplada.
        """

        try:
            if not self.db_manager:
                logger.warning("No hay conexión a base de datos para actualizar mesa")
                return False
            # Actualizar en base de datos (solo campos persistentes de la tabla mesas)
            self.db_manager.execute(
                """
                UPDATE mesas SET numero = ?, zona = ?, estado = ?, capacidad = ? WHERE id = ?
                """,
                (
                    mesa_actualizada.numero,
                    mesa_actualizada.zona,
                    mesa_actualizada.estado,
                    mesa_actualizada.capacidad,
                    mesa_actualizada.id,
                ),
            )
            # Actualizar en caché (incluye alias temporal y otros campos no persistentes)
            for idx, mesa in enumerate(self._mesas_cache):
                if mesa.id == mesa_actualizada.id:
                    self._mesas_cache[idx] = mesa_actualizada
                    break
            # Emisión global: mesa individual y lista completa
            if mesa_event_bus:
                mesa_event_bus.mesa_actualizada.emit(mesa_actualizada)
                mesa_event_bus.mesas_actualizadas.emit(self._mesas_cache.copy())
            return True
        except Exception as e:
            logger.error("Error actualizando mesa: %s", e)
            return False

    """Servicio para la gestión del TPV"""

    def __init__(self, db_manager=None):
        """TODO: Add docstring"""
        self.db_manager = db_manager
        self.logger = logging.getLogger(self.__class__.__name__)
        self._mesas_cache = []
        self._categorias_cache = []
        self._productos_cache = []
        self._comandas_cache = {}  # {mesa_id: Comanda}
        self._next_comanda_id = 1  # ID para comandas
        
        # Optimized caches
        self._reservas_cache = {}
        self._historical_cache = {}
        
        # Thread safety locks
        self._cache_lock = Lock()
        self._comanda_lock = Lock()

        self._load_datos()

    def get_service_name(self) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna el nombre de este servicio"""
        return "TPVService"

    def _load_datos(self):
        """Carga los datos desde la base de datos o crea datos de prueba"""
        _ = False

        if self.db_manager:
            self._load_mesas_from_db()
            self._load_categorias_from_db()
            self._load_productos_from_db()
            self._load_comandas_from_db()

            # Verificar si se cargaron datos
            if self._mesas_cache or self._productos_cache:
                _ = True
                if mesa_event_bus:
                    mesa_event_bus.mesas_actualizadas.emit(self._mesas_cache.copy())

        # Si no hay base de datos o no se cargaron datos, usar datos de prueba
        if not data_loaded:
            self._load_datos_prueba()
            if mesa_event_bus:
                mesa_event_bus.mesas_actualizadas.emit(self._mesas_cache.copy())

    def _load_mesas_from_db(self):
        """Carga las mesas desde la base de datos"""
        if not self.db_manager:
            self.logger.warning("No hay gestor de base de datos disponible")
            return

        try:
            # print("[DEBUG TPVService] _load_mesas_from_db llamado")  # Eliminado debug
            _ = self.db_manager.query(
                "SELECT id, numero, zona, estado, capacidad FROM mesas"
            )
            self._mesas_cache = []
            for row in result:
                _ = Mesa(
                    id=row[0],
                    _ = row[1],
                    zona=row[2] or "Sin zona",
                    _ = row[3] or "libre",
                    capacidad=row[4] or 4,
                )
                self._mesas_cache.append(mesa)
            # print("[DEBUG TPVService] _load_mesas_from_db: %s mesas cargadas" % len(self._mesas_cache))  # Eliminado debug
            self.logger.info(
                f"Cargadas {len(self._mesas_cache)} mesas desde la base de datos"
            )
        except Exception as e:
            self.logger.error("Error cargando mesas: %s", e)
            # print("[DEBUG TPVService] _load_mesas_from_db: error %s" % e)  # Eliminado debug
            self._mesas_cache = []

    def _load_categorias_from_db(self):
        """Carga las categorías desde la base de datos"""
        if not self.db_manager:
            self.logger.warning("No hay gestor de base de datos disponible")
            return

        try:
            _ = self.db_manager.query(
                "SELECT id, nombre FROM categorias WHERE activa = 1"
            )
            self._categorias_cache = []
            for row in result:
                categoria = {"id": row[0], "nombre": row[1]}
                self._categorias_cache.append(categoria)
            self.logger.info(
                f"Cargadas {len(self._categorias_cache)} categorías desde la base de datos"
            )
        except Exception as e:
            self.logger.error("Error cargando categorías: %s", e)
            self._categorias_cache = []

    def _load_productos_from_db(self):
        """Carga los productos desde la base de datos"""
        if not self.db_manager:
            self.logger.warning("No hay gestor de base de datos disponible")
            return

        try:
            _ = self.db_manager.query(
                """
                SELECT id, nombre, precio, categoria, stock
                FROM productos
                WHERE precio IS NOT NULL AND precio > 0
            """
            )
            self._productos_cache = []
            for row in result:
                _ = Producto(
                    id=row[0],
                    _ = row[1],
                    precio=row[2] or 0.0,
                    _ = row[3] or "Sin categoría",
                    stock=row[4] if row[4] is not None else None,
                )
                self._productos_cache.append(producto)
            self.logger.info(
                f"Cargados {len(self._productos_cache)} productos desde la base de datos"
            )
        except Exception as e:
            self.logger.error("Error cargando productos: %s", e)
            self._productos_cache = []

    def _load_comandas_from_db(self):
        """Carga las comandas activas desde la base de datos. Optimizado para evitar N+1 queries."""
        if not self.db_manager:
            self.logger.warning("No hay gestor de base de datos disponible")
            return

        try:
            # Single query para comandas y detalles (JOIN optimizado)
            _ = self.db_manager.query(
                """
                SELECT 
                    c.id, c.mesa_id, c.usuario_id, c.fecha_hora, c.estado, c.total,
                    cd.producto_id, cd.cantidad, cd.precio_unitario,
                    p.nombre as producto_nombre
                FROM comandas c
                LEFT JOIN comanda_detalles cd ON c.id = cd.comanda_id
                LEFT JOIN productos p ON cd.producto_id = p.id
                WHERE c.estado IN ('abierta', 'en_proceso')
                ORDER BY c.id, cd.id
            """
            )
            
            # Procesar resultados agrupados
            self._comandas_cache = {}
            _ = {}
            
            for row in result:
                _ = row[0]
                mesa_id = row[1]
                
                # Crear comanda si no existe
                if comanda_id not in comandas_dict:
                    comandas_dict[comanda_id] = Comanda(
                        id=comanda_id,
                        _ = mesa_id,
                        fecha_apertura=(
                            datetime.fromisoformat(row[3]) if row[3] else datetime.now()
                        ),
                        _ = None,
                        estado=row[4] or "abierta",
                        _ = [],
                    )
                    comandas_dict[comanda_id].usuario_id = row[2]
                
                # Añadir línea si existe
                if row[6]:  # producto_id exists
                    _ = LineaComanda(
                        producto_id=row[6],
                        _ = row[9] or f"Producto {row[6]}",
                        precio_unidad=row[8],
                        _ = row[7],
                    )
                    comandas_dict[comanda_id].lineas.append(linea)
            
            # Poblar cache por mesa_id
            for comanda in comandas_dict.values():
                self._comandas_cache[comanda.mesa_id] = comanda
                
            self.logger.info(
                f"Cargadas {len(self._comandas_cache)} comandas activas desde la base de datos (optimizado)"
            )
        except Exception as e:
            self.logger.error("Error cargando comandas: %s", e)
            self._comandas_cache = {}

    def _load_datos_prueba(self):
        """Carga datos de prueba cuando no hay base de datos"""
        # Datos de prueba
        self._mesas_cache = [
            Mesa("T01", 4, "libre", "Comedor"),
            Mesa("T02", 4, "ocupada", "Comedor"),
            Mesa("T03", 2, "libre", "Comedor"),
            Mesa("T04", 6, "reservada", "Comedor"),
            Mesa("T05", 4, "libre", "Terraza"),
            Mesa("T06", 4, "libre", "Terraza"),
            Mesa("T07", 2, "ocupada", "Terraza"),
            Mesa("T08", 2, "libre", "Terraza"),
            Mesa("B01", 2, "ocupada", "Barra"),
            Mesa("B02", 2, "libre", "Barra"),
        ]
        _ = [
            mesa.numero for mesa in self._mesas_cache if mesa.estado == "ocupada"
        ]
        for mesa_numero in mesa_ocupada_numeros:
            self._crear_comanda_prueba(mesa_numero)

        self._categorias_cache = [
            {"id": 1, "nombre": "Bebidas"},
            {"id": 2, "nombre": "Entrantes"},
            {"id": 3, "nombre": "Platos Principales"},
            {"id": 4, "nombre": "Postres"},
            {"id": 5, "nombre": "Menú del día"},
        ]

        self._productos_cache = [
            Producto(1, "Coca Cola", 2.50, "Bebidas"),
            Producto(2, "Agua", 1.50, "Bebidas"),
            Producto(3, "Cerveza", 2.80, "Bebidas"),
            Producto(4, "Vino tinto", 3.50, "Bebidas"),
            Producto(5, "Café", 1.30, "Bebidas"),
            Producto(6, "Zumo", 2.20, "Bebidas"),
            Producto(7, "Té", 1.80, "Bebidas"),
            Producto(8, "Batido", 3.00, "Bebidas"),
            # Entrantes
            Producto(9, "Patatas bravas", 5.50, "Entrantes"),
            Producto(10, "Croquetas", 7.00, "Entrantes"),
            # Platos principales
            Producto(11, "Paella", 12.00, "Platos Principales"),
            Producto(12, "Entrecot", 18.50, "Platos Principales"),
            # Postres
            Producto(13, "Tarta", 4.50, "Postres"),
            Producto(14, "Helado", 3.80, "Postres"),
        ]

        # Comandas de prueba para mesas ocupadas
        _ = [
            mesa.numero for mesa in self._mesas_cache if mesa.estado == "ocupada"
        ]
        for mesa_numero in mesa_ocupada_numeros:
            self._crear_comanda_prueba(mesa_numero)

    def _crear_comanda_prueba(self, mesa_id: str):
        """Crea una comanda de prueba para una mesa"""
        if mesa_id == "T02":  # Mesa 2
            _ = [
                LineaComanda(1, "Coca Cola", 2.50, 2),
                LineaComanda(3, "Cerveza", 2.80, 1),
                LineaComanda(9, "Patatas bravas", 5.50, 1),
            ]
        elif mesa_id == "T07":  # Mesa 7
            _ = [
                LineaComanda(4, "Vino tinto", 3.50, 1),
                LineaComanda(10, "Croquetas", 7.00, 1),
                LineaComanda(11, "Paella", 12.00, 2),
            ]
        elif mesa_id == "B01":  # Barra 1
            _ = [
                LineaComanda(5, "Café", 1.30, 2),
                LineaComanda(13, "Tarta", 4.50, 1),
            ]
        else:
            _ = []

        comanda = Comanda(
            id=None,
            _ = mesa_id,
            fecha_apertura=datetime.now(),
            _ = None,
            estado="abierta",
            _ = lineas,
        )

        self._comandas_cache[mesa_id] = comanda

    # === MÉTODOS DE ACCESO A DATOS ===

    def get_mesas(self) -> List[Mesa]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna lista de todas las mesas"""
        return self._mesas_cache.copy()

    def get_mesa_by_id(self, mesa_numero: str) -> Optional[Mesa]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna una mesa por su número (identificador de negocio, ej: 'T01')"""
        for mesa in self._mesas_cache:
            if mesa.numero == mesa_numero:
                return mesa
        return None

    def get_categorias(self) -> List[Dict]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna lista de categorías de productos"""
        return self._categorias_cache.copy()

    def get_productos_by_categoria(self, categoria_id: int) -> List[Producto]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna productos filtrados por categoría"""
        _ = next(
            (
                cat["nombre"]
                for cat in self._categorias_cache
                if cat["id"] == categoria_id
            ),
            None,
        )
        if not categoria_nombre:
            return []

        return [p for p in self._productos_cache if p.categoria == categoria_nombre]

    def get_productos(self, texto_busqueda: str = "") -> List[Producto]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna todos los productos, opcionalmente filtrados por texto de búsqueda"""
        if not texto_busqueda:
            return self._productos_cache.copy()

        texto_busqueda = texto_busqueda.lower()
        return [p for p in self._productos_cache if texto_busqueda in p.nombre.lower()]

    def get_comanda_activa(self, mesa_id: str) -> Optional[Comanda]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna la comanda activa para una mesa - Optimizado con JOIN y cache inteligente"""
        # Thread-safe cache access
        with self._comanda_lock:
            comanda = self._comandas_cache.get(mesa_id)
            if comanda is not None:
                return comanda
                
        # Si no está en caché, cargar con JOIN optimizado
        if not self.db_manager:
            return None
            
        try:
            # Single JOIN query optimizada
            _ = self.db_manager.query(
                """
                SELECT 
                    c.id, c.mesa_id, c.usuario_id, c.fecha_hora, c.estado, c.total,
                    cd.producto_id, cd.cantidad, cd.precio_unitario,
                    p.nombre as producto_nombre
                FROM comandas c
                LEFT JOIN comanda_detalles cd ON c.id = cd.comanda_id
                LEFT JOIN productos p ON cd.producto_id = p.id
                WHERE c.mesa_id = ? AND c.estado IN ('abierta', 'en_proceso')
                ORDER BY c.fecha_hora DESC, cd.id
                LIMIT 50
                """,
                (mesa_id,),
            )
            
            if not rows:
                return None
                
            # Procesar primera comanda encontrada
            _ = rows[0]
            comanda = Comanda(
                id=first_row[0],
                _ = str(first_row[1]),
                fecha_apertura=(
                    datetime.fromisoformat(first_row[3]) if first_row[3] else datetime.now()
                ),
                _ = None,
                estado=first_row[4] or "abierta",
                _ = [],
                usuario_id=first_row[2]
            )
            
            # Procesar todas las líneas de la comanda
            for row in rows:
                if row[0] == comanda.id and row[6]:  # Misma comanda y producto existe
                    _ = LineaComanda(
                        producto_id=row[6],
                        _ = row[9] or f"Producto {row[6]}",
                        precio_unidad=row[8],
                        _ = row[7],
                    )
                    comanda.lineas.append(linea)
            
            # Cache thread-safe
            with self._comanda_lock:
                self._comandas_cache[mesa_id] = comanda
                
            return comanda
            
        except Exception as e:
            self.logger.error(
                f"Error recargando comanda activa desde BD para mesa {mesa_id}: {e}"
            )
            return None

    # === MÉTODOS DE NEGOCIO ===

    def add_producto_comanda(
        self, mesa_id: str, producto_id: int, cantidad: int = 1
    ) -> Comanda:
        """Añade un producto a una comanda"""
        # Obtener comanda o crear una nueva
        comanda = self.get_comanda_activa(mesa_id)
        if not comanda:
            _ = self.crear_comanda(mesa_id)

        # Buscar el producto
        producto = next((p for p in self._productos_cache if p.id == producto_id), None)
        if not producto:
            raise ValueError(f"No existe producto con ID {producto_id}")

        # Verificar si el producto ya está en la comanda
        for linea in comanda.lineas:
            if linea.producto_id == producto_id:
                linea.cantidad += cantidad
                return comanda

        # Si no está, añadir nueva línea
        _ = LineaComanda(
            producto_id=producto.id,
            _ = producto.nombre,
            precio_unidad=producto.precio,
            _ = cantidad,
        )

        comanda.lineas.append(linea)
        return comanda

    def cerrar_comanda(self, mesa_id: str, estado: str = "pagada") -> Optional[Comanda]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cierra una comanda con el estado especificado (pagada o cancelada)"""
        if estado not in ["pagada", "cancelada"]:
            raise ValueError(
                "Estado de comanda no válido. Debe ser 'pagada' o 'cancelada'"
            )

        # Verificar que existe la comanda
        comanda = self.get_comanda_activa(mesa_id)
        if not comanda:
            return None

        # Cerrar la comanda
        comanda.fecha_cierre = datetime.now()
        comanda.estado = estado

        # Liberar la mesa
        for m in self._mesas_cache:
            if m.numero == mesa_id:
                m.estado = "libre"
                break

        # Quitar de comandas activas
        self._comandas_cache.pop(mesa_id)

        # TODO: Persistir en BD

        return comanda

    def cambiar_estado_mesa(self, mesa_id: str, nuevo_estado: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cambia el estado de una mesa"""
        if nuevo_estado not in ["libre", "ocupada", "reservada"]:
            raise ValueError("Estado de mesa no válido")

        # Verificar que la mesa existe
        mesa = self.get_mesa_by_id(mesa_id)
        if not mesa:
            return False

        # Si pasa de ocupada a otro estado, verificar que no tiene comanda activa
        if mesa.estado == "ocupada" and nuevo_estado != "ocupada":
            if mesa_id in self._comandas_cache:
                raise ValueError(
                    "No se puede cambiar el estado de una mesa con comanda activa"
                )

        # Cambiar estado
        for m in self._mesas_cache:
            if m.numero == mesa_id:
                m.estado = nuevo_estado
                return True

        return False

    def cambiar_estado_comanda(
        self, comanda_id: int, nuevo_estado: str, callback: Optional[Any] = None
    ) -> bool:
        """
        Cambia el estado de una comanda (pedido) validando la transición y actualizando en BD y memoria.
        Permite callback/señal para acciones adicionales (notificaciones, impresión, etc).
        """
        _ = {
            "abierta": ["en_proceso", "cancelada"],
            "en_proceso": ["pagada", "cancelada"],
            "pagada": ["cerrada"],
            # "cerrada": []
        }
        # Buscar comanda en caché
        comanda = None
        for c in self._comandas_cache.values():
            if c.id == comanda_id:
                _ = c
                break
        if not comanda:
            self.logger.error("Comanda %s no encontrada", comanda_id)
            return False
        estado_actual = comanda.estado
        if nuevo_estado not in TRANSICIONES_VALIDAS.get(estado_actual, []):
            self.logger.warning(
                f"Transición inválida: {estado_actual} → {nuevo_estado}"
            )
            return False
        # Actualizar en memoria
        comanda.estado = nuevo_estado
        # Persistir toda la comanda (cabecera y líneas) para asegurar consistencia
        if self.db_manager is None:
            self.logger.error(
                f"No se puede actualizar la base de datos: db_manager es None (comanda {comanda_id})"
            )
            return False
        try:
            self.persistir_comanda(comanda)
            self.logger.info(
                f"Comanda {comanda_id} actualizada: {estado_actual} → {nuevo_estado}"
            )
            # Emitir evento o callback si aplica
            if callback:
                callback(comanda)
            # Emitir señal global de comanda actualizada
            try:

                mesa_event_bus.comanda_actualizada.emit(comanda)
            except Exception as e:
    logging.error("Error: %s", e)
            return True
        except Exception as e:
            self.logger.error(
                f"Error actualizando estado de comanda {comanda_id} en BD: {e}"
            )
            return False

    # === MÉTODOS ADICIONALES PARA EL MÓDULO TPV ===

    def get_todas_mesas(self) -> List[Mesa]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna todas las mesas disponibles"""
        return self._mesas_cache.copy()

    def get_mesa_por_id(self, mesa_numero: str) -> Optional[Mesa]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna una mesa por su número (identificador de negocio, ej: 'T01')"""
        for mesa in self._mesas_cache:
            if mesa.numero == mesa_numero:
                return mesa
        return None

    def get_categorias_productos(self) -> List[str]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna todas las categorías de productos"""
        return [cat["nombre"] for cat in self._categorias_cache]

    def get_todos_productos(self) -> List[Producto]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna todos los productos"""
        return self._productos_cache.copy()

    def get_productos_por_categoria(self, categoria: str) -> List[Producto]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna productos de una categoría específica"""
        # Mostrar todos los productos de la categoría, sin filtrar por stock
        return [p for p in self._productos_cache if p.categoria == categoria]

    def get_producto_por_id(self, producto_id: int) -> Optional[Producto]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna un producto por su ID"""
        for producto in self._productos_cache:
            if producto.id == producto_id:
                return producto
        return None

    def get_comandas_activas(self) -> List[Comanda]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna todas las comandas activas"""
        return list(self._comandas_cache.values())

    def get_comanda_por_id(self, comanda_id: int) -> Optional[Comanda]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna una comanda por su ID - Optimizado con JOIN para evitar N+1 queries"""
        # Buscar en caché primero
        for comanda in self._comandas_cache.values():
            if comanda.id == comanda_id:
                return comanda
                
        # Si no está en caché, buscar en BD con JOIN optimizado
        if not self.db_manager:
            return None
            
        try:
            # Single JOIN query para comanda + detalles + productos
            _ = self.db_manager.query(
                """
                SELECT 
                    c.id, c.mesa_id, c.usuario_id, c.fecha_hora, c.estado, c.total,
                    cd.producto_id, cd.cantidad, cd.precio_unitario,
                    p.nombre as producto_nombre
                FROM comandas c
                LEFT JOIN comanda_detalles cd ON c.id = cd.comanda_id
                LEFT JOIN productos p ON cd.producto_id = p.id
                WHERE c.id = ?
                ORDER BY cd.id
                """,
                (comanda_id,),
            )
            
            if not rows:
                return None
                
            # Procesar resultados agrupados
            _ = rows[0]
            comanda = Comanda(
                id=first_row[0],
                _ = str(first_row[1]),
                fecha_apertura=(
                    datetime.fromisoformat(first_row[3]) if first_row[3] else datetime.now()
                ),
                _ = None,
                estado=first_row[4] or "abierta",
                _ = [],
                usuario_id=first_row[2]
            )
            
            # Procesar líneas de la comanda
            for row in rows:
                if row[6]:  # producto_id exists
                    _ = LineaComanda(
                        producto_id=row[6],
                        _ = row[9] or f"Producto {row[6]}",
                        precio_unidad=row[8],
                        _ = row[7],
                    )
                    comanda.lineas.append(linea)
            
            # Guardar en caché (thread-safe)
            with self._comanda_lock:
                self._comandas_cache[comanda.mesa_id] = comanda
                
            return comanda
            
        except Exception as e:
            self.logger.error(
                f"Error recargando comanda por id desde BD para comanda {comanda_id}: {e}"
            )
            return None

    def agregar_producto_a_comanda(
        self,
        comanda_id: int,
        producto_id: int,
        producto_nombre: str,
        precio: float,
        cantidad: int,
    ) -> bool:
        """Agrega un producto a una comanda existente"""
        comanda = self.get_comanda_por_id(comanda_id)
        if not comanda:
            return False

        # Log para diagnóstico: mostrar lineas antes
        self.logger.debug("[agregar_producto_a_comanda] Antes de agregar: lineas=%s", comanda.lineas)

        # Verificar si ya existe el producto en la comanda
        for linea in comanda.lineas:
            if linea.producto_id == producto_id:
                linea.cantidad += cantidad
                self.logger.debug("[agregar_producto_a_comanda] Producto ya existe, nueva cantidad: %s", linea.cantidad)
                self.logger.debug("[agregar_producto_a_comanda] Lineas antes de persistir: %s", comanda.lineas)
                self.persistir_comanda(comanda)
                return True

        # Si no existe, añadir una nueva línea
        _ = LineaComanda(
            producto_id=producto_id,
            _ = producto_nombre,
            precio_unidad=precio,
            _ = cantidad,
        )

        comanda.lineas.append(nueva_linea)
        self.logger.debug("[agregar_producto_a_comanda] Añadido producto nuevo. Lineas antes de persistir: %s", comanda.lineas)
        self.persistir_comanda(comanda)
        return True

    def eliminar_producto_de_comanda(self, comanda_id: int, producto_id: int) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Elimina un producto de una comanda"""
        comanda = self.get_comanda_por_id(comanda_id)
        if not comanda:
            return False

        # Buscar el producto en las líneas
        _ = []
        eliminado = False
        for linea in comanda.lineas:
            if linea.producto_id != producto_id:
                nueva_lineas.append(linea)
            else:
                eliminado = True

        if eliminado:
            comanda.lineas = nueva_lineas
            self.persistir_comanda(comanda)
            return True
        return False

    def cambiar_cantidad_producto(
        self, comanda_id: int, producto_id: int, nueva_cantidad: int
    ) -> bool:
        """Cambia la cantidad de un producto en una comanda"""
        if nueva_cantidad <= 0:
            return self.eliminar_producto_de_comanda(comanda_id, producto_id)

        comanda = self.get_comanda_por_id(comanda_id)
        if not comanda:
            return False

        for linea in comanda.lineas:
            if linea.producto_id == producto_id:
                linea.cantidad = nueva_cantidad
                self.persistir_comanda(comanda)
                return True

        return False

    def crear_comanda(self, mesa_id: str, usuario_id: int = -1) -> Comanda:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Crea una nueva comanda para una mesa.
        Refactorizado para separación de responsabilidades.
        """
        if not self._validate_mesa_for_comanda(mesa_id):
            raise ValueError(f"No se puede crear comanda para mesa {mesa_id}")
            
        # Si ya hay una comanda activa, retornarla
        existing_comanda = self._get_existing_comanda(mesa_id)
        if existing_comanda:
            return existing_comanda

        # Crear y persistir nueva comanda
        comanda = self._create_new_comanda(mesa_id, usuario_id)
        self._setup_comanda_and_mesa(comanda, mesa_id)
        
        return comanda
    
    def _validate_mesa_for_comanda(self, mesa_id: str) -> bool:
        """Valida que se pueda crear una comanda para la mesa"""
        mesa = self.get_mesa_por_id(mesa_id)
        return mesa is not None
    
    def _get_existing_comanda(self, mesa_id: str) -> Optional[Comanda]:
        """Obtiene comanda existente si la hay"""
        with self._comanda_lock:
            return self._comandas_cache.get(mesa_id)
    
    def _create_new_comanda(self, mesa_id: str, usuario_id: int) -> Comanda:
        """Crea una nueva instancia de comanda"""
        _ = Comanda(
            id=None,
            _ = mesa_id,
            fecha_apertura=datetime.now(),
            _ = None,
            estado="abierta",
            _ = [],
            usuario_id=usuario_id,
        )
        
        # Persistir la comanda
        if not self.persistir_comanda(comanda):
            raise RuntimeError(f"Error persistiendo comanda para mesa {mesa_id}")
            
        return comanda
    
    def _setup_comanda_and_mesa(self, comanda: Comanda, mesa_id: str):
        """Configura la comanda y actualiza el estado de la mesa"""
        # Actualizar cache
        with self._comanda_lock:
            self._comandas_cache[mesa_id] = comanda
            
        # Actualizar mesa y emitir eventos
        mesa = self.get_mesa_por_id(mesa_id)
        if mesa:
            mesa.estado = "ocupada"
            self._emit_comanda_events(comanda, mesa)
    
    def _emit_comanda_events(self, comanda: Comanda, mesa: Mesa):
        """Emite eventos de actualización de comanda y mesa"""
        try:
            if mesa_event_bus:
                mesa_event_bus.mesa_actualizada.emit(mesa)
                mesa_event_bus.emit_comanda_actualizada(comanda)
        except Exception as e:
            self.logger.error("Error emitiendo eventos: %s", e)


    def pagar_comanda(self, comanda_id: int, usuario_id: int = -1) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Procesa el pago de una comanda. Refactorizado para separación de responsabilidades."""
        comanda = self.get_comanda_por_id(comanda_id)
        if not comanda:
            return False

        try:
            # Procesar pago en pasos separados
            if not self._process_stock_deduction(comanda, usuario_id):
                return False
                
            if not self._mark_comanda_as_paid(comanda):
                return False
                
            self._release_mesa_from_comanda(comanda)
            self._emit_payment_events(comanda)
            
            return True
            
        except Exception as e:
            self.logger.error("Error procesando pago de comanda {comanda_id}: %s", e)
            return False
    
    def _process_stock_deduction(self, comanda: Comanda, usuario_id: int) -> bool:
        """Procesa la deducción de stock para todos los productos de la comanda"""
        if not self.db_manager:
            return True  # Skip if no DB
            
        for linea in comanda.lineas:
            try:
                self.db_manager.descontar_stock_y_registrar(
                    _ = linea.producto_id,
                    cantidad=linea.cantidad,
                    _ = usuario_id,
                    observaciones=f"Venta comanda {comanda.id}",
                )
            except Exception as e:
                self.logger.error(
                    f"Error descontando stock producto {linea.producto_id}: {e}"
                )
                return False
        return True
    
    def _mark_comanda_as_paid(self, comanda: Comanda) -> bool:
        """Marca la comanda como pagada en BD"""
        comanda.estado = "pagada"
        comanda.fecha_cierre = datetime.now()
        
        if not self.db_manager:
            return True
            
        try:
            self.db_manager.execute(
                "UPDATE comandas SET estado = ?, fecha_cierre = ? WHERE id = ?",
                (
                    "pagada",
                    comanda.fecha_cierre.strftime("%Y-%m-%d %H:%M:%S"),
                    comanda.id,
                ),
            )
            return True
        except Exception as e:
            self.logger.error(
                f"Error actualizando estado de comanda {comanda.id} en BD: {e}"
            )
            return False
    
    def _release_mesa_from_comanda(self, comanda: Comanda):
        """Libera la mesa asociada a la comanda"""
        mesa = self.get_mesa_por_id(comanda.mesa_id)
        if not mesa:
            return
            
        # Actualizar estado de mesa
        mesa.estado = "libre"
        mesa.alias = None
        mesa.personas_temporal = None
        
        # Persistir en BD
        if self.db_manager:
            try:
                self.db_manager.execute(
                    "UPDATE mesas SET estado = ? WHERE id = ?",
                    ("libre", mesa.id),
                )
            except Exception as e:
                self.logger.error("Error liberando mesa {mesa.id} en BD: %s", e)
    
    def _emit_payment_events(self, comanda: Comanda):
        """Emite eventos de actualización tras el pago"""
        _ = self.get_mesa_por_id(comanda.mesa_id)
        
        if mesa_event_bus:
            try:
                if mesa:
                    mesa_event_bus.mesa_actualizada.emit(mesa)
                mesa_event_bus.comanda_actualizada.emit(comanda)
            except Exception as e:
                self.logger.error("Error emitiendo eventos de pago: %s", e)

    def liberar_mesa(self, mesa_id: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Libera una mesa y elimina su comanda"""
        # Verificar que existe la mesa
        mesa = self.get_mesa_por_id(mesa_id)
        if not mesa:
            return False

        # Cambiar estado, eliminar comanda y resetear nombre temporal
        for m in self._mesas_cache:
            if m.numero == mesa_id:
                m.estado = "libre"
                m.alias = None  # Resetear alias al liberar mesa
                m.personas_temporal = None  # Resetear personas temporal al liberar mesa
                break

        if mesa_id in self._comandas_cache:
            del self._comandas_cache[mesa_id]

        # Log eliminado por redundante
        return True

    def generar_siguiente_numero_mesa(self, zona: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Genera el siguiente número de mesa contextualizado por zona.

        Args:
            zona: Zona donde se creará la mesa (ej: "Terraza", "Interior", "VIP", "Principal")

        Returns:
            str: Siguiente número disponible para la zona (ej: "T05", "I03", "V02", "P12")
        """
        try:
            # Obtener todas las mesas de la zona específica
            mesas_zona = [mesa for mesa in self._mesas_cache if mesa.zona == zona]

            # Si no hay mesas en la zona, empezar con 01
            if not mesas_zona:
                zona_inicial = zona[0].upper() if zona else "P"
                return f"{zona_inicial}01"

            # Extraer números existentes de la zona
            _ = []
            zona_inicial = zona[0].upper() if zona else "P"

            for mesa in mesas_zona:
                # Intentar extraer el número del identificador de la mesa
                _ = mesa.numero

                # Si el número ya tiene el formato de zona (T01, I05, etc.)
                if len(numero_str) >= 2 and numero_str[0].upper() == zona_inicial:
                    try:
                        numero = int(numero_str[1:])
                        numeros_existentes.append(numero)
                    except ValueError:
                        # Si no se puede convertir, usar el número tal como está
                        try:
                            numero = int(numero_str)
                            numeros_existentes.append(numero)
                        except ValueError:
                            continue
                else:
                    # Si es un número simple, usarlo directamente
                    try:
                        numero = int(numero_str)
                        numeros_existentes.append(numero)
                    except ValueError:
                        continue

            # Encontrar el siguiente número disponible
            _ = 1
            if numeros_existentes:
                _ = max(numeros_existentes) + 1

            # Formatear con ceros a la izquierda
            return f"{zona_inicial}{siguiente_numero:02d}"

        except Exception as e:
            logger.error(
                f"Error generando siguiente número de mesa para zona {zona}: {e}"
            )
            # Fallback: usar zona inicial + 01
            zona_inicial = zona[0].upper() if zona else "P"
            return f"{zona_inicial}01"

    def crear_mesa(self, capacidad: int, zona: str = "Principal") -> Optional[Mesa]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Crea una nueva mesa con numeración automática contextualizada por zona.

        Args:
            capacidad: Número de personas que puede acomodar la mesa
            zona: Zona donde se ubicará la mesa

        Returns:
            Mesa: Nueva mesa creada o None si hay error
        """
        # Input validation
        if not isinstance(capacidad, int) or capacidad <= 0:
            logger.error("Capacidad inválida: %s", capacidad)
            return None
            
        if not zona or not isinstance(zona, str) or len(zona.strip()) == 0:
            logger.error("Zona inválida: %s", zona)
            return None
            
        _ = zona.strip()
        
        try:
            if not self.db_manager:
                logger.warning("No hay conexión a base de datos para crear mesa")
                return None

            # Generar automáticamente el siguiente número para la zona
            _ = self.generar_siguiente_numero_mesa(zona)

            # Verificar que no existe una mesa con ese número (por seguridad)
            for mesa_existente in self._mesas_cache:
                if mesa_existente.numero == numero_mesa:
                    logger.warning("Ya existe una mesa con el número %s", numero_mesa)
                    # Intentar con el siguiente número
                    _ = zona[0].upper() if zona else "P"
                    siguiente = int(numero_mesa[1:]) + 1
                    _ = f"{zona_inicial}{siguiente:02d}"

            # Crear nueva mesa en la base de datos
            _ = self.db_manager.execute(
                """
                INSERT INTO mesas (numero, zona, estado, capacidad)
                VALUES (?, ?, ?, ?)
            """,
                (numero_mesa, zona, "libre", capacidad),
            )

            # Crear objeto Mesa y agregarlo al cache
            _ = Mesa(
                id=mesa_id,
                _ = numero_mesa,
                zona=zona,
                _ = "libre",
                capacidad=capacidad,
            )

            self._mesas_cache.append(nueva_mesa)
            logger.info(
                f"Mesa {numero_mesa} creada correctamente en zona {zona} con ID {mesa_id}"
            )

            # Emitir evento global de mesas actualizadas

            mesa_event_bus.mesas_actualizadas.emit(self._mesas_cache.copy())

            return nueva_mesa

        except Exception as e:
            logger.error("Error creando mesa: %s", e)
            return None

    def crear_mesa_con_numero(
        self, numero: int, capacidad: int, zona: str = "Principal"
    ) -> Optional[Mesa]:
        """
        Método de compatibilidad para crear mesa con número específico.

        Args:
            numero: Número específico para la mesa
            capacidad: Número de personas que puede acomodar la mesa
            zona: Zona donde se ubicará la mesa

        Returns:
            Mesa: Nueva mesa creada o None si hay error
        """
        try:
            if not self.db_manager:
                logger.warning("No hay conexión a base de datos para crear mesa")
                return None

            # Verificar que no existe una mesa con ese número
            for mesa_existente in self._mesas_cache:
                if mesa_existente.numero == str(numero):
                    logger.warning("Ya existe una mesa con el número %s", numero)
                    return None

            # Crear nueva mesa en la base de datos
            _ = self.db_manager.execute(
                """
                INSERT INTO mesas (numero, zona, estado, capacidad)
                VALUES (?, ?, ?, ?)
            """,
                (str(numero), zona, "libre", capacidad),
            )

            # Crear objeto Mesa y agregarlo al cache
            _ = Mesa(
                id=mesa_id,
                _ = str(numero),
                zona=zona,
                _ = "libre",
                capacidad=capacidad,
            )

            self._mesas_cache.append(nueva_mesa)
            # Log eliminado por redundante

            return nueva_mesa

        except Exception as e:
            logger.error("Error creando mesa: %s", e)
            return None

    def eliminar_mesa(self, mesa_id: int) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Elimina una mesa de la base de datos"""
        try:
            if not self.db_manager:
                logger.warning("No hay conexión a base de datos para eliminar mesa")
                return False

            # Verificar que la mesa existe
            _ = None
            for mesa in self._mesas_cache:
                if mesa.id == mesa_id:
                    _ = mesa
                    break

            if not mesa_existente:
                logger.warning("No se encontró la mesa con ID %s", mesa_id)
                return False

            # Verificar que la mesa no esté ocupada
            if mesa_existente.estado == "ocupada":
                logger.warning(
                    f"No se puede eliminar la mesa {mesa_existente.numero} porque está ocupada"
                )
                return False

            # Eliminar de la base de datos
            self.db_manager.execute("DELETE FROM mesas WHERE id = ?", (mesa_id,))

            # Eliminar del cache
            self._mesas_cache = [
                mesa for mesa in self._mesas_cache if mesa.id != mesa_id
            ]

            logger.info(
                f"Mesa {mesa_existente.numero} eliminada correctamente de la base de datos"
            )
            return True

        except Exception as e:
            logger.error("Error eliminando mesa: %s", e)
            return False

    def cambiar_personas_temporal_mesa(self, mesa_id: str, nuevo_numero: int) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cambia el número de personas temporal de una mesa (no persistente)"""
        mesa = self.get_mesa_por_id(mesa_id)
        if mesa:
            mesa.personas_temporal = nuevo_numero
            return True
        return False

    def resetear_personas_mesa(self, mesa_id: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Resetea el número de personas temporal de una mesa"""
        mesa = self.get_mesa_por_id(mesa_id)
        if mesa:
            mesa.personas_temporal = None
            return True
        return False

    def cambiar_alias_mesa(self, mesa_id: str, nuevo_alias: Optional[str]) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cambia el alias temporal de una mesa (solo en memoria)"""
        try:
            # Validar alias
            if nuevo_alias is not None:
                nuevo_alias = nuevo_alias.strip()
            if not nuevo_alias:
                _ = None
            # Buscar y actualizar la mesa
            for mesa in self._mesas_cache:
                if mesa.id == mesa_id:
                    mesa.alias = nuevo_alias
                    self.logger.info(
                        f"Alias de mesa {mesa.numero} cambiado a: {nuevo_alias}"
                    )
                    return True
            return False
        except Exception as e:
            self.logger.error("Error cambiando alias de mesa {mesa_id}: %s", e)
            return False

    def resetear_alias_mesa(self, mesa_id: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Resetea el alias de una mesa al nombre por defecto"""
        try:
            for mesa in self._mesas_cache:
                if mesa.id == mesa_id:
                    mesa.alias = None
                    self.logger.info(
                        f"Alias de mesa {mesa.numero} reseteado al defecto"
                    )
                    return True
            return False
        except Exception as e:
            self.logger.error("Error reseteando alias de mesa {mesa_id}: %s", e)
            return False

    def crear_reserva(
        self,
        mesa_id: str,
        cliente: str,
        fecha_hora: datetime,
        duracion_min: int = 120,
        telefono: str = "",
        personas: int = 1,
        notas: str = "",
    ) -> Optional[Reserva]:
        """Crea una reserva persistente para una mesa (modelo unificado) y actualiza el estado de la mesa en BD a 'reservada'."""
        # Input validation
        if not mesa_id or not isinstance(mesa_id, str):
            self.logger.error("Mesa ID inválido")
            return None
            
        if not cliente or not isinstance(cliente, str) or len(cliente.strip()) == 0:
            self.logger.error("Cliente inválido")
            return None
            
        if not isinstance(fecha_hora, datetime):
            self.logger.error("Fecha/hora inválida")
            return None
            
        if not isinstance(duracion_min, int) or duracion_min <= 0:
            self.logger.error("Duración inválida: %s", duracion_min)
            return None
            
        if not isinstance(personas, int) or personas <= 0:
            self.logger.error("Número de personas inválido: %s", personas)
            return None
            
        _ = cliente.strip()
        telefono = telefono.strip() if telefono else ""
        _ = notas.strip() if notas else ""
        
        if not self.db_manager:
            self.logger.warning("No hay conexión a base de datos para crear reserva")
            return None
        # Validar solapamiento
        if self.reserva_solapada(
            mesa_id, fecha_hora.date(), fecha_hora.time(), duracion_min
        ):
            self.logger.warning(
                "Ya existe una reserva para esa mesa, fecha y rango horario"
            )
            return None
        try:
            _ = self.db_manager.execute(
                """
                INSERT INTO reservas (mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    mesa_id,
                    cliente,
                    fecha_hora.isoformat(),
                    duracion_min,
                    "activa",
                    notas,
                    telefono,
                    personas,
                ),
            )
            # --- FIX: Actualizar el estado de la mesa en la base de datos a 'reservada' ---
            try:
                self.db_manager.execute(
                    "UPDATE mesas SET estado = ? WHERE numero = ?",
                    ("reservada", mesa_id),
                )
            except Exception as e:
                self.logger.error("Error actualizando estado de mesa {mesa_id} a 'reservada' en BD: %s", e)
            return Reserva(
                id=reserva_id,
                _ = mesa_id,
                cliente_nombre=cliente,
                _ = telefono,
                fecha_reserva=fecha_hora.date(),
                _ = fecha_hora.strftime("%H:%M"),
                numero_personas=personas,
                _ = "confirmada",
                notas=notas,
            )
        except Exception as e:
            self.logger.error("Error creando reserva: %s", e)
            return None

    def get_reservas_mesa(self, mesa_id: str, fecha: Optional[date] = None) -> list:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene reservas activas de una mesa - Optimizado con cache y batch loading"""
        if not self.db_manager:
            return []
            
        # Cache key para reservas
        _ = f"{mesa_id}_{fecha.isoformat() if fecha else 'all'}"
        
        # Verificar cache de reservas
        if not hasattr(self, '_reservas_cache'):
            self._reservas_cache = {}
            
        if cache_key in self._reservas_cache:
            return self._reservas_cache[cache_key]
            
        try:
            # Query optimizada con índices
            if fecha:
                _ = """
                    SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas 
                    FROM reservas 
                    WHERE mesa_id = ? AND estado = 'activa' AND date(fecha_hora) = ?
                    ORDER BY fecha_hora
                """
                _ = (mesa_id, fecha.isoformat())
            else:
                _ = """
                    SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas 
                    FROM reservas 
                    WHERE mesa_id = ? AND estado = 'activa'
                    ORDER BY fecha_hora
                """
                _ = (mesa_id,)
                
            _ = self.db_manager.query(query, params)
            
            reservas = [
                Reserva(
                    id=row[0],
                    _ = row[1],
                    cliente_nombre=row[2],
                    _ = row[7] or "",
                    fecha_reserva=datetime.fromisoformat(row[3]).date(),
                    _ = datetime.fromisoformat(row[3]).strftime("%H:%M"),
                    numero_personas=row[8] if row[8] is not None else 1,
                    _ = row[5],
                    notas=row[6] or "",
                )
                for row in rows
            ]
            
            # Cache result
            self._reservas_cache[cache_key] = reservas
            return reservas
            
        except Exception as e:
            self.logger.error("Error obteniendo reservas: %s", e)
            return []

    def cancelar_reserva(self, reserva_id: int) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cancela una reserva por su ID y actualiza el estado de la mesa en BD a 'libre' si no hay más reservas activas."""
        if not self.db_manager:
            return False
        try:
            # Obtener mesa_id de la reserva antes de cancelar
            _ = self.db_manager.query(
                "SELECT mesa_id FROM reservas WHERE id = ?", (reserva_id,)
            )
            _ = row[0][0] if row and len(row[0]) > 0 else None
            self.db_manager.execute(
                "UPDATE reservas SET estado = 'cancelada' WHERE id = ?", (reserva_id,)
            )
            # Si no hay más reservas activas para esa mesa, actualizar estado a 'libre'
            if mesa_id:
                _ = self.db_manager.query(
                    "SELECT COUNT(*) FROM reservas WHERE mesa_id = ? AND estado = 'activa'",
                    (mesa_id,),
                )
                if rows and rows[0][0] == 0:
                    try:
                        self.db_manager.execute(
                            "UPDATE mesas SET estado = ? WHERE numero = ?",
                            ("libre", mesa_id),
                        )
                    except Exception as e:
                        self.logger.error("Error actualizando estado de mesa {mesa_id} a 'libre' en BD: %s", e)
            return True
        except Exception as e:
            self.logger.error("Error cancelando reserva: %s", e)
            return False

    def reserva_solapada(
        self, mesa_id: str, fecha: date, hora: time, duracion_min: int = 120
    ) -> bool:
        """Comprueba si existe una reserva activa para la mesa en la fecha y rango horario dados (solapamiento real)"""
        if not self.db_manager:
            return False
        try:
            from datetime import datetime, timedelta

            hora_inicio_nueva = datetime.combine(fecha, hora)
            hora_fin_nueva = hora_inicio_nueva + timedelta(minutes=duracion_min)
            _ = self.db_manager.query(
                "SELECT hora, duracion_min FROM reservas WHERE mesa_id = ? AND fecha = ? AND estado = 'activa'",
                (mesa_id, fecha.isoformat()),
            )
            for row in rows:
                _ = datetime.combine(
                    fecha, datetime.strptime(row[0], "%H:%M:%S").time()
                )
                _ = row[1] if row[1] is not None else 120
                hora_fin_existente = hora_existente + timedelta(
                    _ = duracion_existente
                )
                # Solapamiento: inicio < fin_existente y fin > inicio_existente
                if (hora_inicio_nueva < hora_fin_existente) and (
                    hora_fin_nueva > hora_existente
                ):
                    return True
            return False
        except Exception as e:
            self.logger.error("Error comprobando solapamiento de reserva: %s", e)
            return False


# TODO: Revisar y migrar todos los usos de Reserva en el sistema para usar este modelo unificado.
# TODO: Documentar en README de área y dejar registro de excepción si algún flujo requiere compatibilidad temporal.
    # === MÉTODOS DE OPTIMIZACIÓN Y CACHE ===
    
    def clear_cache(self, cache_type: str = "all"):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Limpia caches para optimizar memoria - Thread safe"""
        try:
            with self._cache_lock:
                if cache_type == "all" or cache_type == "reservas":
                    self._reservas_cache.clear()
                    
                if cache_type == "all" or cache_type == "historical":
                    self._historical_cache.clear()
                    
                if cache_type == "all" or cache_type == "comandas":
                    with self._comanda_lock:
                        # Solo limpiar comandas cerradas del cache
                        _ = {k: v for k, v in self._comandas_cache.items() 
                                         if v.estado in ('abierta', 'en_proceso')}
                        self._comandas_cache = active_comandas
                        
            self.logger.info("Cache %s limpiado exitosamente", cache_type)
            
        except Exception as e:
            self.logger.error("Error limpiando cache {cache_type}: %s", e)
    
    def get_cache_stats(self) -> Dict[str, int]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna estadísticas de uso de cache"""
        try:
            with self._cache_lock:
                return {
                    "mesas_cache": len(self._mesas_cache),
                    "productos_cache": len(self._productos_cache),
                    "comandas_cache": len(self._comandas_cache),
                    "reservas_cache": len(getattr(self, '_reservas_cache', {})),
                    "historical_cache": len(getattr(self, '_historical_cache', {})),
                }
        except Exception as e:
            self.logger.error("Error obteniendo estadísticas de cache: %s", e)
            return {}
    
    def optimize_performance(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Optimiza el rendimiento del servicio"""
        try:
            # Limpiar caches antiguos
            self.clear_cache("historical")
            
            # Recargar datos críticos si es necesario
            if not self._mesas_cache and self.db_manager:
                self._load_mesas_from_db()
                
            if not self._productos_cache and self.db_manager:
                self._load_productos_from_db()
                
            self.logger.info("Optimización de rendimiento completada")
            
        except Exception as e:
            self.logger.error("Error en optimización de rendimiento: %s", e)