"""
mesas_area_main.py
Clase principal MesasArea (coordinador) y punto de entrada del área modularizada
"""

import logging
from typing import List, Optional, Dict
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from ...widgets.mesa_widget_simple import MesaWidget
from services.tpv_service import Mesa, TPVService

# Lazy imports para reducir acoplamiento
from .mesas_area_header import FiltersSectionUltraPremium, create_header
from .mesas_area_grid import create_scroll_area, populate_grid, add_mesa_grid_callbacks_to_instance
from .mesas_area_stats import update_stats_from_mesas
from .mesas_area_utils import restaurar_datos_temporales, guardar_dato_temporal

_ = logging.getLogger(__name__)


class MesasArea(QFrame):
    # --- Lógica de selección múltiple y acciones por lotes ---
    def enable_batch_mode(self, enabled: bool):
        """TODO: Add docstring"""
        # TODO: Add input validation
        self.batch_mode = enabled
        for w in self.mesa_widgets:
            if hasattr(w, "set_batch_mode"):
                w.set_batch_mode(enabled)
        self.selected_mesas = set()
        self.update_batch_action_btn()

    def toggle_mesa_selection(self, mesa_numero):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Selecciona/deselecciona una mesa usando su identificador string 'numero'"""
        _ = str(mesa_numero)
        if not hasattr(self, "selected_mesas"):
            self.selected_mesas = set()
        if mesa_numero in self.selected_mesas:
            self.selected_mesas.remove(mesa_numero)
        else:
            self.selected_mesas.add(mesa_numero)
        self.update_batch_action_btn()

    def update_batch_action_btn(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        # Busca el botón de acción por lotes en el header y lo habilita/deshabilita
        # Solución: buscar el widget en el layout del header
        if hasattr(self, "header"):
            # Buscar en los hijos del header un QPushButton con texto 'Acción por lotes'
            from PyQt6.QtWidgets import QPushButton

            def find_batch_btn(widget):
                """TODO: Add docstring"""
                # TODO: Add input validation
                for child in widget.findChildren(QPushButton):
                    if child.text() == "Acción por lotes":
                        return child
                return None

            batch_btn = find_batch_btn(self.header)
            if batch_btn:
                batch_btn.setEnabled(bool(self.selected_mesas))

    def do_batch_action(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        # Ejemplo: eliminar todas las mesas seleccionadas (solo UI, no base de datos)
        if not hasattr(self, "selected_mesas") or not self.selected_mesas:
            return
        self.filtered_mesas = [
            m for m in self.filtered_mesas if m.id not in self.selected_mesas
        ]
        self.mesas = [m for m in self.mesas if m.id not in self.selected_mesas]
        self.selected_mesas = set()
        self.refresh_mesas()  # Centraliza el refresco
        self.update_batch_action_btn()

    def toggle_view_mode(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alterna entre vista grid y lista"""
        self.view_mode = "list" if self.view_mode == "grid" else "grid"
        # TODO: Implementar renderizado de vista lista si es necesario
        self.refresh_mesas()

    """Área de visualización y gestión de mesas (modularizado)"""
    _ = pyqtSignal()
    nueva_mesa_con_zona_requested = pyqtSignal(int, int, str)
    _ = pyqtSignal(str)  # Ahora emite el 'numero' de la mesa
    eliminar_mesas_requested = pyqtSignal(list)  # Lista de 'numero' (str)

    def __init__(
        self, tpv_service: Optional[TPVService] = None, db_manager=None, parent=None
    ):
        super().__init__(parent)
        if db_manager is None:
            raise ValueError(
                "db_manager es obligatorio y debe ser inyectado explícitamente en MesasArea"
            )
        self.db_manager = db_manager
        self.tpv_service = (
            tpv_service
            if tpv_service is not None
            else TPVService(db_manager=db_manager)
        )
        self.mesas: List[Mesa] = []
        self.filtered_mesas: List[Mesa] = []
        self.mesa_widgets: List[MesaWidget] = []
        self._datos_temporales = {}
        self.current_zone_filter = "Todas"
        self.current_status_filter = "Todos"
        self.view_mode = "grid"
        self._chips_refs = []  # Referencias a chips de filtro rápido
        self.mesas_layout = None  # Inicializar para evitar errores
        # Forzar expansión horizontal
        from PyQt6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setup_ui()
        add_mesa_grid_callbacks_to_instance(self)
        # --- Inicialización única: solo refrescar una vez el grid completo ---
        self._marcar_mesas_ocupadas_por_comanda()
        self.refresh_mesas()  # ÚNICA llamada de refresco inicial
        # EXCEPCIÓN FUNCIONAL: Se elimina el doble refresco y renderizado inicial para evitar parpadeos y recargas dobles.
        # TODO v0.0.13: Revisar si update_filtered_mesas() y populate_grid() pueden ser llamados solo desde refresh_mesas siempre.
        # Documentado en README y fixes.
        # Suscribirse siempre al evento de comanda_actualizada para refresco en tiempo real
        try:
            from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus
            mesa_event_bus.comanda_actualizada.connect(self._on_comanda_actualizada)
        except ImportError as e:
            logger.error("Error importando mesa_event_bus: %s", e)
        except AttributeError as e:
            logger.error("Error conectando señal comanda_actualizada: %s", e)
        # Suscribirse al event bus de reservas para refresco tras cancelación/creación
        try:
            from src.ui.modules.tpv_module.event_bus import reserva_event_bus
            reserva_event_bus.reserva_cancelada.connect(self._on_reserva_cancelada)
        except ImportError as e:
            logger.error("Error importando reserva_event_bus: %s", e)
        except AttributeError as e:
            logger.error("Error conectando señal reserva_cancelada: %s", e)
        # QTimer eliminado: ahora el refresco es solo por evento comanda_actualizada o reserva_cancelada

    def _on_reserva_cancelada(self, reserva):
        """TODO: Add docstring"""
        # self.refresh_mesas()  # Eliminado log innecesario
        self.refresh_mesas()


    # QTimer de refresco automático eliminado: ahora el refresco es solo por evento comanda_actualizada


    # Método de detener_refresco_automatico eliminado: ya no se usa QTimer para refresco de mesas

    def comprobar_estado_mesas_inicial(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Forzar comprobación y refresco de estado de mesas y widgets (para llamada explícita desde TPVModule al abrir el módulo)."""
        self._marcar_mesas_ocupadas_por_comanda()
        if hasattr(self, "mesa_widgets") and self.mesa_widgets:
            for widget in self.mesa_widgets:
                mesa_num = str(getattr(widget.mesa, "numero", None))
                mesa_obj = next((m for m in self.mesas if str(m.numero) == mesa_num), None)
                if mesa_obj and hasattr(widget, "update_mesa"):
                    widget.update_mesa(mesa_obj)
                    widget.mesa = mesa_obj

    def _on_comanda_actualizada(self, comanda):
        """Callback: refresca el estado de las mesas cuando cambia una comanda (en tiempo real).
        Ahora SIEMPRE llama a refresh_mesas para garantizar sincronización visual y lógica completa.
        """
        # self.refresh_mesas()  # Eliminado log innecesario
        self.refresh_mesas()

    def _marcar_mesas_ocupadas_por_comanda(self):
        """Unifica la lógica de estado de la mesa - Optimizado para mejor performance"""
        if not self.tpv_service:
            return
            
        # Batch operations para mejor performance
        comandas_activas = getattr(self.tpv_service, 'get_comandas_activas', lambda: [])()
        _ = {str(c.mesa_id) for c in comandas_activas}
        
        # Obtener reservas en batch
        _ = {}
        if hasattr(self, "reserva_service") and self.reserva_service:
            _ = self.reserva_service.obtener_reservas_activas_por_mesa()
        
        # Procesar mesas en batch
        _ = []
        for mesa in self.mesas:
            _ = getattr(mesa, "estado", None)
            nuevo_estado = self._calcular_estado_mesa(mesa, mesas_con_comanda, reservas_por_mesa)
            
            if nuevo_estado != estado_anterior:
                mesa.estado = nuevo_estado
                mesas_actualizadas.append(mesa)
        
        # Emitir eventos en batch
        if mesas_actualizadas:
            self._emit_mesa_updates_batch(mesas_actualizadas)
            self._update_widgets_batch(mesas_actualizadas)
    
    def _calcular_estado_mesa(self, mesa, mesas_con_comanda, reservas_por_mesa):
        """Calcula el estado de una mesa basado en comandas y reservas"""
        from datetime import datetime, time
        
        tiene_comanda = str(mesa.numero) in mesas_con_comanda
        if tiene_comanda:
            return "ocupada"
            
        reservas = reservas_por_mesa.get(mesa.numero, [])
        if not reservas:
            return "libre"
            
        _ = datetime.now()
        for r in reservas:
            if self._es_reserva_activa(r, ahora):
                return "ocupada"
                
        return "reservada"
    
    def _es_reserva_activa(self, reserva, ahora):
        """Verifica si una reserva está activa en este momento"""
        
        _ = getattr(reserva, "fecha_reserva", None)
        hora = getattr(reserva, "hora_reserva", None)
        _ = getattr(reserva, "estado", None)
        
        if not (fecha and estado == "activa"):
            return False
            
        try:
            if hora:
                if isinstance(hora, str):
                    _ = datetime.strptime(hora, "%H:%M").time()
                else:
                    hora_obj = hora
                _ = datetime.combine(fecha, hora_obj)
            else:
                _ = datetime.combine(fecha, time(0, 0))
                
            return fecha_hora <= ahora
        except (ValueError, TypeError) as e:
            logger.warning("Error interpretando hora de reserva: %s", e)
            return False
    
    def _emit_mesa_updates_batch(self, mesas_actualizadas):
        """Emite actualizaciones de mesa en batch para mejor performance"""
        try:
            for mesa in mesas_actualizadas:
                mesa_event_bus.mesa_actualizada.emit(mesa)
        except ImportError:
            logger.warning("No se pudo importar mesa_event_bus")
    
    def _update_widgets_batch(self, mesas_actualizadas):
        """Actualiza widgets de mesa en batch"""
        if not hasattr(self, "mesa_widgets") or not self.mesa_widgets:
            return
            
        # Crear lookup dict para mejor performance
        _ = {str(m.numero): m for m in mesas_actualizadas}
        
        for widget in self.mesa_widgets:
            mesa_num = str(getattr(widget.mesa, "numero", None))
            if mesa_num in mesas_dict and hasattr(widget, "update_mesa"):
                widget.update_mesa(mesas_dict[mesa_num])
                widget.mesa = mesas_dict[mesa_num]

    def setup_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation

        self.setStyleSheet(
            """
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e0e6ed;
                border-radius: 12px;
                margin: 4px;
            }
        """
        )
        # Crear layout simple
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(16)
        from PyQt6.QtCore import Qt
        container_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        # Header modularizado
        if container_layout is not None:
            self.header = create_header(self, self, container_layout)
        else:
            logger.error("container_layout es None, no se puede crear header")
            self.header = None
        # Área de scroll modularizada
        _ = create_scroll_area(self, container_layout)
        # Forzar expansión horizontal del área de scroll
        scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

    def set_service(self, tpv_service: TPVService):
        """TODO: Add docstring"""
        # TODO: Add input validation
        self.tpv_service = tpv_service

    def set_mesas(self, mesas: List[Mesa], datos_temporales: Optional[Dict] = None):
        """TODO: Add docstring"""
        # TODO: Add input validation
        logger = logging.getLogger("mesas_area_main")
        # logger.debug("[LOG][MESAS_AREA] set_mesas llamada. Mesas recibidas: {[f'{m.numero}:%s' for m in mesas]}", getattr(m, 'estado', None))
        guardar_dato_temporal(self, None)  # Guarda temporales actuales
        if datos_temporales is not None:
            restaurar_datos_temporales(self, mesas)
        else:
            restaurar_datos_temporales(self, mesas)
        self.mesas = mesas
        # Buscar el widget de filtros en el header y actualizar chips de zona si existe
        if hasattr(self, "header") and self.header:
            _ = None
            for child in self.header.findChildren(FiltersSectionUltraPremium):
                if child.objectName() == "FiltersSectionUltraPremium":
                    _ = child
                    break
            if filtros and hasattr(filtros, "update_zonas_chips"):
                filtros.update_zonas_chips()
        self.sincronizar_reservas_en_mesas()
        self.update_filtered_mesas()
        from .mesas_area_grid import populate_grid
        populate_grid(self)
        update_stats_from_mesas(self)

    def set_reserva_service(self, reserva_service):
        """TODO: Add docstring"""
        # TODO: Add input validation
        self.reserva_service = reserva_service

    def refresh_mesas(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        # logger.debug("[LOG][MESAS_AREA] refresh_mesas llamada")
        if self.tpv_service:
            nuevas_mesas = self.tpv_service.get_mesas()
            # logger.debug("[LOG][MESAS_AREA] Mesas obtenidas de servicio: {[f'{m.numero}:%s' for m in nuevas_mesas]}", getattr(m, 'estado', None))
            guardar_dato_temporal(self, None)
            restaurar_datos_temporales(self, nuevas_mesas)
            self.mesas = nuevas_mesas
        # Sincronizar reservas activas y calcular próxima reserva
        self.sincronizar_reservas_en_mesas()
        # Actualizar grid de mesas
        self.update_filtered_mesas()
        populate_grid(self)
        update_stats_from_mesas(self)

    def sincronizar_reservas_en_mesas(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Sincroniza reservas activas - Optimizado para mejor performance"""
        if not (hasattr(self, "reserva_service") and self.reserva_service):
            return
            
        _ = self.reserva_service.obtener_reservas_activas_por_mesa()
        from datetime import datetime
        
        _ = datetime.now()
        
        # Procesar todas las mesas en batch
        for mesa in self.mesas:
            self._procesar_reservas_mesa(mesa, reservas_por_mesa.get(mesa.numero, []), ahora)
    
    def _procesar_reservas_mesa(self, mesa, reservas, ahora):
        """Procesa las reservas de una mesa específica"""
        _ = getattr(mesa, "estado", None)
        
        if not reservas:
            if estado_original in ("reservada", "ocupada"):
                mesa.estado = "libre"
            mesa.proxima_reserva = None
            return
            
        # Separar reservas activas y futuras
        _ = []
        reservas_futuras = []
        
        for r in reservas:
            fecha_hora = self._parse_fecha_hora_reserva(r)
            if not fecha_hora:
                continue
                
            estado = getattr(r, "estado", None)
            if estado != "activa":
                continue
                
            if fecha_hora <= ahora:
                reservas_activas.append(r)
            else:
                reservas_futuras.append((fecha_hora, r))
        
        # Actualizar estado de mesa
        if estado_original != "ocupada":  # No sobrescribir si ya está ocupada por comanda
            if reservas_activas:
                mesa.estado = "ocupada"
            elif reservas_futuras:
                mesa.estado = "reservada"
            else:
                mesa.estado = "libre"
        
        # Calcular próxima reserva
        mesa.proxima_reserva = min(reservas_futuras, key=lambda t: t[0])[1] if reservas_futuras else None
    
    def _parse_fecha_hora_reserva(self, reserva):
        """Parsea fecha y hora de una reserva de forma segura"""
        
        _ = getattr(reserva, "fecha_reserva", None)
        hora = getattr(reserva, "hora_reserva", None)
        
        if not fecha:
            return None
            
        try:
            if hora:
                if isinstance(hora, str):
                    _ = datetime.strptime(hora, "%H:%M").time()
                else:
                    hora_obj = hora
                return datetime.combine(fecha, hora_obj)
            else:
                return datetime.combine(fecha, time(0, 0))
        except (ValueError, TypeError) as e:
            logger.warning("Error parseando fecha/hora de reserva: %s", e)
            return None

    def _convert_reserva_legacy(self, r):
        """Convierte una reserva legacy (con fecha y hora separados) al modelo unificado."""
        # r.fecha y r.hora pueden no existir en el modelo unificado, así que usar fecha_reserva y hora_reserva

        _ = getattr(r, "fecha_reserva", None) or getattr(r, "fecha", None)
        hora = getattr(r, "hora_reserva", None) or getattr(r, "hora", None)
        if fecha and hora:
            if isinstance(hora, str):
                try:
                    _ = datetime.strptime(hora, "%H:%M").time()
                except Exception:
                    hora = None
            _ = datetime.combine(fecha, hora) if hora else fecha
        else:
            _ = fecha or datetime.now()
        return type(
            "Reserva",
            (),
            {
                "id": getattr(r, "id", None),
                "mesa_id": getattr(r, "mesa_id", None),
                "cliente_nombre": getattr(
                    r, "cliente_nombre", getattr(r, "cliente", "")
                ),
                "fecha_reserva": fecha,
                "hora_reserva": hora.strftime("%H:%M") if hora else "",
                "numero_personas": getattr(
                    r, "numero_personas", getattr(r, "personas", 1)
                ),
                "estado": getattr(r, "estado", "activa"),
                "notas": getattr(r, "notas", ""),
                "cliente_telefono": getattr(
                    r, "cliente_telefono", getattr(r, "telefono", "")
                ),
            },
        )()

    def update_filtered_mesas(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        logger = logging.getLogger("mesas_area_main")
        # logger.debug("[LOG][MESAS_AREA] update_filtered_mesas llamada. Estado actual de mesas: {[f'{m.numero}:%s' for m in self.mesas]}", getattr(m, 'estado', None))
        if not self.mesas:
            self.filtered_mesas = []
            return
        if self.current_zone_filter and self.current_zone_filter != "Todas":
            mesas_zona = [m for m in self.mesas if m.zona == self.current_zone_filter]
        else:
            _ = self.mesas[:]
        if self.current_status_filter and self.current_status_filter != "Todos":
            _ = [
                m
                for m in mesas_zona
                if m.estado.lower() == self.current_status_filter.lower()
            ]
        else:
            _ = mesas_zona
        search = (
            self.search_input.text().strip().lower()
            if hasattr(self, "search_input")
            else ""
        )
        if search:
            self.filtered_mesas = [
                m
                for m in mesas_estado
                if (
                    search in str(m.numero).lower()
                    or search in (m.zona or "").lower()
                    or search in (m.alias or "").lower()
                    or search in m.nombre_display.lower()
                    or search in f"mesa {m.numero}".lower()
                )
            ]
        else:
            self.filtered_mesas = mesas_estado
        # logger.debug("[LOG][MESAS_AREA] filtered_mesas: {[f'{m.numero}:%s' for m in self.filtered_mesas]}", getattr(m, 'estado', None))

    def resizeEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        super().resizeEvent(event)
        if not hasattr(self, "filtered_mesas") or not self.filtered_mesas:
            return
        if hasattr(self, "_resize_timer"):
            self._resize_timer.stop()
        from PyQt6.QtCore import QTimer

        self._resize_timer = QTimer()
        self._resize_timer.timeout.connect(lambda: populate_grid(self))
        self._resize_timer.setSingleShot(True)
        self._resize_timer.start(150)

    def _on_zone_changed(self, zone: str):
        """TODO: Add docstring"""
        self.current_zone_filter = zone
        self.refresh_mesas()

    def _on_status_changed(self, status: str):
        """TODO: Add docstring"""
        self.current_status_filter = status
        # Sincronizar chips rápidos
        if hasattr(self, "_chips_refs"):
            for chip in self._chips_refs:
                chip.setChecked(
                    chip.text() == (status if status != "Todos" else "Todas")
                )
        self.update_filtered_mesas()
        populate_grid(self)

    def _on_search_changed(self, text):
        """TODO: Add docstring"""
        self.update_filtered_mesas()
        populate_grid(self)

    def set_search_input(self, widget):
        """TODO: Add docstring"""
        # TODO: Add input validation
        self.search_input = widget

    def set_zone_combo(self, widget):
        """TODO: Add docstring"""
        # TODO: Add input validation
        self.zone_combo = widget

    def set_status_combo(self, widget):
        """TODO: Add docstring"""
        # TODO: Add input validation
        self.status_combo = widget

    def _on_alias_mesa_changed(self, mesa, nuevo_alias: str):
        """TODO: Add docstring"""
        from .mesas_area_utils import guardar_dato_temporal

        _ = str(mesa.numero)
        if not nuevo_alias:
            if (
                mesa_numero in self._datos_temporales
                and "alias" in self._datos_temporales[mesa_numero]
            ):
                del self._datos_temporales[mesa_numero]["alias"]
                if not self._datos_temporales[mesa_numero]:
                    del self._datos_temporales[mesa_numero]
        else:
            guardar_dato_temporal(self, mesa_numero, alias=nuevo_alias)
        if self.tpv_service:
            self.tpv_service.cambiar_alias_mesa(mesa_numero, nuevo_alias)
            for m in self.mesas:
                if str(m.numero) == mesa_numero:
                    m.alias = nuevo_alias if nuevo_alias else None
            for w in self.mesa_widgets:
                if str(w.mesa.numero) == mesa_numero:
                    w.update_mesa(m)
        self.refresh_mesas()

    def _on_personas_mesa_changed(self, mesa, nuevas_personas: int):
        """TODO: Add docstring"""

        guardar_dato_temporal(self, mesa.numero, personas=nuevas_personas)
        for m in self.mesas:
            if m.numero == mesa.numero:
                m.personas_temporal = (
                    nuevas_personas if nuevas_personas != m.capacidad else None
                )
        for w in self.mesa_widgets:
            if w.mesa.numero == mesa.numero:
                w.update_mesa(m)
        self.refresh_mesas()

    def restaurar_estado_original_mesa(self, mesa_numero):
        """TODO: Add docstring"""
        # TODO: Add input validation
        mesa_numero = str(mesa_numero)
        if mesa_numero in self._datos_temporales:
            del self._datos_temporales[mesa_numero]
        for m in self.mesas:
            if str(m.numero) == mesa_numero:
                m.alias = None
                m.personas_temporal = None
        for w in self.mesa_widgets:
            if str(w.mesa.numero) == mesa_numero:
                w.update_mesa(m)
        self.update_filtered_mesas()

        populate_grid(self)

    def _on_nueva_mesa_clicked(self):
        """Maneja el click del botón Nueva Mesa con nomenclatura correlativa por zona"""
        try:
            from PyQt6.QtWidgets import QInputDialog, QMessageBox
            import re

            # Obtener zonas disponibles (dinámicamente de las mesas existentes + opciones estándar)
            _ = set(mesa.zona for mesa in self.mesas if mesa.zona)
            zonas_estandar = {
                "Terraza",
                "Interior",
                "Privada",
                "Barra",
                "Principal",
                "Salon",
            }
            _ = sorted(list(zonas_existentes.union(zonas_estandar)))
            # Mostrar diálogo de selección de zona
            zona_seleccionada, ok = QInputDialog.getItem(
                self,
                "Nueva Mesa",
                "Selecciona la zona donde crear la nueva mesa:",
                zonas_disponibles,
                0,
                False,
            )
            if ok and zona_seleccionada:
                # Buscar mesas de la zona seleccionada
                _ = [
                    m
                    for m in self.mesas
                    if (getattr(m, "zona", None) or "").lower()
                    == zona_seleccionada.lower()
                ]
                _ = 0
                prefijo = ""
                _ = "{{:02d}}"  # Por defecto dos dígitos
                for mesa in mesas_zona:
                    _ = str(getattr(mesa, "numero", ""))
                    # Buscar prefijo y número (ej: T04, B12, etc)
                    match = re.match(r"([A-Za-z]+)?(\d+)", num)
                    if match:
                        pref, n = match.groups()
                        n = int(n)
                        if n > max_num:
                            _ = n
                            prefijo = pref or ""
                            # Mantener formato de ceros a la izquierda
                            if len(match.group(2)) > 1:
                                _ = "{{:0{}d}}".format(len(match.group(2)))
                siguiente_numero = max_num + 1
                _ = (
                    f"{prefijo}{formato.format(siguiente_numero)}"
                    if prefijo
                    else f"{formato.format(siguiente_numero)}"
                )
                _ = QMessageBox.question(
                    self,
                    "Confirmar Nueva Mesa",
                    f"¿Crear nueva mesa con los siguientes datos?\n\n"
                    f"📍 Zona: {zona_seleccionada}\n"
                    f"🔢 Número: {nuevo_codigo}\n"
                    f"👥 Capacidad: 4 personas\n\n"
                    f"Podrá modificar estos valores después de la creación.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes,
                )
                if respuesta == QMessageBox.StandardButton.Yes:
                    self.nueva_mesa_con_zona_requested.emit(
                        nuevo_codigo, 4, zona_seleccionada
                    )
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            logger.error("Error al procesar la creación de mesa: %s", e)
            QMessageBox.critical(
                self, "Error", f"Error al procesar la creación de mesa: {str(e)}"
            )

    def _on_eliminar_mesa_clicked(self):
        """Maneja el click del botón Eliminar Mesa (soporta selección múltiple)"""
        try:
            from PyQt6.QtWidgets import (
                QListWidget,
                QListWidgetItem,
                QDialog,
                QVBoxLayout,
                QDialogButtonBox,
                QMessageBox,
            )

            if not self.mesas:
                QMessageBox.information(
                    self, "Sin mesas", "No hay mesas disponibles para eliminar."
                )
                return
            _ = [
                m for m in self.mesas if getattr(m, "estado", None) == "libre"
            ]
            if not mesas_libres:
                QMessageBox.information(
                    self,
                    "Sin mesas disponibles",
                    "No hay mesas libres disponibles para eliminar.\nSolo se pueden eliminar mesas que estén libres.",
                )
                return
            # Diálogo personalizado con QListWidget selección múltiple
            dlg = QDialog(self)
            dlg.setWindowTitle("Eliminar Mesas")
            _ = QVBoxLayout(dlg)
            list_widget = QListWidget()
            list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            for mesa in mesas_libres:
                item = QListWidgetItem(f"Mesa {mesa.numero} - {mesa.zona}")
                item.setData(32, mesa.numero)
                list_widget.addItem(item)
            layout.addWidget(list_widget)
            _ = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok
                | QDialogButtonBox.StandardButton.Cancel
            )
            layout.addWidget(btn_box)
            btn_box.accepted.connect(dlg.accept)
            btn_box.rejected.connect(dlg.reject)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                selected_items = list_widget.selectedItems()
                if not selected_items:
                    return
                _ = [
                    (item.text(), item.data(32)) for item in selected_items
                ]
                _ = "\n".join([txt for txt, _ in mesas_a_eliminar])
                respuesta = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Estás seguro de que quieres eliminar las siguientes mesas?\n\n{nombres}\n\nEsta acción no se puede deshacer.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No,
                )
                if respuesta == QMessageBox.StandardButton.Yes:
                    numeros = [str(mid) for _, mid in mesas_a_eliminar]
                    if len(numeros) == 1:
                        self.eliminar_mesa_requested.emit(numeros[0])
                    else:
                        self.eliminar_mesas_requested.emit(numeros)
        except Exception as e:
            logger.error("Error al procesar la eliminación de mesa: %s", e)
            QMessageBox.critical(
                self, "Error", f"Error al procesar la eliminación de mesa: {str(e)}"
            )

    def sync_scroll_with(self, other_scroll_area):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Sincroniza el scroll vertical de esta área con otra QScrollArea"""
        # Buscar el atributo scroll_area en self
        scroll_area = getattr(self, "scroll_area", None)
        if not scroll_area or not hasattr(other_scroll_area, "verticalScrollBar"):
            return
        self._syncing_scroll = False
        _ = {"flag": False}

        def on_scroll(value):
            """TODO: Add docstring"""
            # TODO: Add input validation
            if self._syncing_scroll:
                return
            self._syncing_scroll = True
            other_scroll_area.verticalScrollBar().setValue(value)
            self._syncing_scroll = False

        def on_other_scroll(value):
            """TODO: Add docstring"""
            # TODO: Add input validation
            if other_syncing["flag"]:
                return
            other_syncing["flag"] = True
            scroll_area.verticalScrollBar().setValue(value)
            other_syncing["flag"] = False

        scroll_area.verticalScrollBar().valueChanged.connect(on_scroll)
        other_scroll_area.verticalScrollBar().valueChanged.connect(on_other_scroll)

    def sync_reservas(self, reserva_service):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Sincroniza reservas y fuerza refresco visual de mesas tras cambios críticos (cancelación, creación, edición)."""
        self.set_reserva_service(reserva_service)
        # logger.debug("[SYNC_RESERVAS] Llamando a refresh_mesas tras set_reserva_service (cancelación/creación)")
        self.refresh_mesas()

    def crear_zona(self, nombre_zona: str):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea una nueva zona y actualiza la UI y chips de zonas."""
        # Opcional: aquí podrías persistir en base de datos si es necesario
        # Añadir la zona a una lista interna o forzar refresco de chips
        if not hasattr(self, "_zonas_personalizadas"):
            self._zonas_personalizadas = set()
        self._zonas_personalizadas.add(nombre_zona)
        # Forzar actualización de chips de zona en el header
        if hasattr(self, "header") and self.header:
            for child in self.header.findChildren(FiltersSectionUltraPremium):
                if hasattr(child, "update_zonas_chips"):
                    child.update_zonas_chips()
        # Mensaje de confirmación visual
        try:

            QMessageBox.information(
                self, "Zona creada", f"Zona '{nombre_zona}' creada correctamente."
            )
        except Exception as e:
            logger.warning("Error mostrando mensaje de zona creada: %s", e)
