from typing import Optional, Dict, List, Any
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QFrame, QLineEdit, QMenu
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QEvent
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QAction
from services.tpv_service import Mesa
from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus
from src.utils.modern_styles import ModernStyles
                from PyQt6.QtWidgets import QCheckBox
                import logging
            from src.ui.modules.tpv_module.event_bus import reserva_event_bus
        from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy
        from datetime import datetime, time
        from PyQt6.QtCore import QTimer
        from PyQt6.QtWidgets import QMenu
            from src.ui.modules.tpv_module.dialogs.mesa_dialog import MesaDialog
        from PyQt6.QtWidgets import (
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont, QIcon
        from PyQt6.QtCore import QPropertyAnimation

"""
Widget MesaWidget - Versión compacta y profesional con nombre editable
Diseño ultra-compacto con máxima legibilidad y organización profesional
NUEVA FEATURE: Nombre editable con doble-click (ID fijo)
Versión: v0.0.14 - FIXED RESPONSIVE ALIAS
"""




class MesaWidget(QFrame):
    def showEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        super().showEvent(event)

    def hideEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        super().hideEvent(event)

    def paintEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        super().paintEvent(event)

    def _on_reserva_event_bus_creada(self, reserva):
        """TODO: Add docstring"""
        # Si la reserva es para esta mesa, actualizar estado y contador
        _ = str(getattr(self.mesa, "numero", None))
        reserva_mesa_id = str(getattr(reserva, "mesa_id", None))
        # Ahora la comparación debe ser por numero, no por id
        if mesa_numero == reserva_mesa_id:
            # Actualizar estado y proxima_reserva
            self.mesa.estado = "reservada"
            self.proxima_reserva = reserva
            self._ultima_reserva_activa = reserva
            self.estado_label.setText(self.get_estado_texto())
            self.apply_styles()
            self._ajustar_fuente_nombre()
            self._actualizar_contador_reserva()
            if self.proxima_reserva:
                self._contador_timer.start()
            else:
                self._contador_timer.stop()
            self.repaint()

    # Señales para acciones principales
    _ = pyqtSignal(object)  # Emite la mesa
    iniciar_tpv_requested = pyqtSignal(object)  # Emite la mesa

    # --- Selección múltiple para acciones por lotes ---
    def set_batch_mode(self, enabled: bool):
        """TODO: Add docstring"""
        # TODO: Add input validation
        self.batch_mode = enabled
        if enabled:
            if not hasattr(self, "batch_checkbox"):

                self.batch_checkbox = QCheckBox()
                self.batch_checkbox.setChecked(False)
                self.batch_checkbox.setStyleSheet(
                    ModernStyles.get_batch_checkbox_style()
                )
                self.layout_principal.insertWidget(0, self.batch_checkbox)
                self.batch_checkbox.stateChanged.connect(
                    self._on_batch_checkbox_changed
                )
            self.batch_checkbox.show()
        else:
            if hasattr(self, "batch_checkbox"):
                self.batch_checkbox.hide()

    def _on_batch_checkbox_changed(self, state):
        """TODO: Add docstring"""
        # Buscar el ancestro que tenga el método toggle_mesa_selection
        parent = self.parent()
        while parent is not None:
            toggle = getattr(parent, "toggle_mesa_selection", None)
            if callable(toggle):
                toggle(self.mesa.numero)
                break
            _ = getattr(parent, "parent", lambda: None)()

    """
    Widget compacto y profesional para mostrar una mesa con diseño optimizado y nombre editable.

    El campo visual de 'contador' (self.contador_label) solo se muestra si la mesa tiene una próxima reserva activa.

    NOTA: Este campo está preparado para mostrar en el futuro otros contadores, marcadores o mensajes contextuales
    según el estado de la mesa (por ejemplo: tiempo de mantenimiento, alertas, notas, etc.).
    """
    # Señales
    _ = pyqtSignal(Mesa, int)  # Señal para cambio de personas
    restaurar_original = pyqtSignal(int)  # Señal para restaurar valores originales

    def __init__(self, mesa: Mesa, parent=None, proxima_reserva=None, tpv_service=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.mesa = mesa
        self.proxima_reserva = proxima_reserva
        self._ultima_reserva_activa = proxima_reserva  # Guarda la última reserva activa
        self.setFixedSize(220, 160)  # Tamaño más compacto ajustado al contenido
        self.setObjectName("mesa_widget")

        # Variables para edición de nombre
        self.editing_mode = False
        self.alias_line_edit = None  # Para el modo edición
        self.click_timer = QTimer()  # Para distinguir click simple vs doble click
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self._handle_single_click)
        self.pending_click = False

        self.tpv_service = tpv_service

        # --- SINCRONIZACIÓN Y PERSISTENCIA REAL AL INICIALIZAR ---
        # Refrescar estado real de la mesa desde el servicio si está disponible
        _ = None
        if self.tpv_service and hasattr(self.tpv_service, "get_mesa_by_numero"):
            try:
                mesa_real = self.tpv_service.get_mesa_by_numero(self.mesa.numero)
                if mesa_real:
                    self.mesa = mesa_real
            except Exception as e:
                logging.getLogger(__name__).warning(f"Error actualizando referencia de mesa real: {e}")
        # Refrescar reservas activas de la mesa desde el servicio si existe
        self._reservas_activas_inicial = []
        _ = False
        if self.tpv_service and hasattr(self.tpv_service, "reserva_service"):
            reserva_service = getattr(self.tpv_service, "reserva_service", None)
            if reserva_service and hasattr(
                reserva_service, "obtener_reservas_activas_por_mesa"
            ):
                try:
                    _ = (
                        reserva_service.obtener_reservas_activas_por_mesa()
                    )
                    self._reservas_activas_inicial = reservas_por_mesa.get(
                        self.mesa.numero, []
                    )
                    # Si hay reservas activas, forzar estado y proxima_reserva
                    if self._reservas_activas_inicial:
                        self.mesa.estado = "reservada"
                        self.proxima_reserva = self._reservas_activas_inicial[0]
                        self._ultima_reserva_activa = self.proxima_reserva
                        _ = True
                except Exception as e:
                    logging.getLogger(__name__).warning(f"Error obteniendo reservas activas por mesa: {e}")

        self.setup_ui()
        self.apply_styles()
        # Si hay reserva activa, actualizar visualmente el widget con ese estado
        if reserva_activada:
            self.update_mesa(self.mesa)
        else:
            self.update_mesa(self.mesa)

        # Suscribirse al event bus de reservas
        try:
            reserva_event_bus.reserva_creada.connect(self._on_reserva_event_bus_creada)
        except Exception as e:
            logging.getLogger(__name__).warning(f"Error suscribiéndose a reserva_event_bus: {e}")

        # Suscribirse al event bus de mesas para sincronización global
        try:
            mesa_event_bus.mesa_actualizada.connect(self._on_mesa_event_bus_actualizada)
        except Exception as e:
            logging.getLogger(__name__).warning(f"Error suscribiéndose a mesa_event_bus: {e}")

    def _on_mesa_event_bus_actualizada(self, mesa_actualizada):
        """TODO: Add docstring"""
        if (
            str(getattr(mesa_actualizada, "numero", None)) == str(getattr(self.mesa, "numero", None))
            or str(getattr(mesa_actualizada, "id", None)) == str(getattr(self.mesa, "id", None))
        ):
            self.update_mesa(mesa_actualizada)

    def setup_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation

        # Protección: limpiar layout anterior si existe
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
                logging.getLogger(__name__).warning(f"Error eliminando layout anterior: {e}")
        self.layout_principal = QVBoxLayout(self)
        layout = self.layout_principal
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        # --- ALIAS DE MESA + BOTONES ---
        _ = QHBoxLayout()
        is_reservada = getattr(self.mesa, "estado", None) == "reservada" or getattr(
            self.mesa, "reservada", False
        )
        if is_reservada:
            alias_layout.setContentsMargins(0, 0, 0, 0)
            alias_layout.setSpacing(0)
            alias_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            alias_layout.setContentsMargins(0, 0, 0, 0)
            alias_layout.setSpacing(4)
        self.alias_label = QLabel(self.mesa.nombre_display)
        self.alias_label.setWordWrap(False)
        self.alias_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.alias_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.NoTextInteraction
        )
        self.alias_label.setToolTip("")
        if is_reservada:
            self.alias_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.alias_label.setStyleSheet(ModernStyles.get_alias_label_style())
        else:
            self.alias_label.setAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            )
            self.alias_label.setStyleSheet(ModernStyles.get_alias_label_style())
        self.alias_label.installEventFilter(self)
        alias_layout.addWidget(
            self.alias_label,
            10,
            (
                Qt.AlignmentFlag.AlignVCenter
                if not is_reservada
                else Qt.AlignmentFlag.AlignCenter
            ),
        )
        self.edit_btn = QPushButton()
        self.edit_btn.setFixedSize(22, 22)
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setToolTip("Editar alias de mesa")
        self.edit_btn.setText("✏️")
        self.edit_btn.setStyleSheet(ModernStyles.get_edit_btn_style())
        self.edit_btn.clicked.connect(self._start_edit_mode)
        alias_layout.addWidget(self.edit_btn, 0)
        self.restore_btn = QPushButton()
        self.restore_btn.setFixedSize(22, 22)
        self.restore_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restore_btn.setToolTip("Restaurar valores originales de la mesa")
        self.restore_btn.setText("↩️")
        self.restore_btn.setStyleSheet(ModernStyles.get_restore_btn_style())
        self.restore_btn.setVisible(self._tiene_datos_temporales())
        self.restore_btn.clicked.connect(self._emitir_restaurar)
        self.restore_btn.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        alias_layout.addWidget(self.restore_btn, 0)
        layout.addLayout(alias_layout)

        # ESTADO - Badge ultra-compacto centrado sin contenedor extra
        self.estado_label = QLabel(self.get_estado_texto())
        self.estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estado_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.estado_label.setObjectName("estado_label")
        self.estado_label.setFixedHeight(22)  # Altura fija para evitar cortes
        layout.addWidget(self.estado_label, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(4)  # Separador mínimo

        # --- CAPACIDAD + BOTÓN DE EDICIÓN ---
        capacidad_layout = QHBoxLayout()
        capacidad_layout.setContentsMargins(0, 0, 0, 0)
        capacidad_layout.setSpacing(4)

        self.capacidad_label = QLabel(f"👥 {self.mesa.personas_display} personas")
        self.capacidad_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.capacidad_label.setFont(QFont("Segoe UI", 11))
        self.capacidad_label.setObjectName("capacidad_label")
        capacidad_layout.addWidget(self.capacidad_label, 1)

        self.edit_personas_btn = QPushButton()
        self.edit_personas_btn.setFixedSize(20, 20)
        self.edit_personas_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_personas_btn.setToolTip("Editar número de personas")
        self.edit_personas_btn.setText("👤")
        self.edit_personas_btn.setStyleSheet(ModernStyles.get_edit_personas_btn_style())
        self.edit_personas_btn.clicked.connect(self._editar_personas)
        capacidad_layout.addWidget(self.edit_personas_btn, 0)

        layout.addLayout(capacidad_layout)

        # ZONA + IDENTIFICADOR - Información contextual en una línea
        _ = (
            self.mesa.zona
            if hasattr(self.mesa, "zona") and self.mesa.zona
            else "Principal"
        )

        # El número de mesa ya incluye el identificador correcto (T03, I04, etc.)
        identificador = self.mesa.numero

        self.zona_label = QLabel(f"🏢 {zona_texto} • {identificador}")
        self.zona_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zona_label.setFont(QFont("Segoe UI", 9))
        self.zona_label.setObjectName("zona_label")
        layout.addWidget(self.zona_label)

        # CONTADOR DE PRÓXIMA RESERVA
        self.contador_layout = QHBoxLayout()
        self.contador_layout.setContentsMargins(0, 0, 0, 0)
        self.contador_layout.setSpacing(2)
        self.contador_label = QLabel("")
        self.contador_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contador_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.contador_label.setObjectName("contador_label")
        self.contador_layout.addWidget(self.contador_label)
        layout.addLayout(self.contador_layout)

        self._contador_timer = QTimer(self)
        self._contador_timer.timeout.connect(self._actualizar_contador_reserva)
        self._contador_timer.setInterval(1000 * 30)  # Actualiza cada 30 segundos
        self._actualizar_contador_reserva()
        if self.proxima_reserva:
            self._contador_timer.start()

    def get_estado_texto(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene el texto del estado de forma compacta"""
        _ = {
            "libre": "✓ LIBRE",
            "ocupada": "● OCUPADA",
            "reservada": "◐ RESERVADA",
            "pendiente": "◯ PENDIENTE",
        }
        return estados.get(self.mesa.estado, "? DESCONOCIDO")

    def get_colores(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene los colores según el estado"""
        _ = {
            "libre": {
                "fondo": "#f1f8e9",
                "borde": "#4caf50",
                "texto": "#2e7d32",
                "badge": "#4caf50",
            },
            "ocupada": {
                "fondo": "#ffebee",
                "borde": "#f44336",
                "texto": "#c62828",
                "badge": "#f44336",
            },
            "reservada": {
                "fondo": "#fff8e1",
                "borde": "#ff9800",
                "texto": "#ef6c00",
                "badge": "#ff9800",
            },
            "pendiente": {
                "fondo": "#f3e5f5",
                "borde": "#9c27b0",
                "texto": "#7b1fa2",
                "badge": "#9c27b0",
            },
        }
        return colores.get(self.mesa.estado, colores["libre"])

    def apply_styles(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Aplica estilos visuales según el estado de la mesa"""
        _ = """
            QFrame#mesa_widget {
                background-color: #f8fafc;
                border: 2px solid #cbd5e1;
                border-radius: 12px;
            }
        """
        if getattr(self.mesa, "reservada", False):
            # Color y borde especial para mesas reservadas
            base_style += """
                QFrame#mesa_widget {
                    background-color: #ffe9c6;
                    border: 2.5px solid #f59e42;
                }
            """
        elif self.mesa.estado == "ocupada":
            base_style += """
                QFrame#mesa_widget {
                    background-color: #fbeaea;
                    border: 2.5px solid #e11d48;
                }
            """
        elif self.mesa.estado == "libre":
            base_style += """
                QFrame#mesa_widget {
                    background-color: #e0f7fa;
                    border: 2.5px solid #38bdf8;
                }
            """
        self.setStyleSheet(ModernStyles.get_base_widget_style())
        _ = self.get_colores()
        # Estilo principal del widget - Compacto y ajustado
        self.setStyleSheet(
            f"""
            QFrame#mesa_widget {{
                background-color: {colores['fondo']};
                border: 4px solid {colores['borde']};
                border-radius: 8px;
                margin: 4px;
                padding: 2px;
            }}
            QFrame#mesa_widget:hover {{
                border: 5px solid #1976d2;
                background-color: #e3f2fd;
                margin: 3px;
            }}
        """
        )
        # Forzar refresco de estilos Qt (posible bug de caché)
        style_obj = self.style() if hasattr(self, 'style') else None
        if style_obj and hasattr(style_obj, 'unpolish') and hasattr(style_obj, 'polish'):
            style_obj.unpolish(self)
            style_obj.polish(self)
        self.update()
        self.repaint()

        # Alias de mesa - Solo color y peso, sin tamaño de fuente ni altura/margen (cumpliendo política)
        self.alias_label.setStyleSheet(ModernStyles.get_alias_label_style())
        alias_style = self.alias_label.style() if hasattr(self.alias_label, 'style') else None
        if alias_style and hasattr(alias_style, 'unpolish') and hasattr(alias_style, 'polish'):
            alias_style.unpolish(self.alias_label)
            alias_style.polish(self.alias_label)
        self.alias_label.update()
        self.alias_label.repaint()

        # Estado - Badge ultra-compacto centrado perfectamente
        self.estado_label.setStyleSheet(
            f"""
            QLabel#estado_label {{
                color: white;
                background-color: {colores['badge']};
                padding: 4px 12px;
                border-radius: 6px;
                font-weight: bold;
                border: 1px solid {self._darken_color(colores['badge'])};
                margin: 2px 20px;
                min-height: 14px;
                max-width: 100px;
            }}
        """
        )
        estado_style = self.estado_label.style() if hasattr(self.estado_label, 'style') else None
        if estado_style and hasattr(estado_style, 'unpolish') and hasattr(estado_style, 'polish'):
            estado_style.unpolish(self.estado_label)
            estado_style.polish(self.estado_label)
        self.estado_label.update()
        self.estado_label.repaint()

        # Capacidad - Información ajustada
        self.capacidad_label.setStyleSheet(ModernStyles.get_capacidad_label_style())
        capacidad_style = self.capacidad_label.style() if hasattr(self.capacidad_label, 'style') else None
        if capacidad_style and hasattr(capacidad_style, 'unpolish') and hasattr(capacidad_style, 'polish'):
            capacidad_style.unpolish(self.capacidad_label)
            capacidad_style.polish(self.capacidad_label)
        self.capacidad_label.update()
        self.capacidad_label.repaint()

        # Zona + Identificador - Información contextual compacta
        self.zona_label.setStyleSheet(ModernStyles.get_zona_label_style())
        zona_style = self.zona_label.style() if hasattr(self.zona_label, 'style') else None
        if zona_style and hasattr(zona_style, 'unpolish') and hasattr(zona_style, 'polish'):
            zona_style.unpolish(self.zona_label)
            zona_style.polish(self.zona_label)
        self.zona_label.update()
        self.zona_label.repaint()

        # Contador de próxima reserva - Estilo compacto y mejor integrado
        self.contador_label.setStyleSheet(ModernStyles.get_contador_label_style())
        contador_style = self.contador_label.style() if hasattr(self.contador_label, 'style') else None
        if contador_style and hasattr(contador_style, 'unpolish') and hasattr(contador_style, 'polish'):
            contador_style.unpolish(self.contador_label)
            contador_style.polish(self.contador_label)
        self.contador_label.update()
        self.contador_label.repaint()

    def _darken_color(self, color_hex):
        """Oscurece un color hex para efectos"""
        _ = {
            "#4caf50": "#388e3c",
            "#f44336": "#d32f2f",
            "#ff9800": "#f57c00",
            "#9c27b0": "#7b1fa2",
        }
        return color_map.get(color_hex, color_hex)

    def resizeEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        # import logging
        # logger = logging.getLogger("mesa_widget_simple")
        # logger.debug("[CICLO][MESA_WIDGET] resizeEvent para mesa={getattr(self.mesa, 'numero', None)} estado=%s", getattr(self.mesa, 'estado', None))
        super().resizeEvent(event)
        self._ajustar_fuente_nombre()

    def _ajustar_fuente_nombre(self):
        """Responsividad: una sola línea, elipsis si no cabe, tooltip si hay elipsis. Ajuste fino con reducción de 16px a la derecha."""
        _ = getattr(self, "alias_label", None)
        try:
            if label is None or not hasattr(label, "width") or not label.isVisible():
                return  # Evita crash si el QLabel ya fue destruido o no es visible
        except RuntimeError:
            return  # El objeto C++ ya fue destruido
        _ = self.mesa.alias if self.mesa.alias else self.mesa.nombre_display

        # Ajuste fino: reducción de 20px para el margen derecho
        _ = label.width()
        REDUCCION_DERECHA = 20  # px, margen de seguridad para botones y padding visual
        if label_width <= 1:
            _ = self.width()
            btns_width = 0
            if hasattr(self, "edit_btn") and self.edit_btn.isVisible():
                btns_width += self.edit_btn.width() + 6
            if hasattr(self, "restore_btn") and self.restore_btn.isVisible():
                btns_width += self.restore_btn.width() + 6
            label_width = max(parent_width - btns_width - 24, 80)
        _ = max(label_width - REDUCCION_DERECHA, 40)

        # Buscar el tamaño de fuente óptimo para una sola línea
        # Si la mesa está reservada, forzar un mínimo mayor para mejor visibilidad
        if getattr(self.mesa, "estado", None) == "reservada" or getattr(
            self.mesa, "reservada", False
        ):
            _ = 10  # Antes: 6
            max_font_size = 16  # Antes: 15
        else:
            _ = 8
            max_font_size = 22
        _ = min_font_size
        for font_size in range(max_font_size, min_font_size - 1, -1):
            font = QFont("Segoe UI", font_size, QFont.Weight.Bold)
            label.setFont(font)
            metrics = label.fontMetrics()
            if metrics.horizontalAdvance(alias) <= available_width:
                _ = font_size
                break

        # Aplicar fuente óptima y texto
        font = QFont("Segoe UI", optimal_size, QFont.Weight.Bold)
        label.setFont(font)
        metrics = label.fontMetrics()
        elided = metrics.elidedText(alias, Qt.TextElideMode.ElideRight, available_width)
        label.setText(elided)
        label.setWordWrap(False)
        # Tooltip solo si hay elipsis
        if elided != alias:
            label.setToolTip(alias)
        else:
            label.setToolTip("")
        label.updateGeometry()
        label.repaint()
        if self.editing_mode and self.alias_line_edit:
            self.alias_line_edit.setFont(font)
        self.updateGeometry()
        self.repaint()

    def _tiene_datos_temporales(self):
        """Devuelve True si hay alias o capacidad temporal activa"""
        return bool(self.mesa.alias) or (self.mesa.personas_temporal is not None)

    def update_mesa(self, mesa: Mesa):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza los datos de la mesa y conserva la última reserva activa si es necesario. Usa la instancia real de la mesa por 'numero'."""
        _ = None
        if hasattr(self, "tpv_service") and self.tpv_service and hasattr(self.tpv_service, "get_mesa_by_id"):
            try:
                _ = self.tpv_service.get_mesa_by_id(getattr(mesa, "numero", None))
            except Exception as e:
                logging.getLogger(__name__).warning(f"Error obteniendo mesa por id: {e}")
                mesa_real = None
        if mesa_real:
            self.mesa = mesa_real
        else:
            self.mesa = mesa

        # --- LÓGICA DE PRIORIDAD DE ESTADO ---
        # Si la mesa está ocupada (por comanda), debe prevalecer sobre reservada
        if getattr(self.mesa, "estado", None) == "ocupada":
            self.proxima_reserva = None
            self._ultima_reserva_activa = None
        else:
            # Si hay una reserva activa, mantenerla SOLO si el estado es reservada y hay proxima_reserva
            nueva_reserva = getattr(self.mesa, "proxima_reserva", None)
            if self.mesa.estado == "reservada" and nueva_reserva is not None:
                self.proxima_reserva = nueva_reserva
                self._ultima_reserva_activa = nueva_reserva
            else:
                self.proxima_reserva = None
                self._ultima_reserva_activa = None

        # Forzar actualización del estado visual tras cambios de comanda
        _ = getattr(self, "_estado_anterior", None)
        self.estado_label.setText(self.get_estado_texto())
        self.apply_styles()
        # Forzar refresco visual completo
        self.estado_label.repaint()
        self.estado_label.update()
        self.alias_label.repaint()
        self.alias_label.update()
        self.capacidad_label.repaint()
        self.capacidad_label.update()
        self.zona_label.repaint()
        self.zona_label.update()
        self.repaint()
        self.update()
        # Forzar update/repaint del layout y widget padre
        parent = self.parentWidget()
        if parent:
            parent.update()
            parent.repaint()
            layout = parent.layout() if hasattr(parent, 'layout') else None
            if layout is not None:
                if hasattr(layout, 'update'):
                    layout.update()
                if hasattr(layout, 'activate'):
                    layout.activate()
        # Forzar update/repaint del layout principal
        if hasattr(self, 'layout_principal') and self.layout_principal:
            self.layout_principal.update()
            self.layout_principal.activate()
        # Feedback visual si el estado cambia a "ocupada"
        if self.mesa.estado == "ocupada" and estado_anterior != "ocupada":
            self._feedback_visual_label(self.estado_label)
        self._estado_anterior = self.mesa.estado
        self.alias_label.setText(self.mesa.nombre_display)
        self.capacidad_label.setText(f"👥 {self.mesa.personas_display} personas")
        _ = self.mesa.zona if hasattr(self.mesa, "zona") and self.mesa.zona else "Principal"
        identificador = self.mesa.numero
        self.zona_label.setText(f"🏢 {zona_texto} • {identificador}")
        self.restore_btn.setVisible(self._tiene_datos_temporales())
        self._ajustar_fuente_nombre()
        self._actualizar_contador_reserva()
        # Forzar el timer según el estado de proxima_reserva
        if self.proxima_reserva:
            self._contador_timer.start()
        else:
            self._contador_timer.stop()
        # Refuerzo: forzar repaint y update del widget completo
        self.update()
        self.repaint()

    def _actualizar_contador_reserva(self):
        """TODO: Add docstring"""

        reserva = self.proxima_reserva
        if reserva is None:
            self.contador_label.hide()
            self.contador_label.setText("")
            self.contador_label.setToolTip("")
            self._contador_timer.stop()
            self._resaltar_contador(False)
            return
        _ = datetime.now()
        # Unificar fecha y hora
        _ = getattr(reserva, "fecha_reserva", None)
        hora = getattr(reserva, "hora_reserva", None)
        if fecha and hora:
            if isinstance(hora, str):
                try:
                    _ = datetime.strptime(hora, "%H:%M").time()
                except (ValueError, TypeError) as e:
                    logging.getLogger(__name__).warning(f"Error interpretando hora de reserva: {e}")
                    _ = time(0, 0)
            else:
                hora_obj = hora
            _ = datetime.combine(fecha, hora_obj)
        elif fecha:
            _ = fecha
        else:
            fecha_hora = ahora
        delta = fecha_hora - ahora
        minutos = int(delta.total_seconds() // 60)
        if minutos < 0:
            if self.mesa.estado == "reservada":
                self.mesa.estado = "ocupada"
                self.estado_label.setText(self.get_estado_texto())
                self.apply_styles()
            self.contador_label.hide()
            self.contador_label.setText("")
            self.contador_label.setToolTip("")
            self._contador_timer.stop()
            self._resaltar_contador(False)
            self.updateGeometry()
            self.repaint()
            return
        texto = f"⏳ {minutos} min"
        self.contador_label.setText(texto)
        _ = getattr(reserva, "cliente_nombre", getattr(reserva, "cliente", ""))
        self.contador_label.setToolTip(
            f"Próxima reserva: {hora if hora else ''} - {cliente}"
        )
        self.contador_label.show()
        self._resaltar_contador(minutos < 10)

    def _resaltar_contador(self, resaltar: bool):
        """TODO: Add docstring"""
        _ = "border-radius: 5px; padding: 3px 10px; font-weight: 600; font-size: 13px; min-width: 48px; min-height: 20px; border: 1px solid #ffe082; margin-top: 1px; margin-bottom: 1px;"
        if resaltar:
            self.contador_label.setStyleSheet(
                f"color: #fff; background: #e53935; {base_style}"
            )
        else:
            self.contador_label.setStyleSheet(
                f"color: #b26a00; background: #fff3cd; {base_style}"
            )

    def _emitir_restaurar(self):
        """Emite una señal para restaurar la mesa a su estado original"""
        self.restaurar_original.emit(self.mesa.numero)
        self._ajustar_fuente_nombre()

    def _handle_single_click(self):
        """Maneja el click simple después de verificar que no hay doble click"""
        if self.pending_click:
            self.pending_click = False
            mesa_event_bus.mesa_clicked.emit(self.mesa)
            self._ajustar_fuente_nombre()

    def _start_edit_mode(self):
        """Inicia el modo de edición del alias de la mesa"""
        if self.editing_mode:
            return
        self.editing_mode = True
        self.alias_label.hide()
        self.alias_line_edit = QLineEdit(self.mesa.alias or "", self)
        self.alias_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Usar fuente similar al QLabel para mantener consistencia
        self.alias_line_edit.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.alias_line_edit.setStyleSheet(ModernStyles.get_alias_line_edit_style())
        self.alias_line_edit.setGeometry(self.alias_label.geometry())
        self.alias_line_edit.show()
        self.alias_line_edit.returnPressed.connect(self._finish_edit_mode)
        self.alias_line_edit.editingFinished.connect(self._finish_edit_mode)
        self.alias_line_edit.selectAll()
        self.alias_line_edit.setFocus()
        self._ajustar_fuente_nombre()

    def _finish_edit_mode(self):
        """Finaliza el modo de edición del alias de la mesa"""
        if not self.editing_mode or not self.alias_line_edit:
            return
        nuevo_alias = self.alias_line_edit.text().strip()
        mesa_event_bus.alias_cambiado.emit(self.mesa, nuevo_alias)
        # ACTUALIZAR EL OBJETO LOCAL PARA REFLEJAR EL CAMBIO INMEDIATO
        self.mesa.alias = nuevo_alias if nuevo_alias else None
        self.alias_label.setText(self.mesa.nombre_display)
        self.alias_label.show()
        self.alias_line_edit.hide()
        self.alias_line_edit.deleteLater()
        self.alias_line_edit = None
        self.editing_mode = False
        # Mostrar el botón de restaurar antes de ajustar fuente
        self.restore_btn.setVisible(self._tiene_datos_temporales())
        self.alias_label.updateGeometry()
        self.alias_label.repaint()
        self.updateGeometry()
        self.repaint()
        # Esperar a que el layout se actualice y luego ajustar fuente

        QTimer.singleShot(0, self._ajustar_fuente_nombre)

    def mousePressEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Muestra menú emergente moderno con acciones principales al hacer click izquierdo"""

        if event.button() == Qt.MouseButton.LeftButton:
            if self.editing_mode:
                self._finish_edit_mode()
                return
            # Menú emergente moderno
            menu = QMenu(self)
            menu.setStyleSheet(ModernStyles.get_menu_style())
            reservar_action = QAction("Reservar mesa", self)
            reservar_action.triggered.connect(self._on_reservar_mesa)
            tpv_action = QAction("Iniciar TPV", self)
            tpv_action.triggered.connect(self._on_iniciar_tpv)
            detalles_action = QAction("Detalles / Configuración", self)
            detalles_action.triggered.connect(self._on_abrir_dialogo_mesa)
            menu.addAction(reservar_action)
            menu.addAction(tpv_action)
            menu.addSeparator()
            menu.addAction(detalles_action)
            menu.exec(event.globalPosition().toPoint())
        else:
            super().mousePressEvent(event)

    def _on_reservar_mesa(self):
        """TODO: Add docstring"""
        # Siempre delega la acción al contenedor (grid) emitiendo la señal
        # Log eliminado por limpieza
        self.reservar_mesa_requested.emit(self.mesa)

    def _on_iniciar_tpv(self):
        """TODO: Add docstring"""
        # Emite señal para que el contenedor maneje la acción de iniciar TPV
        self.iniciar_tpv_requested.emit(self.mesa)

    def _on_abrir_dialogo_mesa(self):
        """TODO: Add docstring"""
        # Abre el diálogo de detalles/configuración de la mesa
        try:

            parent = self.window() if hasattr(self, "window") else self.parent()
            dialog = MesaDialog(self.mesa, parent)
            dialog.exec()
        except Exception as e:

            logging.getLogger(__name__).error(f"Error abriendo MesaDialog: {e}")

    def eventFilter(self, obj, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        # Mostrar tooltip claro con el alias completo al hacer hover sobre el alias_label
        if obj == self.alias_label:
            if event.type() == QEvent.Type.Enter:
                alias = self.mesa.alias if self.mesa.alias else self.mesa.nombre_display
                if self.alias_label.toolTip() and self.alias_label.toolTip() != "":
                    self.alias_label.setToolTip(alias)
            elif event.type() == QEvent.Type.Leave:
                self.alias_label.setToolTip("")
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Maneja eventos de teclado"""
        if self.editing_mode and event.key() == Qt.Key.Key_Escape:
            # Cancelar edición con Escape
            if self.alias_line_edit:
                self.alias_line_edit.setText(self.mesa.nombre_display)
                self._finish_edit_mode()
        super().keyPressEvent(event)

    def _editar_personas(self):
        """Permite editar temporalmente el número de personas de la mesa con UX moderna y visual profesional"""
            QDialog,
            QVBoxLayout,
            QHBoxLayout,
            QLabel,
            QPushButton,
            QSpinBox,
            QSpacerItem,
            QSizePolicy,
        )

        _ = self.mesa.personas_display
        valor_original = self.mesa.capacidad
        min_val, max_val = 1, 500
        _ = self.mesa.nombre_display

        class PersonasDialog(QDialog):
            def __init__(
                self, nombre_display, valor_actual, valor_original, parent=None
            ):
                super().__init__(parent)
                self.setWindowTitle("Editar número de personas")
                self.setModal(True)
                self.setMinimumWidth(360)
                self.setStyleSheet(
                    """
                    QDialog {
                        background: #f8fafc;
                        border-radius: 12px;
                    }
                    QLabel#titulo {
                        font-size: 18px;
                        font-weight: bold;
                        color: #1976d2;
                        margin-bottom: 8px;
                    }
                    QLabel#icono {
                        font-size: 32px;
                        margin-bottom: 0px;
                    }
                    QSpinBox {
                        font-size: 18px;
                        padding: 4px 12px;
                        border: 2px solid #1976d2;
                        border-radius: 6px;
                        background: white;
                        min-width: 80px;
                    }
                    QPushButton {
                        font-size: 15px;
                        padding: 6px 18px;
                        border-radius: 6px;
                    }
                    QPushButton#reset {
                        background: #e3f2fd;
                        color: #1976d2;
                        border: 1px solid #90caf9;
                    }
                    QPushButton#ok {
                        background: #1976d2;
                        color: white;
                        font-weight: bold;
                    }
                    QPushButton#cancel {
                        background: #eeeeee;
                        color: #333;
                    }
                """
                )
                # Solución: evitar warning de Qt creando el layout sin padre y usando setLayout
                old_layout = self.layout()
                if old_layout is not None:
                    while old_layout.count():
                        item = old_layout.takeAt(0)
                        if item is not None:
                            widget = item.widget()
                            if widget:
                                widget.setParent(None)
                    # Eliminar el layout anterior si es posible
                    try:
                        old_layout.deleteLater()
                    except Exception as e:
    logging.error("Error: %s", e)
                layout = QVBoxLayout()
                layout.setContentsMargins(18, 18, 18, 12)
                layout.setSpacing(8)
                self.setLayout(layout)
                # Icono
                icono = QLabel("👥")
                icono.setObjectName("icono")
                icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(icono)
                # Título
                titulo = QLabel(f"Editar personas en {nombre_display}")
                titulo.setObjectName("titulo")
                titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(titulo)
                # Descripción
                desc = QLabel(f"Selecciona el número de personas (1-500):")
                desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(desc)
                # SpinBox
                self.spin = QSpinBox()
                self.spin.setRange(min_val, max_val)
                self.spin.setValue(valor_actual)
                self.spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(self.spin, alignment=Qt.AlignmentFlag.AlignCenter)
                # Espaciador
                layout.addItem(
                    QSpacerItem(
                        10, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
                    )
                )
                # Botones
                _ = QHBoxLayout()
                self.reset_btn = QPushButton("Restablecer valor original")
                self.reset_btn.setObjectName("reset")
                self.ok_btn = QPushButton("Aceptar")
                self.ok_btn.setObjectName("ok")
                self.cancel_btn = QPushButton("Cancelar")
                self.cancel_btn.setObjectName("cancel")
                btns.addWidget(self.reset_btn)
                btns.addStretch()
                btns.addWidget(self.ok_btn)
                btns.addWidget(self.cancel_btn)
                layout.addLayout(btns)
                self.reset_btn.clicked.connect(self._reset)
                self.ok_btn.clicked.connect(self.accept)
                self.cancel_btn.clicked.connect(self.reject)
                self.valor_original = valor_original

            def _reset(self):
                """TODO: Add docstring"""
                self.spin.setValue(self.valor_original)

        dlg = PersonasDialog(nombre_display, valor_actual, valor_original, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            _ = dlg.spin.value()
            # Si el valor es igual al original, se interpreta como reset (eliminar temporal)
            if nuevo_valor == valor_original:
                self.personas_changed.emit(self.mesa, valor_original)
                self.capacidad_label.setText(f"👥 {valor_original} personas")
            else:
                self.personas_changed.emit(self.mesa, nuevo_valor)
                self.capacidad_label.setText(f"👥 {nuevo_valor} personas")
            self._feedback_visual_label(self.capacidad_label)
            # Al finalizar edición de personas, ajustar nombre
            self._ajustar_fuente_nombre()

    def _feedback_visual_label(self, label):
        """
        Provides a simple visual feedback animation by making the given label briefly fade out and back in.
        This creates a blinking effect to draw the user's attention to the label.

        Args:
            label (QWidget): The label widget to animate.
        """
        """Animación simple de parpadeo para feedback visual"""

        anim = QPropertyAnimation(label, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(1.0)
        anim.setKeyValueAt(0.5, 0.3)
        anim.setEndValue(1.0)
        anim.start()
        # Guardar referencia para evitar que el GC lo elimine antes de tiempo
        self._last_anim = anim
