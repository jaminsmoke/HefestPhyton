# Servicio de gestión del Terminal Punto de Venta (TPV).

import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, date, time, timedelta

from .base_service import BaseService
from core.hefest_data_models import Reserva

logger = logging.getLogger(__name__)


@dataclass
class Mesa:
    """Clase de datos para una mesa"""

    numero: str  # Identificador único de negocio (ej: 'T01', 'I04')
    capacidad: int
    estado: str  # libre, ocupada, reservada
    zona: str  # Comedor, terraza, barra
    id: Optional[int] = None  # Solo referencia interna (autoincremental BD)
    alias: Optional[str] = None  # Alias temporal de la mesa (no persistente)
    personas_temporal: Optional[int] = (
        None  # Número de personas temporal (no persistente)
    )
    notas: Optional[str] = None  # Notas temporales de la mesa (no persistente)
    reservada: bool = False  # Indica si la mesa está reservada actualmente
    proxima_reserva: Optional[object] = (
        None  # Reserva futura más próxima (no persistente)
    )

    @property
    def nombre_display(self) -> str:
        """
        Obtiene el nombre a mostrar para la mesa:
        1. Si hay próxima reserva activa y tiene cliente_nombre, mostrar ese nombre
        2. Si hay alias temporal, mostrar alias
        3. Si no, mostrar nombre predeterminado
        """
        if self.proxima_reserva is not None:
            cliente = getattr(self.proxima_reserva, "cliente_nombre", None)
            if cliente:
                return cliente
        if self.alias:
            return self.alias
        return f"Mesa {self.numero}"

    @property
    def personas_display(self) -> int:
        """Obtiene el número de personas a mostrar:
        - Si hay próxima reserva activa y tiene personas válidas, muestra ese valor
        - Si no, muestra el valor temporal si existe
        - Si no, la capacidad real de la mesa
        """
        # 1. Prioridad: próxima reserva activa
        if self.proxima_reserva is not None:
            # Intentar primero 'numero_personas' (modelo unificado), luego 'personas' (legacy)
            personas_reserva = getattr(self.proxima_reserva, "numero_personas", None)
            if personas_reserva is None:
                personas_reserva = getattr(self.proxima_reserva, "personas", None)
            if (
                personas_reserva is not None
                and isinstance(personas_reserva, int)
                and personas_reserva > 0
            ):
                return personas_reserva
        # 2. Valor temporal (edición manual)
        if self.personas_temporal is not None:
            return self.personas_temporal
        # 3. Capacidad real
        return self.capacidad


@dataclass
class Producto:
    """Clase de datos para un producto"""

    id: int
    nombre: str
    precio: float
    categoria: str
    stock_actual: Optional[int] = None


@dataclass
class LineaComanda:
    """Clase de datos para una línea de comanda"""

    producto_id: int
    producto_nombre: str
    precio_unidad: float
    cantidad: int

    @property
    def total(self) -> float:
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
        total = 0
        for desc in self.descuentos:
            if desc.tipo == "porcentaje":
                total += self.subtotal * (desc.valor / 100)
            else:  # cantidad_fija
                total += desc.valor
        return total

    @property
    def total_pagado(self) -> float:
        return sum(pago.monto for pago in self.metodos_pago)

    @property
    def cambio(self) -> float:
        return max(0, self.total_pagado - self.total)


