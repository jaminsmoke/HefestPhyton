"""
Widget MesaWidget - Versión compacta y profesional con nombre editable
Diseño ultra-compacto con máxima legibilidad y organización profesional
NUEVA FEATURE: Nombre editable con doble-click (ID fijo)
Versión: v0.0.13
"""

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QFrame, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from services.tpv_service import Mesa


class MesaWidget(QFrame):
    """Widget compacto y profesional para mostrar una mesa con diseño optimizado y nombre editable"""
    # Señales
    mesa_clicked = pyqtSignal(Mesa)
    mesa_double_clicked = pyqtSignal(Mesa)
    alias_changed = pyqtSignal(Mesa, str)  # Señal para cambio de alias
    personas_changed = pyqtSignal(Mesa, int)  # Señal para cambio de personas
    restaurar_original = pyqtSignal(int)  # Señal para restaurar valores originales

    def __init__(self, mesa: Mesa, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.setFixedSize(220, 160)  # Tamaño más compacto ajustado al contenido
        self.setObjectName("mesa_widget")

        # Variables para edición de nombre
        self.editing_mode = False
        self.alias_line_edit = None  # Para el modo edición
        self.click_timer = QTimer()  # Para distinguir click simple vs doble click
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self._handle_single_click)
        self.pending_click = False

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        """Configura la interfaz ultra-compacta ajustada al contenido"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)  # Márgenes mínimos
        layout.setSpacing(2)  # Espaciado muy reducido

        # --- ALIAS DE MESA + BOTÓN DE EDICIÓN ---
        from PyQt6.QtWidgets import QHBoxLayout, QPushButton
        from PyQt6.QtGui import QIcon
        alias_layout = QHBoxLayout()
        alias_layout.setContentsMargins(0, 0, 0, 0)
        alias_layout.setSpacing(4)
        self.alias_label = QLabel(self.mesa.nombre_display)
        alias_layout.addWidget(self.alias_label, 1)
        self.edit_btn = QPushButton()
        self.edit_btn.setFixedSize(22, 22)
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setToolTip("Editar alias de mesa")
        # Icono de lápiz unicode o usa un icono si tienes recursos
        self.edit_btn.setText("✏️")
        self.edit_btn.setStyleSheet("border: none; background: transparent; font-size: 14px;")
        self.edit_btn.clicked.connect(self._start_edit_mode)
        alias_layout.addWidget(self.edit_btn, 0)

        # Botón contextual de restaurar (solo si hay cambios temporales)
        from PyQt6.QtWidgets import QSizePolicy
        self.restore_btn = QPushButton()
        self.restore_btn.setFixedSize(22, 22)
        self.restore_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restore_btn.setToolTip("Restaurar valores originales de la mesa")
        self.restore_btn.setText("↩️")
        self.restore_btn.setStyleSheet("border: none; background: transparent; font-size: 14px; color: #888;")
        self.restore_btn.setVisible(self._tiene_datos_temporales())
        self.restore_btn.clicked.connect(self._emitir_restaurar)
        self.restore_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
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
        self.edit_personas_btn.setStyleSheet("border: none; background: transparent; font-size: 13px;")
        self.edit_personas_btn.clicked.connect(self._editar_personas)
        capacidad_layout.addWidget(self.edit_personas_btn, 0)

        layout.addLayout(capacidad_layout)

        # ZONA + IDENTIFICADOR - Información contextual en una línea
        zona_texto = self.mesa.zona if hasattr(self.mesa, 'zona') and self.mesa.zona else "Principal"

        # El número de mesa ya incluye el identificador correcto (T03, I04, etc.)
        identificador = self.mesa.numero

        self.zona_label = QLabel(f"🏢 {zona_texto} • {identificador}")
        self.zona_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zona_label.setFont(QFont("Segoe UI", 9))
        self.zona_label.setObjectName("zona_label")
        layout.addWidget(self.zona_label)

    def get_estado_texto(self):
        """Obtiene el texto del estado de forma compacta"""
        estados = {
            'libre': '✓ LIBRE',
            'ocupada': '● OCUPADA',
            'reservada': '◐ RESERVADA',
            'pendiente': '◯ PENDIENTE'
        }
        return estados.get(self.mesa.estado, '? DESCONOCIDO')

    def get_colores(self):
        """Obtiene los colores según el estado"""
        colores = {
            'libre': {
                'fondo': '#f1f8e9',
                'borde': '#4caf50',
                'texto': '#2e7d32',
                'badge': '#4caf50'
            },
            'ocupada': {
                'fondo': '#ffebee',
                'borde': '#f44336',
                'texto': '#c62828',
                'badge': '#f44336'
            },
            'reservada': {
                'fondo': '#fff8e1',
                'borde': '#ff9800',
                'texto': '#ef6c00',
                'badge': '#ff9800'
            },
            'pendiente': {
                'fondo': '#f3e5f5',
                'borde': '#9c27b0',
                'texto': '#7b1fa2',
                'badge': '#9c27b0'
            }
        }
        return colores.get(self.mesa.estado, colores['libre'])

    def apply_styles(self):
        """Aplica estilos ultra-compactos ajustados al contenido"""
        colores = self.get_colores()

        # Estilo principal del widget - Compacto y ajustado
        self.setStyleSheet(f"""
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
        """)

        # Alias de mesa - Prominente pero compacto
        self.alias_label.setStyleSheet(f"""
            QLabel#alias_label {{
                color: {colores['texto']};
                font-weight: bold;
                background-color: transparent;
                border: none;
                padding: 1px;
                margin: 0px;
                min-height: 24px;
            }}
        """)

        # Estado - Badge ultra-compacto centrado perfectamente
        self.estado_label.setStyleSheet(f"""
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
        """)

        # Capacidad - Información ajustada
        self.capacidad_label.setStyleSheet(f"""
            QLabel#capacidad_label {{
                color: {colores['texto']};
                font-weight: 500;
                background-color: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 4px;
                padding: 2px 6px;
                min-height: 18px;
                margin: 1px 0px;
            }}
        """)

        # Zona + Identificador - Información contextual compacta
        self.zona_label.setStyleSheet(f"""
            QLabel#zona_label {{
                color: #555555;
                font-weight: 500;
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 4px;
                padding: 2px 8px;
                min-height: 16px;
                margin: 0px;
            }}
        """)

    def _darken_color(self, color_hex):
        """Oscurece un color hex para efectos"""
        color_map = {
            '#4caf50': '#388e3c',
            '#f44336': '#d32f2f',
            '#ff9800': '#f57c00',
            '#9c27b0': '#7b1fa2',
        }
        return color_map.get(color_hex, color_hex)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._ajustar_fuente_nombre()

    def _ajustar_fuente_nombre(self):
        """Ajusta el tamaño de fuente del nombre para que quepa en el espacio disponible, con elipsis si es necesario"""
        label = self.alias_label
        text = label.text()
        if not text:
            return
        # Usar el ancho real del label (menos el botón)
        label_width = label.width() or (self.width() - 50)
        max_width = max(label_width, 60)  # Nunca menos de 60px
        min_font = 7
        max_font = 22
        font = QFont("Segoe UI", max_font, QFont.Weight.Bold)
        label.setFont(font)
        metrics = label.fontMetrics()
        while metrics.horizontalAdvance(text) > max_width and font.pointSize() > min_font:
            font.setPointSize(font.pointSize() - 1)
            label.setFont(font)
            metrics = label.fontMetrics()
        # Si aún no cabe, poner elipsis
        if metrics.horizontalAdvance(text) > max_width:
            elided = metrics.elidedText(text, Qt.TextElideMode.ElideRight, max_width)
            label.setText(elided)
        else:
            label.setText(text)
        # Si está en modo edición, también ajustar el QLineEdit
        if self.editing_mode and self.alias_line_edit:
            self.alias_line_edit.setFont(font)

    def _tiene_datos_temporales(self):
        """Devuelve True si hay alias o capacidad temporal activa"""
        return bool(self.mesa.alias) or (self.mesa.personas_temporal is not None)

    def update_mesa(self, mesa: Mesa):
        """Actualiza los datos de la mesa"""
        self.mesa = mesa
        self.alias_label.setText(mesa.nombre_display)
        self._ajustar_fuente_nombre()
        self.capacidad_label.setText(f"👥 {mesa.personas_display} personas")
        self.estado_label.setText(self.get_estado_texto())
        zona_texto = mesa.zona if hasattr(mesa, 'zona') and mesa.zona else "Principal"
        identificador = mesa.numero
        self.zona_label.setText(f"🏢 {zona_texto} • {identificador}")
        self.restore_btn.setVisible(self._tiene_datos_temporales())
        self.apply_styles()

    def _emitir_restaurar(self):
        """Emite una señal para restaurar la mesa a su estado original"""
        self.restaurar_original.emit(self.mesa.id)

    def _handle_single_click(self):
        """Maneja el click simple después de verificar que no hay doble click"""
        if self.pending_click:
            self.pending_click = False
            self.mesa_clicked.emit(self.mesa)

    def _start_edit_mode(self):
        """Inicia el modo de edición del alias de la mesa"""
        if self.editing_mode:
            return
        self.editing_mode = True
        self.alias_label.hide()
        self.alias_line_edit = QLineEdit(self.mesa.alias or "", self)
        self.alias_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alias_line_edit.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.alias_line_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #2196f3;
                border-radius: 8px;
                padding: 4px 8px;
                background: #f5faff;
                color: #1f2937;
            }
        """)
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
        self.alias_changed.emit(self.mesa, nuevo_alias)
        # ACTUALIZAR EL OBJETO LOCAL PARA REFLEJAR EL CAMBIO INMEDIATO
        self.mesa.alias = nuevo_alias if nuevo_alias else None
        self.alias_label.setText(self.mesa.nombre_display)
        self.alias_label.show()
        self.alias_line_edit.hide()
        self.alias_line_edit.deleteLater()
        self.alias_line_edit = None
        self.editing_mode = False
        self._ajustar_fuente_nombre()

    def mousePressEvent(self, event):
        """Maneja click simple con delay para distinguir de doble click"""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.editing_mode:
                # Si estamos editando, salir del modo edición
                self._finish_edit_mode()
            else:
                # Iniciar timer para click simple
                self.pending_click = True
                self.click_timer.start(300)  # 300ms de delay
        super().mousePressEvent(event)

    # Eliminar eventFilter: ya no es necesario
    def eventFilter(self, obj, event):
        return super().eventFilter(obj, event)

    # Eliminar lógica de doble click para edición
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mesa_double_clicked.emit(self.mesa)
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        """Maneja eventos de teclado"""
        if self.editing_mode and event.key() == Qt.Key.Key_Escape:
            # Cancelar edición con Escape
            if self.alias_line_edit:
                self.alias_line_edit.setText(self.mesa.nombre_display)
                self._finish_edit_mode()
        super().keyPressEvent(event)

    def _editar_personas(self):
        """Permite editar temporalmente el número de personas de la mesa con UX moderna y visual profesional"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QSpacerItem, QSizePolicy
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont, QIcon
        valor_actual = self.mesa.personas_display
        valor_original = self.mesa.capacidad
        min_val, max_val = 1, 500
        nombre_display = self.mesa.nombre_display

        class PersonasDialog(QDialog):
            def __init__(self, nombre_display, valor_actual, valor_original, parent=None):
                super().__init__(parent)
                self.setWindowTitle("Editar número de personas")
                self.setModal(True)
                self.setMinimumWidth(360)
                self.setStyleSheet("""
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
                """)
                layout = QVBoxLayout(self)
                layout.setContentsMargins(18, 18, 18, 12)
                layout.setSpacing(8)
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
                layout.addItem(QSpacerItem(10, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
                # Botones
                btns = QHBoxLayout()
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
                self.spin.setValue(self.valor_original)

        dlg = PersonasDialog(nombre_display, valor_actual, valor_original, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            nuevo_valor = dlg.spin.value()
            # Si el valor es igual al original, se interpreta como reset (eliminar temporal)
            if nuevo_valor == valor_original:
                self.personas_changed.emit(self.mesa, valor_original)
                self.capacidad_label.setText(f"👥 {valor_original} personas")
            else:
                self.personas_changed.emit(self.mesa, nuevo_valor)
                self.capacidad_label.setText(f"👥 {nuevo_valor} personas")
            self._feedback_visual_label(self.capacidad_label)

    def _feedback_visual_label(self, label):
        """Animación simple de parpadeo para feedback visual"""
        from PyQt6.QtCore import QPropertyAnimation
        anim = QPropertyAnimation(label, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(1.0)
        anim.setKeyValueAt(0.5, 0.3)
        anim.setEndValue(1.0)
        anim.start()
        # Guardar referencia para evitar que el GC lo elimine antes de tiempo
        self._last_anim = anim
