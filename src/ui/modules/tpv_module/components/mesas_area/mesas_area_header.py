from .mesas_area_stats import create_subcontenedor_metric_cards
from typing import Any
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, Qt
from data.db_manager import DatabaseManager
from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

"""
mesas_area_header.py
Componentes de header, filtros y estadísticas para MesasArea
"""


from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)


def create_title_section_ultra_premium():
    section = QFrame()
    section.setObjectName("TitleSectionUltraPremium")
    section.setFixedSize(260, 75)
    section.setStyleSheet(
        """
        QFrame#TitleSectionUltraPremium {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff,
                stop:0.3 #fafbfc,
                stop:0.7 #f6f8fa,
                stop:1 #f1f4f8);
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            margin: 3px;                padding: 2px;
        }
        QFrame#TitleSectionUltraPremium:hover {
            border: 2px solid #cbd5e1;
        }        """
    )
    layout = QHBoxLayout(section)
    layout.setContentsMargins(12, 6, 12, 6)
    layout.setSpacing(10)
    icon_container = QFrame()
    icon_container.setFixedSize(52, 52)
    icon_container.setStyleSheet(
        """
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #5b21b6,
                stop:0.3 #4c1d95,
                stop:0.7 #3730a3,
                stop:1 #312e81);
            border: 2px solid #1e1b4b;
            border-radius: 26px;
        }
    """
    )
    # Refuerzo: limpiar layout anterior de icon_container
    old_icon_layout = icon_container.layout()
    if old_icon_layout is not None:
        while old_icon_layout.count():
            item = old_icon_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
        try:
            old_icon_layout.deleteLater()
        except Exception as e:
            import logging

            logging.getLogger(__name__).warning(
                f"Error eliminando layout anterior de icon_container: {e}"
            )
    icon_layout = QVBoxLayout()
    icon_layout.setContentsMargins(0, 0, 0, 0)
    icon_container.setLayout(icon_layout)
    icon_label = QLabel("🍽️")
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    icon_label.setStyleSheet(
        """
        QLabel {
            font-size: 20px;
            color: white;
            background: transparent;
            border: none;
        }        """
    )
    icon_layout.addWidget(icon_label)
    layout.addWidget(icon_container)
    # Refuerzo: crear text_container como QWidget y asignar layout
    from PyQt6.QtWidgets import QWidget

    text_widget = QWidget()
    text_layout = QVBoxLayout()
    text_layout.setSpacing(1)
    text_layout.setContentsMargins(0, 0, 0, 0)
    text_widget.setLayout(text_layout)
    title_label = QLabel("GESTIÓN DE MESAS")
    title_label.setStyleSheet(
        """
        QLabel {
            font-size: 14px;
            font-weight: bold;
            color: #1e293b;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            letter-spacing: 0.3px;
            margin: 0px;
            padding: 0px;
            line-height: 1.1;
        }
    """
    )
    text_layout.addWidget(title_label)
    subtitle_label = QLabel("Terminal Punto de Venta")
    subtitle_label.setStyleSheet(
        """
        QLabel {
            font-size: 11px;
            color: #64748b;
            font-weight: 500;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            margin: 0px;
            padding: 0px;
            line-height: 1.0;
        }
    """
    )
    text_layout.addWidget(subtitle_label)
    text_layout.addStretch()
    status_label = QLabel("● Sistema Activo")
    status_label.setStyleSheet(
        """
        QLabel {
            font-size: 10px;
            color: #16a34a;
            font-weight: bold;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            margin: 0px;
            padding: 0px;
            line-height: 1.0;
        }
    """
    )
    text_layout.addWidget(status_label)
    layout.addWidget(text_widget)
    layout.addStretch()
    return section


def create_ultra_premium_separator():
    sep = QFrame()
    sep.setFixedWidth(0)
    sep.setStyleSheet("background: transparent; border: none;")
    return sep


from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt


