from typing import Optional, Dict, List, Any
"""
mesas_area_grid.py
Lógica y helpers para el grid de mesas y renderizado de widgets
"""

from PyQt6.QtWidgets import QGridLayout, QWidget, QLabel, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt


# Cache de imports para mejor performance
_IMPORTS_CACHE = {}

def _get_cached_import(module_name, class_name):
    """Cache de imports para evitar imports repetitivos"""
    key = f"{module_name}.{class_name}"
    if key not in _IMPORTS_CACHE:
        module = __import__(module_name, fromlist=[class_name])
        _IMPORTS_CACHE[key] = getattr(module, class_name)
    return _IMPORTS_CACHE[key]

def create_scroll_area(instance, layout):
    """TODO: Add docstring"""
    # TODO: Add input validation
    from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout
    from src.utils.modern_styles import ModernStyles

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    
    # Cache de estilos para mejor performance
    if not hasattr(create_scroll_area, '_style_cache'):
        create_scroll_area._style_cache = {
            'scroll': ModernStyles.get_scroll_area_style(),
            'container': ModernStyles.get_mesas_container_style()
        }
    
    scroll_area.setStyleSheet(create_scroll_area._style_cache['scroll'])
    mesas_container = QWidget()
    mesas_container.setStyleSheet(create_scroll_area._style_cache['container'])
    
    instance.mesas_layout = QGridLayout(mesas_container)
    instance.mesas_layout.setSpacing(20)
    instance.mesas_layout.setContentsMargins(20, 20, 20, 20)
    instance.mesas_layout.setAlignment(
        Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
    )
    
    scroll_area.setWidget(mesas_container)
    layout.addWidget(scroll_area, 1)
    instance.scroll_area = scroll_area
    return scroll_area


