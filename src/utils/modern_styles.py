from typing import Optional, Dict, List, Any
"""
Hefest - Modern Styles
Sistema de estilos QSS modular para una apariencia moderna y profesional

Este módulo contiene definiciones de estilos CSS para todos los componentes
de la aplicación, organizados de manera modular y fácil de mantener.
"""


class ModernStyles:
    @classmethod
    def get_reserva_list_item_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "background: #fff; border-radius: 10px; border: 1.5px solid #e0e0e0;"

    @classmethod
    def get_reserva_badge_style(cls, estado):
        """TODO: Add docstring"""
        # TODO: Add input validation
        _ = {
            "confirmada": "#4caf50",
            "pendiente": "#ff9800",
            "cancelada": "#f44336",
            "ocupada": "#1976d2",
            "libre": "#9e9e9e",
        }
        _ = colores.get(estado, "#bdbdbd")
        return (
            f"background: {color}; color: #fff; border-radius: 6px; padding: 4px 8px;"
        )

    @classmethod
    def get_stats_section_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return """
        QFrame#SubContenedorMetricCards {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #fef7ff, stop:0.5 #fdf4ff, stop:1 #fef7ff);
            border: 1.5px solid #d946ef;
            border-radius: 14px;
            padding: 2px 8px 18px 8px;
            margin: 2px 0 8px 0;
            min-height: 120px;
        }
        """

    @classmethod
    def get_stats_title_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "background: #f3e8ff; border-radius: 6px; padding: 1px 10px 1px 6px; border: 1px solid #d946ef; margin-bottom: 0px;"

    @classmethod
    def get_stats_refresh_btn_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return """
        QPushButton {
            background: #f3e8ff;
            border: 1.5px solid #d946ef;
            border-radius: 14px;
            font-size: 15px;
            color: #a21caf;
            font-weight: bold;
            margin-left: 8px;
        }
        QPushButton:hover {
            background: #e9d5ff;
            color: #7c2dbe;
        }
        """

    @classmethod
    def get_stats_config_btn_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return """
        QPushButton {
            background: #f3e8ff;
            border: 1.5px solid #d946ef;
            border-radius: 14px;
            font-size: 15px;
            color: #a21caf;
            font-weight: bold;
            margin-left: 6px;
        }
        QPushButton:hover {
            background: #e9d5ff;
            color: #7c2dbe;
        }
        """

    @classmethod
    def get_stats_last_refresh_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 10px; color: #64748b; background: #f3f4f6; border-radius: 6px; padding: 2px 8px; margin-top: 2px;"

    @classmethod
    def get_stats_separator_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "color: #d1d5db; font-size: 14px; margin: 0px 8px;"

    @classmethod
    def get_kpi_widget_style(cls, color, bg_color):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return f"""
        QFrame#KPIWidget {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {bg_color}, stop:0.5 #f3e8ff, stop:1 #e0e7ff);
            border: 2.5px solid {color};
            border-radius: 18px;
            margin: 4px;
            padding: 8px 6px 10px 6px;
            box-shadow: 0 4px 24px 0 rgba(120, 60, 180, 0.10), 0 1.5px 8px 0 rgba(120, 60, 180, 0.08);
            backdrop-filter: blur(8px);
            background-color: rgba(255,255,255,0.55);
        }}
        """

    @classmethod
    def get_kpi_icon_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 38px; margin-bottom: 2px;"

    @classmethod
    def get_kpi_value_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 28px; font-weight: bold; color: #222;"

    @classmethod
    def get_kpi_alias_label_style(cls, small=False):
        """TODO: Add docstring"""
        # TODO: Add input validation
        if small:
            return "font-size: 10px; color: #6b21a8; margin-top: 1px; padding: 0 2px; max-width: 170px; min-width: 60px; min-height: 14px; max-height: 22px; qproperty-alignment: 'AlignHCenter'; background: transparent; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"
        else:
            return "font-size: 12px; color: #6b21a8; margin-top: 2px; padding: 0 4px; max-width: 170px; min-width: 60px; min-height: 18px; max-height: 28px; qproperty-alignment: 'AlignHCenter'; background: transparent; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"

    @classmethod
    def get_alias_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "text-overflow: ellipsis; white-space: nowrap; overflow: hidden; padding: 0px; margin: 0px; background: transparent;"

    @classmethod
    def get_estado_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 13px; font-weight: 600; color: #fff; border-radius: 6px; padding: 2px 8px; background: #6c757d;"

    @classmethod
    def get_capacidad_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 12px; color: #495057; background: #f1f3f4; border-radius: 4px; padding: 1px 6px;"

    @classmethod
    def get_zona_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 12px; color: #64748b; background: #e2e8f0; border-radius: 4px; padding: 1px 6px;"

    @classmethod
    def get_contador_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 12px; color: #fff; background: #e53935; border-radius: 8px; padding: 2px 8px;"

    @classmethod
    def get_edit_btn_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "border: none; background: transparent; font-size: 14px; color: #1976d2;"

    @classmethod
    def get_restore_btn_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "border: none; background: transparent; font-size: 14px; color: #888;"

    @classmethod
    def get_edit_personas_btn_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "border: none; background: transparent; font-size: 13px;"

    @classmethod
    def get_batch_checkbox_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "margin-left:2px;margin-right:2px;"

    @classmethod
    def get_alias_line_edit_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 14px; padding: 2px 6px; border-radius: 4px; border: 1px solid #e0e0e0;"

    @classmethod
    def get_menu_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "QMenu { background: #fff; border-radius: 8px; border: 1px solid #e0e0e0; } QMenu::item { padding: 8px 24px; } QMenu::item:selected { background: #f1f5f9; color: #1976d2; }"

    @classmethod
    def get_base_widget_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "border-radius: 12px; background: #fff; border: 1px solid #e0e0e0;"

    @classmethod
    def get_scroll_area_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilo para QScrollArea y barras de scroll"""
        return f"""
        QScrollArea {{
            border: none;
            background-color: {cls.COLORS['background']};
            border-radius: 8px;
        }}
        QScrollBar:vertical {{
            background-color: {cls.COLORS['surface_hover']};
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background-color: #bdc3c7;
            border-radius: 6px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: #95a5a6;
        }}
        """

    @classmethod
    def get_mesas_container_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilo para el contenedor de mesas"""
        return f"""
        QWidget {{
            background-color: {cls.COLORS['background']};
            border-radius: 8px;
        }}
        """

    @classmethod
    def get_empty_message_frame_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilo para el mensaje de 'no mesas encontradas'"""
        return f"""
        QFrame {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f8f9fa, stop:1 #e9ecef);
            border: 2px dashed #dee2e6;
            border-radius: 16px;
            padding: 30px;
            margin: 20px;
        }}
        """

    @classmethod
    def get_icon_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 48px; color: #6c757d; margin: 10px;"

    @classmethod
    def get_title_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 20px; font-weight: bold; color: #495057; margin: 8px;"

    @classmethod
    def get_subtitle_label_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "font-size: 14px; color: #6c757d; margin: 4px;"

    """Contenedor para todos los estilos modernos de la aplicación"""

    # Paleta de colores moderna
    _ = {
        # Primarios
        "primary": "#3b82f6",
        "primary_hover": "#2563eb",
        "primary_pressed": "#1d4ed8",
        # Secundarios
        "secondary": "#64748b",
        "secondary_hover": "#475569",
        # Superficie
        "surface": "#ffffff",
        "surface_variant": "#f8fafc",
        "surface_hover": "#f1f5f9",
        # Fondo
        "background": "#f4f4f4",
        "background_alt": "#e2e8f0",
        # Texto
        "text_primary": "#1f2937",
        "text_secondary": "#6b7280",
        "text_muted": "#9ca3af",
        # Estados
        "success": "#22c55e",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6",
        # Bordes
        "border": "#e5e7eb",
        "border_focus": "#3b82f6",
        "border_error": "#ef4444",
    }

    @classmethod
    def get_main_window_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilo para la ventana principal"""
        return f"""
        QMainWindow {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
        }}

        QMainWindow::separator {{
            background-color: {cls.COLORS['border']};
            width: 1px;
            height: 1px;
        }}
        """

    @classmethod
    def get_button_styles(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para botones modernos"""
        return f"""
        /* Botón primario */
        QPushButton[class="primary"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary']}, stop:1 {cls.COLORS['primary_hover']});
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            min-width: 120px;
        }}

        QPushButton[class="primary"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary_hover']}, stop:1 {cls.COLORS['primary_pressed']});
        }}

        QPushButton[class="primary"]:pressed {{
            background: {cls.COLORS['primary_pressed']};
        }}

        /* Botón secundario */
        QPushButton[class="secondary"] {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            min-width: 120px;
        }}

        QPushButton[class="secondary"]:hover {{
            background-color: {cls.COLORS['surface_hover']};
            border-color: {cls.COLORS['secondary']};
        }}

        QPushButton[class="secondary"]:pressed {{
            background-color: {cls.COLORS['background_alt']};
        }}

        /* Botón outline */
        QPushButton[class="outline"] {{
            background-color: transparent;
            color: {cls.COLORS['primary']};
            border: 2px solid {cls.COLORS['primary']};
            border-radius: 8px;
            padding: 10px 22px;
            font-size: 14px;
            font-weight: 600;
            min-width: 120px;
        }}

        QPushButton[class="outline"]:hover {{
            background-color: {cls.COLORS['primary']};
            color: white;
        }}

        QPushButton[class="outline"]:pressed {{
            background-color: {cls.COLORS['primary_pressed']};
            border-color: {cls.COLORS['primary_pressed']};
        }}

        /* Botones de sidebar */
        QPushButton[class="sidebar"] {{
            background-color: transparent;
            color: {cls.COLORS['text_secondary']};
            border: none;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            font-weight: 500;
            text-align: left;
            min-height: 44px;
        }}

        QPushButton[class="sidebar"]:hover {{
            background-color: {cls.COLORS['surface_hover']};
            color: {cls.COLORS['text_primary']};
        }}

        QPushButton[class="sidebar"]:checked {{
            background-color: {cls.COLORS['primary']};
            color: white;
        }}
        """

    @classmethod
    def get_input_styles(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para inputs y formularios"""
        return f"""
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {cls.COLORS['text_primary']};
        }}

        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {cls.COLORS['border_focus']};
            outline: none;
        }}

        QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
            background-color: {cls.COLORS['background_alt']};
            color: {cls.COLORS['text_muted']};
        }}

        QComboBox {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 14px;
            color: {cls.COLORS['text_primary']};
            min-height: 20px;
        }}

        QComboBox:focus {{
            border-color: {cls.COLORS['border_focus']};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}

        QComboBox::down-arrow {{
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iNiIgdmlld0JveD0iMCAwIDEwIDYiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNSA1TDkgMSIgc3Ryb2tlPSIjNkI3MjgwIiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
        }}

        QSpinBox, QDoubleSpinBox {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 14px;
            color: {cls.COLORS['text_primary']};
        }}

        QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {cls.COLORS['border_focus']};
        }}
        """

    @classmethod
    def get_table_styles(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para tablas"""
        return f"""
        QTableWidget {{
            background-color: {cls.COLORS['surface']};
            alternate-background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            gridline-color: {cls.COLORS['border']};
            selection-background-color: rgba(59, 130, 246, 0.1);
            selection-color: {cls.COLORS['text_primary']};
            font-size: 14px;
        }}

        QTableWidget::item {{
            padding: 12px 16px;
            border-bottom: 1px solid {cls.COLORS['border']};
        }}

        QTableWidget::item:selected {{
            background-color: rgba(59, 130, 246, 0.1);
            color: {cls.COLORS['text_primary']};
        }}

        QHeaderView::section {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['surface_variant']}, stop:1 {cls.COLORS['background_alt']});
            color: {cls.COLORS['text_primary']};
            padding: 12px 16px;
            border: none;
            border-bottom: 2px solid {cls.COLORS['border']};
            font-weight: 600;
            font-size: 13px;
        }}

        QHeaderView::section:hover {{
            background-color: {cls.COLORS['surface_hover']};
        }}
        """

    @classmethod
    def get_tab_styles(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para pestañas"""
        return f"""
        QTabWidget::pane {{
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            background-color: {cls.COLORS['surface']};
            top: -1px;
        }}

        QTabBar::tab {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['surface_variant']}, stop:1 {cls.COLORS['background_alt']});
            color: {cls.COLORS['text_secondary']};
            padding: 12px 24px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border: 1px solid {cls.COLORS['border']};
            border-bottom: none;
            font-size: 14px;
            font-weight: 500;
            min-width: 80px;
        }}

        QTabBar::tab:selected {{
            background: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
            border-color: {cls.COLORS['primary']};
            border-bottom: 2px solid {cls.COLORS['primary']};
            font-weight: 600;
        }}

        QTabBar::tab:hover:!selected {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['surface_hover']}, stop:1 {cls.COLORS['surface_variant']});
            color: {cls.COLORS['text_primary']};
        }}
        """

    @classmethod
    def get_sidebar_styles(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para el sidebar"""
        return f"""
        QFrame[class="sidebar"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['surface']}, stop:1 {cls.COLORS['surface_variant']});
            border-right: 1px solid {cls.COLORS['border']};
        }}

        QFrame[class="sidebar-header"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['surface']}, stop:1 {cls.COLORS['surface_variant']});
            border: none;
            border-bottom: 1px solid {cls.COLORS['border']};
        }}

        QLabel[class="sidebar-title"] {{
            color: {cls.COLORS['text_primary']};
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 1px;
        }}

        QLabel[class="sidebar-subtitle"] {{
            color: {cls.COLORS['text_secondary']};
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        """

    @classmethod
    def get_card_styles(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para tarjetas"""
        return f"""
        QFrame[class="card"] {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 12px;
            padding: 20px;
        }}

        QFrame[class="card"]:hover {{
            border-color: {cls.COLORS['primary']};
            background-color: {cls.COLORS['surface_hover']};
        }}

        QFrame[class="glass-card"] {{
            background-color: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 20px;
        }}
        """

    @classmethod
    def get_status_bar_styles(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para la barra de estado"""
        return f"""
        QStatusBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['surface_variant']}, stop:1 {cls.COLORS['background_alt']});
            border-top: 1px solid {cls.COLORS['border']};
            color: {cls.COLORS['text_secondary']};
            font-size: 12px;
            padding: 5px;
        }}

        QStatusBar::item {{
            border: none;
        }}
        """

    @classmethod
    def get_scrollbar_styles(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para scrollbars"""
        return f"""
        QScrollBar:vertical {{
            background: {cls.COLORS['background_alt']};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}

        QScrollBar::handle:vertical {{
            background: {cls.COLORS['text_muted']};
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {cls.COLORS['text_secondary']};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background: {cls.COLORS['background_alt']};
            height: 12px;
            border-radius: 6px;
            margin: 0;
        }}

        QScrollBar::handle:horizontal {{
            background: {cls.COLORS['text_muted']};
            border-radius: 6px;
            min-width: 20px;
            margin: 2px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background: {cls.COLORS['text_secondary']};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        """

    @classmethod
    def get_dialog_styles(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para diálogos"""
        return f"""
        QDialog {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 12px;
        }}

        QDialog[class="glass"] {{
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
        }}
        """

    @classmethod
    def get_complete_stylesheet(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna la hoja de estilos completa"""
        return "\n".join(
            [
                cls.get_main_window_style(),
                cls.get_button_styles(),
                cls.get_input_styles(),
                cls.get_table_styles(),
                cls.get_tab_styles(),
                cls.get_sidebar_styles(),
                cls.get_card_styles(),
                cls.get_status_bar_styles(),
                cls.get_scrollbar_styles(),
                cls.get_dialog_styles(),
            ]
        )


