"""
Estilos básicos para reemplazar ModernStyles eliminado
Este es un stub temporal que evita errores de importación.
TODO: Refactorizar para usar estilos base integrados o eliminar referencias.
"""


class BaseStyles:
    """Clase de estilos básica que reemplaza ModernStyles eliminado"""
    
    @staticmethod
    def get_scroll_area_style() -> str:
        """Estilo básico para scroll areas"""
        return """
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        """
    
    @staticmethod 
    def get_mesas_container_style() -> str:
        """Estilo básico para contenedor de mesas"""
        return """
        QWidget {
            background-color: #f5f5f5;
            border-radius: 8px;
        }
        """
    
    @staticmethod
    def get_empty_message_frame_style() -> str:
        """Estilo básico para frames de mensaje vacío"""
        return """
        QFrame {
            background-color: white;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            padding: 20px;
        }
        """
    
    @staticmethod
    def get_icon_label_style() -> str:
        """Estilo básico para labels de iconos"""
        return """
        QLabel {
            color: #666666;
            font-size: 48px;
        }
        """
    
    @staticmethod
    def get_title_label_style() -> str:
        """Estilo básico para labels de título"""
        return """
        QLabel {
            color: #333333;
            font-size: 18px;
            font-weight: bold;
        }
        """
    
    @staticmethod
    def get_subtitle_label_style() -> str:
        """Estilo básico para labels de subtítulo"""
        return """
        QLabel {
            color: #666666;
            font-size: 14px;
        }
        """
    
    @staticmethod
    def get_batch_checkbox_style() -> str:
        """Estilo básico para checkboxes de lote"""
        return """
        QCheckBox {
            spacing: 5px;
        }
        """
    
    @staticmethod
    def get_alias_label_style() -> str:
        """Estilo básico para labels de alias"""
        return """
        QLabel {
            font-weight: bold;
            color: #333333;
        }
        """
    
    @staticmethod
    def get_edit_btn_style() -> str:
        """Estilo básico para botones de edición"""
        return """
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        """
    
    @staticmethod
    def get_restore_btn_style() -> str:
        """Estilo básico para botones de restaurar"""
        return """
        QPushButton {
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #1e7e34;
        }
        """
    
    @staticmethod
    def get_edit_personas_btn_style() -> str:
        """Estilo básico para botones de editar personas"""
        return """
        QPushButton {
            background-color: #6c757d;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #545b62;
        }
        """
    
    @staticmethod
    def get_base_widget_style() -> str:
        """Estilo básico para widgets base"""
        return """
        QWidget {
            background-color: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        """
    
    @staticmethod
    def get_capacidad_label_style() -> str:
        """Estilo básico para labels de capacidad"""
        return """
        QLabel {
            color: #666666;
            font-size: 12px;
        }
        """
    
    @staticmethod
    def get_zona_label_style() -> str:
        """Estilo básico para labels de zona"""
        return """
        QLabel {
            color: #666666;
            font-size: 12px;
        }
        """
    
    @staticmethod
    def get_contador_label_style() -> str:
        """Estilo básico para labels de contador"""
        return """
        QLabel {
            color: #666666;
            font-size: 12px;
        }
        """
    
    @staticmethod
    def get_alias_line_edit_style() -> str:
        """Estilo básico para line edits de alias"""
        return """
        QLineEdit {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 6px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-color: #007bff;
        }
        """
    
    @staticmethod
    def get_menu_style() -> str:
        """Estilo básico para menús"""
        return """
        QMenu {
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        QMenu::item {
            padding: 6px 12px;
        }
        QMenu::item:selected {
            background-color: #f0f0f0;
        }
        """
    
    @staticmethod
    def get_reserva_badge_style(estado: str) -> str:
        """Estilo básico para badges de reserva"""
        colors = {
            'confirmada': '#28a745',
            'pendiente': '#ffc107', 
            'cancelada': '#dc3545',
            'default': '#6c757d'
        }
        color = colors.get(estado.lower(), colors['default'])
        return f"""
        QLabel {{
            background-color: {color};
            color: white;
            border-radius: 12px;
            padding: 4px 8px;
            font-size: 10px;
            font-weight: bold;
        }}
        """
    
    @staticmethod
    def get_reserva_list_item_style() -> str:
        """Estilo básico para items de lista de reservas"""
        return """
        QWidget {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            margin: 2px;
        }
        QWidget:hover {
            background-color: #f8f9fa;
        }
        """
    
    @staticmethod
    def get_stats_section_style() -> str:
        """Estilo básico para secciones de estadísticas"""
        return """
        QWidget {
            background-color: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            padding: 16px;
        }
        """
    
    @staticmethod
    def get_stats_title_label_style() -> str:
        """Estilo básico para títulos de estadísticas"""
        return """
        QLabel {
            color: #333333;
            font-size: 16px;
            font-weight: bold;
        }
        """
    
    @staticmethod
    def get_stats_refresh_btn_style() -> str:
        """Estilo básico para botón de actualizar estadísticas"""
        return """
        QPushButton {
            background-color: #17a2b8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #138496;
        }
        """
    
    @staticmethod
    def get_stats_config_btn_style() -> str:
        """Estilo básico para botón de configurar estadísticas"""
        return """
        QPushButton {
            background-color: #6c757d;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #545b62;
        }
        """
    
    @staticmethod
    def get_stats_last_refresh_label_style() -> str:
        """Estilo para etiquetas de última actualización de estadísticas"""
        return """
        QLabel {
            color: #666666;
            font-size: 10px;
            margin-top: 5px;
        }
        """
    
    @staticmethod
    def get_kpi_widget_style(color: str, bg_color: str) -> str:
        """Estilo para widgets KPI"""
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

    @staticmethod
    def get_kpi_icon_label_style() -> str:
        """Estilo para etiquetas de iconos KPI"""
        return "font-size: 38px; margin-bottom: 2px;"

    @staticmethod
    def get_kpi_value_label_style() -> str:
        """Estilo para etiquetas de valores KPI"""
        return "font-size: 28px; font-weight: bold; color: #222;"

    @staticmethod
    def get_kpi_alias_label_style(small: bool = False) -> str:
        """Estilo para etiquetas de alias KPI"""
        if small:
            return "font-size: 10px; color: #6b21a8; margin-top: 1px; padding: 0 2px; max-width: 170px; min-width: 60px; min-height: 14px; max-height: 22px; qproperty-alignment: 'AlignHCenter'; background: transparent; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"
        else:
            return "font-size: 12px; color: #6b21a8; margin-top: 2px; padding: 0 4px; max-width: 170px; min-width: 60px; min-height: 18px; max-height: 28px; qproperty-alignment: 'AlignHCenter'; background: transparent; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"


# Alias para compatibilidad
ModernStyles = BaseStyles