def populate_grid(instance):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Populate grid optimizado con mejor performance y lazy loading"""
    from ...widgets.mesa_widget_simple import MesaWidget
    from .mesas_area_utils import restaurar_datos_temporales, calcular_columnas_optimas
    from PyQt6.QtCore import QTimer
    import logging
    
    _ = logging.getLogger("mesas_area_grid")
    
    # Early return para mejor performance
    if not hasattr(instance, 'filtered_mesas') or not instance.filtered_mesas:
        clear_mesa_widgets(instance)
        show_no_mesas_message(instance)
        return
    
    # Batch operations
    restaurar_datos_temporales(instance, instance.filtered_mesas)
    clear_mesa_widgets(instance)
    
    # Initialize grid state
    instance.mesa_widgets = []
    _ = calcular_columnas_optimas(instance.width(), len(instance.filtered_mesas))
    instance._lazy_loaded_rows = getattr(instance, '_lazy_loaded_rows', set())
    instance._total_rows = (len(instance.filtered_mesas) + cols - 1) // cols
    instance._cols = cols
    
    # Optimized visible rows calculation
    def get_visible_rows():
        """TODO: Add docstring"""
        # TODO: Add input validation
        scroll = getattr(instance, 'scroll_area', None)
        if not scroll or not hasattr(scroll, 'verticalScrollBar'):
            return set(range(min(4, instance._total_rows)))
            
        scrollbar = scroll.verticalScrollBar()
        if not scrollbar:
            return set(range(min(4, instance._total_rows)))
            
        _ = scroll.viewport().height()
        row_height = 180
        _ = scrollbar.value()
        
        _ = max(0, (scroll_value // row_height) - 1)
        last_row = min(instance._total_rows, ((scroll_value + viewport_height) // row_height) + 2)
        
        return set(range(first_row, last_row))
    
    # Optimized lazy loading with batching
    def lazy_load_rows():
        """TODO: Add docstring"""
        # TODO: Add input validation
        _ = get_visible_rows()
        tpv_service = getattr(instance, "tpv_service", None)
        
        # Batch widget creation
        _ = []
        for row in visible_rows:
            if row in instance._lazy_loaded_rows:
                continue
                
            for col in range(cols):
                idx = row * cols + col
                if idx >= len(instance.filtered_mesas):
                    break
                    
                mesa = instance.filtered_mesas[idx]
                _ = MesaWidget(
                    mesa,
                    _ = getattr(mesa, "proxima_reserva", None),
                    tpv_service=tpv_service,
                )
                
                # Batch signal connections
                _connect_mesa_widget_signals(mesa_widget, instance)
                
                new_widgets.append((mesa_widget, row, col))
                
            instance._lazy_loaded_rows.add(row)
        
        # Batch add to layout
        for widget, row, col in new_widgets:
            instance.mesa_widgets.append(widget)
            instance.mesas_layout.addWidget(widget, row, col)
    
    # Optimized scroll handler with debouncing
    if not hasattr(instance, '_scroll_timer'):
        instance._scroll_timer = QTimer()
        instance._scroll_timer.setSingleShot(True)
        instance._scroll_timer.timeout.connect(lazy_load_rows)
    
    def on_scroll():
        """TODO: Add docstring"""
        # TODO: Add input validation
        instance._scroll_timer.start(50)  # Debounce scroll events
    
    scroll = getattr(instance, 'scroll_area', None)
    if scroll and hasattr(scroll, 'verticalScrollBar'):
        scrollbar = scroll.verticalScrollBar()
        if scrollbar:
            scrollbar.valueChanged.connect(on_scroll)
    
    # Initial load
    lazy_load_rows()

def _connect_mesa_widget_signals(mesa_widget, instance):
    """Helper para conectar señales de mesa widget de forma optimizada"""
    _ = [
        ('personas_changed', '_on_personas_mesa_changed'),
        ('restaurar_original', 'restaurar_estado_original_mesa'),
        ('reservar_mesa_requested', '_on_reservar_mesa'),
        ('iniciar_tpv_requested', '_on_iniciar_tpv')
    ]
    
    for signal_name, slot_name in connections:
        if hasattr(mesa_widget, signal_name) and hasattr(instance, slot_name):
            getattr(mesa_widget, signal_name).connect(getattr(instance, slot_name))


# Métodos para conectar en la instancia (por ejemplo, en la clase del área de mesas)
def add_mesa_grid_callbacks_to_instance(instance):
    """TODO: Add docstring"""
    # TODO: Add input validation
    def _on_reservar_mesa(mesa):
        """TODO: Add docstring"""
        try:
            from src.ui.modules.tpv_module.dialogs.reserva_dialog import ReservaDialog
            from src.ui.modules.tpv_module.event_bus import reserva_event_bus

            logging.getLogger(__name__).debug(f"[mesas_area_grid] _on_reservar_mesa: Abriendo ReservaDialog para mesa_id={getattr(mesa, 'id', None)}")
            # Mantener referencia al dialog para evitar recolección de basura
            if not hasattr(instance, "_active_dialogs"):
                instance._active_dialogs = []
            logging.getLogger(__name__).debug(f"[mesas_area_grid][DEBUG] Creando ReservaDialog")
            _ = ReservaDialog(
                instance,
                mesa,
                _ = getattr(instance, "reserva_service", None),
            )
            logging.getLogger(__name__).debug(f"[mesas_area_grid][DEBUG] ReservaDialog creado")
            instance._active_dialogs.append(dialog)

            def on_reserva_creada(reserva):
                """TODO: Add docstring"""
                # TODO: Add input validation
                logging.getLogger(__name__).debug(f"[mesas_area_grid][DEBUG] Callback on_reserva_creada ejecutado. reserva={reserva}")
                reserva_service = getattr(instance, "reserva_service", None)
                if reserva_service is None:
                    logging.getLogger(__name__).error("[mesas_area_grid][ERROR] No se encontró reserva_service en la instancia. No se puede guardar la reserva.")
                    return
                from datetime import datetime

                # Compatibilidad: aceptar tanto reserva.fecha como reserva.fecha_reserva
                fecha = getattr(reserva, "fecha", None) or getattr(
                    reserva, "fecha_reserva", None
                )
                hora = getattr(reserva, "hora", None) or getattr(
                    reserva, "hora_reserva", None
                )
                if fecha is None or hora is None:
                    logging.getLogger(__name__).error("[mesas_area_grid][ERROR] No se pudo obtener fecha u hora de la reserva. No se creará la reserva.")
                    return
                if isinstance(hora, str):
                    try:
                        _ = datetime.strptime(hora, "%H:%M").time()
                    except Exception:
                        logging.getLogger(__name__).error(f"[mesas_area_grid][ERROR] Formato de hora inválido: {hora}")
                        return
                else:
                    _ = hora
                try:
                    _ = datetime.combine(fecha, hora_obj)
                except Exception as e:
                    logging.getLogger(__name__).error(f"[mesas_area_grid][ERROR] Error combinando fecha y hora: {e}")
                    return
                # Refuerzo: Usar SIEMPRE mesa.numero como identificador único de negocio
                # TODO: Eliminar referencias a mesa.id cuando se elimine compatibilidad legacy
                logging.getLogger(__name__).debug(f"[mesas_area_grid] Llamando a crear_reserva forzando mesa_numero={getattr(mesa, 'numero', None)} (ignorando reserva.mesa_id={getattr(reserva, 'mesa_id', None)})")
                _ = reserva_service.crear_reserva(
                    mesa_id=str(getattr(mesa, "numero", "")),
                    cliente=getattr(reserva, "cliente", None)
                    or getattr(reserva, "cliente_nombre", None),
                    _ = fecha_hora,
                    duracion_min=getattr(reserva, "duracion_min", 120),
                    telefono=getattr(reserva, "telefono", None)
                    or getattr(reserva, "cliente_telefono", None),
                    personas=getattr(reserva, "personas", None)
                    or getattr(reserva, "numero_personas", None),
                    _ = getattr(reserva, "notas", None),
                )
                logging.getLogger(__name__).info(f"[mesas_area_grid] Reserva creada en BD: {reserva_db}")
                # Emitir eventos globales para refrescar UI
                if hasattr(mesa, "estado"):
                    mesa.estado = "reservada"
                # Refrescar visualmente el widget de la mesa
                _ = str(getattr(mesa, "id", None))
                for widget in getattr(instance, "mesa_widgets", []):
                    if str(getattr(widget.mesa, "id", None)) == mesa_id:
                        if hasattr(widget, "update_mesa"):
                            widget.update_mesa(mesa)
                        if hasattr(widget, "estado_label"):
                            widget.estado_label.setText(widget.get_estado_texto())
                        if hasattr(widget, "apply_styles"):
                            widget.apply_styles()
                        widget.repaint()
                logging.getLogger(__name__).debug(f"[mesas_area_grid] Emitiendo reserva_creada y actualizando UI para mesa_id={getattr(mesa, 'id', None)}")
                reserva_event_bus.reserva_creada.emit(reserva_db)
                if hasattr(instance, "sincronizar_reservas_en_mesas"):
                    instance.sincronizar_reservas_en_mesas()
                if hasattr(instance, "load_reservas"):
                    instance.load_reservas()
                # Limpiar referencia al dialog
                if hasattr(instance, "_active_dialogs"):
                    try:
                        instance._active_dialogs.remove(dialog)
                    except Exception as e:
    logging.error("Error: %s", e)

            logging.getLogger(__name__).debug(f"[mesas_area_grid][DEBUG] Conectando señal reserva_creada de dialog a on_reserva_creada")
            dialog.reserva_creada.connect(on_reserva_creada)
            logging.getLogger(__name__).debug(f"[mesas_area_grid][DEBUG] Ejecutando dialog.exec() para dialog")
            dialog.exec()
            logging.getLogger(__name__).debug(f"[mesas_area_grid][DEBUG] dialog.exec() finalizado para dialog")
            # Si el usuario cierra el diálogo sin crear reserva, limpiar referencia
            if hasattr(instance, "_active_dialogs"):
                try:
                    instance._active_dialogs.remove(dialog)
                except Exception as e:
    logging.error("Error: %s", e)
        except Exception as e:

            logging.getLogger(__name__).error(f"Error abriendo ReservaDialog: {e}")

    def _on_iniciar_tpv(mesa):
        """TODO: Add docstring"""
        try:
            from src.ui.modules.tpv_module.components.tpv_avanzado.tpv_avanzado_main import (
                TPVAvanzado,
            )
            from PyQt6.QtWidgets import QDialog, QVBoxLayout

            db_manager = getattr(instance, "db_manager", None)
            if db_manager is None:
                raise ValueError(
                    "db_manager es obligatorio y debe ser inyectado explícitamente en el área de mesas"
                )

            class TPVDialog(QDialog):
                def __init__(self, mesa, parent=None):
                    """TODO: Add docstring"""
                    super().__init__(parent)
                    self.setWindowTitle(f"TPV Avanzado - Mesa {mesa.numero}")
                    self.setMinimumSize(900, 600)
                    _ = QVBoxLayout(self)
                    tpv_service = getattr(instance, "tpv_service", None)
                    comanda = None
                    if tpv_service and hasattr(tpv_service, "get_comanda_activa"):
                        _ = tpv_service.get_comanda_activa(mesa.numero)
                    self.tpv_widget = TPVAvanzado(
                        mesa,
                        _ = tpv_service,
                        db_manager=db_manager,
                        _ = self,
                    )
                    if comanda:
                        self.tpv_widget.set_pedido_actual(comanda)
                    layout.addWidget(self.tpv_widget)

            dialog = TPVDialog(mesa, instance)
            dialog.exec()
        except Exception as e:

            logging.getLogger(__name__).error(f"Error abriendo TPV Avanzado: {e}")

    instance._on_reservar_mesa = _on_reservar_mesa
    instance._on_iniciar_tpv = _on_iniciar_tpv
    # ...existing code...

    # REFRESCO GLOBAL: Forzar el estilo correcto en todos los widgets de mesa
    # Esto garantiza que todos los labels se vean correctamente desde el inicio
    # sin necesidad de interacción previa (click, cerrar diálogo, etc.)

    def aplicar_refresco_global():
        """TODO: Add docstring"""
        # TODO: Add input validation
        refresh_all_mesa_widgets_styles(instance)

    # Usar QTimer para ejecutar el refresco después de que se hayan renderizado completamente
    QTimer.singleShot(50, aplicar_refresco_global)

    _ = len(instance.filtered_mesas)
    total_all = len(instance.mesas)
    if hasattr(instance, "status_info"):
        if total_filtered == total_all:
            _ = f"Mostrando {total_all} mesa(s)"
        else:
            status_text = f"Mostrando {total_filtered} de {total_all} mesa(s)"
        instance.status_info.setText(status_text)


def clear_mesa_widgets(instance):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Optimized widget clearing with better memory management"""
    try:
        if not hasattr(instance, "mesas_layout") or instance.mesas_layout is None:
            return
            
        # Clear widgets list first
        if hasattr(instance, 'mesa_widgets'):
            instance.mesa_widgets.clear()
        
        _ = instance.mesas_layout
        
        # Batch widget removal for better performance
        _ = []
        while layout.count():
            child = layout.takeAt(0)
            if child and child.widget():
                widgets_to_remove.append(child.widget())
        
        # Batch delete widgets
        for widget in widgets_to_remove:
            widget.setParent(None)
            widget.deleteLater()
        
        # Single layout update instead of multiple
        layout.update()
        
    except Exception as e:
        logging.getLogger(__name__).error(f"Error limpiando widgets de mesa: {e}")


