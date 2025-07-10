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

# Importar subcomponentes
from .mesas_area_header import FiltersSectionUltraPremium
from .mesas_area_header import create_header
from .mesas_area_grid import (
    create_scroll_area,
    populate_grid,
    add_mesa_grid_callbacks_to_instance,
)
from .mesas_area_stats import update_stats_from_mesas
from .mesas_area_utils import (
    restaurar_datos_temporales,
    guardar_dato_temporal,
)

logger = logging.getLogger(__name__)


class MesasArea(QFrame):
    # --- Lógica de selección múltiple y acciones por lotes ---
    def enable_batch_mode(self, enabled: bool):
        self.batch_mode = enabled
        for w in self.mesa_widgets:
            if hasattr(w, "set_batch_mode"):
                w.set_batch_mode(enabled)
        self.selected_mesas = set()
        self.update_batch_action_btn()

    def toggle_mesa_selection(self, mesa_numero):
        """Selecciona/deselecciona una mesa usando su identificador string 'numero'"""
        mesa_numero = str(mesa_numero)
        if not hasattr(self, "selected_mesas"):
            self.selected_mesas = set()
        if mesa_numero in self.selected_mesas:
            self.selected_mesas.remove(mesa_numero)
        else:
            self.selected_mesas.add(mesa_numero)
        self.update_batch_action_btn()

    def update_batch_action_btn(self):
        # Busca el botón de acción por lotes en el header y lo habilita/deshabilita
        # Solución: buscar el widget en el layout del header
        if hasattr(self, "header"):
            # Buscar en los hijos del header un QPushButton con texto 'Acción por lotes'
            from PyQt6.QtWidgets import QPushButton

            def find_batch_btn(widget):
                for child in widget.findChildren(QPushButton):
                    if child.text() == "Acción por lotes":
                        return child
                return None

            batch_btn = find_batch_btn(self.header)
            if batch_btn:
                batch_btn.setEnabled(bool(self.selected_mesas))

    def do_batch_action(self):
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
        """Alterna entre vista grid y lista"""
        self.view_mode = "list" if self.view_mode == "grid" else "grid"
        # TODO: Implementar renderizado de vista lista si es necesario
        self.refresh_mesas()

    """Área de visualización y gestión de mesas (modularizado)"""
    nueva_mesa_requested = pyqtSignal()
    nueva_mesa_con_zona_requested = pyqtSignal(int, int, str)
    eliminar_mesa_requested = pyqtSignal(str)  # Ahora emite el 'numero' de la mesa
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
            logger.error(f"Error importando mesa_event_bus: {e}")
        except AttributeError as e:
            logger.error(f"Error conectando señal comanda_actualizada: {e}")
        # Suscribirse al event bus de reservas para refresco tras cancelación/creación
        try:
            from src.ui.modules.tpv_module.event_bus import reserva_event_bus
            reserva_event_bus.reserva_cancelada.connect(self._on_reserva_cancelada)
        except ImportError as e:
            logger.error(f"Error importando reserva_event_bus: {e}")
        except AttributeError as e:
            logger.error(f"Error conectando señal reserva_cancelada: {e}")
        # QTimer eliminado: ahora el refresco es solo por evento comanda_actualizada o reserva_cancelada

    def _on_reserva_cancelada(self, reserva):
        # self.refresh_mesas()  # Eliminado log innecesario
        self.refresh_mesas()


    # QTimer de refresco automático eliminado: ahora el refresco es solo por evento comanda_actualizada


    # Método de detener_refresco_automatico eliminado: ya no se usa QTimer para refresco de mesas

    def comprobar_estado_mesas_inicial(self):
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
        """Unifica la lógica de estado de la mesa: ocupada si hay comanda activa o reserva en curso, reservada si solo hay reserva futura, libre si ninguna."""
        if not self.tpv_service:
            return
        comandas_activas = (
            self.tpv_service.get_comandas_activas()
            if hasattr(self.tpv_service, "get_comandas_activas")
            else []
        )
        mesas_con_comanda = set(str(c.mesa_id) for c in comandas_activas)
        # LOG DIAGNÓSTICO: imprimir comandas activas y mesas_con_comanda
        # Logs de debug eliminados para limpieza
        # Obtener reservas activas si hay reserva_service
        reservas_por_mesa = {}
        if hasattr(self, "reserva_service") and self.reserva_service:
            reservas_por_mesa = self.reserva_service.obtener_reservas_activas_por_mesa()
        from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus
        from datetime import datetime, time
        ahora = datetime.now()
        for mesa in self.mesas:
            estado_anterior = getattr(mesa, "estado", None)
            # logger.debug(f"[DEBUG][ANTES] mesa {mesa.numero} estado={estado_anterior}")
            tiene_comanda = str(mesa.numero) in mesas_con_comanda
            reservas = reservas_por_mesa.get(mesa.numero, [])
            reserva_en_curso = None
            for r in reservas:
                fecha = getattr(r, "fecha_reserva", None)
                hora = getattr(r, "hora_reserva", None)
                if fecha and hora:
                    try:
                        if isinstance(hora, str):
                            hora_obj = datetime.strptime(hora, "%H:%M").time()
                        else:
                            hora_obj = hora
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Error interpretando hora de reserva: {e}")
                        hora_obj = time(0, 0)
                    fecha_hora = datetime.combine(fecha, hora_obj)
                elif fecha:
                    fecha_hora = datetime.combine(fecha, time(0, 0))
                else:
                    fecha_hora = None
                estado_reserva = getattr(r, "estado", None)
                if (
                    fecha_hora is not None
                    and estado_reserva is not None
                    and fecha_hora <= ahora
                    and estado_reserva == "activa"
                ):
                    reserva_en_curso = r
                    break
            if tiene_comanda or reserva_en_curso:
                mesa.estado = "ocupada"
            elif reservas:
                mesa.estado = "reservada"
            else:
                mesa.estado = "libre"
            # logger.debug(f"[DEBUG][DESPUES] mesa {mesa.numero} estado={mesa.estado}")
            if getattr(mesa, "estado", None) != estado_anterior:
                # logger.debug(f"[LOG][MESAS_AREA] mesa_actualizada.emit: mesa={mesa.numero} estado={mesa.estado}")
                mesa_event_bus.mesa_actualizada.emit(mesa)
        # Refrescar widgets de mesa responsivamente (FIX: siempre usar la referencia actualizada de Mesa)
        if hasattr(self, "mesa_widgets") and self.mesa_widgets:
            for widget in self.mesa_widgets:
                mesa_num = str(getattr(widget.mesa, "numero", None))
                mesa_obj = next((m for m in self.mesas if str(m.numero) == mesa_num), None)
                if mesa_obj and hasattr(widget, "update_mesa"):
                    # logger.debug(f"[LOG][MESAS_AREA] Llamando update_mesa en widget para mesa={mesa_num} estado={mesa_obj.estado}")
                    widget.update_mesa(mesa_obj)
                    widget.mesa = mesa_obj
        # Refrescar grid visual si ya está renderizado (opcional, solo si hay cambios estructurales)
        if hasattr(self, "mesas_layout") and self.mesas_layout is not None:
            from .mesas_area_grid import refresh_all_mesa_widgets_styles
            refresh_all_mesa_widgets_styles(self)

    def setup_ui(self):
        from PyQt6.QtWidgets import QSizePolicy

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
        # Refuerzo: limpiar layout anterior y crear layout sin parent
        old_layout = self.layout()
        if old_layout is not None:
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            try:
                old_layout.deleteLater()
            except Exception as e:
                logger.warning(f"Error eliminando layout anterior: {e}")
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(16)
        from PyQt6.QtCore import Qt

        container_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.setLayout(container_layout)
        # Header modularizado
        self.header = create_header(self, self, container_layout)
        # Área de scroll modularizada
        scroll_area = create_scroll_area(self, container_layout)
        # Forzar expansión horizontal del área de scroll
        scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

    def set_service(self, tpv_service: TPVService):
        self.tpv_service = tpv_service

    def set_mesas(self, mesas: List[Mesa], datos_temporales: Optional[Dict] = None):
        import logging
        logger = logging.getLogger("mesas_area_main")
        # logger.debug(f"[LOG][MESAS_AREA] set_mesas llamada. Mesas recibidas: {[f'{m.numero}:{getattr(m, 'estado', None)}' for m in mesas]}")
        guardar_dato_temporal(self, None)  # Guarda temporales actuales
        if datos_temporales is not None:
            restaurar_datos_temporales(self, mesas)
        else:
            restaurar_datos_temporales(self, mesas)
        self.mesas = mesas
        # Buscar el widget de filtros en el header y actualizar chips de zona si existe
        if hasattr(self, "header") and self.header is not None:
            filtros = None
            for child in self.header.findChildren(FiltersSectionUltraPremium):
                if child.objectName() == "FiltersSectionUltraPremium":
                    filtros = child
                    break
            if filtros and hasattr(filtros, "update_zonas_chips"):
                filtros.update_zonas_chips()
        self.sincronizar_reservas_en_mesas()
        self.refresh_mesas()
        update_stats_from_mesas(self)

    def set_reserva_service(self, reserva_service):
        self.reserva_service = reserva_service

    def refresh_mesas(self):
        # logger.debug("[LOG][MESAS_AREA] refresh_mesas llamada")
        if self.tpv_service:
            nuevas_mesas = self.tpv_service.get_mesas()
            # logger.debug(f"[LOG][MESAS_AREA] Mesas obtenidas de servicio: {[f'{m.numero}:{getattr(m, 'estado', None)}' for m in nuevas_mesas]}")
            guardar_dato_temporal(self, None)
            restaurar_datos_temporales(self, nuevas_mesas)
            self.mesas = nuevas_mesas
        # Sincronizar reservas activas y calcular próxima reserva
        self.sincronizar_reservas_en_mesas()
        # logger.debug(f"[LOG][MESAS_AREA] Estado de mesas tras sincronizar reservas: {[f'{m.numero}:{getattr(m, 'estado', None)}' for m in self.mesas]}")
        # FIX: Se elimina llamada recursiva a self.refresh_mesas() para evitar recursion depth exceeded

    def sincronizar_reservas_en_mesas(self):
        """Sincroniza reservas activas y calcula próxima reserva para cada mesa. SOLO modelo unificado. Usa numero como identificador.
        Respeta el estado 'ocupada' si la mesa ya está ocupada por comanda."""
        if hasattr(self, "reserva_service") and self.reserva_service:
            reservas_por_mesa = self.reserva_service.obtener_reservas_activas_por_mesa()
            from datetime import datetime, time

            ahora = datetime.now()
            for mesa in self.mesas:
                estado_original = getattr(mesa, "estado", None)
                tiene_reservas = mesa.numero in reservas_por_mesa
                reservas = reservas_por_mesa.get(mesa.numero, [])
                # Determinar si hay una reserva en curso
                reserva_en_curso = None
                for r in reservas:
                    fecha = getattr(r, "fecha_reserva", None)
                    hora = getattr(r, "hora_reserva", None)
                    if fecha and hora:
                        try:
                            if isinstance(hora, str):
                                hora_obj = datetime.strptime(hora, "%H:%M").time()
                            else:
                                hora_obj = hora
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Error interpretando hora de reserva: {e}")
                            hora_obj = time(0, 0)
                        fecha_hora = datetime.combine(fecha, hora_obj)
                    elif fecha:
                        fecha_hora = datetime.combine(fecha, time(0, 0))
                    else:
                        fecha_hora = None
                    estado = getattr(r, "estado", None)
                    if (
                        fecha_hora is not None
                        and estado is not None
                        and fecha_hora <= ahora
                        and estado == "activa"
                    ):
                        reserva_en_curso = r
                        break
                # SOLO modificar el estado si la mesa NO está ocupada por comanda
                if estado_original == "ocupada":
                    # No sobrescribir, solo calcular proxima_reserva
                    pass
                elif reserva_en_curso:
                    mesa.estado = "ocupada"
                elif tiene_reservas:
                    mesa.estado = "reservada"
                elif estado_original in ("reservada", "ocupada"):
                    mesa.estado = "libre"
                # Calcular próxima reserva activa (>= ahora)
                futuras = []
                for r in reservas:
                    fecha = getattr(r, "fecha_reserva", None)
                    hora = getattr(r, "hora_reserva", None)
                    if fecha and hora:
                        try:
                            if isinstance(hora, str):
                                hora_obj = datetime.strptime(hora, "%H:%M").time()
                            else:
                                hora_obj = hora
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Error interpretando hora de reserva: {e}")
                            hora_obj = time(0, 0)
                        fecha_hora = datetime.combine(fecha, hora_obj)
                    elif fecha:
                        fecha_hora = datetime.combine(fecha, time(0, 0))
                    else:
                        fecha_hora = None
                    estado = getattr(r, "estado", None)
                    if (
                        fecha_hora is not None
                        and estado is not None
                        and fecha_hora >= ahora
                        and estado == "activa"
                    ):
                        futuras.append((fecha_hora, r))
                if futuras:
                    mesa.proxima_reserva = min(futuras, key=lambda t: t[0])[1]
                else:
                    mesa.proxima_reserva = None
        # Eliminar vestigio legacy: _convert_reserva_legacy y referencias legacy eliminadas

    def _convert_reserva_legacy(self, r):
        """Convierte una reserva legacy (con fecha y hora separados) al modelo unificado."""
        # r.fecha y r.hora pueden no existir en el modelo unificado, así que usar fecha_reserva y hora_reserva
        from datetime import datetime

        fecha = getattr(r, "fecha_reserva", None) or getattr(r, "fecha", None)
        hora = getattr(r, "hora_reserva", None) or getattr(r, "hora", None)
        if fecha and hora:
            if isinstance(hora, str):
                try:
                    hora = datetime.strptime(hora, "%H:%M").time()
                except Exception:
                    hora = None
            fecha_hora = datetime.combine(fecha, hora) if hora else fecha
        else:
            fecha_hora = fecha or datetime.now()
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
        import logging
        logger = logging.getLogger("mesas_area_main")
        # logger.debug(f"[LOG][MESAS_AREA] update_filtered_mesas llamada. Estado actual de mesas: {[f'{m.numero}:{getattr(m, 'estado', None)}' for m in self.mesas]}")
        if not self.mesas:
            self.filtered_mesas = []
            return
        if self.current_zone_filter and self.current_zone_filter != "Todas":
            mesas_zona = [m for m in self.mesas if m.zona == self.current_zone_filter]
        else:
            mesas_zona = self.mesas[:]
        if self.current_status_filter and self.current_status_filter != "Todos":
            mesas_estado = [
                m
                for m in mesas_zona
                if m.estado.lower() == self.current_status_filter.lower()
            ]
        else:
            mesas_estado = mesas_zona
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
        # logger.debug(f"[LOG][MESAS_AREA] filtered_mesas: {[f'{m.numero}:{getattr(m, 'estado', None)}' for m in self.filtered_mesas]}")

    def resizeEvent(self, event):
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
        self.current_zone_filter = zone
        self.refresh_mesas()

    def _on_status_changed(self, status: str):
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
        self.update_filtered_mesas()
        populate_grid(self)

    def set_search_input(self, widget):
        self.search_input = widget

    def set_zone_combo(self, widget):
        self.zone_combo = widget

    def set_status_combo(self, widget):
        self.status_combo = widget

    def _on_alias_mesa_changed(self, mesa, nuevo_alias: str):
        from .mesas_area_utils import guardar_dato_temporal

        mesa_numero = str(mesa.numero)
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
        from .mesas_area_utils import guardar_dato_temporal

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
        from .mesas_area_grid import populate_grid

        populate_grid(self)

    def _on_nueva_mesa_clicked(self):
        """Maneja el click del botón Nueva Mesa con nomenclatura correlativa por zona"""
        try:
            from PyQt6.QtWidgets import QInputDialog, QMessageBox
            import re

            # Obtener zonas disponibles (dinámicamente de las mesas existentes + opciones estándar)
            zonas_existentes = set(mesa.zona for mesa in self.mesas if mesa.zona)
            zonas_estandar = {
                "Terraza",
                "Interior",
                "Privada",
                "Barra",
                "Principal",
                "Salon",
            }
            zonas_disponibles = sorted(list(zonas_existentes.union(zonas_estandar)))
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
                mesas_zona = [
                    m
                    for m in self.mesas
                    if (getattr(m, "zona", None) or "").lower()
                    == zona_seleccionada.lower()
                ]
                max_num = 0
                prefijo = ""
                formato = "{{:02d}}"  # Por defecto dos dígitos
                for mesa in mesas_zona:
                    num = str(getattr(mesa, "numero", ""))
                    # Buscar prefijo y número (ej: T04, B12, etc)
                    match = re.match(r"([A-Za-z]+)?(\d+)", num)
                    if match:
                        pref, n = match.groups()
                        n = int(n)
                        if n > max_num:
                            max_num = n
                            prefijo = pref or ""
                            # Mantener formato de ceros a la izquierda
                            if len(match.group(2)) > 1:
                                formato = "{{:0{}d}}".format(len(match.group(2)))
                siguiente_numero = max_num + 1
                nuevo_codigo = (
                    f"{prefijo}{formato.format(siguiente_numero)}"
                    if prefijo
                    else f"{formato.format(siguiente_numero)}"
                )
                respuesta = QMessageBox.question(
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
            logger.error(f"Error al procesar la creación de mesa: {e}")
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
            mesas_libres = [
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
            layout = QVBoxLayout(dlg)
            list_widget = QListWidget()
            list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            for mesa in mesas_libres:
                item = QListWidgetItem(f"Mesa {mesa.numero} - {mesa.zona}")
                item.setData(32, mesa.numero)
                list_widget.addItem(item)
            layout.addWidget(list_widget)
            btn_box = QDialogButtonBox(
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
                mesas_a_eliminar = [
                    (item.text(), item.data(32)) for item in selected_items
                ]
                nombres = "\n".join([txt for txt, _ in mesas_a_eliminar])
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
            from PyQt6.QtWidgets import QMessageBox
            logger.error(f"Error al procesar la eliminación de mesa: {e}")
            QMessageBox.critical(
                self, "Error", f"Error al procesar la eliminación de mesa: {str(e)}"
            )

    def sync_scroll_with(self, other_scroll_area):
        """Sincroniza el scroll vertical de esta área con otra QScrollArea"""
        # Buscar el atributo scroll_area en self
        scroll_area = getattr(self, "scroll_area", None)
        if not scroll_area or not hasattr(other_scroll_area, "verticalScrollBar"):
            return
        self._syncing_scroll = False
        other_syncing = {"flag": False}

        def on_scroll(value):
            if self._syncing_scroll:
                return
            self._syncing_scroll = True
            other_scroll_area.verticalScrollBar().setValue(value)
            self._syncing_scroll = False

        def on_other_scroll(value):
            if other_syncing["flag"]:
                return
            other_syncing["flag"] = True
            scroll_area.verticalScrollBar().setValue(value)
            other_syncing["flag"] = False

        scroll_area.verticalScrollBar().valueChanged.connect(on_scroll)
        other_scroll_area.verticalScrollBar().valueChanged.connect(on_other_scroll)

    def sync_reservas(self, reserva_service):
        """Sincroniza reservas y fuerza refresco visual de mesas tras cambios críticos (cancelación, creación, edición)."""
        self.set_reserva_service(reserva_service)
        # logger.debug("[SYNC_RESERVAS] Llamando a refresh_mesas tras set_reserva_service (cancelación/creación)")
        self.refresh_mesas()

    def crear_zona(self, nombre_zona: str):
        """Crea una nueva zona y actualiza la UI y chips de zonas."""
        # Opcional: aquí podrías persistir en base de datos si es necesario
        # Añadir la zona a una lista interna o forzar refresco de chips
        if not hasattr(self, "_zonas_personalizadas"):
            self._zonas_personalizadas = set()
        self._zonas_personalizadas.add(nombre_zona)
        # Forzar actualización de chips de zona en el header
        if hasattr(self, "header") and self.header is not None:
            for child in self.header.findChildren(FiltersSectionUltraPremium):
                if hasattr(child, "update_zonas_chips"):
                    child.update_zonas_chips()
        # Mensaje de confirmación visual
        try:
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.information(
                self, "Zona creada", f"Zona '{nombre_zona}' creada correctamente."
            )
        except Exception as e:
            logger.warning(f"Error mostrando mensaje de zona creada: {e}")