class AnimatedStyles:
    """Estilos con definiciones para elementos animados"""

    @classmethod
    def get_hover_transition_style(cls):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """CSS para transiciones hover (NO SOPORTADO en PyQt6, solo referencia)"""
        return """
        /* PyQt6 NO soporta transition ni box-shadow. Estas líneas son solo referencia. */
        /* .hover-transition {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        } */
        .scale-on-hover:hover {
            /* transform: scale(1.02); */
        }
        .lift-on-hover:hover {
            /* transform: translateY(-2px); */
            /* box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); */
        }
        /* .fade-transition {
            transition: opacity 0.3s ease;
        } */
        /* .slide-transition {
            transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        } */
        """


class ThemeManager:
    """Gestor de temas para la aplicación"""

    _ = {
        "light": {
            "bg": "#f8fafc",
            "card": "#ffffff",
            "text": "#1f2937",
            "text_secondary": "#6b7280",
            "primary": "#3b82f6",
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444",
            "border": "#e5e7eb",
            "hover": "#f1f5f9",
        },
        "dark": {
            "bg": "#1e293b",
            "card": "#334155",
            "text": "#f1f5f9",
            "text_secondary": "#94a3b8",
            "primary": "#60a5fa",
            "success": "#34d399",
            "warning": "#fbbf24",
            "danger": "#f87171",
            "border": "#475569",
            "hover": "#1f2937",
        },
        "professional": {
            "bg": "#f0f4f8",
            "card": "#ffffff",
            "text": "#1a365d",
            "text_secondary": "#4a5568",
            "primary": "#2b6cb0",
            "success": "#2f855a",
            "warning": "#c05621",
            "danger": "#c53030",
            "border": "#e2e8f0",
            "hover": "#edf2f7",
        },
    }

    @classmethod
    def get_theme(cls, theme_name="light"):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene un tema por nombre"""
        return cls.THEMES.get(theme_name, cls.THEMES["light"])

    @classmethod
    def get_stylesheet(cls, theme_name="light"):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Genera el stylesheet para el tema seleccionado"""
        _ = cls.get_theme(theme_name)
        return f"""
            QWidget {{
                background: {theme['bg']};
                color: {theme['text']};
            }}

            QLabel {{
                background: transparent;
                color: {theme['text']};
            }}

            ModernCard {{
                background: {theme['card']};
                border: 1px solid {theme['border']};
                border-radius: 8px;
            }}

            ModernCard:hover {{
                background: {theme['hover']};
                border-color: {theme['primary']};
            }}

            QPushButton.action-button {{
                background: {theme['primary']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }}

            QPushButton.action-button:hover {{
                background: {theme['hover']};
                color: {theme['primary']};
                border: 1px solid {theme['primary']};
            }}

            QPushButton.secondary-button {{
                background: transparent;
                color: {theme['primary']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
            }}

            QPushButton.secondary-button:hover {{
                background: {theme['hover']};
                border-color: {theme['primary']};
            }}

            QTabWidget::pane {{
                border: 1px solid {theme['border']};
                border-radius: 8px;
                background: {theme['card']};
            }}

            QTabBar::tab {{
                padding: 8px 16px;
                margin-right: 4px;
                border: 1px solid {theme['border']};
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                background: {theme['bg']};
                color: {theme['text_secondary']};
            }}

            QTabBar::tab:selected {{
                background: {theme['card']};
                color: {theme['text']};
                border-bottom-color: {theme['card']};
            }}

            QScrollArea {{
                border: none;
                background: transparent;
            }}

            QScrollArea > QWidget > QWidget {{
                background: transparent;
            }}
        """


# Instancia global para fácil acceso
modern_styles = ModernStyles()