# --- NUEVA CLASE SOLO UI MODERNA DE CHIPS ---
class FiltersSectionUltraPremium(QFrame):
    def editar_zona(self) -> None:
        from PyQt6.QtWidgets import QMessageBox, QInputDialog

        zonas_db = [z for z in self.db.get_zonas() if z["nombre"] != "Todas"]
        if not zonas_db:
            QMessageBox.information(self, "Editar zona", "No hay zonas para editar.")
            return
        zonas_nombres = [z["nombre"] for z in zonas_db]
        zona_a_editar, ok = QInputDialog.getItem(
            self, "Editar zona", "Selecciona la zona a editar:", zonas_nombres, 0, False
        )
        if not (ok and zona_a_editar):
            return
        zona_obj = next((z for z in zonas_db if z["nombre"] == zona_a_editar), None)
        if not zona_obj:
            QMessageBox.critical(
                self, "Error", "No se encontró la zona en la base de datos."
            )
            return
        nuevo_nombre, ok2 = QInputDialog.getText(
            self, "Nuevo nombre", f"Nuevo nombre para la zona '{zona_a_editar}':"
        )
        if not (ok2 and nuevo_nombre):
            return
        nuevo_nombre = nuevo_nombre.strip()
        if not nuevo_nombre:
            QMessageBox.warning(
                self, "Nombre inválido", "El nombre de la zona no puede estar vacío."
            )
            return
        if any(z["nombre"] == nuevo_nombre for z in zonas_db):
            QMessageBox.warning(
                self, "Duplicado", f"Ya existe una zona con el nombre '{nuevo_nombre}'."
            )
            return
        try:
            self.db.update_zona_nombre(zona_obj["id"], nuevo_nombre)
            mesa_event_bus.zonas_actualizadas.emit(self.db.get_zonas())
            QMessageBox.information(
                self,
                "Zona editada",
                f"Zona '{zona_a_editar}' renombrada a '{nuevo_nombre}' correctamente.",
            )
        except Exception as e:
            import logging

            logging.getLogger(__name__).error(f"No se pudo editar la zona: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo editar la zona: {e}")

    def eliminar_zona(self) -> None:
        from PyQt6.QtWidgets import QMessageBox, QInputDialog

        zonas_db = [z for z in self.db.get_zonas()]
        zonas_nombres = [z["nombre"] for z in zonas_db if z["nombre"] != "Todas"]
        if not zonas_nombres:
            QMessageBox.information(
                self, "Eliminar zona", "No hay zonas para eliminar."
            )
            return
        zona_a_eliminar, ok = QInputDialog.getItem(
            self,
            "Eliminar zona",
            "Selecciona la zona a eliminar:",
            zonas_nombres,
            0,
            False,
        )
        if ok and zona_a_eliminar:
            # Verificar si hay mesas asociadas a la zona
            mesas_asociadas = False
            if hasattr(self.instance, "mesas"):
                mesas_asociadas = any(
                    getattr(m, "zona", None) == zona_a_eliminar
                    for m in getattr(self.instance, "mesas", [])
                )
            if mesas_asociadas:
                QMessageBox.warning(
                    self,
                    "No permitido",
                    f"No se puede eliminar la zona '{zona_a_eliminar}' porque tiene mesas asociadas.",
                )
                return
            zona_obj = next(
                (z for z in zonas_db if z["nombre"] == zona_a_eliminar), None
            )
            if not zona_obj:
                QMessageBox.critical(
                    self, "Error", "No se encontró la zona en la base de datos."
                )
                return
            confirm = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar la zona '{zona_a_eliminar}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    self.db.delete_zona(zona_obj["id"])
                    mesa_event_bus.zona_eliminada.emit(zona_obj["id"])
                    mesa_event_bus.zonas_actualizadas.emit(self.db.get_zonas())
                    QMessageBox.information(
                        self,
                        "Zona eliminada",
                        f"Zona '{zona_a_eliminar}' eliminada correctamente.",
                    )
                except Exception as e:
                    import logging

                    logging.getLogger(__name__).error(
                        f"No se pudo eliminar la zona: {e}"
                    )
                    QMessageBox.critical(
                        self, "Error", f"No se pudo eliminar la zona: {e}"
                    )

    def __init__(self, instance: Any):  # TODO: instance es dinámico, requiere Any
        super().__init__()
        self.setObjectName("FiltersSectionUltraPremium")
        self.setStyleSheet(
            """
            QFrame#FiltersSectionUltraPremium {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f0f9ff, stop:0.5 #e0f2fe, stop:1 #f0f9ff);
                border: 1.5px solid #0ea5e9;
                border-radius: 14px;
                padding: 6px 0px 8px 0px; /* Padding mínimo */
                margin: 2px;
                min-width: 480px;  /* Aumentar ancho mínimo al tener más espacio */
                max-width: 800px;  /* Aumentar ancho máximo para aprovechar el espacio liberado */
                min-height: 200px;
            }
        """
        )
        self.db = DatabaseManager()
        mesa_event_bus.zonas_actualizadas.connect(self.update_zonas_chips)
        # Aplicar política de tamaño más conservadora para evitar expansión excesiva
        from PyQt6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        main_hbox = QHBoxLayout(self)
        main_hbox.setContentsMargins(0, 0, 0, 0)  # Sin margen extra
        main_hbox.setSpacing(4)  # Aumentar espacio entre subcontenedores

        # --- Subcontenedor de Estados ---
        subcontenedor_estados = QFrame()
        subcontenedor_estados.setObjectName("SubcontenedorEstados")
        subcontenedor_estados.setStyleSheet(
            """
            QFrame#SubcontenedorEstados {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f1f5f9, stop:1 #e0e7ef);
                border: 1.2px dashed #38bdf8;
                border-radius: 8px;
                min-width: 0px;
                min-height: 90px;
            }
        """
        )
        subcontenedor_estados.setMinimumHeight(90)
        subcontenedor_estados.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )
        right_vbox = QVBoxLayout(subcontenedor_estados)
        right_vbox.setContentsMargins(
            0, 0, 0, 8
        )  # Padding inferior estándar para estados
        right_vbox.setSpacing(5)
        estados_title = QLabel("Estados")
        estados_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        estados_title.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: 800;
                color: #fff;
                letter-spacing: 0.5px;
                padding: 0px 0 6px 0;
                min-width: 0px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #38bdf8);
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                border: none;
                margin: 0px;
            }
        """
        )
        right_vbox.addWidget(estados_title, alignment=Qt.AlignmentFlag.AlignTop)
        chips_container = QFrame()
        chips_container.setObjectName("ChipsEstadosContainer")
        chips_container.setStyleSheet(
            "QFrame#ChipsEstadosContainer { background: transparent; border: none; min-width: 0px; padding-left: 0px; padding-right: 0px; }"
        )
        chips_layout = QVBoxLayout(chips_container)
        chips_layout.setSpacing(6)
        chips_layout.setContentsMargins(0, 0, 0, 0)
        self.estado_chips: list[Any] = []
        estados = [
            ("Todos", "#64748b"),
            ("Libre", "#22c55e"),
            ("Ocupada", "#ef4444"),
            ("Reservada", "#f59e0b"),
        ]

        def on_chip_clicked_factory(estado: Any) -> Any:
            def handler() -> None:
                self.set_estado_chip_selected(estado)
                if hasattr(instance, "_on_status_changed"):
                    instance._on_status_changed(estado)

            return handler

        for nombre, color in estados:
            btn = QPushButton(nombre)
            btn.setCheckable(True)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background: #fff;
                    color: {color};
                    border: 1.2px solid {color};
                    border-radius: 14px;
                    padding: 2px 8px;
                    font-size: 12px;
                    font-weight: 600;
                    min-width: 0px;
                    min-height: 22px;
                    text-align: center;
                }}
                QPushButton:checked {{
                    background: {color};
                    color: #fff;
                    border: 2px solid {color};
                }}
            """
            )
            btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            chips_layout.addWidget(btn)
            btn.clicked.connect(on_chip_clicked_factory(nombre))
            self.estado_chips.append(btn)
        right_vbox.addWidget(chips_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.set_estado_chip_selected("Todos")
        right_vbox.addStretch(1)
        main_hbox.addWidget(subcontenedor_estados, 1)  # Dar peso al subcontenedor

        # --- Subcontenedor de Zonas ---
        subcontenedor_zonas = QFrame()
        subcontenedor_zonas.setObjectName("SubcontenedorZonas")
        subcontenedor_zonas.setStyleSheet(
            """
            QFrame#SubcontenedorZonas {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f1f5f9, stop:1 #e0e7ef);
                border: 1.2px dashed #38bdf8;
                border-radius: 8px;
                min-width: 0px;
                min-height: 90px;
            }
        """
        )
        subcontenedor_zonas.setMinimumHeight(90)
        subcontenedor_zonas.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )
        zonas_vbox = QVBoxLayout(subcontenedor_zonas)
        zonas_vbox.setContentsMargins(
            0, 0, 0, 20
        )  # Aumentar padding inferior para igualar altura visual
        zonas_vbox.setSpacing(5)
        zonas_title = QLabel("Zonas")
        zonas_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        zonas_title.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: 800;
                color: #fff;
                letter-spacing: 0.5px;
                padding: 0px 0 6px 0;
                min-width: 0px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #0ea5e9);
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                border: none;
                margin: 0px;
            }
        """
        )
        zonas_vbox.addWidget(zonas_title, alignment=Qt.AlignmentFlag.AlignTop)
        self.chips_zonas_container = QFrame()
        self.chips_zonas_container.setObjectName("ChipsZonasContainer")
        self.chips_zonas_container.setStyleSheet(
            "QFrame#ChipsZonasContainer { background: transparent; border: none; min-width: 0px; padding: 0; }"
        )
        from PyQt6.QtWidgets import QSizePolicy as QSP

        self.chips_zonas_container.setSizePolicy(QSP.Policy.Minimum, QSP.Policy.Fixed)
        self.chips_zonas_layout = QGridLayout(self.chips_zonas_container)
        self.chips_zonas_layout.setSpacing(8)
        self.chips_zonas_layout.setContentsMargins(0, 0, 0, 0)
        self.zonas_chips: list[Any] = []
        zonas_vbox.addWidget(self.chips_zonas_container)
        zonas_vbox.addStretch(1)
        main_hbox.addWidget(
            subcontenedor_zonas, 2
        )  # Dar más peso al subcontenedor de zonas

        # --- Subcontenedor de Búsqueda/Acción (a la derecha de Zonas) ---
        subcontenedor_busqueda_accion = QFrame()
        subcontenedor_busqueda_accion.setObjectName("SubcontenedorBusquedaAccion")
        subcontenedor_busqueda_accion.setStyleSheet(
            """
            QFrame#SubcontenedorBusquedaAccion {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f1f5f9, stop:1 #e0e7ef);
                border: 1.2px dashed #38bdf8;
                border-radius: 8px;
                min-width: 360px;  /* Ancho mínimo para asegurar espacio suficiente */
                min-height: 90px;
            }
        """
        )
        subcontenedor_busqueda_accion.setMinimumHeight(90)
        subcontenedor_busqueda_accion.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )
        subcontenedor_busqueda_accion.setMaximumWidth(
            900
        )  # Aumentar ancho máximo para más espacio
        # Layout vertical para varias filas de botones
        busqueda_accion_vbox = QVBoxLayout(subcontenedor_busqueda_accion)
        busqueda_accion_vbox.setContentsMargins(0, 0, 0, 20)
        busqueda_accion_vbox.setSpacing(6)
        # Título arriba
        busqueda_accion_title = QLabel("Gestión")
        busqueda_accion_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        busqueda_accion_title.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: 800;
                color: #fff;
                letter-spacing: 0.5px;
                padding: 0px 0 6px 0;
                min-width: 0px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #38bdf8);
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                border: none;
                margin: 0px;
            }
        """
        )
        busqueda_accion_vbox.addWidget(busqueda_accion_title)

        # Botones de gestión divididos en 3 filas
        gestion_buttons = [
            {"text": "Nueva Mesa", "icon": "➕🍽️", "tooltip": "Crear nueva mesa"},
            {
                "text": "Eliminar Mesa",
                "icon": "🗑️🍽️",
                "tooltip": "Eliminar mesa seleccionada",
            },
            {"text": "Nueva Zona", "icon": "➕📍", "tooltip": "Crear nueva zona"},
            {
                "text": "Eliminar Zona",
                "icon": "🗑️📍",
                "tooltip": "Eliminar zona seleccionada",
            },
            {
                "text": "Editar Zona",
                "icon": "✏️📍",
                "tooltip": "Editar zona seleccionada",
            },
            {
                "text": "Refrescar Estado",
                "icon": "🔄",
                "tooltip": "Refrescar estado de mesas y zonas",
            },
            {
                "text": "Ver Historial",
                "icon": "📜",
                "tooltip": "Ver historial de cambios",
            },
            {
                "text": "Mover Comanda de Mesa",
                "icon": "🔀🧾",
                "tooltip": "Mover comanda de una mesa a otra (próximamente)",
            },
        ]
        filas = [
            gestion_buttons[0:3],  # Nueva Mesa, Eliminar Mesa, Nueva Zona
            gestion_buttons[3:6],  # Eliminar Zona, Editar Zona, Refrescar Estado
            gestion_buttons[6:8],  # Ver Historial, Mover Comanda de Mesa
        ]
        self.gestion_btns: list[Any] = []
        for fila in filas:
            fila_hbox = QHBoxLayout()
            fila_hbox.setSpacing(6)
            for btn_info in fila:
                # Ajuste especial para los botones de zona (emoji más pequeño)
                if btn_info["text"] in ["Nueva Zona", "Eliminar Zona"]:
                    btn = QPushButton(f"{btn_info['icon']} {btn_info['text']}")
                    btn.setToolTip(btn_info["tooltip"])
                    btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn.setStyleSheet(
                        """
                        QPushButton {
                            background: #f1f5f9;
                            color: #0ea5e9;
                            border: 1.2px solid #38bdf8;
                            border-radius: 8px;
                            padding: 2px 7px;
                            font-size: 10px; /* Más pequeño solo para zona */
                            font-weight: 600;
                            min-width: 0px;
                            min-height: 22px;
                        }
                        QPushButton:hover {
                            background: #e0e7ef;
                            color: #0284c7;
                            border: 1.5px solid #0ea5e9;
                        }
                    """
                    )
                    btn.setSizePolicy(
                        QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
                    )
                else:
                    btn = QPushButton(f"{btn_info['icon']} {btn_info['text']}")
                    btn.setToolTip(btn_info["tooltip"])
                    btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn.setStyleSheet(
                        """
                        QPushButton {
                            background: #f1f5f9;
                            color: #0ea5e9;
                            border: 1.2px solid #38bdf8;
                            border-radius: 8px;
                            padding: 2px 7px;
                            font-size: 12px;
                            font-weight: 600;
                            min-width: 0px;
                            min-height: 22px;
                        }
                        QPushButton:hover {
                            background: #e0e7ef;
                            color: #0284c7;
                            border: 1.5px solid #0ea5e9;
                        }
                    """
                    )
                    btn.setSizePolicy(
                        QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
                    )
                fila_hbox.addWidget(btn)
                self.gestion_btns.append(btn)
            fila_hbox.addStretch(1)
            busqueda_accion_vbox.addLayout(fila_hbox)

        # Lógica de creación de zona para el botón 'Nueva Zona'
        def crear_nueva_zona() -> None:
            from PyQt6.QtWidgets import QInputDialog, QMessageBox

            zonas_db = [z["nombre"] for z in self.db.get_zonas()]
            nueva_zona, ok = QInputDialog.getText(
                self, "Crear nueva zona", "Nombre de la nueva zona:"
            )
            if ok and nueva_zona:
                nueva_zona = nueva_zona.strip()
                if not nueva_zona:
                    QMessageBox.warning(
                        self,
                        "Zona inválida",
                        "El nombre de la zona no puede estar vacío.",
                    )
                    return
                if nueva_zona in zonas_db:
                    QMessageBox.warning(
                        self, "Zona duplicada", f"La zona '{nueva_zona}' ya existe."
                    )
                    return
                try:
                    self.db.create_zona(nueva_zona)
                    mesa_event_bus.zona_creada.emit({"nombre": nueva_zona})
                    mesa_event_bus.zonas_actualizadas.emit(self.db.get_zonas())
                    QMessageBox.information(
                        self,
                        "Zona creada",
                        f"Zona '{nueva_zona}' creada correctamente.",
                    )
                except Exception as e:
                    import logging

                    logging.getLogger(__name__).error(f"No se pudo crear la zona: {e}")
                    QMessageBox.critical(
                        self, "Error", f"No se pudo crear la zona: {e}"
                    )

        # Conectar el botón 'Nueva Zona' a la función
        for btn in self.gestion_btns:
            if btn.text().endswith("Nueva Zona"):
                btn.clicked.connect(crear_nueva_zona)
            if btn.text().endswith("Eliminar Zona"):
                try:
                    btn.clicked.disconnect()
                except Exception as e:
                    import logging

                    logging.getLogger(__name__).warning(
                        f"Error desconectando señal de botón Eliminar Zona: {e}"
                    )
                btn.clicked.connect(self.eliminar_zona)
            if btn.text().endswith("Editar Zona"):
                try:
                    btn.clicked.disconnect()
                except Exception as e:
                    import logging

                    logging.getLogger(__name__).warning(
                        f"Error desconectando señal de botón Editar Zona: {e}"
                    )
                btn.clicked.connect(self.editar_zona)

        # Fila 4: Barra de búsqueda avanzada
        from PyQt6.QtWidgets import QLineEdit

        search_line = QLineEdit()
        search_line.setPlaceholderText(
            "Buscar mesa por nombre, número, zona o alias..."
        )
        search_line.setClearButtonEnabled(True)
        search_line.setStyleSheet(
            """
            QLineEdit {
                background: #fff;
                border: 1.5px solid #38bdf8;
                border-radius: 8px;
                padding: 0px 0px 0px 0px;
                font-size: 14px;
                color: #0ea5e9;
                margin-top: 1px;
                margin-bottom: 0px;
                min-height: 22px;
            }
            QLineEdit:focus {
                border: 2px solid #0ea5e9;
                background: #f0f9ff;
            }
        """
        )
        # Forzar expansión horizontal máxima de la barra de búsqueda
        search_line.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )
        # Conectar búsqueda avanzada
        if hasattr(instance, "_on_search_changed"):
            search_line.textChanged.connect(instance._on_search_changed)
        # Guardar referencia para acceso externo
        self.search_input = search_line
        if hasattr(instance, "set_search_input"):
            instance.set_search_input(search_line)
        busqueda_accion_vbox.addWidget(search_line)
        busqueda_accion_vbox.addStretch(1)
        main_hbox.addWidget(
            subcontenedor_busqueda_accion, 3
        )  # Aumentar peso para dar más espacio

        # Eliminar el spacer expansivo para evitar espacio libre a la derecha
        # from PyQt6.QtWidgets import QSpacerItem, QSizePolicy as QSP
        # main_hbox.addSpacerItem(QSpacerItem(0, 0, QSP.Policy.Expanding, QSP.Policy.Minimum))
        self.instance = instance

        # --- Conexión lógica de botones de acción ---
        # Asume que 'instance' es MesasArea y tiene los métodos _on_nueva_mesa_clicked, _on_eliminar_mesa_clicked, etc.
        btn_map = {
            "Nueva Mesa": "_on_nueva_mesa_clicked",
            "Eliminar Mesa": "_on_eliminar_mesa_clicked",
            # TODO: Añadir aquí los métodos para los otros botones cuando estén implementados
            # 'Nueva Zona': '_on_nueva_zona_clicked',
            # 'Eliminar Zona': '_on_eliminar_zona_clicked',
            # 'Editar Zona': '_on_editar_zona_clicked',
            # 'Refrescar Estado': '_on_refrescar_estado_clicked',
            # 'Ver Historial': '_on_ver_historial_clicked',
            # 'Mover Comanda de Mesa': '_on_mover_comanda_clicked',
        }
        for btn in self.gestion_btns:
            for key, method in btn_map.items():
                if key in btn.text() and hasattr(self.instance, method):
                    btn.clicked.connect(getattr(self.instance, method))

        self.update_zonas_chips()

    def set_estado_chip_selected(self, selected_estado: str) -> None:
        for btn in self.estado_chips:
            btn.setChecked(btn.text() == selected_estado)

    def set_zona_chip_selected(self, selected_zona: str) -> None:
        for btn in self.zonas_chips:
            btn.setChecked(btn.text() == selected_zona)
        if hasattr(self.instance, "_on_zone_changed"):
            self.instance._on_zone_changed(selected_zona)

    def update_zonas_chips(self) -> None:
        # Elimina los chips actuales
        for i in reversed(range(self.chips_zonas_layout.count())):
            item = self.chips_zonas_layout.itemAt(i)
            widget = item.widget() if item is not None else None
            if widget is not None:
                widget.setParent(None)
        self.zonas_chips.clear()
        zonas_actuales = [z["nombre"] for z in self.db.get_zonas()]
        zonas_actuales = ["Todas"] + sorted(zonas_actuales)

        def on_zona_chip_clicked_factory(zona: Any) -> Any:
            def handler() -> None:
                self.set_zona_chip_selected(zona)

            return handler

        # --- Organización en columnas ---
        max_filas = 3  # Menos elementos por columna para evitar solapamiento
        col = 0
        fila = 0
        for nombre in zonas_actuales:
            btn = QPushButton(nombre)
            btn.setCheckable(True)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background: #fff;
                    color: #0ea5e9;
                    border: 1.2px solid #0ea5e9;
                    border-radius: 14px;
                    padding: 2px 8px;
                    font-size: 12px;
                    font-weight: 600;
                    min-width: 0px;
                    min-height: 28px;
                    text-align: center;
                }}
                QPushButton:checked {{
                    background: #0ea5e9;
                    color: #fff;
                    border: 2px solid #0ea5e9;
                }}
            """
            )
            btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            self.chips_zonas_layout.addWidget(btn, fila, col)
            btn.clicked.connect(on_zona_chip_clicked_factory(nombre))
            self.zonas_chips.append(btn)
            fila += 1
            if fila >= max_filas:
                fila = 0
                col += 1
        self.set_zona_chip_selected("Todas")

    def get_zonas_from_instance(self) -> list[str]:
        zonas_unicas = set()
        if hasattr(self.instance, "mesas") and self.instance.mesas:
            for mesa in self.instance.mesas:
                if hasattr(mesa, "zona") and mesa.zona:
                    zonas_unicas.add(mesa.zona)
        # Incluir zonas personalizadas aunque no haya mesas asociadas
        if hasattr(self.instance, "_zonas_personalizadas"):
            zonas_unicas.update(self.instance._zonas_personalizadas)
        return ["Todas"] + sorted(zonas_unicas)


def update_ultra_premium_stats_ui(
    instance: Any, zonas: int, total: int, libres: int, ocupadas: int, reservadas: int
) -> None:
    """Actualiza los valores de las tarjetas premium del header (solo UI, sin lógica de cálculo)"""

    # Helper para animar highlight cuando cambia el valor
    def animate_pulse(widget: Any) -> None:
        if not widget:
            return
        anim = QPropertyAnimation(widget, b"styleSheet")
        anim.setDuration(350)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        orig_style = widget.styleSheet()
        highlight = (
            orig_style.replace("background:", "background: #fffbe6;")
            if "background:" in orig_style
            else orig_style + "\nbackground: #fffbe6;"
        )
        anim.setStartValue(highlight)
        anim.setEndValue(orig_style)
        widget._pulse_anim = anim
        anim.start()

    # Transición suave de números
    def animate_number(
        label: Any, old_value: Any, new_value: Any, duration: int = 350
    ) -> None:
        try:
            old = int(old_value)
            new = int(new_value)
        except (ValueError, TypeError) as e:
            import logging

            logging.getLogger(__name__).warning(f"Error animando número: {e}")
            label.setText(str(new_value))
            return
        if old == new:
            label.setText(str(new_value))
            return
        steps = max(10, int(duration / 30))
        delta = (new - old) / steps
        current = [float(old)]
        count = [0]

        def update():
            if count[0] >= steps:
                label.setText(str(new))
                timer.stop()
                return
            value = int(round(current[0]))
            label.setText(str(value))
            current[0] += delta
            count[0] += 1

        timer = QTimer()
        timer.timeout.connect(update)
        timer.start(int(duration / steps))
        # Mantener referencia para evitar garbage collection
        label._number_anim_timer = timer

    # Actualizar y animar si cambia el valor
    def set_value_and_animate(
        widget: Any, new_value: Any, badge_logic: Any = None
    ) -> None:
        if widget and hasattr(widget, "value_label"):
            label = widget.value_label
            trend = getattr(widget, "trend_label", None)
            badge = getattr(widget, "badge_label", None)
            old = label.text()
            # Tendencia: comparar con último valor
            try:
                prev = (
                    int(widget._last_value)
                    if widget._last_value is not None
                    else int(old)
                )
                curr = int(new_value)
                if trend:
                    if curr > prev:
                        trend.setText("▲")
                        trend.setStyleSheet(
                            "font-size: 26px; color: #22c55e; font-weight: bold; background: transparent; border: none;"
                        )
                    elif curr < prev:
                        trend.setText("▼")
                        trend.setStyleSheet(
                            "font-size: 26px; color: #ef4444; font-weight: bold; background: transparent; border: none;"
                        )
                    else:
                        trend.setText("—")
                        trend.setStyleSheet(
                            "font-size: 26px; color: #64748b; font-weight: bold; background: transparent; border: none;"
                        )
            except Exception:
                if trend:
                    trend.setText("—")
                    trend.setStyleSheet(
                        "font-size: 26px; color: #64748b; font-weight: bold; background: transparent; border: none;"
                    )
            # Badge de alerta (lógica por métrica)
            if badge and badge_logic:
                badge_text, badge_color, badge_tooltip, show = badge_logic(new_value)
                if show:
                    badge.setText(badge_text)
                    badge.setStyleSheet(
                        f"font-size: 16px; color: #fff; background: {badge_color}; border-radius: 9px; padding: 0 6px; margin-left: 4px; font-weight: bold;"
                    )
                    badge.setToolTip(badge_tooltip)
                    badge.show()
                else:
                    badge.hide()
            elif badge:
                badge.hide()
            widget._last_value = new_value
            if str(new_value) != old:
                try:
                    int(old)
                    int(new_value)
                    animate_number(label, old, new_value)
                except (ValueError, TypeError) as e:
                    import logging

                    logging.getLogger(__name__).warning(
                        f"Error animando número en set_value_and_animate: {e}"
                    )
                    label.setText(str(new_value))
                animate_pulse(widget)
            else:
                label.setText(str(new_value))

    # Badge lógica para ocupadas: alerta si >80% del total
    def badge_ocupadas(val: Any) -> tuple[str, str, str, bool]:
        try:
            val = int(val)
            total_widget = getattr(instance, "mesas_total_widget", None)
            total = (
                int(total_widget.value_label.text())
                if (total_widget and hasattr(total_widget, "value_label"))
                else 0
            )
            if total > 0 and val / total >= 0.8:
                return ("!", "#ef4444", "Alerta: Más del 80% de mesas ocupadas", True)
        except (ValueError, TypeError) as e:
            import logging

            logging.getLogger(__name__).warning(f"Error calculando badge ocupadas: {e}")
        return ("", "#ef4444", "", False)

    # Badge lógica para reservadas: alerta si >0
    def badge_reservadas(val: Any) -> tuple[str, str, str, bool]:
        try:
            val = int(val)
            if val > 0:
                return ("!", "#f59e0b", "Alerta: Hay mesas reservadas", True)
        except (ValueError, TypeError) as e:
            import logging

            logging.getLogger(__name__).warning(
                f"Error calculando badge reservadas: {e}"
            )
        return ("", "#f59e0b", "", False)

    set_value_and_animate(getattr(instance, "zonas_widget", None), zonas)
    set_value_and_animate(getattr(instance, "mesas_total_widget", None), total)
    set_value_and_animate(getattr(instance, "mesas_libres_widget", None), libres)
    set_value_and_animate(
        getattr(instance, "mesas_ocupadas_widget", None),
        ocupadas,
        badge_logic=badge_ocupadas,
    )
    set_value_and_animate(
        getattr(instance, "mesas_reservadas_widget", None),
        reservadas,
        badge_logic=badge_reservadas,
    )

    set_value_and_animate(getattr(instance, "zonas_widget", None), zonas)
    set_value_and_animate(getattr(instance, "mesas_total_widget", None), total)
    set_value_and_animate(getattr(instance, "mesas_libres_widget", None), libres)
    set_value_and_animate(getattr(instance, "mesas_ocupadas_widget", None), ocupadas)
    set_value_and_animate(
        getattr(instance, "mesas_reservadas_widget", None), reservadas
    )
    # Forzar actualización visual
    for attr in [
        "zonas_widget",
        "mesas_total_widget",
        "mesas_libres_widget",
        "mesas_ocupadas_widget",
        "mesas_reservadas_widget",
    ]:
        widget = getattr(instance, attr, None)
        if widget:
            widget.update()
            widget.repaint()


def create_header(parent: Any, instance: Any, layout: Any) -> Any:
    # Imports locales eliminados (ya están al inicio del archivo)
    # Contenedor principal del header
    header_container = QFrame()
    header_container.setObjectName("HeaderContainerUltraPremium")
    header_container.setStyleSheet(
        """
        QFrame#HeaderContainerUltraPremium {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fefefe,
                stop:0.2 #fdfdfd,
                stop:0.8 #f9fafb,
                stop:1 #f3f4f6);
            border: 2px solid;
            border-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #e5e7eb, stop:0.5 #d1d5db, stop:1 #e5e7eb);
            border-radius: 16px;
            margin: 2px;
        }
    """
    )
    header_layout = QHBoxLayout(header_container)
    header_layout.setContentsMargins(8, 6, 8, 6)  # Márgenes más pequeños
    header_layout.setSpacing(6)  # Más espacio entre los contenedores principales

    # Eliminar sección izquierda del título para compactar el header
    # from PyQt6.QtWidgets import QSizePolicy, QWidget
    # left_section_widget = QWidget()
    # left_section_layout = QVBoxLayout(left_section_widget)
    # left_section_layout.setSpacing(8)
    # title_status_container = create_title_section_ultra_premium()
    # left_section_layout.addWidget(title_status_container)
    # left_section_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    # header_layout.addWidget(left_section_widget, 0)
    # # Separador
    # separator1 = create_ultra_premium_separator()
    # header_layout.addWidget(separator1, 0)

    # Sección principal: filtros y control (solo UI moderna de chips)
    filters_container = FiltersSectionUltraPremium(instance)
    # Dar más espacio al contenedor de filtros ahora que no hay título
    filters_container.setSizePolicy(
        QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
    )
    header_layout.addWidget(filters_container, 1)  # Dar peso para expansión
    # Separador
    separator2 = create_ultra_premium_separator()
    header_layout.addWidget(separator2, 0)
    # Sección derecha: estadísticas premium
    from PyQt6.QtWidgets import QWidget

    right_section_widget = QWidget()
    right_section_widget.setMinimumWidth(580)  # Mantener mínimo para 5 tarjetas
    # Eliminar máximo para permitir expansión
    right_section_layout = QVBoxLayout(right_section_widget)
    right_section_layout.setSpacing(8)
    stats_container = create_subcontenedor_metric_cards(instance)
    right_section_layout.addWidget(stats_container)
    right_section_widget.setSizePolicy(
        QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
    )
    header_layout.addWidget(right_section_widget, 1)  # Dar peso para expansión
    # El header debe expandirse horizontalmente según el contenido
    # Eliminar min-width global, solo policies expansivas
    header_container.setSizePolicy(
        QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
    )
    layout.addWidget(header_container)
    return header_container


# Export explícito para el import en mesas_area_main
__all__ = ["create_header", "FiltersSectionUltraPremium"]

# TODO: Existen métodos y atributos dinámicos en 'instance' y en los chips/botones.
#       Se utiliza 'Any' para cumplir con la integración dinámica del sistema.
#       Refactorizar a futuro si la arquitectura lo permite para tipado estricto.

# NOTA: Algunos avisos de tipado parcial en métodos de PyQt y base de datos son inevitables por la naturaleza dinámica de PyQt y la integración con objetos externos.
#       Esta excepción está documentada en este archivo y debe revisarse si se refactoriza la arquitectura.