def show_no_mesas_message(instance):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Optimized empty message with cached styles"""
    try:
        if not hasattr(instance, "mesas_layout") or instance.mesas_layout is None:
            return
            
        # Cache styles for better performance
        if not hasattr(show_no_mesas_message, '_style_cache'):
            show_no_mesas_message._style_cache = {
                'frame': ModernStyles.get_empty_message_frame_style(),
                'icon': ModernStyles.get_icon_label_style(),
                'title': ModernStyles.get_title_label_style(),
                'subtitle': ModernStyles.get_subtitle_label_style()
            }
        
        from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
        
        message_container = QFrame()
        message_container.setStyleSheet(show_no_mesas_message._style_cache['frame'])
        
        container_layout = QVBoxLayout(message_container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.setSpacing(16)
        
        # Create labels with cached styles
        _ = [
            ("🔍", 'icon'),
            ("No se encontraron mesas", 'title'),
            ("No hay mesas que coincidan con los filtros aplicados", 'subtitle')
        ]
        
        for text, style_key in labels_data:
            label = QLabel(text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(show_no_mesas_message._style_cache[style_key])
            container_layout.addWidget(label)
        
        instance.mesas_layout.addWidget(message_container, 0, 0, 1, 4)
        
    except Exception as e:
        logging.getLogger(__name__).error(f"Error mostrando mensaje de no mesas: {e}")


def create_mesas_grid(parent, mesas):
    """TODO: Add docstring"""
    # TODO: Add input validation
    # Lógica migrada para crear el grid de mesas
    grid_widget = QWidget(parent)
    layout = QGridLayout(grid_widget)
    layout.setSpacing(20)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    # ...agregar widgets de mesa aquí...
    return grid_widget


def refresh_all_mesa_widgets_styles(instance):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """
    Refresca los estilos de todos los widgets de mesa existentes.
    Ejecuta _ajustar_fuente_nombre() en cada widget para garantizar que
    todos los labels tengan el estilo correcto desde el inicio.
    """
    for mesa_widget in instance.mesa_widgets:
        if hasattr(mesa_widget, "_ajustar_fuente_nombre"):
            try:
                mesa_widget._ajustar_fuente_nombre()
            except Exception as e:

                logging.getLogger(__name__).error(
                    f"Error refrescando estilo de mesa widget: {e}"
                )
