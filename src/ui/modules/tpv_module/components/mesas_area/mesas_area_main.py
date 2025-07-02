"""
mesas_area_main.py
Clase principal MesasArea (coordinador) y punto de entrada del área modularizada
"""

import logging
from typing import List, Optional, Callable, Dict
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from ...widgets.mesa_widget_simple import MesaWidget
from services.tpv_service import Mesa, TPVService
from ...mesa_event_bus import mesa_event_bus

# Importar subcomponentes
from .mesas_area_header import create_header
from .mesas_area_grid import create_scroll_area, populate_grid
from .mesas_area_stats import update_stats_from_mesas
from .mesas_area_utils import calcular_columnas_optimas, restaurar_datos_temporales, guardar_dato_temporal

logger = logging.getLogger(__name__)

class MesasArea(QFrame):
    # --- Lógica de selección múltiple y acciones por lotes ---
    def enable_batch_mode(self, enabled: bool):
        self.batch_mode = enabled
        for w in self.mesa_widgets:
            if hasattr(w, 'set_batch_mode'):
                w.set_batch_mode(enabled)
        self.selected_mesas = set()
        self.update_batch_action_btn()

    def toggle_mesa_selection(self, mesa_id):
        if not hasattr(self, 'selected_mesas'):
            self.selected_mesas = set()
        if mesa_id in self.selected_mesas:
            self.selected_mesas.remove(mesa_id)
        else:
            self.selected_mesas.add(mesa_id)
        self.update_batch_action_btn()

    def update_batch_action_btn(self):
        # Busca el botón de acción por lotes en el header y lo habilita/deshabilita
        # Solución: buscar el widget en el layout del header
        if hasattr(self, 'header'):
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
        if not hasattr(self, 'selected_mesas') or not self.selected_mesas:
            return
        self.filtered_mesas = [m for m in self.filtered_mesas if m.id not in self.selected_mesas]
        self.mesas = [m for m in self.mesas if m.id not in self.selected_mesas]
        self.selected_mesas = set()
        self.update_filtered_mesas()
        populate_grid(self)
        self.update_batch_action_btn()
    def toggle_view_mode(self):
        """Alterna entre vista grid y lista"""
        self.view_mode = "list" if self.view_mode == "grid" else "grid"
        # TODO: Implementar renderizado de vista lista si es necesario
        populate_grid(self)
    """Área de visualización y gestión de mesas (modularizado)"""
    nueva_mesa_requested = pyqtSignal()
    nueva_mesa_con_zona_requested = pyqtSignal(int, int, str)
    eliminar_mesa_requested = pyqtSignal(int)

    def __init__(self, tpv_service: Optional[TPVService] = None, parent=None):
        super().__init__(parent)
        self.tpv_service = tpv_service
        self.mesas: List[Mesa] = []
        self.filtered_mesas: List[Mesa] = []
        self.mesa_widgets: List[MesaWidget] = []
        self._datos_temporales = {}
        self.current_zone_filter = "Todas"
        self.current_status_filter = "Todos"
        self.view_mode = "grid"
        self._chips_refs = []  # Referencias a chips de filtro rápido
        self.setup_ui()




    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e0e6ed;
                border-radius: 12px;
                margin: 4px;
            }
        """)
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(16)
        # Header modularizado
        self.header = create_header(self, self, container_layout)
        # Área de scroll modularizada
        create_scroll_area(self, container_layout)

    def set_service(self, tpv_service: TPVService):
        self.tpv_service = tpv_service

    def set_mesas(self, mesas: List[Mesa], datos_temporales: Optional[Dict] = None):
        guardar_dato_temporal(self, None)  # Guarda temporales actuales
        if datos_temporales is not None:
            restaurar_datos_temporales(self, mesas)
        else:
            restaurar_datos_temporales(self, mesas)
        self.mesas = mesas
        self.sincronizar_reservas_en_mesas()
        self.update_filtered_mesas()
        populate_grid(self)
        update_stats_from_mesas(self)

    def set_reserva_service(self, reserva_service):
        self.reserva_service = reserva_service

    def refresh_mesas(self):
        if self.tpv_service:
            nuevas_mesas = self.tpv_service.get_mesas()
            guardar_dato_temporal(self, None)
            restaurar_datos_temporales(self, nuevas_mesas)
            self.mesas = nuevas_mesas
        # Sincronizar reservas activas y calcular próxima reserva
        self.sincronizar_reservas_en_mesas()
        self.update_filtered_mesas()
        populate_grid(self)

    def sincronizar_reservas_en_mesas(self):
        """Sincroniza reservas activas y calcula próxima reserva para cada mesa. SOLO modelo unificado."""
        if hasattr(self, 'reserva_service') and self.reserva_service:
            reservas_por_mesa = self.reserva_service.obtener_reservas_activas_por_mesa()
            from datetime import datetime, time
            ahora = datetime.now()
            for mesa in self.mesas:
                tiene_reservas = mesa.id in reservas_por_mesa
                reservas = reservas_por_mesa.get(mesa.id, [])
                # Determinar si hay una reserva en curso
                reserva_en_curso = None
                for r in reservas:
                    # Unificar fecha_hora para modelo unificado
                    fecha = getattr(r, 'fecha_reserva', None)
                    hora = getattr(r, 'hora_reserva', None)
                    if fecha and hora:
                        try:
                            if isinstance(hora, str):
                                hora_obj = datetime.strptime(hora, '%H:%M').time()
                            else:
                                hora_obj = hora
                        except Exception:
                            hora_obj = time(0, 0)
                        fecha_hora = datetime.combine(fecha, hora_obj)
                    elif fecha:
                        fecha_hora = datetime.combine(fecha, time(0, 0))
                    else:
                        fecha_hora = None
                    estado = getattr(r, 'estado', None)
                    if fecha_hora is not None and estado is not None and fecha_hora <= ahora and estado == 'activa':
                        reserva_en_curso = r
                        break
                if reserva_en_curso:
                    mesa.estado = 'ocupada'
                elif tiene_reservas:
                    mesa.estado = 'reservada'
                elif getattr(mesa, 'estado', None) in ('reservada', 'ocupada'):
                    mesa.estado = 'libre'
                # Calcular próxima reserva activa (>= ahora)
                futuras = []
                for r in reservas:
                    fecha = getattr(r, 'fecha_reserva', None)
                    hora = getattr(r, 'hora_reserva', None)
                    if fecha and hora:
                        try:
                            if isinstance(hora, str):
                                hora_obj = datetime.strptime(hora, '%H:%M').time()
                            else:
                                hora_obj = hora
                        except Exception:
                            hora_obj = time(0, 0)
                        fecha_hora = datetime.combine(fecha, hora_obj)
                    elif fecha:
                        fecha_hora = datetime.combine(fecha, time(0, 0))
                    else:
                        fecha_hora = None
                    estado = getattr(r, 'estado', None)
                    if fecha_hora is not None and estado is not None and fecha_hora >= ahora and estado == 'activa':
                        futuras.append((fecha_hora, r))
                if futuras:
                    # Elegir la reserva más próxima
                    mesa.proxima_reserva = min(futuras, key=lambda t: t[0])[1]
                else:
                    mesa.proxima_reserva = None
        # Eliminar vestigio legacy: _convert_reserva_legacy y referencias legacy eliminadas

    def _convert_reserva_legacy(self, r):
        """Convierte una reserva legacy (con fecha y hora separados) al modelo unificado."""
        # r.fecha y r.hora pueden no existir en el modelo unificado, así que usar fecha_reserva y hora_reserva
        from datetime import datetime
        fecha = getattr(r, 'fecha_reserva', None) or getattr(r, 'fecha', None)
        hora = getattr(r, 'hora_reserva', None) or getattr(r, 'hora', None)
        if fecha and hora:
            if isinstance(hora, str):
                try:
                    hora = datetime.strptime(hora, '%H:%M').time()
                except Exception:
                    hora = None
            fecha_hora = datetime.combine(fecha, hora) if hora else fecha
        else:
            fecha_hora = fecha or datetime.now()
        return type('Reserva', (), {
            'id': getattr(r, 'id', None),
            'mesa_id': getattr(r, 'mesa_id', None),
            'cliente_nombre': getattr(r, 'cliente_nombre', getattr(r, 'cliente', '')),
            'fecha_reserva': fecha,
            'hora_reserva': hora.strftime('%H:%M') if hora else '',
            'numero_personas': getattr(r, 'numero_personas', getattr(r, 'personas', 1)),
            'estado': getattr(r, 'estado', 'activa'),
            'notas': getattr(r, 'notas', ''),
            'cliente_telefono': getattr(r, 'cliente_telefono', getattr(r, 'telefono', ''))
        })()

    def update_filtered_mesas(self):
        if not self.mesas:
            self.filtered_mesas = []
            return
        if self.current_zone_filter and self.current_zone_filter != "Todas":
            mesas_zona = [m for m in self.mesas if m.zona == self.current_zone_filter]
        else:
            mesas_zona = self.mesas[:]
        if self.current_status_filter and self.current_status_filter != "Todos":
            mesas_estado = [m for m in mesas_zona if m.estado.lower() == self.current_status_filter.lower()]
        else:
            mesas_estado = mesas_zona
        search = self.search_input.text().strip().lower() if hasattr(self, 'search_input') else ""
        if search:
            self.filtered_mesas = [m for m in mesas_estado if search in str(m.numero).lower() or search in (m.zona or '').lower() or search in (m.alias or '').lower()]
        else:
            self.filtered_mesas = mesas_estado

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not hasattr(self, 'filtered_mesas') or not self.filtered_mesas:
            return
        if hasattr(self, '_resize_timer'):
            self._resize_timer.stop()
        from PyQt6.QtCore import QTimer
        self._resize_timer = QTimer()
        self._resize_timer.timeout.connect(lambda: populate_grid(self))
        self._resize_timer.setSingleShot(True)
        self._resize_timer.start(150)

    def _on_zone_changed(self, zone: str):
        self.current_zone_filter = zone
        self.update_filtered_mesas()
        populate_grid(self)

    def _on_status_changed(self, status: str):
        self.current_status_filter = status
        # Sincronizar chips rápidos
        if hasattr(self, '_chips_refs'):
            for chip in self._chips_refs:
                chip.setChecked(chip.text() == (status if status != "Todos" else "Todas"))
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
        if not nuevo_alias:
            if mesa.id in self._datos_temporales and 'alias' in self._datos_temporales[mesa.id]:
                del self._datos_temporales[mesa.id]['alias']
                if not self._datos_temporales[mesa.id]:
                    del self._datos_temporales[mesa.id]
        else:
            guardar_dato_temporal(self, mesa.id, alias=nuevo_alias)
        if self.tpv_service:
            self.tpv_service.cambiar_alias_mesa(mesa.id, nuevo_alias)
            for m in self.mesas:
                if m.id == mesa.id:
                    m.alias = nuevo_alias if nuevo_alias else None
            for w in self.mesa_widgets:
                if w.mesa.id == mesa.id:
                    w.update_mesa(m)
        self.update_filtered_mesas()
        from .mesas_area_grid import populate_grid
        populate_grid(self)

    def _on_personas_mesa_changed(self, mesa, nuevas_personas: int):
        from .mesas_area_utils import guardar_dato_temporal
        guardar_dato_temporal(self, mesa.id, personas=nuevas_personas)
        for m in self.mesas:
            if m.id == mesa.id:
                m.personas_temporal = nuevas_personas if nuevas_personas != m.capacidad else None
        for w in self.mesa_widgets:
            if w.mesa.id == mesa.id:
                w.update_mesa(m)
        self.update_filtered_mesas()
        from .mesas_area_grid import populate_grid
        populate_grid(self)

    def restaurar_estado_original_mesa(self, mesa_id: int):
        if mesa_id in self._datos_temporales:
            del self._datos_temporales[mesa_id]
        for m in self.mesas:
            if m.id == mesa_id:
                m.alias = None
                m.personas_temporal = None
        for w in self.mesa_widgets:
            if w.mesa.id == mesa_id:
                w.update_mesa(m)
        self.update_filtered_mesas()
        from .mesas_area_grid import populate_grid
        populate_grid(self)

    def _on_nueva_mesa_clicked(self):
        """Maneja el click del botón Nueva Mesa con selección de zona"""
        try:
            from PyQt6.QtWidgets import QInputDialog, QMessageBox
            # Obtener zonas disponibles (dinámicamente de las mesas existentes + opciones estándar)
            zonas_existentes = set(mesa.zona for mesa in self.mesas if mesa.zona)
            zonas_estandar = {"Terraza", "Interior", "Privada", "Barra", "Principal", "Salon"}
            zonas_disponibles = sorted(list(zonas_existentes.union(zonas_estandar)))
            # Mostrar diálogo de selección de zona
            zona_seleccionada, ok = QInputDialog.getItem(
                self,
                "Nueva Mesa",
                "Selecciona la zona donde crear la nueva mesa:",
                zonas_disponibles,
                0,
                False
            )
            if ok and zona_seleccionada:
                # Calcular el próximo número de mesa disponible
                numeros_existentes = []
                for mesa in self.mesas:
                    if str(mesa.numero).isdigit():
                        numeros_existentes.append(int(mesa.numero))
                siguiente_numero = max(numeros_existentes, default=0) + 1
                respuesta = QMessageBox.question(
                    self,
                    "Confirmar Nueva Mesa",
                    f"¿Crear nueva mesa con los siguientes datos?\n\n"
                    f"📍 Zona: {zona_seleccionada}\n"
                    f"🔢 Número: {siguiente_numero}\n"
                    f"👥 Capacidad: 4 personas\n\n"
                    f"Podrá modificar estos valores después de la creación.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes
                )
                if respuesta == QMessageBox.StandardButton.Yes:
                    self.nueva_mesa_con_zona_requested.emit(siguiente_numero, 4, zona_seleccionada)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al procesar la creación de mesa: {str(e)}")

    def _on_eliminar_mesa_clicked(self):
        """Maneja el click del botón Eliminar Mesa"""
        try:
            from PyQt6.QtWidgets import QInputDialog, QMessageBox
            if not self.mesas:
                QMessageBox.information(self, "Sin mesas", "No hay mesas disponibles para eliminar.")
                return
            opciones_mesas = []
            mesas_disponibles = []
            for mesa in self.mesas:
                if getattr(mesa, 'estado', None) == "libre":
                    texto_opcion = f"Mesa {mesa.numero} - {mesa.zona}"
                    opciones_mesas.append(texto_opcion)
                    mesas_disponibles.append(mesa)
            if not opciones_mesas:
                QMessageBox.information(
                    self,
                    "Sin mesas disponibles",
                    "No hay mesas libres disponibles para eliminar.\nSolo se pueden eliminar mesas que estén libres."
                )
                return
            opcion_seleccionada, ok = QInputDialog.getItem(
                self,
                "Eliminar Mesa",
                "Selecciona la mesa que deseas eliminar:",
                opciones_mesas,
                0,
                False
            )
            if ok and opcion_seleccionada:
                indice_seleccionado = opciones_mesas.index(opcion_seleccionada)
                mesa_a_eliminar = mesas_disponibles[indice_seleccionado]
                respuesta = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Estás seguro de que quieres eliminar la Mesa {mesa_a_eliminar.numero}?\nEsta acción no se puede deshacer.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if respuesta == QMessageBox.StandardButton.Yes:
                    self.eliminar_mesa_requested.emit(mesa_a_eliminar.id)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al procesar la eliminación de mesa: {str(e)}")

    def sync_scroll_with(self, other_scroll_area):
        """Sincroniza el scroll vertical de esta área con otra QScrollArea"""
        # Buscar el atributo scroll_area en self
        scroll_area = getattr(self, 'scroll_area', None)
        if not scroll_area or not hasattr(other_scroll_area, 'verticalScrollBar'):
            return
        self._syncing_scroll = False
        other_syncing = {'flag': False}
        def on_scroll(value):
            if self._syncing_scroll:
                return
            self._syncing_scroll = True
            other_scroll_area.verticalScrollBar().setValue(value)
            self._syncing_scroll = False
        def on_other_scroll(value):
            if other_syncing['flag']:
                return
            other_syncing['flag'] = True
            scroll_area.verticalScrollBar().setValue(value)
            other_syncing['flag'] = False
        scroll_area.verticalScrollBar().valueChanged.connect(on_scroll)
        other_scroll_area.verticalScrollBar().valueChanged.connect(on_other_scroll)

    def sync_reservas(self, reserva_service):
        self.set_reserva_service(reserva_service)
        self.refresh_mesas()
