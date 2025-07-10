# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
import logging
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, date
from .base_service import BaseService
            from datetime import datetime

"""
InventarioService - Versión Corregida con Soporte Completo de Categorías para Proveedores
=======================================================================================
Versión: v0.0.12
Fecha: 2025-06-20
Cambios: Restauración completa + soporte de categorías para proveedores
"""



_ = logging.getLogger(__name__)

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
    fecha_ultima_entrada: Optional[datetime] = None

    def necesita_reposicion(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Indica si el producto necesita reposición"""
        return self.stock_actual <= self.stock_minimo

    @property
    def valor_total(self) -> float:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valor total del stock (precio * cantidad)"""
        return self.precio * self.stock_actual

class InventarioService(BaseService):
    """Servicio para la gestión del inventario con datos reales"""

    def __init__(self, db_manager=None):
        """TODO: Add docstring"""
        super().__init__(db_manager)
        self.logger.info("InventarioService inicializado con base de datos real" if db_manager else "InventarioService inicializado sin base de datos")

    def get_service_name(self) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna el nombre de este servicio"""
        return "InventarioService"

    def _convert_db_row_to_producto(self, row) -> Producto:
        """Convierte una fila de la base de datos a un objeto Producto"""
        try:
            # Convertir sqlite3.Row a dict si es necesario
            if hasattr(row, 'keys'):
                _ = dict(row)
            else:
                _ = row

            return Producto(
                _ = row_dict.get('id'),
                nombre=row_dict.get('nombre', ''),
                _ = row_dict.get('categoria', 'General'),
                precio=float(row_dict.get('precio', 0.0)),
                _ = int(row_dict.get('stock', 0)),
                stock_minimo=int(row_dict.get('stock_minimo', 5)),
                _ = row_dict.get('proveedor_id'),
                proveedor_nombre=row_dict.get('proveedor_nombre'),
                _ = None
            )
        except Exception as e:
            logger.error("Error convirtiendo fila a producto: %s", e)
            # Retornar producto básico en caso de error
            return Producto(
                _ = None,
                nombre="Error",
                _ = "General",
                precio=0.0,
                _ = 0,
                stock_minimo=5
            )

    def get_productos(self, texto_busqueda: str = "", categoria: str = "") -> List[Producto]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna productos filtrados por texto y/o categoría"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos, retornando lista vacía")
            return []

        # Validar entrada
        if texto_busqueda and len(texto_busqueda) > 100:
            logger.warning("Texto de búsqueda demasiado largo, truncando")
            _ = texto_busqueda[:100]

        if categoria and len(categoria) > 50:
            logger.warning("Nombre de categoría demasiado largo, truncando")
            _ = categoria[:50]

        try:
            # Construir consulta SQL con filtros
            query = "SELECT * FROM productos WHERE 1=1"
            _ = []

            if texto_busqueda and texto_busqueda.strip():
                query += " AND nombre LIKE ?"
                params.append(f"%{texto_busqueda.strip()}%")

            if categoria and categoria.strip():
                query += " AND categoria = ?"
                params.append(categoria.strip())

            query += " ORDER BY nombre"

            # Ejecutar consulta
            rows = self.db_manager.query(query, params)

            # Validar que rows no sea None
            if rows is None:
                logger.warning("Query retornó None, usando lista vacía")
                _ = []

            # Convertir filas a objetos Producto
            _ = []
            for row in rows:
                try:
                    producto = self._convert_db_row_to_producto(row)
                    if producto.id is not None:  # Solo agregar productos válidos
                        productos.append(producto)
                except Exception as e:
                    logger.error("Error procesando producto: %s", e)
                    continue

            return productos

        except Exception as e:
            logger.error("Error obteniendo productos: %s", e)
            return []

    def crear_producto(self, nombre: str, categoria: str, precio: float,
        """TODO: Add docstring"""
                      stock_inicial: int = 0, stock_minimo: int = 5, **kwargs) -> Optional[Producto]:
        """Crear un nuevo producto en el inventario"""
        if not self.require_database("crear producto"):
            return None

        assert self.db_manager is not None  # Type checker assertion

        try:
            # Validaciones mejoradas
            if not nombre or not nombre.strip():
                logger.error("El nombre del producto es requerido")
                return None

            # Validar longitud del nombre
            if len(nombre.strip()) > 200:
                logger.error("El nombre del producto es demasiado largo (máximo 200 caracteres)")
                return None

            # Validar categoría
            if not categoria or not categoria.strip():
                _ = "General"

            # Validar precio
            if precio < 0:
                logger.error("El precio no puede ser negativo")
                return None

            # Validar stock
            if stock_inicial < 0:
                logger.error("El stock inicial no puede ser negativo")
                return None

            if stock_minimo < 0:
                logger.error("El stock mínimo no puede ser negativo")
                return None

            # Verificar si el producto ya existe
            productos_existentes = self.get_productos(texto_busqueda=nombre.strip())
            if any(p.nombre.lower() == nombre.strip().lower() for p in productos_existentes):
                logger.warning("Ya existe un producto con nombre '%s'", nombre.strip())
                return None

            # Insertar nuevo producto
            _ = """
                INSERT INTO productos (nombre, categoria, precio, stock, stock_minimo)
                VALUES (?, ?, ?, ?, ?)
            """
            
            _ = self.db_manager.execute(query, (
                nombre.strip(),
                categoria.strip(),
                precio,
                stock_inicial,
                stock_minimo
            ))

            if result:
                logger.info("Producto '%s' creado exitosamente", nombre)
                # Retornar el producto creado
                productos_creados = self.get_productos(texto_busqueda=nombre.strip())
                return productos_creados[0] if productos_creados else None
            else:
                logger.error("Error insertando producto '%s' en la base de datos", nombre)
                return None

        except Exception as e:
            logger.error("Error creando producto: %s", e)
            return None

    def actualizar_producto(self, producto_id: int, **campos) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar un producto existente"""
        if not self.require_database("actualizar producto"):
            return False

        assert self.db_manager is not None

        try:
            # Verificar que el producto existe
            producto_actual = self.buscar_producto_por_id(producto_id)
            if not producto_actual:
                logger.error("No se encontró producto con ID %s", producto_id)
                return False

            # Preparar campos para actualizar
            _ = {}
            if 'nombre' in campos and campos['nombre'] and campos['nombre'].strip():
                campos_validos['nombre'] = campos['nombre'].strip()
            
            if 'categoria' in campos and campos['categoria'] and campos['categoria'].strip():
                campos_validos['categoria'] = campos['categoria'].strip()
            
            if 'precio' in campos and campos['precio'] is not None and campos['precio'] >= 0:
                campos_validos['precio'] = float(campos['precio'])
            
            if 'stock' in campos and campos['stock'] is not None and campos['stock'] >= 0:
                campos_validos['stock'] = int(campos['stock'])
            
            if 'stock_minimo' in campos and campos['stock_minimo'] is not None and campos['stock_minimo'] >= 0:
                campos_validos['stock_minimo'] = int(campos['stock_minimo'])

            if not campos_validos:
                logger.warning("No hay campos válidos para actualizar")
                return False

            # Construir query de actualización
            _ = []
            valores = []
            for campo, valor in campos_validos.items():
                set_clauses.append(f"{campo} = ?")
                valores.append(valor)

            query = f"UPDATE productos SET {', '.join(set_clauses)} WHERE id = ?"
            valores.append(producto_id)

            result = self.db_manager.execute(query, valores)

            if result:
                logger.info("Producto ID %s actualizado exitosamente", producto_id)
                return True
            else:
                logger.error("Error actualizando producto ID %s", producto_id)
                return False

        except Exception as e:
            logger.error("Error actualizando producto: %s", e)
            return False

    def eliminar_producto(self, producto_id: int) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Eliminar un producto del inventario"""
        if not self.require_database("eliminar producto"):
            return False

        assert self.db_manager is not None

        try:
            # Verificar que el producto existe
            producto = self.buscar_producto_por_id(producto_id)
            if not producto:
                logger.error("No se encontró producto con ID %s", producto_id)
                return False

            # Eliminar producto
            query = "DELETE FROM productos WHERE id = ?"
            result = self.db_manager.execute(query, (producto_id,))

            if result:
                logger.info("Producto '{producto.nombre}' (ID %s) eliminado exitosamente", producto_id)
                return True
            else:
                logger.error("Error eliminando producto ID %s", producto_id)
                return False

        except Exception as e:
            logger.error("Error eliminando producto: %s", e)
            return False

    def actualizar_stock(self, producto_id: int, nuevo_stock: int) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar el stock de un producto"""
        if not self.require_database("actualizar stock"):
            return False

        assert self.db_manager is not None

        try:
            if nuevo_stock < 0:
                logger.error("El stock no puede ser negativo")
                return False

            # Verificar que el producto existe
            producto = self.buscar_producto_por_id(producto_id)
            if not producto:
                logger.error("No se encontró producto con ID %s", producto_id)
                return False

            # Actualizar stock
            query = "UPDATE productos SET stock = ? WHERE id = ?"
            result = self.db_manager.execute(query, (nuevo_stock, producto_id))

            if result:
                logger.info("Stock del producto '{producto.nombre}' actualizado a %s", nuevo_stock)
                return True
            else:
                logger.error("Error actualizando stock del producto ID %s", producto_id)
                return False

        except Exception as e:
            logger.error("Error actualizando stock: %s", e)
            return False

    def get_categorias(self) -> List[str]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtener lista de categorías únicas de productos"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos, retornando categorías por defecto")
            return ['Bebidas', 'Comida', 'Limpieza', 'Papelería', 'General']

        try:
            query = "SELECT DISTINCT categoria FROM productos WHERE categoria IS NOT NULL AND categoria != '' ORDER BY categoria"
            rows = self.db_manager.query(query)

            if not rows:
                logger.info("No se encontraron categorías, retornando categorías por defecto")
                return ['Bebidas', 'Comida', 'Limpieza', 'Papelería', 'General']

            _ = []
            for row in rows:
                if hasattr(row, 'keys'):
                    _ = row['categoria']
                else:
                    _ = row[0]
                
                if categoria and categoria.strip():
                    categorias.append(categoria.strip())

            # Asegurar que siempre haya categorías por defecto
            categorias_default = ['Bebidas', 'Comida', 'Limpieza', 'Papelería', 'General']
            for cat in categorias_default:
                if cat not in categorias:
                    categorias.append(cat)

            return sorted(categorias)

        except Exception as e:
            logger.error("Error obteniendo categorías: %s", e)
            return ['Bebidas', 'Comida', 'Limpieza', 'Papelería', 'General']

    def get_estadisticas_inventario(self) -> Dict[str, Any]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtener estadísticas generales del inventario"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos, retornando estadísticas vacías")
            return {
                'total_productos': 0,
                'productos_stock_bajo': 0,
                'productos_sin_stock': 0,
                'valor_total_inventario': 0.0,
                'categorias_activas': 0,
                'producto_mas_caro': '',
                'valor_promedio_producto': 0.0
            }

        try:
            # Obtener todos los productos
            _ = self.get_productos()
            
            if not productos:
                return {
                    'total_productos': 0,
                    'productos_stock_bajo': 0,
                    'productos_sin_stock': 0,
                    'valor_total_inventario': 0.0,
                    'categorias_activas': 0,
                    'producto_mas_caro': '',
                    'valor_promedio_producto': 0.0
                }

            # Calcular estadísticas
            _ = len(productos)
            productos_stock_bajo = len([p for p in productos if p.necesita_reposicion()])
            productos_sin_stock = len([p for p in productos if p.stock_actual == 0])
            _ = sum(p.valor_total for p in productos)
            categorias_activas = len(set(p.categoria for p in productos))
            
            producto_mas_caro = max(productos, key=lambda p: p.precio, default=None)
            _ = producto_mas_caro.nombre if producto_mas_caro else ''
            
            valor_promedio = valor_total / total_productos if total_productos > 0 else 0.0

            return {
                'total_productos': total_productos,
                'productos_stock_bajo': productos_stock_bajo,
                'productos_sin_stock': productos_sin_stock,
                'valor_total_inventario': valor_total,
                'categorias_activas': categorias_activas,
                'producto_mas_caro': producto_mas_caro_nombre,
                'valor_promedio_producto': valor_promedio
            }

        except Exception as e:
            logger.error("Error obteniendo estadísticas: %s", e)
            return {
                'total_productos': 0,
                'productos_stock_bajo': 0,
                'productos_sin_stock': 0,
                'valor_total_inventario': 0.0,
                'categorias_activas': 0,
                'producto_mas_caro': '',
                'valor_promedio_producto': 0.0
            }

    # ========================================
    # MÉTODOS PARA GESTIÓN DE PROVEEDORES CON SOPORTE DE CATEGORÍAS
    # ========================================

    def get_proveedores(self) -> List[Dict[str, Any]]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtener lista de proveedores desde la tabla proveedores con soporte de categorías"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos, retornando lista vacía")
            return []

        try:
            # Obtener proveedores de la tabla proveedores real
            _ = """
                SELECT 
                    id, 
                    nombre,
                    contacto,
                    telefono,
                    email,
                    direccion,
                    categoria,
                    fecha_registro,
                    activo,
                    notas
                FROM proveedores 
                WHERE activo = 1
                ORDER BY categoria, nombre
            """
            rows = self.db_manager.query(query)

            if not rows:
                logger.info("No se encontraron proveedores en la base de datos")
                return []

            _ = []
            for row in rows:
                try:
                    if hasattr(row, 'keys'):
                        _ = dict(row)
                    else:
                        # Convertir tupla/lista a diccionario
                        _ = {
                            'id': row[0] if len(row) > 0 else None,
                            'nombre': row[1] if len(row) > 1 else '',
                            'contacto': row[2] if len(row) > 2 else '',
                            'telefono': row[3] if len(row) > 3 else '',
                            'email': row[4] if len(row) > 4 else '',
                            'direccion': row[5] if len(row) > 5 else '',
                            'categoria': row[6] if len(row) > 6 else 'General',
                            'fecha_registro': row[7] if len(row) > 7 else '',
                            'activo': row[8] if len(row) > 8 else True,
                            'notas': row[9] if len(row) > 9 else ''
                        }

                    # Validar datos básicos
                    _ = proveedor_dict.get('id')
                    nombre = proveedor_dict.get('nombre', '')
                    _ = nombre.strip() if nombre else ''
                    
                    if proveedor_id and nombre:
                        _ = proveedor_dict.get('contacto', '') or ''
                        telefono = proveedor_dict.get('telefono', '') or ''
                        _ = proveedor_dict.get('email', '') or ''
                        direccion = proveedor_dict.get('direccion', '') or ''
                        _ = proveedor_dict.get('categoria', 'General') or 'General'
                        notas = proveedor_dict.get('notas', '') or ''
                        
                        proveedores.append({
                            'id': proveedor_id,
                            'nombre': nombre,
                            'contacto': contacto.strip() if contacto else '',
                            'telefono': telefono.strip() if telefono else '',
                            'email': email.strip() if email else '',
                            'direccion': direccion.strip() if direccion else '',
                            'categoria': categoria.strip() if categoria else 'General',
                            'fecha_creacion': proveedor_dict.get('fecha_registro', ''),
                            'activo': bool(proveedor_dict.get('activo', True)),
                            'notas': notas.strip() if notas else ''
                        })
                
                except Exception as e:
                    logger.error("Error procesando proveedor: %s", e)
                    continue

            logger.info("Obtenidos %s proveedores de la base de datos", len(proveedores))
            return proveedores

        except Exception as e:
            logger.error("Error obteniendo proveedores: %s", e)
            # Retornar proveedores por defecto en caso de error
            return [
                {"id": 1, "nombre": "Proveedor General", "contacto": "info@proveedor.com", "telefono": "123-456-789", "categoria": "General"},
                {"id": 2, "nombre": "Distribuciones SA", "contacto": "ventas@distribuciones.com", "telefono": "987-654-321", "categoria": "Bebidas"},
                {"id": 3, "nombre": "Suministros Locales", "contacto": "pedidos@suministros.com", "telefono": "555-123-456", "categoria": "Comida"}
            ]

    def crear_proveedor(self, nombre: str, contacto: str = "", telefono: str = "", 
        """TODO: Add docstring"""
                       email: str = "", direccion: str = "", categoria: str = "General") -> bool:
        """Crear un nuevo proveedor en la tabla proveedores con soporte de categoría"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos")
            return False
            
        if not nombre or not nombre.strip():
            logger.error("El nombre del proveedor no puede estar vacío")
            return False
            
        try:
            
            # Verificar si el proveedor ya existe
            existing_query = "SELECT COUNT(*) FROM proveedores WHERE LOWER(nombre) = LOWER(?)"
            _ = self.db_manager.query(existing_query, (nombre.strip(),))
            
            if existing_count and existing_count[0][0] > 0:
                logger.warning("El proveedor '%s' ya existe", nombre)
                return False
            
            # Validar y limpiar categoría
            if not categoria or not categoria.strip():
                _ = "General"
            
            # Insertar nuevo proveedor en la tabla proveedores
            _ = """
                INSERT INTO proveedores (nombre, contacto, telefono, email, direccion, categoria, fecha_registro, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            _ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            success = self.db_manager.execute(
                insert_query, 
                (nombre.strip(), contacto.strip(), telefono.strip(), 
                 email.strip(), direccion.strip(), categoria.strip(), 
                 fecha_registro, True)
            )
            
            if success:
                logger.info("Proveedor '{nombre}' creado exitosamente con categoría '%s'", categoria)
                return True
            else:
                logger.error("Error al insertar proveedor '%s' en la base de datos", nombre)
                return False
            
        except Exception as e:
            logger.error("Error creando proveedor: %s", e)
            return False

    def actualizar_proveedor(self, proveedor_id: int, nombre: str, contacto: str = "", 
        """TODO: Add docstring"""
                           telefono: str = "", email: str = "", direccion: str = "", 
                           categoria: str = "General") -> bool:
        """Actualizar un proveedor existente en la tabla proveedores con soporte de categoría"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos")
            return False
            
        if not nombre or not nombre.strip():
            logger.error("El nombre del proveedor no puede estar vacío")
            return False
            
        try:
            # Validar y limpiar categoría
            if not categoria or not categoria.strip():
                _ = "General"
            
            # Actualizar proveedor en la tabla proveedores
            _ = """
                UPDATE proveedores 
                SET nombre = ?, contacto = ?, telefono = ?, email = ?, direccion = ?, categoria = ?
                WHERE id = ?
            """
            
            # Usar conexión directa para verificar rowcount
            with self.db_manager._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(update_query, (
                    nombre.strip(), contacto.strip(), telefono.strip(), 
                    email.strip(), direccion.strip(), categoria.strip(), 
                    proveedor_id
                ))
                _ = cursor.rowcount
                conn.commit()
            
            if rows_affected > 0:
                logger.info("Proveedor ID {proveedor_id} actualizado exitosamente con categoría '{categoria}' (%s filas afectadas)", rows_affected)
                return True
            else:
                logger.warning("No se encontró proveedor con ID %s", proveedor_id)
                return False
            
        except Exception as e:
            logger.error("Error actualizando proveedor: %s", e)
            return False

    def eliminar_proveedor(self, proveedor_id: int) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Eliminar un proveedor (marcar como inactivo)"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos")
            return False
            
        try:
            # Marcar como inactivo en lugar de eliminar físicamente
            update_query = "UPDATE proveedores SET activo = 0 WHERE id = ?"
            
            with self.db_manager._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(update_query, (proveedor_id,))
                _ = cursor.rowcount
                conn.commit()
            
            if rows_affected > 0:
                logger.info("Proveedor ID %s marcado como inactivo exitosamente", proveedor_id)
                return True
            else:
                logger.warning("No se encontró proveedor con ID %s", proveedor_id)
                return False
            
        except Exception as e:
            logger.error("Error eliminando proveedor: %s", e)
            return False

    def get_categorias_proveedores(self) -> List[str]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtener lista de categorías únicas de proveedores"""
        if not self.db_manager:
            logger.warning("Sin conexión a base de datos, retornando categorías por defecto")
            return ['General', 'Bebidas', 'Comida', 'Limpieza', 'Papelería', 'Servicios']

        try:
            query = "SELECT DISTINCT categoria FROM proveedores WHERE categoria IS NOT NULL AND categoria != '' AND activo = 1 ORDER BY categoria"
            rows = self.db_manager.query(query)

            if not rows:
                logger.info("No se encontraron categorías de proveedores, retornando categorías por defecto")
                return ['General', 'Bebidas', 'Comida', 'Limpieza', 'Papelería', 'Servicios']

            _ = []
            for row in rows:
                if hasattr(row, 'keys'):
                    _ = row['categoria']
                else:
                    _ = row[0]
                
                if categoria and categoria.strip():
                    categorias.append(categoria.strip())

            # Asegurar que siempre haya categorías por defecto
            categorias_default = ['General', 'Bebidas', 'Comida', 'Limpieza', 'Papelería', 'Servicios']
            for cat in categorias_default:
                if cat not in categorias:
                    categorias.append(cat)

            return sorted(categorias)

        except Exception as e:
            logger.error("Error obteniendo categorías de proveedores: %s", e)
            return ['General', 'Bebidas', 'Comida', 'Limpieza', 'Papelería', 'Servicios']

    # ========================================
    # MÉTODOS ADICIONALES ÚTILES
    # ========================================

    def buscar_producto_por_id(self, producto_id: int) -> Optional[Producto]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Buscar un producto específico por ID"""
        if not self.db_manager:
            return None

        try:
            productos = self.get_productos()
            return next((p for p in productos if p.id == producto_id), None)
        except Exception as e:
            logger.error("Error buscando producto por ID {producto_id}: %s", e)
            return None

    def get_productos_stock_bajo(self) -> List[Producto]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtener productos que necesitan reposición"""
        try:
            productos = self.get_productos()
            return [p for p in productos if p.necesita_reposicion()]
        except Exception as e:
            logger.error("Error obteniendo productos con stock bajo: %s", e)
            return []

    def get_productos_sin_stock(self) -> List[Producto]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtener productos sin stock"""
        try:
            productos = self.get_productos()
            return [p for p in productos if p.stock_actual == 0]
        except Exception as e:
            logger.error("Error obteniendo productos sin stock: %s", e)
            return []

    # ========================================
    # MÉTODOS ALIAS PARA COMPATIBILIDAD
    # ========================================
    
    def get_products(self, *args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para get_productos"""
        return self.get_productos(*args, **kwargs)

    def create_product(self, *args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para crear_producto"""
        return self.crear_producto(*args, **kwargs)

    def update_product(self, *args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para actualizar_producto"""
        return self.actualizar_producto(*args, **kwargs)

    def delete_product(self, *args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para eliminar_producto"""
        return self.eliminar_producto(*args, **kwargs)

    def update_stock_alias(self, *args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para actualizar_stock"""
        return self.actualizar_stock(*args, **kwargs)

    def get_categories(self, *args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para get_categorias"""
        return self.get_categorias(*args, **kwargs)

    def get_stats(self, *args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para get_estadisticas_inventario"""
        return self.get_estadisticas_inventario(*args, **kwargs)

    def obtener_proveedores(self, *args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para get_proveedores - compatibilidad con versiones anteriores"""
        return self.get_proveedores(*args, **kwargs)

    def editar_proveedor(self, proveedor_id: int, nombre: str, contacto: str = "", telefono: str = "", **kwargs) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para actualizar_proveedor - compatibilidad con versiones anteriores"""
        return self.actualizar_proveedor(proveedor_id, nombre, contacto, telefono, **kwargs)

    def agregar_producto(self, *args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para crear_producto - compatibilidad con versiones anteriores"""
        return self.crear_producto(*args, **kwargs)