@dataclass
class TPVService(BaseService):
    def eliminar_mesa_por_numero(self, numero: str) -> bool:
        """Elimina una mesa de la base de datos usando el identificador string 'numero'"""
        try:
            if not self.db_manager:
                logger.warning("No hay conexión a base de datos para eliminar mesa")
                return False

            # Buscar la mesa por numero
            mesa_existente = None
            for mesa in self._mesas_cache:
                if mesa.numero == numero:
                    mesa_existente = mesa
                    break

            if not mesa_existente:
                logger.warning(f"No se encontró la mesa con numero {numero}")
                return False

            # Verificar que la mesa no esté ocupada
            if mesa_existente.estado == "ocupada":
                logger.warning(
                    f"No se puede eliminar la mesa {mesa_existente.numero} porque está ocupada"
                )
                return False

            # Eliminar de la base de datos
            self.db_manager.execute("DELETE FROM mesas WHERE numero = ?", (numero,))

            # Eliminar del cache
            self._mesas_cache = [
                mesa for mesa in self._mesas_cache if mesa.numero != numero
            ]

            logger.info(
                f"Mesa {mesa_existente.numero} eliminada correctamente de la base de datos (por numero)"
            )
            return True

        except Exception as e:
            logger.error(f"Error eliminando mesa por numero: {e}")
            return False

    def persistir_comanda(self, comanda: Comanda) -> bool:
        """
        Persiste la comanda y sus líneas en la base de datos.
        Si la comanda existe, la actualiza; si no, la inserta.
        Borra y vuelve a insertar las líneas para reflejar el estado actual.
        """
        if not self.db_manager:
            self.logger.error("No hay conexión a base de datos para persistir comanda")
            return False
        try:
            # Insertar o actualizar comanda
            comanda_data = {
                "id": comanda.id,
                "mesa_id": comanda.mesa_id,
                "usuario_id": comanda.usuario_id,
                "fecha_hora": comanda.fecha_apertura.strftime("%Y-%m-%d %H:%M:%S"),
                "estado": comanda.estado,
                "total": comanda.total,
            }
            # Intentar actualizar, si no existe, insertar
            updated = self.db_manager.update("comandas", comanda.id, comanda_data)
            if not updated:
                self.db_manager.insert("comandas", comanda_data)

            # Borrar líneas anteriores
            with self.db_manager._get_connection() as conn:
                conn.execute(
                    "DELETE FROM comanda_detalles WHERE comanda_id = ?", (comanda.id,)
                )
                # Insertar líneas actuales
                for linea in comanda.lineas:
                    detalle = {
                        "comanda_id": comanda.id,
                        "producto_id": linea.producto_id,
                        "cantidad": linea.cantidad,
                        "precio_unitario": linea.precio_unidad,
                        "notas": getattr(linea, "notas", None),
                    }
                    self.db_manager.insert("comanda_detalles", detalle)
                conn.commit()
                # Auditoría: consultar líneas tras commit
                cursor = conn.execute(
                    "SELECT producto_id, cantidad, precio_unitario FROM comanda_detalles WHERE comanda_id = ?",
                    (comanda.id,),
                )
                lineas_db = cursor.fetchall()
                # Log de auditoría eliminado por redundante
            # Emitir señal global de comanda actualizada
            try:
                from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

                mesa_event_bus.comanda_actualizada.emit(comanda)
            except Exception:
                pass
            return True
        except Exception as e:
            self.logger.error(f"Error persistiendo comanda {comanda.id}: {e}")
            return False

    def update_mesa(self, mesa_actualizada: "Mesa") -> bool:
        """
        Actualiza una mesa en la base de datos y en el caché global.
        Emite eventos globales tras la persistencia para sincronización desacoplada.
        """
        from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

        try:
            if not self.db_manager:
                logger.warning("No hay conexión a base de datos para actualizar mesa")
                return False
            # Actualizar en base de datos (solo campos persistentes)
            self.db_manager.execute(
                """
                UPDATE mesas SET numero = ?, zona = ?, estado = ?, capacidad = ?, notas = ? WHERE id = ?
                """,
                (
                    mesa_actualizada.numero,
                    mesa_actualizada.zona,
                    mesa_actualizada.estado,
                    mesa_actualizada.capacidad,
                    mesa_actualizada.notas,
                    mesa_actualizada.id,
                ),
            )
            # Actualizar en caché (incluye alias temporal y otros campos no persistentes)
            for idx, mesa in enumerate(self._mesas_cache):
                if mesa.id == mesa_actualizada.id:
                    self._mesas_cache[idx] = mesa_actualizada
                    break
            # Emisión global: mesa individual y lista completa
            mesa_event_bus.mesa_actualizada.emit(mesa_actualizada)
            mesa_event_bus.mesas_actualizadas.emit(self._mesas_cache.copy())
            return True
        except Exception as e:
            logger.error(f"Error actualizando mesa: {e}")
            return False

    """Servicio para la gestión del TPV"""

    def __init__(self, db_manager=None):
        super().__init__(db_manager)
        import logging

        logger = logging.getLogger(__name__)
        logger.info(
            f"[TPVService] db_manager recibido en constructor: {type(db_manager)} - {db_manager}"
        )
        self._mesas_cache = []
        self._categorias_cache = []
        self._productos_cache = []
        self._comandas_cache = {}  # {mesa_id: Comanda}
        self._next_comanda_id = 1  # ID para comandas

        self._load_datos()

    def get_service_name(self) -> str:
        """Retorna el nombre de este servicio"""
        return "TPVService"

    def _load_datos(self):
        """Carga los datos desde la base de datos o crea datos de prueba"""
        data_loaded = False

        if self.db_manager:
            self.logger.info("Intentando cargar datos del TPV desde base de datos")
            # print("[DEBUG TPVService] _load_datos: llamando a _load_mesas_from_db")  # Eliminado debug
            self._load_mesas_from_db()
            # print(f"[DEBUG TPVService] _load_datos: después de _load_mesas_from_db, _mesas_cache tiene {len(self._mesas_cache)} mesas")  # Eliminado debug
            self._load_categorias_from_db()
            self._load_productos_from_db()
            self._load_comandas_from_db()

            # Verificar si se cargaron datos
            if self._mesas_cache or self._productos_cache:
                data_loaded = True
                self.logger.info("Datos cargados exitosamente desde base de datos")
                # Emitir la señal global con la lista inicial de mesas
                from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

                mesa_event_bus.mesas_actualizadas.emit(self._mesas_cache.copy())

        # Si no hay base de datos o no se cargaron datos, usar datos de prueba
        if not data_loaded:
            if self.db_manager:
                self.logger.warning("Base de datos vacía, cargando datos de prueba")
            else:
                # Eliminado log obsoleto: ya no se permite inicializar sin base de datos en producción
                pass
            self._load_datos_prueba()
            # Emitir la señal global con la lista inicial de mesas de prueba
            from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

            mesa_event_bus.mesas_actualizadas.emit(self._mesas_cache.copy())

    def _load_mesas_from_db(self):
        """Carga las mesas desde la base de datos"""
        if not self.db_manager:
            self.logger.warning("No hay gestor de base de datos disponible")
            return

        try:
            # print("[DEBUG TPVService] _load_mesas_from_db llamado")  # Eliminado debug
            result = self.db_manager.query(
                "SELECT id, numero, zona, estado, capacidad FROM mesas"
            )
            self._mesas_cache = []
            for row in result:
                mesa = Mesa(
                    id=row[0],
                    numero=row[1],
                    zona=row[2] or "Sin zona",
                    estado=row[3] or "libre",
                    capacidad=row[4] or 4,
                )
                self._mesas_cache.append(mesa)
            # print(f"[DEBUG TPVService] _load_mesas_from_db: {len(self._mesas_cache)} mesas cargadas")  # Eliminado debug
            self.logger.info(
                f"Cargadas {len(self._mesas_cache)} mesas desde la base de datos"
            )
        except Exception as e:
            self.logger.error(f"Error cargando mesas: {e}")
            # print(f"[DEBUG TPVService] _load_mesas_from_db: error {e}")  # Eliminado debug
            self._mesas_cache = []

    def _load_categorias_from_db(self):
        """Carga las categorías desde la base de datos"""
        if not self.db_manager:
            self.logger.warning("No hay gestor de base de datos disponible")
            return

        try:
            result = self.db_manager.query(
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
            self.logger.error(f"Error cargando categorías: {e}")
            self._categorias_cache = []

    def _load_productos_from_db(self):
        """Carga los productos desde la base de datos"""
        if not self.db_manager:
            self.logger.warning("No hay gestor de base de datos disponible")
            return

        try:
            result = self.db_manager.query(
                """
                SELECT id, nombre, precio, categoria, stock_actual
                FROM productos
                WHERE precio IS NOT NULL AND precio > 0
            """
            )
            self._productos_cache = []
            for row in result:
                producto = Producto(
                    id=row[0],
                    nombre=row[1],
                    precio=row[2] or 0.0,
                    categoria=row[3] or "Sin categoría",
                    stock_actual=row[4] if row[4] is not None else None,
                )
                self._productos_cache.append(producto)
            self.logger.info(
                f"Cargados {len(self._productos_cache)} productos desde la base de datos"
            )
        except Exception as e:
            self.logger.error(f"Error cargando productos: {e}")
            self._productos_cache = []

    def _load_comandas_from_db(self):
        """Carga las comandas activas desde la base de datos"""
        if not self.db_manager:
            self.logger.warning("No hay gestor de base de datos disponible")
            return

        try:
            result = self.db_manager.query(
                """
                SELECT id, mesa_id, usuario_id, fecha_hora, estado, total
                FROM comandas
                WHERE estado IN ('abierta', 'en_proceso')
            """
            )
            self._comandas_cache = {}
            for row in result:
                comanda_id = row[0]
                mesa_id = row[1]

                # Cargar detalles de la comanda
                detalles = self.db_manager.query(
                    """
                    SELECT producto_id, cantidad, precio_unitario
                    FROM comanda_detalles
                    WHERE comanda_id = ?
                """,
                    (comanda_id,),
                )
                lineas = []
                for detalle in detalles:
                    producto = next(
                        (p for p in self._productos_cache if p.id == detalle[0]), None
                    )
                    if producto and hasattr(producto, "nombre"):
                        nombre_producto = producto.nombre
                    else:
                        nombre_producto = f"Producto {detalle[0]}"

                    linea = LineaComanda(
                        producto_id=detalle[0],
                        producto_nombre=nombre_producto,
                        precio_unidad=detalle[2],
                        cantidad=detalle[1],
                    )
                    lineas.append(linea)

                # Log de auditoría de líneas recuperadas
                # Log de auditoría eliminado por redundante

                comanda = Comanda(
                    id=comanda_id,
                    mesa_id=mesa_id,
                    fecha_apertura=(
                        datetime.fromisoformat(row[3]) if row[3] else datetime.now()
                    ),
                    fecha_cierre=None,
                    estado=row[4] or "abierta",
                    lineas=lineas,
                )
                self._comandas_cache[mesa_id] = comanda
            # Log de auditoría de caché final
            # Log de auditoría eliminado por redundante
            self.logger.info(
                f"Cargadas {len(self._comandas_cache)} comandas activas desde la base de datos"
            )
        except Exception as e:
            self.logger.error(f"Error cargando comandas: {e}")
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
        mesa_ocupada_numeros = [
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
        mesa_ocupada_numeros = [
            mesa.numero for mesa in self._mesas_cache if mesa.estado == "ocupada"
        ]
        for mesa_numero in mesa_ocupada_numeros:
            self._crear_comanda_prueba(mesa_numero)

    def _crear_comanda_prueba(self, mesa_id: str):
        """Crea una comanda de prueba para una mesa"""
        if mesa_id == "T02":  # Mesa 2
            lineas = [
                LineaComanda(1, "Coca Cola", 2.50, 2),
                LineaComanda(3, "Cerveza", 2.80, 1),
                LineaComanda(9, "Patatas bravas", 5.50, 1),
            ]
        elif mesa_id == "T07":  # Mesa 7
            lineas = [
                LineaComanda(4, "Vino tinto", 3.50, 1),
                LineaComanda(10, "Croquetas", 7.00, 1),
                LineaComanda(11, "Paella", 12.00, 2),
            ]
        elif mesa_id == "B01":  # Barra 1
            lineas = [
                LineaComanda(5, "Café", 1.30, 2),
                LineaComanda(13, "Tarta", 4.50, 1),
            ]
        else:
            lineas = []

        comanda = Comanda(
            id=None,
            mesa_id=mesa_id,
            fecha_apertura=datetime.now(),
            fecha_cierre=None,
            estado="abierta",
            lineas=lineas,
        )

        self._comandas_cache[mesa_id] = comanda

    # === MÉTODOS DE ACCESO A DATOS ===

    def get_mesas(self) -> List[Mesa]:
        """Retorna lista de todas las mesas"""
        return self._mesas_cache.copy()

    def get_mesa_by_id(self, mesa_id: str) -> Optional[Mesa]:
        """Retorna una mesa por su ID"""
        for mesa in self._mesas_cache:
            if mesa.id == mesa_id:
                return mesa
        return None

    def get_categorias(self) -> List[Dict]:
        """Retorna lista de categorías de productos"""
        return self._categorias_cache.copy()

    def get_productos_by_categoria(self, categoria_id: int) -> List[Producto]:
        """Retorna productos filtrados por categoría"""
        categoria_nombre = next(
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
        """Retorna todos los productos, opcionalmente filtrados por texto de búsqueda"""
        if not texto_busqueda:
            return self._productos_cache.copy()

        texto_busqueda = texto_busqueda.lower()
        return [p for p in self._productos_cache if texto_busqueda in p.nombre.lower()]

    def get_comanda_activa(self, mesa_id: str) -> Optional[Comanda]:
        """Retorna la comanda activa para una mesa, si existe. Si no está en caché, la recarga desde la base de datos."""
        comanda = self._comandas_cache.get(mesa_id)
        if comanda is not None:
            return comanda
        # Si no está en caché, intentar cargar solo la comanda de esa mesa desde la base de datos
        if not self.db_manager:
            return None
        try:
            rows = self.db_manager.query(
                """
                SELECT id, mesa_id, usuario_id, fecha_hora, estado, total
                FROM comandas
                WHERE mesa_id = ? AND estado IN ('abierta', 'en_proceso')
                ORDER BY fecha_hora DESC LIMIT 1
                """,
                (mesa_id,),
            )
            if not rows or len(rows) == 0:
                return None
            row = rows[0]
            comanda_id = row[0]
            # Cargar detalles de la comanda
            detalles = self.db_manager.query(
                """
                SELECT producto_id, cantidad, precio_unitario
                FROM comanda_detalles
                WHERE comanda_id = ?
                """,
                (comanda_id,),
            )
            lineas = []
            for detalle in detalles:
                producto = next(
                    (p for p in self._productos_cache if p.id == detalle[0]), None
                )
                if producto and hasattr(producto, "nombre"):
                    nombre_producto = producto.nombre
                else:
                    nombre_producto = f"Producto {detalle[0]}"
                linea = LineaComanda(
                    producto_id=detalle[0],
                    producto_nombre=nombre_producto,
                    precio_unidad=detalle[2],
                    cantidad=detalle[1],
                )
                lineas.append(linea)
            comanda = Comanda(
                id=row[0],
                mesa_id=str(row[1]),
                fecha_apertura=(
                    datetime.fromisoformat(row[3]) if row[3] else datetime.now()
                ),
                fecha_cierre=None,
                estado=row[4] or "abierta",
                lineas=lineas,
            )
            comanda.usuario_id = row[2] if len(row) > 2 else None
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
            comanda = self.crear_comanda(mesa_id)

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
        linea = LineaComanda(
            producto_id=producto.id,
            producto_nombre=producto.nombre,
            precio_unidad=producto.precio,
            cantidad=cantidad,
        )

        comanda.lineas.append(linea)
        return comanda

    def cerrar_comanda(self, mesa_id: str, estado: str = "pagada") -> Optional[Comanda]:
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
            if m.id == mesa_id:
                m.estado = "libre"
                break

        # Quitar de comandas activas
        self._comandas_cache.pop(mesa_id)

        # TODO: Persistir en BD

        return comanda

    def cambiar_estado_mesa(self, mesa_id: str, nuevo_estado: str) -> bool:
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
            if m.id == mesa_id:
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
        TRANSICIONES_VALIDAS = {
            "abierta": ["en_proceso", "cancelada"],
            "en_proceso": ["pagada", "cancelada"],
            "pagada": ["cerrada"],
            # "cerrada": []
        }
        # Buscar comanda en caché
        comanda = None
        for c in self._comandas_cache.values():
            if c.id == comanda_id:
                comanda = c
                break
        if not comanda:
            self.logger.error(f"Comanda {comanda_id} no encontrada")
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
                from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

                mesa_event_bus.comanda_actualizada.emit(comanda)
            except Exception:
                pass
            return True
        except Exception as e:
            self.logger.error(
                f"Error actualizando estado de comanda {comanda_id} en BD: {e}"
            )
            return False

    # === MÉTODOS ADICIONALES PARA EL MÓDULO TPV ===

    def get_todas_mesas(self) -> List[Mesa]:
        """Retorna todas las mesas disponibles"""
        return self._mesas_cache.copy()

    def get_mesa_por_id(self, mesa_id: str) -> Optional[Mesa]:
        """Retorna una mesa por su id"""
        for mesa in self._mesas_cache:
            if mesa.id == mesa_id:
                return mesa
        return None

    def get_categorias_productos(self) -> List[str]:
        """Retorna todas las categorías de productos"""
        return [cat["nombre"] for cat in self._categorias_cache]

    def get_todos_productos(self) -> List[Producto]:
        """Retorna todos los productos"""
        return self._productos_cache.copy()

    def get_productos_por_categoria(self, categoria: str) -> List[Producto]:
        """Retorna productos de una categoría específica"""
        return [p for p in self._productos_cache if p.categoria == categoria]

    def get_producto_por_id(self, producto_id: int) -> Optional[Producto]:
        """Retorna un producto por su ID"""
        for producto in self._productos_cache:
            if producto.id == producto_id:
                return producto
        return None

    def get_comandas_activas(self) -> List[Comanda]:
        """Retorna todas las comandas activas"""
        return list(self._comandas_cache.values())

    def get_comanda_por_id(self, comanda_id: int) -> Optional[Comanda]:
        """Retorna una comanda por su ID, primero en caché, si no la busca en la base de datos."""
        for comanda in self._comandas_cache.values():
            if comanda.id == comanda_id:
                return comanda
        # Si no está en caché, buscar en la base de datos
        if not self.db_manager:
            return None
        try:
            rows = self.db_manager.query(
                """
                SELECT id, mesa_id, usuario_id, fecha_hora, estado, total
                FROM comandas
                WHERE id = ?
                LIMIT 1
                """,
                (comanda_id,),
            )
            if not rows or len(rows) == 0:
                return None
            row = rows[0]
            detalles = self.db_manager.query(
                """
                SELECT producto_id, cantidad, precio_unitario
                FROM comanda_detalles
                WHERE comanda_id = ?
                """,
                (comanda_id,),
            )
            lineas = []
            for detalle in detalles:
                producto = next(
                    (p for p in self._productos_cache if p.id == detalle[0]), None
                )
                if producto and hasattr(producto, "nombre"):
                    nombre_producto = producto.nombre
                else:
                    nombre_producto = f"Producto {detalle[0]}"
                linea = LineaComanda(
                    producto_id=detalle[0],
                    producto_nombre=nombre_producto,
                    precio_unidad=detalle[2],
                    cantidad=detalle[1],
                )
                lineas.append(linea)
            comanda = Comanda(
                id=row[0],
                mesa_id=row[1],
                fecha_apertura=(
                    datetime.fromisoformat(row[3]) if row[3] else datetime.now()
                ),
                fecha_cierre=None,
                estado=row[4] or "abierta",
                lineas=lineas,
            )
            comanda.usuario_id = row[2] if len(row) > 2 else None
            # Guardar en caché para futuras búsquedas
            self._comandas_cache[row[1]] = comanda
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

        # Verificar si ya existe el producto en la comanda
        for linea in comanda.lineas:
            if linea.producto_id == producto_id:
                linea.cantidad += cantidad
                self.persistir_comanda(comanda)
                return True

        # Si no existe, añadir una nueva línea
        nueva_linea = LineaComanda(
            producto_id=producto_id,
            producto_nombre=producto_nombre,
            precio_unidad=precio,
            cantidad=cantidad,
        )

        comanda.lineas.append(nueva_linea)
        self.persistir_comanda(comanda)
        return True

    def eliminar_producto_de_comanda(self, comanda_id: int, producto_id: int) -> bool:
        """Elimina un producto de una comanda"""
        comanda = self.get_comanda_por_id(comanda_id)
        if not comanda:
            return False

        # Buscar el producto en las líneas
        nueva_lineas = []
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
        """
        Crea una nueva comanda para una mesa, registrando el usuario_id (usuario/camarero/cajero).
        """
        # Verificar que la mesa existe
        mesa = self.get_mesa_por_id(mesa_id)
        if not mesa:
            raise ValueError(f"No existe mesa con ID {mesa_id}")

        # Si ya hay una comanda activa, retornarla
        if mesa_id in self._comandas_cache:
            return self._comandas_cache[mesa_id]

        # Crear nueva comanda
        comanda = Comanda(
            id=None,
            mesa_id=mesa_id,
            fecha_apertura=datetime.now(),
            fecha_cierre=None,
            estado="abierta",
            lineas=[],
            usuario_id=usuario_id,
        )
        self._comandas_cache[mesa_id] = comanda

        # Persistir en base de datos si es posible
        if self.db_manager:
            try:
                comanda_id = self.db_manager.execute(
                    """
                    INSERT INTO comandas (mesa_id, usuario_id, fecha_hora, estado, total)
                    VALUES (?, ?, datetime('now'), ?, 0)
                    """,
                    (mesa_id, usuario_id, "abierta"),
                )
                comanda.id = comanda_id  # Asignar el ID generado a la comanda
            except Exception as e:
                self.logger.error(f"Error insertando comanda en BD: {e}")
                # TODO: Manejar rollback si es necesario

        return comanda

    def guardar_comanda(self, comanda_id: int) -> bool:
        """Guarda una comanda (simulado)"""
        comanda = self.get_comanda_por_id(comanda_id)
        if not comanda:
            return False  # En una implementación real, persistiríamos en la BD
        # Log eliminado por redundante
        return True

    def pagar_comanda(self, comanda_id: int, usuario_id: int = -1) -> bool:
        """Procesa el pago de una comanda, descuenta stock, registra movimientos, marca como pagada en BD y libera la mesa."""
        comanda = self.get_comanda_por_id(comanda_id)
        if not comanda:
            return False

        # Descontar stock y registrar movimientos
        if self.db_manager:
            for linea in comanda.lineas:
                try:
                    self.db_manager.descontar_stock_y_registrar(
                        producto_id=linea.producto_id,
                        cantidad=linea.cantidad,
                        usuario_id=usuario_id,
                        observaciones=f"Venta comanda {comanda_id}",
                    )
                except Exception as e:
                    self.logger.error(
                        f"Error descontando stock producto {linea.producto_id}: {e}"
                    )
                    return False

        # Marcar como pagada y persistir en BD
        comanda.estado = "pagada"
        comanda.fecha_cierre = datetime.now()
        if self.db_manager:
            try:
                self.db_manager.execute(
                    "UPDATE comandas SET estado = ?, fecha_cierre = ? WHERE id = ?",
                    (
                        "pagada",
                        comanda.fecha_cierre.strftime("%Y-%m-%d %H:%M:%S"),
                        comanda_id,
                    ),
                )
            except Exception as e:
                self.logger.error(
                    f"Error actualizando estado de comanda {comanda_id} en BD: {e}"
                )
                return False

        # Liberar la mesa asociada
        mesa = self.get_mesa_por_id(comanda.mesa_id)
        if mesa:
            mesa.estado = "libre"
            mesa.alias = None
            mesa.personas_temporal = None
            if self.db_manager:
                try:
                    self.db_manager.execute(
                        "UPDATE mesas SET estado = ?, alias = NULL WHERE id = ?",
                        ("libre", mesa.id),
                    )
                except Exception as e:
                    self.logger.error(f"Error liberando mesa {mesa.id} en BD: {e}")
            # Emitir señal de mesa actualizada
            try:
                from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

                mesa_event_bus.mesa_actualizada.emit(mesa)
            except Exception:
                pass

        # Emitir señal global de comanda actualizada
        try:
            from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

            mesa_event_bus.comanda_actualizada.emit(comanda)
        except Exception:
            pass

        # Log eliminado por redundante
        return True

    def liberar_mesa(self, mesa_id: str) -> bool:
        """Libera una mesa y elimina su comanda"""
        # Verificar que existe la mesa
        mesa = self.get_mesa_por_id(mesa_id)
        if not mesa:
            return False

        # Cambiar estado, eliminar comanda y resetear nombre temporal
        for m in self._mesas_cache:
            if m.id == mesa_id:
                m.estado = "libre"
                m.alias = None  # Resetear alias al liberar mesa
                m.personas_temporal = None  # Resetear personas temporal al liberar mesa
                break

        if mesa_id in self._comandas_cache:
            del self._comandas_cache[mesa_id]

        # Log eliminado por redundante
        return True

    def generar_siguiente_numero_mesa(self, zona: str) -> str:
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
            numeros_existentes = []
            zona_inicial = zona[0].upper() if zona else "P"

            for mesa in mesas_zona:
                # Intentar extraer el número del identificador de la mesa
                numero_str = mesa.numero

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
            siguiente_numero = 1
            if numeros_existentes:
                siguiente_numero = max(numeros_existentes) + 1

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
        """
        Crea una nueva mesa con numeración automática contextualizada por zona.

        Args:
            capacidad: Número de personas que puede acomodar la mesa
            zona: Zona donde se ubicará la mesa

        Returns:
            Mesa: Nueva mesa creada o None si hay error
        """
        try:
            if not self.db_manager:
                logger.warning("No hay conexión a base de datos para crear mesa")
                return None

            # Generar automáticamente el siguiente número para la zona
            numero_mesa = self.generar_siguiente_numero_mesa(zona)

            # Verificar que no existe una mesa con ese número (por seguridad)
            for mesa_existente in self._mesas_cache:
                if mesa_existente.numero == numero_mesa:
                    logger.warning(f"Ya existe una mesa con el número {numero_mesa}")
                    # Intentar con el siguiente número
                    zona_inicial = zona[0].upper() if zona else "P"
                    siguiente = int(numero_mesa[1:]) + 1
                    numero_mesa = f"{zona_inicial}{siguiente:02d}"

            # Crear nueva mesa en la base de datos
            mesa_id = self.db_manager.execute(
                """
                INSERT INTO mesas (numero, zona, estado, capacidad)
                VALUES (?, ?, ?, ?)
            """,
                (numero_mesa, zona, "libre", capacidad),
            )

            # Crear objeto Mesa y agregarlo al cache
            nueva_mesa = Mesa(
                id=mesa_id,
                numero=numero_mesa,
                zona=zona,
                estado="libre",
                capacidad=capacidad,
            )

            self._mesas_cache.append(nueva_mesa)
            logger.info(
                f"Mesa {numero_mesa} creada correctamente en zona {zona} con ID {mesa_id}"
            )

            # Emitir evento global de mesas actualizadas
            from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

            mesa_event_bus.mesas_actualizadas.emit(self._mesas_cache.copy())

            return nueva_mesa

        except Exception as e:
            logger.error(f"Error creando mesa: {e}")
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
                    logger.warning(f"Ya existe una mesa con el número {numero}")
                    return None

            # Crear nueva mesa en la base de datos
            mesa_id = self.db_manager.execute(
                """
                INSERT INTO mesas (numero, zona, estado, capacidad)
                VALUES (?, ?, ?, ?)
            """,
                (str(numero), zona, "libre", capacidad),
            )

            # Crear objeto Mesa y agregarlo al cache
            nueva_mesa = Mesa(
                id=mesa_id,
                numero=str(numero),
                zona=zona,
                estado="libre",
                capacidad=capacidad,
            )

            self._mesas_cache.append(nueva_mesa)
            # Log eliminado por redundante

            return nueva_mesa

        except Exception as e:
            logger.error(f"Error creando mesa: {e}")
            return None

    def eliminar_mesa(self, mesa_id: int) -> bool:
        """Elimina una mesa de la base de datos"""
        try:
            if not self.db_manager:
                logger.warning("No hay conexión a base de datos para eliminar mesa")
                return False

            # Verificar que la mesa existe
            mesa_existente = None
            for mesa in self._mesas_cache:
                if mesa.id == mesa_id:
                    mesa_existente = mesa
                    break

            if not mesa_existente:
                logger.warning(f"No se encontró la mesa con ID {mesa_id}")
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
            logger.error(f"Error eliminando mesa: {e}")
            return False

    def cambiar_personas_temporal_mesa(self, mesa_id: str, nuevo_numero: int) -> bool:
        """Cambia el número de personas temporal de una mesa (no persistente)"""
        mesa = self.get_mesa_por_id(mesa_id)
        if mesa:
            mesa.personas_temporal = nuevo_numero
            return True
        return False

    def resetear_personas_mesa(self, mesa_id: str) -> bool:
        """Resetea el número de personas temporal de una mesa"""
        mesa = self.get_mesa_por_id(mesa_id)
        if mesa:
            mesa.personas_temporal = None
            return True
        return False

    def cambiar_alias_mesa(self, mesa_id: str, nuevo_alias: Optional[str]) -> bool:
        """Cambia el alias temporal de una mesa (solo en memoria)"""
        try:
            # Validar alias
            if nuevo_alias is not None:
                nuevo_alias = nuevo_alias.strip()
            if not nuevo_alias:
                nuevo_alias = None
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
            self.logger.error(f"Error cambiando alias de mesa {mesa_id}: {e}")
            return False

    def resetear_alias_mesa(self, mesa_id: str) -> bool:
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
            self.logger.error(f"Error reseteando alias de mesa {mesa_id}: {e}")
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
        """Crea una reserva persistente para una mesa (modelo unificado)"""
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
            reserva_id = self.db_manager.execute(
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
            return Reserva(
                id=reserva_id,
                mesa_id=mesa_id,
                cliente_nombre=cliente,
                cliente_telefono=telefono,
                fecha_reserva=fecha_hora.date(),
                hora_reserva=fecha_hora.strftime("%H:%M"),
                numero_personas=personas,
                estado="confirmada",
                notas=notas,
            )
        except Exception as e:
            self.logger.error(f"Error creando reserva: {e}")
            return None

    def get_reservas_mesa(self, mesa_id: str, fecha: Optional[date] = None) -> list:
        """Obtiene reservas activas de una mesa, opcionalmente filtradas por fecha (modelo unificado)"""
        if not self.db_manager:
            return []
        try:
            query = "SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas FROM reservas WHERE mesa_id = ? AND estado = 'activa'"
            params: list[Any] = [mesa_id]
            if fecha:
                query += " AND date(fecha_hora) = ?"
                params.append(fecha.isoformat())
            rows = self.db_manager.query(query, tuple(params))
            reservas = [
                Reserva(
                    id=row[0],
                    mesa_id=row[1],
                    cliente_nombre=row[2],
                    cliente_telefono=row[7] or "",
                    fecha_reserva=datetime.fromisoformat(row[3]).date(),
                    hora_reserva=datetime.fromisoformat(row[3]).strftime("%H:%M"),
                    numero_personas=row[8] if row[8] is not None else 1,
                    estado=row[5],
                    notas=row[6] or "",
                )
                for row in rows
            ]
            return reservas
        except Exception as e:
            self.logger.error(f"Error obteniendo reservas: {e}")
            return []

    def cancelar_reserva(self, reserva_id: int) -> bool:
        """Cancela una reserva por su ID"""
        if not self.db_manager:
            return False
        try:
            self.db_manager.execute(
                "UPDATE reservas SET estado = 'cancelada' WHERE id = ?", (reserva_id,)
            )
            return True
        except Exception as e:
            self.logger.error(f"Error cancelando reserva: {e}")
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
            rows = self.db_manager.query(
                "SELECT hora, duracion_min FROM reservas WHERE mesa_id = ? AND fecha = ? AND estado = 'activa'",
                (mesa_id, fecha.isoformat()),
            )
            for row in rows:
                hora_existente = datetime.combine(
                    fecha, datetime.strptime(row[0], "%H:%M:%S").time()
                )
                duracion_existente = row[1] if row[1] is not None else 120
                hora_fin_existente = hora_existente + timedelta(
                    minutes=duracion_existente
                )
                # Solapamiento: inicio < fin_existente y fin > inicio_existente
                if (hora_inicio_nueva < hora_fin_existente) and (
                    hora_fin_nueva > hora_existente
                ):
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error comprobando solapamiento de reserva: {e}")
            return False


# TODO: Revisar y migrar todos los usos de Reserva en el sistema para usar este modelo unificado.
# TODO: Documentar en README de área y dejar registro de excepción si algún flujo requiere compatibilidad temporal.
