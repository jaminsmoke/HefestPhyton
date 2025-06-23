"""
Componente MesasArea - Área de visualización y gestión de mesas
Versión: v0.0.13
"""

import logging
from typing import List, Optional, Callable
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QFrame, QScrollArea, QPushButton, QLineEdit, QComboBox,
                            QMenu, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction

from services.tpv_service import Mesa
from ..widgets.mesa_widget_simple import MesaWidget

logger = logging.getLogger(__name__)


class MesasArea(QFrame):
    """Área de visualización y gestión de mesas"""
    
    # Señales
    mesa_clicked = pyqtSignal(Mesa)
    nueva_mesa_requested = pyqtSignal()
    nueva_mesa_con_zona_requested = pyqtSignal(int, int, str)  # número, capacidad, zona
    eliminar_mesa_requested = pyqtSignal(int)  # Emite el ID de la mesa a eliminar
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesas: List[Mesa] = []
        self.filtered_mesas: List[Mesa] = []
        self.mesa_widgets: List[MesaWidget] = []
        
        self.current_zone_filter = "Todas"
        self.current_status_filter = "Todos"
        self.view_mode = "grid"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del área de mesas"""
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
        
        # Header del área de mesas
        self.create_header(container_layout)
          # Separador
        self.create_separator(container_layout)
          # Área de scroll para las mesas
        self.create_scroll_area(container_layout)
    
    def create_header(self, layout: QVBoxLayout):
        """🏆 ULTRA-PREMIUM HEADER - Diseño ultra-moderno con secciones encapsuladas"""
        
        # 🎨 CONTAINER PRINCIPAL ULTRA-PREMIUM
        header_container = QFrame()
        header_container.setObjectName("HeaderContainerUltraPremium")
        header_container.setStyleSheet("""
            QFrame#HeaderContainerUltraPremium {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fefefe, 
                    stop:0.2 #fdfdfd, 
                    stop:0.8 #f9fafb, 
                    stop:1 #f3f4f6);
                border: 2px solid;
                border-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e5e7eb,                    stop:0.5 #d1d5db, 
                    stop:1 #e5e7eb);
                border-radius: 16px;
                margin: 2px;
            }
        """)
          # 📐 LAYOUT PRINCIPAL CON ESPACIADO PREMIUM
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(24, 16, 24, 16)
        header_layout.setSpacing(0)  # Controlamos spacing manualmente
        
        # 🏷️ SECCIÓN 1: TÍTULO Y ESTADO APILADOS VERTICALMENTE
        title_status_container = QFrame()
        title_status_container.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
                margin: 0px;
            }
        """)
        
        title_status_layout = QVBoxLayout(title_status_container)
        title_status_layout.setContentsMargins(0, 0, 0, 0)
        title_status_layout.setSpacing(8)  # Espacio entre título y estado
        
        # Agregar título en la parte superior
        title_section = self.create_title_section_ultra_premium()
        title_status_layout.addWidget(title_section)
        
        # Agregar estado en la parte inferior
        status_section = self.create_status_section_ultra_premium()
        title_status_layout.addWidget(status_section)
        
        header_layout.addWidget(title_status_container)
        
        # 🔹 SEPARADOR PREMIUM 1
        separator1 = self.create_ultra_premium_separator()
        header_layout.addWidget(separator1)
        
        # � SECCIÓN 2: FILTROS ENCAPSULADOS
        filters_section = self.create_filters_section_ultra_premium()
        header_layout.addWidget(filters_section)
        
        # 🔹 SEPARADOR PREMIUM 2
        separator2 = self.create_ultra_premium_separator()
        header_layout.addWidget(separator2)
        
        # 📊 SECCIÓN 3: ESTADÍSTICAS ENCAPSULADAS
        stats_section = self.create_stats_section_ultra_premium()
        header_layout.addWidget(stats_section)
        
        layout.addWidget(header_container)
    
    def create_separator(self, layout: QVBoxLayout):
        """Crea un separador horizontal"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: #e0e6ed; margin: 4px 0px;")
        layout.addWidget(separator)
        
    def create_scroll_area(self, layout: QVBoxLayout):
        """Crea el área de scroll para las mesas"""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #fafbfc;
                border-radius: 8px;
            }
            QScrollBar:vertical {
                background-color: #f1f3f4;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #bdc3c7;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #95a5a6;
            }
        """)
        
        # Container para las mesas con padding
        mesas_container = QWidget()
        mesas_container.setStyleSheet("""
            QWidget {
                background-color: #fafbfc;
                border-radius: 8px;
            }
        """)
        
        self.mesas_layout = QGridLayout(mesas_container)
        self.mesas_layout.setSpacing(20)
        self.mesas_layout.setContentsMargins(20, 20, 20, 20)
        self.mesas_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.scroll_area.setWidget(mesas_container)
        layout.addWidget(self.scroll_area, 1)
    def create_compact_stats(self, layout: QHBoxLayout):
        """Crea las estadísticas compactas integradas en el header"""
        from PyQt6.QtGui import QFont
        
        # Separador visual antes de las estadísticas
        separator = QLabel("|")
        separator.setStyleSheet("color: #d1d5db; font-size: 14px; margin: 0px 8px;")
        layout.addWidget(separator)
        
        # Estadísticas compactas
        stats_config = [
            ("📍", "Zonas", "0", "#10b981"),
            ("🍽️", "Total", "0", "#2563eb"), 
            ("🟢", "Libres", "0", "#059669"),
            ("🔴", "Ocupadas", "0", "#dc2626")
        ]
        
        # Almacenar referencias para actualización
        self.stats_widgets = []
        
        for icon, label, value, color in stats_config:
            stat_widget = self.create_compact_stat_widget(icon, label, value, color)
            self.stats_widgets.append({
                'widget': stat_widget,
                'type': label.lower(),
                'icon': icon,
                'label': label
            })
            layout.addWidget(stat_widget)
    
    def create_compact_stat_widget(self, icon: str, label: str, value: str, color: str) -> QWidget:
        """Crea un widget de estadística compacta para el header"""
        from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        
        # Frame principal
        stat_widget = QFrame()
        stat_widget.setFrameStyle(QFrame.Shape.StyledPanel)
        stat_widget.setLineWidth(1)
        
        # Layout vertical
        layout = QVBoxLayout(stat_widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)
        
        # Etiqueta superior (título)
        label_widget = QLabel(f"{icon} {label}")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(8)
        title_font.setBold(False)
        label_widget.setFont(title_font)
        label_widget.setStyleSheet("color: #64748b; margin: 0px; padding: 0px;")
        layout.addWidget(label_widget)
        
        # Valor inferior (destacado)
        value_widget = QLabel(value)
        value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_font = QFont()
        value_font.setPointSize(14)
        value_font.setBold(True)
        value_widget.setFont(value_font)
        value_widget.setStyleSheet(f"color: {color}; margin: 0px; padding: 0px;")
        layout.addWidget(value_widget)
        
        # Estilo del frame contenedor
        stat_widget.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                margin: 0px 2px;
            }}
            QFrame:hover {{
                border-color: {color};
            }}
        """)
        
        # Tamaño compacto para el header
        stat_widget.setFixedSize(65, 40)
        
        return stat_widget
    
    def update_compact_stats(self, zonas: int, total: int, libres: int, ocupadas: int):
        """Actualiza las estadísticas compactas"""
        if not hasattr(self, 'stats_widgets'):
            return
            
        values = {
            'zonas': str(zonas),
            'total': str(total),
            'libres': str(libres),
            'ocupadas': str(ocupadas)
        }
        
        for stat_info in self.stats_widgets:
            widget = stat_info['widget']
            stat_type = stat_info['type']
            
            if stat_type in values:
                new_value = values[stat_type]
                # Actualizar el valor en el widget
                layout = widget.layout()
                if layout and layout.count() >= 2:
                    item = layout.itemAt(1)  # El segundo item es el valor
                    if item:
                        value_label = item.widget()
                        if isinstance(value_label, QLabel):
                            value_label.setText(new_value)
                            value_label.update()
                  # Forzar actualización del widget
                widget.update()
                widget.repaint()
    
    def update_stats_from_mesas(self):
        """Calcula y actualiza las estadísticas basándose en las mesas actuales"""
        if not self.mesas:
            # Si no hay mesas, mostrar valores en 0
            self.update_compact_stats(0, 0, 0, 0)
            return
        
        # Calcular estadísticas reales
        zonas_unicas = set(mesa.zona for mesa in self.mesas)
        zonas_activas = len(zonas_unicas)
        total_mesas = len(self.mesas)
        ocupadas = len([mesa for mesa in self.mesas if mesa.estado == 'ocupada'])
        libres = total_mesas - ocupadas
        
        # Actualizar estadísticas compactas
        self.update_compact_stats(zonas_activas, total_mesas, libres, ocupadas)
        
        # También actualizar la información de estado
        self.status_info.setText(f"Mostrando {len(self.filtered_mesas)} de {total_mesas} mesas")

    def _on_zone_changed(self, zone: str):
        """Maneja el cambio de filtro de zona"""
        self.current_zone_filter = zone
        self.apply_filters()

    def _on_status_changed(self, status: str):
        """Maneja el cambio de filtro de estado"""
        self.current_status_filter = status
        self.apply_filters()

    def set_mesas(self, mesas: List[Mesa]):
        """Establece la lista de mesas"""
        self.mesas = mesas
        self.apply_filters()
        # Actualizar estadísticas compactas después de establecer las mesas
        self.update_stats_from_mesas()
    
    def apply_filters(self, filters: Optional[dict] = None):
        """Aplica filtros específicos o usa los actuales"""
        if filters:
            self.current_zone_filter = filters.get('zone', 'Todas')
            self.current_status_filter = filters.get('status', 'Todos')
            self.view_mode = filters.get('view_mode', 'grid')
        
        try:
            self.filtered_mesas = self.mesas.copy()
            
            # Aplicar filtro de zona
            if self.current_zone_filter != "Todas":
                self.filtered_mesas = [
                    m for m in self.filtered_mesas 
                    if m.zona == self.current_zone_filter
                ]
            
            # Aplicar filtro de estado
            if self.current_status_filter != "Todos":
                estado_map = {
                    "Libre": "libre",
                    "Ocupada": "ocupada", 
                    "Reservada": "reservada"
                }
                estado_filtro = estado_map.get(self.current_status_filter)
                if estado_filtro:
                    self.filtered_mesas = [
                        m for m in self.filtered_mesas 
                        if m.estado == estado_filtro
                    ]
              # Actualizar vista
            QTimer.singleShot(50, self.populate_grid)
            
            # Actualizar estadísticas después de aplicar filtros
            self.update_stats_from_mesas()
            
        except Exception as e:
            logger.error(f"Error aplicando filtros: {e}")
    
    def apply_search(self, search_text: str):
        """Aplica filtro de búsqueda por texto"""
        try:
            if not search_text:
                self.filtered_mesas = self.mesas.copy()
            else:
                # Buscar por número de mesa o zona
                search_lower = search_text.lower()
                self.filtered_mesas = [
                    m for m in self.mesas 
                    if (search_lower in str(m.numero).lower() or 
                        search_lower in m.zona.lower())
                ]            # Aplicar otros filtros después de la búsqueda
            self.apply_filters()
            
        except Exception as e:
            logger.error(f"Error aplicando búsqueda: {e}")
    
    def refresh_mesas(self):
        """Refresca la vista de mesas"""
        self.apply_filters()
        
    def populate_grid(self):
        """Popula el grid de mesas con datos filtrados con cálculo dinámico optimizado"""
        try:
            # Limpiar layout existente
            self._clear_mesa_widgets()
            
            if not self.filtered_mesas:
                self._show_no_mesas_message()
                return
            
            # ✅ CÁLCULO DINÁMICO MEJORADO DE COLUMNAS
            cols = self._calculate_optimal_columns()
            
            for i, mesa in enumerate(self.filtered_mesas):
                row = i // cols
                col = i % cols
                
                # Crear widget de mesa
                mesa_widget = MesaWidget(mesa)
                mesa_widget.mesa_clicked.connect(self.mesa_clicked.emit)
                
                self.mesa_widgets.append(mesa_widget)
                self.mesas_layout.addWidget(mesa_widget, row, col)
            
            # Actualizar información de estado
            total_filtered = len(self.filtered_mesas)
            total_all = len(self.mesas)
            
            if total_filtered == total_all:
                status_text = f"Mostrando {total_all} mesa(s)"
            else:
                status_text = f"Mostrando {total_filtered} de {total_all} mesa(s)"
            
            self.status_info.setText(status_text)
            
        except Exception as e:
            logger.error(f"Error poblando grid de mesas: {e}")
    
    def _calculate_optimal_columns(self) -> int:
        """🧮 Calcula el número óptimo de columnas según el ancho disponible"""
        try:
            # Obtener ancho real del contenedor
            available_width = self.width()            # Si el widget no está completamente inicializado, usar un fallback inteligente
            if available_width <= 100:
                # Usar un valor por defecto robusto basado en resoluciones comunes
                from PyQt6.QtWidgets import QApplication
                try:
                    # Intentar obtener tamaño de la pantalla
                    screen = QApplication.primaryScreen()
                    if screen:
                        screen_geometry = screen.geometry()
                        available_width = max(1000, int(screen_geometry.width() * 0.7))
                    else:
                        available_width = 1200
                except:
                    available_width = 1200  # Fallback para pantallas HD
            
            # ✅ PARÁMETROS OPTIMIZADOS PARA MÁXIMO APROVECHAMIENTO
            widget_width = 220  # Ancho real del widget de mesa
            spacing = 15       # Espaciado entre widgets + márgenes
            padding = 60       # Padding total del contenedor (30px cada lado)
            
            # Calcular ancho útil disponible
            usable_width = available_width - padding
            
            # Calcular número de columnas que caben
            cols_fit = usable_width // (widget_width + spacing)
            
            # ✅ REGLAS DE OPTIMIZACIÓN INTELIGENTE
            # Mínimo 1 columna, máximo razonable 8 (para no hacer widgets demasiado pequeños)
            cols = max(1, min(cols_fit, 8))
            
            # ✅ AJUSTE INTELIGENTE SEGÚN NÚMERO DE MESAS
            total_mesas = len(self.filtered_mesas) if hasattr(self, 'filtered_mesas') else 0
            
            # Si hay pocas mesas, no usar todas las columnas posibles para mejor balance visual
            if total_mesas > 0:
                if total_mesas <= 3:
                    cols = min(cols, total_mesas)  # No más columnas que mesas
                elif total_mesas <= 6:
                    cols = min(cols, 3)  # Máximo 3 columnas para 4-6 mesas                elif total_mesas <= 12:
                    cols = min(cols, 4)  # Máximo 4 columnas para 7-12 mesas
                # Para más mesas, usar el cálculo completo
            
            return cols
            
        except Exception as e:
            logger.error(f"Error calculando columnas óptimas: {e}")
            return 3  # Fallback seguro
    
    def _clear_mesa_widgets(self):
        """Limpia todos los widgets de mesa del layout"""
        try:
            # Limpiar widgets de mesas
            self.mesa_widgets.clear()
            
            # Limpiar layout
            while self.mesas_layout.count():
                child = self.mesas_layout.takeAt(0)
                if child and child.widget():
                    widget = child.widget()
                    if widget:
                        widget.deleteLater()
                        
        except Exception as e:
            logger.error(f"Error limpiando widgets de mesa: {e}")
    
    def _show_no_mesas_message(self):
        """Muestra mensaje cuando no hay mesas que mostrar"""
        try:
            from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
            
            # Container para el mensaje
            message_container = QFrame()
            message_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f8f9fa, stop:1 #e9ecef);
                    border: 2px dashed #dee2e6;
                    border-radius: 16px;
                    padding: 30px;
                    margin: 20px;
                }
            """)
            
            container_layout = QVBoxLayout(message_container)
            container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.setSpacing(16)
            
            # Determinar mensaje según filtros
            icon_text = "🔍"
            title_text = "No se encontraron mesas"
            subtitle_text = "No hay mesas que coincidan con los filtros aplicados"
            
            # Icono grande
            icon_label = QLabel(icon_text)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("""
                QLabel {
                    font-size: 48px;
                    color: #6c757d;
                    margin: 10px;
                }
            """)
            container_layout.addWidget(icon_label)
            
            # Título principal
            title_label = QLabel(title_text)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    color: #495057;
                    margin: 8px;
                }
            """)
            container_layout.addWidget(title_label)
            
            # Subtítulo
            subtitle_label = QLabel(subtitle_text)
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #6c757d;
                    margin: 4px;
                }
            """)
            container_layout.addWidget(subtitle_label)
            
            # Agregar al layout principal ocupando todo el espacio
            self.mesas_layout.addWidget(message_container, 0, 0, 1, 4)
            
        except Exception as e:
            logger.error(f"Error mostrando mensaje de no mesas: {e}")
    
    def _on_nueva_mesa_clicked(self):
        """Maneja el click del botón Nueva Mesa con selección de zona"""
        try:
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
                0,  # Índice inicial
                False  # No editable
            )
            
            if ok and zona_seleccionada:
                # Calcular el próximo número de mesa disponible
                numeros_existentes = []
                for mesa in self.mesas:
                    if mesa.numero.isdigit():
                        numeros_existentes.append(int(mesa.numero))
                siguiente_numero = max(numeros_existentes, default=0) + 1
                
                # Mostrar diálogo de confirmación con los detalles
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
                    # Emitir señal con los datos de la nueva mesa
                    self.nueva_mesa_con_zona_requested.emit(siguiente_numero, 4, zona_seleccionada)
                    logger.info(f"Solicitada creación de mesa #{siguiente_numero} en zona '{zona_seleccionada}'")
                    
        except Exception as e:
            logger.error(f"Error al manejar creación de nueva mesa: {e}")
            QMessageBox.critical(
                self, 
                "Error", 
                f"Error al procesar la creación de mesa: {str(e)}"
            )
        
    def _on_eliminar_mesa_clicked(self):
        """Maneja el click del botón Eliminar Mesa"""
        try:
            # Verificar si hay mesas disponibles
            if not self.mesas:
                QMessageBox.information(
                    self, 
                    "Sin mesas", 
                    "No hay mesas disponibles para eliminar."
                )
                return
            
            # Crear lista de opciones con números de mesa
            opciones_mesas = []
            mesas_disponibles = []
            
            for mesa in self.mesas:
                # Solo permitir eliminar mesas libres para evitar problemas
                if mesa.estado == "libre":
                    texto_opcion = f"Mesa {mesa.numero} - {mesa.zona}"
                    opciones_mesas.append(texto_opcion)
                    mesas_disponibles.append(mesa)
            
            if not opciones_mesas:
                QMessageBox.information(
                    self, 
                    "Sin mesas disponibles", 
                    "No hay mesas libres disponibles para eliminar.\n"
                    "Solo se pueden eliminar mesas que estén libres."
                )
                return
            
            # Mostrar diálogo de selección
            opcion_seleccionada, ok = QInputDialog.getItem(
                self,
                "Eliminar Mesa",
                "Selecciona la mesa que deseas eliminar:",
                opciones_mesas,
                0,  # Índice inicial
                False  # No editable
            )
            
            if ok and opcion_seleccionada:
                # Encontrar la mesa seleccionada
                indice_seleccionado = opciones_mesas.index(opcion_seleccionada)
                mesa_a_eliminar = mesas_disponibles[indice_seleccionado]
                
                # Confirmar eliminación
                respuesta = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Estás seguro de que quieres eliminar la Mesa {mesa_a_eliminar.numero}?\n"
                    f"Esta acción no se puede deshacer.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if respuesta == QMessageBox.StandardButton.Yes:
                    # Emitir señal para eliminar la mesa
                    self.eliminar_mesa_requested.emit(mesa_a_eliminar.id)
                    logger.info(f"Solicitada eliminación de mesa ID: {mesa_a_eliminar.id}")
                    
        except Exception as e:
            logger.error(f"Error al manejar eliminación de mesa: {e}")
            QMessageBox.critical(
                self, 
                "Error", 
                f"Error al procesar la eliminación de mesa: {str(e)}"
            )

    # ==================== MÉTODOS PARA SECCIONES ENCAPSULADAS ====================
    
    def create_title_section_encapsulated(self):
        """Crea la sección de título encapsulada con mejor diseño"""
        title_container = QFrame()
        title_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #fafbfc);
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 16px;
            }
        """)
        
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(8, 8, 8, 8)
        title_layout.setSpacing(4)
        
        # Header con icono y título
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        title_icon = QLabel("🍽️")
        title_icon.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(title_icon)
        
        title_label = QLabel("Gestión de Mesas")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #1e293b;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        title_layout.addLayout(header_layout)
        
        # Subtítulo descriptivo
        subtitle = QLabel("Control y monitoreo")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #64748b;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        title_layout.addWidget(subtitle)
        
        return title_container
    
    def create_premium_separator(self):
        """Crea un separador premium con gradiente mejorado"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 transparent, 
                    stop:0.5 #cbd5e1, 
                    stop:1 transparent);
                width: 1px;
                margin: 8px 12px;
                border: none;
            }
        """)
        separator.setMaximumWidth(1)
        separator.setMinimumHeight(60)
        return separator
    def create_stats_section_encapsulated(self):
        """Crea la sección de estadísticas encapsulada con mejor diseño"""
        stats_container = QFrame()
        stats_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #fafbfc);
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 12px;
            }
        """)
        
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setContentsMargins(8, 8, 8, 8)
        stats_layout.setSpacing(8)
        
        # Etiqueta de sección
        section_label = QLabel("Estadísticas en Vivo")
        section_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 600;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 4px;
            }
        """)
        stats_layout.addWidget(section_label)
        
        # Grid de estadísticas
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(8)
        
        # Crear widgets de estadísticas encapsulados
        mesas_ocupadas = self.create_encapsulated_stat("🪑", "0/8", "#3b82f6")
        venta_hoy = self.create_encapsulated_stat("💰", "€0.00", "#10b981")
        comandas_activas = self.create_encapsulated_stat("⏰", "0", "#f59e0b")
        tiempo_prom = self.create_encapsulated_stat("⏱️", "0min", "#8b5cf6")
        
        stats_grid.addWidget(mesas_ocupadas)
        stats_grid.addWidget(venta_hoy)
        stats_grid.addWidget(comandas_activas)
        stats_grid.addWidget(tiempo_prom)
        
        stats_layout.addLayout(stats_grid)
        
        return stats_container
    
    def create_encapsulated_stat(self, icon: str, value: str, color: str):
        """Crea un widget de estadística individual encapsulado"""
        stat_widget = QFrame()
        stat_widget.setStyleSheet(f"""
            QFrame {{
                background: #ffffff;
                border: 1px solid {color}30;
                border-radius: 8px;
                padding: 4px 8px;
                min-width: 60px;
                max-width: 80px;
            }}
            QFrame:hover {{
                background: {color}08;
                border-color: {color}60;
            }}
        """)
        
        layout = QVBoxLayout(stat_widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 14px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
          # Valor
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                font-weight: bold;
                color: {color};
                text-align: center;
            }}
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        return stat_widget
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # 🏆 MÉTODOS ULTRA-PREMIUM PARA HEADER ENCAPSULADO
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def create_title_section_ultra_premium(self) -> QFrame:
        """🏷️ Crea sección de título ultra-premium CONTEXTUALIZADA y PROFESIONAL"""
        section = QFrame()
        section.setObjectName("TitleSectionUltraPremium")
        section.setFixedSize(260, 75)  # Dimensiones ajustadas para mejor proporción
        
        # Estilo premium con gradiente sutil y bordes refinados
        section.setStyleSheet("""
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
            }        """)
        
        layout = QHBoxLayout(section)
        layout.setContentsMargins(12, 6, 12, 6)  # Márgenes más balanceados para mejor distribución vertical
        layout.setSpacing(10)  # Espaciado óptimo entre icono y texto
        
        # ICONO PREMIUM - TAMAÑO OPTIMIZADO para la proporción del contenedor
        icon_container = QFrame()
        icon_container.setFixedSize(52, 52)  # Tamaño perfecto para el contexto ajustado
        icon_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5b21b6, 
                    stop:0.3 #4c1d95, 
                    stop:0.7 #3730a3, 
                    stop:1 #312e81);
                border: 2px solid #1e1b4b;
                border-radius: 26px;
            }
        """)
        
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel("🍽️")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: white;
                background: transparent;
                border: none;
            }        """)
        icon_layout.addWidget(icon_label)
        
        layout.addWidget(icon_container)
          # 📝 Contenedor de textos OPTIMIZADO para máxima legibilidad sin cortes
        text_container = QVBoxLayout()
        text_container.setSpacing(1)  # Pequeño espaciado entre elementos para mejor separación visual
        text_container.setContentsMargins(0, 0, 0, 0)  # Sin márgenes internos para aprovechar espacio
        
        # TÍTULO PRINCIPAL - OPTIMIZADO para legibilidad perfecta sin cortes
        title_label = QLabel("GESTIÓN DE MESAS")
        title_label.setStyleSheet("""
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
        """)
        text_container.addWidget(title_label)
        
        # SUBTÍTULO - TAMAÑO OPTIMIZADO para máxima legibilidad y mejor jerarquía visual
        subtitle_label = QLabel("Terminal Punto de Venta")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #64748b;
                font-weight: 500;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                margin: 0px;
                padding: 0px;
                line-height: 1.0;
            }
        """)
        text_container.addWidget(subtitle_label)
        
        # ESPACIADOR FLEXIBLE - Empuja el estado hacia la parte inferior del contenedor
        text_container.addStretch()
        
        # INDICADOR DE ESTADO - PEGADO AL FONDO, compacto pero visible y contrastado
        status_label = QLabel("● Sistema Activo")
        status_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #16a34a;
                font-weight: bold;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                margin: 0px;
                padding: 0px;
                line-height: 1.0;
            }
        """)
        text_container.addWidget(status_label)
        
        layout.addLayout(text_container)
        layout.addStretch()
        
        return section
    
    def create_ultra_premium_separator(self) -> QFrame:
        """🔹 Separador vertical ultra-premium con gradiente y efectos"""
        separator = QFrame()
        separator.setFixedWidth(3)
        separator.setMinimumHeight(60)
        separator.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(203, 213, 225, 0.3),
                    stop:0.2 rgba(148, 163, 184, 0.8),
                    stop:0.5 rgba(100, 116, 139, 1.0),
                    stop:0.8 rgba(148, 163, 184, 0.8),                    stop:1 rgba(203, 213, 225, 0.3));
                border-radius: 2px;
                margin: 8px 16px;
            }
        """)
        return separator
    
    def create_filters_section_ultra_premium(self) -> QFrame:
        """🔍 Sección de filtros ultra-premium optimizada"""
        section = QFrame()
        section.setObjectName("FiltersSectionUltraPremium")
        section.setStyleSheet("""
            QFrame#FiltersSectionUltraPremium {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f0f9ff, 
                    stop:0.5 #e0f2fe, 
                    stop:1 #f0f9ff);
                border: 1px solid #0ea5e9;
                border-radius: 12px;
                padding: 8px;
                margin: 4px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(6)
        
        # 🏷️ Header compacto con título ajustado al contenido
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        # Título compacto que no ocupa todo el ancho
        section_title = QLabel("🔍 Filtros y Control")
        section_title.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: bold;
                color: #0369a1;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #dbeafe, stop:1 #bfdbfe);
                border: 1px solid #93c5fd;
                border-radius: 6px;
                padding: 4px 8px;
                margin: 0px;
            }
        """)
        header_layout.addWidget(section_title)
        header_layout.addStretch(1)  # Espaciado flexible para empujar título a la izquierda
        
        layout.addLayout(header_layout)
        
        # 🎛️ Container principal de controles compacto
        controls_container = QFrame()
        controls_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 4px;
            }
        """)
        
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setContentsMargins(8, 6, 8, 6)
        controls_layout.setSpacing(8)        
        # 🔍 Búsqueda compacta optimizada
        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 2px;
            }
        """)
        search_layout = QVBoxLayout(search_container)
        search_layout.setContentsMargins(4, 2, 4, 2)
        search_layout.setSpacing(1)
        
        search_label = QLabel("🔍")
        search_label.setStyleSheet("color: #64748b; font-size: 10px; margin: 0px;")
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar mesa...")
        self.search_input.setFixedWidth(140)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 4px 6px;
                font-size: 11px;
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                background: #f8fafc;
            }
            QLineEdit:hover {
                border-color: #60a5fa;
            }
        """)
        self.search_input.textChanged.connect(self.apply_search)
        search_layout.addWidget(self.search_input)
        controls_layout.addWidget(search_container)
        
        # 📍 Zona compacta optimizada
        zone_container = QFrame()
        zone_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 2px;
            }
        """)
        zone_layout = QVBoxLayout(zone_container)
        zone_layout.setContentsMargins(4, 2, 4, 2)
        zone_layout.setSpacing(1)
        
        zone_label = QLabel("📍 Zona")
        zone_label.setStyleSheet("color: #64748b; font-size: 10px; margin: 0px;")
        zone_layout.addWidget(zone_label)
        
        self.zone_combo = QComboBox()
        self.zone_combo.addItems(["Todas", "Terraza", "Interior", "Privada", "Barra"])
        self.zone_combo.setFixedWidth(100)
        self.zone_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 4px 6px;
                font-size: 11px;
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                min-width: 80px;
            }
            QComboBox:focus {
                border-color: #2563eb;
                background: #f8fafc;
            }
            QComboBox:hover {
                border-color: #60a5fa;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background: #f1f5f9;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #0ea5e9;
                margin-right: 4px;
            }
        """)
        self.zone_combo.currentTextChanged.connect(self._on_zone_changed)
        zone_layout.addWidget(self.zone_combo)
        controls_layout.addWidget(zone_container)
        
        # 🚦 Estado compacto optimizado
        status_container = QFrame()
        status_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 2px;
            }
        """)
        status_layout = QVBoxLayout(status_container)
        status_layout.setContentsMargins(4, 2, 4, 2)
        status_layout.setSpacing(1)
        
        status_label = QLabel("🚦 Estado")
        status_label.setStyleSheet("color: #64748b; font-size: 10px; margin: 0px;")
        status_layout.addWidget(status_label)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Todos", "Libre", "Ocupada", "Reservada"])
        self.status_combo.setFixedWidth(90)
        self.status_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 4px 6px;
                font-size: 11px;
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                min-width: 70px;
            }
            QComboBox:focus {
                border-color: #2563eb;
                background: #f8fafc;
            }
            QComboBox:hover {
                border-color: #60a5fa;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background: #f1f5f9;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #0ea5e9;
                margin-right: 4px;
            }
        """)
        self.status_combo.currentTextChanged.connect(self._on_status_changed)
        status_layout.addWidget(self.status_combo)
        controls_layout.addWidget(status_container)
        
        # 🎯 Separador visual elegante
        separator_frame = QFrame()
        separator_frame.setFixedWidth(2)
        separator_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #cbd5e1, stop:0.5 #94a3b8, stop:1 #cbd5e1);
                border: none;
                border-radius: 1px;
            }
        """)
        controls_layout.addWidget(separator_frame)
          # 📋 Menú de Acciones de Mesa
        acciones_container = QFrame()
        acciones_container.setStyleSheet("""
            QFrame {
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid #34d399;
                border-radius: 6px;
                padding: 2px;
            }
        """)
        acciones_layout = QVBoxLayout(acciones_container)
        acciones_layout.setContentsMargins(4, 2, 4, 2)
        acciones_layout.setSpacing(1)
        
        acciones_label = QLabel("📋 Acciones")
        acciones_label.setStyleSheet("color: #059669; font-size: 10px; margin: 0px; font-weight: bold;")
        acciones_layout.addWidget(acciones_label)
        
        # Botón principal con menú desplegable
        acciones_btn = QPushButton("Gestionar ▼")
        acciones_btn.setFixedWidth(100)
        acciones_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                border: 1px solid #047857;
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 11px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                text-align: left;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #059669, stop:1 #047857);
            }
            QPushButton:pressed {
                background: #047857;
            }
            QPushButton::menu-indicator {
                width: 0px; /* Ocultar el indicador por defecto */
            }
        """)
        
        # Crear menú desplegable
        menu_acciones = QMenu(acciones_btn)
        menu_acciones.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 2px solid #10b981;
                border-radius: 8px;
                padding: 4px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 8px 16px;
                margin: 2px;
                border-radius: 4px;
                color: #374151;
            }
            QMenu::item:selected {
                background-color: #10b981;
                color: white;
            }
            QMenu::item:pressed {
                background-color: #059669;
            }
            QMenu::separator {
                height: 1px;
                background-color: #e5e7eb;
                margin: 4px 8px;
            }
        """)
        
        # Acción: Nueva Mesa
        accion_nueva = QAction("➕ Nueva Mesa", menu_acciones)
        accion_nueva.setToolTip("Crear una nueva mesa")
        accion_nueva.triggered.connect(self._on_nueva_mesa_clicked)
        menu_acciones.addAction(accion_nueva)
        
        # Separador
        menu_acciones.addSeparator()
        
        # Acción: Eliminar Mesa
        accion_eliminar = QAction("🗑️ Eliminar Mesa", menu_acciones)
        accion_eliminar.setToolTip("Eliminar una mesa existente")
        accion_eliminar.triggered.connect(self._on_eliminar_mesa_clicked)
        menu_acciones.addAction(accion_eliminar)
        
        # Conectar menú al botón
        acciones_btn.setMenu(menu_acciones)
        
        acciones_layout.addWidget(acciones_btn)
        controls_layout.addWidget(acciones_container)
        
        # 🔄 Botón actualizar compacto optimizado
        refresh_container = QFrame()
        refresh_container.setStyleSheet("""
            QFrame {
                background: rgba(59, 130, 246, 0.1);
                border: 1px solid #60a5fa;
                border-radius: 6px;
                padding: 2px;
            }
        """)
        refresh_layout = QVBoxLayout(refresh_container)
        refresh_layout.setContentsMargins(4, 2, 4, 2)
        refresh_layout.setSpacing(1)
        
        refresh_label = QLabel("🔄")
        refresh_label.setStyleSheet("color: #2563eb; font-size: 10px; margin: 0px;")
        refresh_layout.addWidget(refresh_label)
        
        refresh_btn = QPushButton("⟳")
        refresh_btn.setFixedSize(30, 24)
        refresh_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #bfdbfe;
                border-radius: 4px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f9ff);
                font-size: 14px;
                color: #2563eb;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f9ff, stop:1 #e0f2fe);
                border-color: #60a5fa;
            }
            QPushButton:pressed {
                background: #e0f2fe;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_mesas)
        refresh_btn.setToolTip("🔄 Actualizar vista de mesas")
        refresh_layout.addWidget(refresh_btn)
        controls_layout.addWidget(refresh_container)
        
        layout.addWidget(controls_container)
        return section
    
    def create_stats_section_ultra_premium(self) -> QFrame:
        """📊 Sección de estadísticas ultra-premium"""
        section = QFrame()
        section.setObjectName("StatsSectionUltraPremium")
        section.setStyleSheet("""
            QFrame#StatsSectionUltraPremium {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fef7ff, 
                    stop:0.5 #fdf4ff, 
                    stop:1 #fef7ff);
                border: 1px solid #d946ef;
                border-radius: 12px;
                padding: 8px;
                margin: 4px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # Título de sección
        section_title = QLabel("📊 Estadísticas en Tiempo Real")
        section_title.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #a21caf;
                margin-bottom: 4px;
            }
        """)
        layout.addWidget(section_title)
        
        # Container de estadísticas
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(8)
          # Configuración de estadísticas ultra-premium
        stats_config = [
            ("📍", "Zonas", "0", "#8b5cf6", "#f3e8ff"),
            ("🍽️", "Total", "0", "#3b82f6", "#dbeafe"), 
            ("🟢", "Libres", "0", "#10b981", "#d1fae5"),
            ("🔴", "Ocupadas", "0", "#ef4444", "#fee2e2"),
            ("📅", "Reservadas", "0", "#f59e0b", "#fef3c7")
        ]
        
        # Crear widgets específicos con referencias individuales
        self.zonas_widget = self.create_ultra_premium_stat("📍", "Zonas", "0", "#8b5cf6", "#f3e8ff")
        self.mesas_total_widget = self.create_ultra_premium_stat("🍽️", "Total", "0", "#3b82f6", "#dbeafe")
        self.mesas_libres_widget = self.create_ultra_premium_stat("🟢", "Libres", "0", "#10b981", "#d1fae5")
        self.mesas_ocupadas_widget = self.create_ultra_premium_stat("🔴", "Ocupadas", "0", "#ef4444", "#fee2e2")
        self.mesas_reservadas_widget = self.create_ultra_premium_stat("📅", "Reservadas", "0", "#f59e0b", "#fef3c7")
        
        # Agregar widgets al layout
        stats_layout.addWidget(self.zonas_widget)
        stats_layout.addWidget(self.mesas_total_widget)
        stats_layout.addWidget(self.mesas_libres_widget)
        stats_layout.addWidget(self.mesas_ocupadas_widget)
        stats_layout.addWidget(self.mesas_reservadas_widget)
        
        # Almacenar referencias para actualización
        self.stats_widgets = [
            {'widget': self.zonas_widget, 'type': 'zonas', 'icon': "📍", 'label': "Zonas"},
            {'widget': self.mesas_total_widget, 'type': 'total', 'icon': "🍽️", 'label': "Total"},
            {'widget': self.mesas_libres_widget, 'type': 'libres', 'icon': "🟢", 'label': "Libres"},
            {'widget': self.mesas_ocupadas_widget, 'type': 'ocupadas', 'icon': "🔴", 'label': "Ocupadas"},
            {'widget': self.mesas_reservadas_widget, 'type': 'reservadas', 'icon': "📅", 'label': "Reservadas"}
        ]
        
        layout.addLayout(stats_layout)
        return section
    
    def create_ultra_premium_stat(self, icon: str, label: str, value: str, color: str, bg_color: str) -> QFrame:
        """📈 Widget de estadística ultra-premium individual"""
        stat_widget = QFrame()
        stat_widget.setFixedSize(80, 70)
        stat_widget.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {bg_color}, stop:1 white);
                border: 2px solid {color};
                border-radius: 10px;
                margin: 2px;
            }}
            QFrame:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,                    stop:0 white, stop:1 {bg_color});
                border-width: 3px;
            }}
        """)
        
        layout = QVBoxLayout(stat_widget)
        layout.setContentsMargins(6, 8, 6, 8)
        layout.setSpacing(4)
        
        # Icono + Label
        header_label = QLabel(f"{icon}")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                color: {color};
                font-weight: bold;
                margin: 0px;
            }}
        """)
        layout.addWidget(header_label)
        
        # Valor principal
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {color};
                margin: 0px;
            }}
        """)
        layout.addWidget(value_label)
          # Descripción
        desc_label = QLabel(label)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet(f"""
            QLabel {{
                font-size: 9px;
                color: {color};
                font-weight: bold;
                margin: 0px;
            }}
        """)
        layout.addWidget(desc_label)
        
        return stat_widget
    
    def create_status_section_ultra_premium(self) -> QFrame:
        """ℹ️ Sección de estado del sistema ultra-premium - COMPACTA y LEGIBLE"""
        section = QFrame()
        section.setObjectName("StatusSectionUltraPremium")
        section.setFixedHeight(52)  # Altura fija compacta como el contenedor de título
        section.setStyleSheet("""
            QFrame#StatusSectionUltraPremium {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f0fdf4, 
                    stop:0.5 #dcfce7, 
                    stop:1 #f0fdf4);
                border: 1px solid #22c55e;
                border-radius: 12px;
                padding: 0px;
                margin: 4px;
                min-width: 180px;
                max-width: 220px;
            }
        """)
        
        layout = QHBoxLayout(section)
        layout.setContentsMargins(10, 6, 10, 6)  # Márgenes más pequeños para aprovechar espacio
        layout.setSpacing(6)
        
        # CONTENEDOR DE TEXTO OPTIMIZADO - Distribución vertical sin cortes
        text_container = QVBoxLayout()
        text_container.setContentsMargins(0, 0, 0, 0)
        text_container.setSpacing(1)  # Espaciado mínimo para máxima compactación
        
        # TÍTULO PRINCIPAL - COMPACTO pero LEGIBLE
        title_label = QLabel("ESTADO DEL SISTEMA")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                font-weight: bold;
                color: #15803d;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                letter-spacing: 0.1px;
                margin: 0px;
                padding: 0px;
                line-height: 1.0;
            }
        """)
        text_container.addWidget(title_label)
        
        # ESTADO PRINCIPAL - OPTIMIZADO para textos variables de filtros
        self.status_info = QLabel("Sistema Activo")
        self.status_info.setWordWrap(True)  # Permite el salto de línea si es necesario
        self.status_info.setStyleSheet("""
            QLabel {
                font-size: 9px;
                color: #166534;
                font-weight: 500;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                margin: 0px;
                padding: 0px;
                line-height: 1.1;
            }
        """)
        text_container.addWidget(self.status_info)
        
        # ESPACIADOR FLEXIBLE - Empuja la conectividad hacia la parte inferior
        text_container.addStretch()
        
        # INDICADOR DE CONECTIVIDAD - PEGADO AL FONDO, ultra-compacto
        connectivity_layout = QHBoxLayout()
        connectivity_layout.setContentsMargins(0, 0, 0, 0)
        connectivity_layout.setSpacing(3)  # Espaciado reducido
        
        connection_indicator = QLabel("●")
        connection_indicator.setStyleSheet("""
            QLabel {
                font-size: 8px;
                color: #16a34a;
                margin: 0px;
                padding: 0px;
                line-height: 1.0;
            }
        """)
        connectivity_layout.addWidget(connection_indicator)
        
        connection_text = QLabel("Conectado")
        connection_text.setStyleSheet("""
            QLabel {
                font-size: 8px;
                color: #15803d;
                font-weight: bold;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                margin: 0px;
                padding: 0px;
                line-height: 1.0;
            }
        """)
        connectivity_layout.addWidget(connection_text)
        connectivity_layout.addStretch()
        
        text_container.addLayout(connectivity_layout)
        
        layout.addLayout(text_container)
        layout.addStretch()
        
        return section
    
    # ==================== MÉTODOS DE APOYO ULTRA-PREMIUM ====================
    
    def update_ultra_premium_stats(self):
        """🔄 Actualiza todas las estadísticas ultra-premium"""
        try:
            if not hasattr(self, 'mesas') or not self.mesas:
                return
                
            # Calcular estadísticas avanzadas
            total_mesas = len(self.mesas)
            mesas_ocupadas = len([m for m in self.mesas if hasattr(m, 'estado') and m.estado == 'ocupada'])
            mesas_libres = total_mesas - mesas_ocupadas
            mesas_reservadas = len([m for m in self.mesas if hasattr(m, 'estado') and m.estado == 'reservada'])
            
            # Zonas únicas
            zonas_unicas = len(set(getattr(m, 'zona', 'Sin zona') for m in self.mesas))
            
            # Venta total simulada (esto vendría del sistema real)
            venta_total = sum([getattr(m, 'venta_hoy', 0.0) for m in self.mesas])
            
            # Comandas activas (simulado)
            comandas_activas = len([m for m in self.mesas if hasattr(m, 'estado') and m.estado == 'ocupada'])
            
            # Tiempo promedio (simulado)
            tiempo_promedio = 25 if comandas_activas > 0 else 0
              # Actualizar widgets específicos si existen
            if hasattr(self, 'mesas_ocupadas_widget'):
                self._update_stat_widget(self.mesas_ocupadas_widget, f"{mesas_ocupadas}")
            
            if hasattr(self, 'mesas_total_widget'):
                self._update_stat_widget(self.mesas_total_widget, f"{total_mesas}")
            
            if hasattr(self, 'mesas_libres_widget'):
                self._update_stat_widget(self.mesas_libres_widget, f"{mesas_libres}")
            
            if hasattr(self, 'mesas_reservadas_widget'):
                self._update_stat_widget(self.mesas_reservadas_widget, f"{mesas_reservadas}")
                
            if hasattr(self, 'zonas_widget'):
                self._update_stat_widget(self.zonas_widget, f"{zonas_unicas}")
              # Actualizar estado del sistema
            if hasattr(self, 'status_info'):
                status_text = f"Mostrando {len(self.filtered_mesas)} de {total_mesas} mesas"
                self.status_info.setText(status_text)
                
        except Exception as e:
            logger.error(f"Error actualizando estadísticas ultra-premium: {e}")
    
    def _update_stat_widget(self, widget, new_value: str):
        """🔧 Actualiza el valor de un widget de estadística específico"""
        try:
            if not widget or not hasattr(widget, 'layout') or not widget.layout():
                return
                
            layout = widget.layout()
            
            # Buscar el label del valor (generalmente el último widget)
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget():
                    child_widget = item.widget()
                    if isinstance(child_widget, QLabel):
                        # Si es el label del valor (tiene texto numérico o con símbolos)
                        current_text = child_widget.text()
                        if any(c.isdigit() or c in ['€', '/', 'min'] for c in current_text):
                            child_widget.setText(new_value)
                            child_widget.update()
                            return
                            
        except Exception as e:
            logger.error(f"Error actualizando widget de estadística: {e}")
    
    def apply_ultra_premium_theme(self):
        """🎨 Aplica el tema ultra-premium a todo el componente"""
        try:
            # Estilo base del componente principal
            self.setStyleSheet("""
                MesasArea {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #fefefe, 
                        stop:0.3 #fdfdfd, 
                        stop:0.7 #f9fafb, 
                        stop:1 #f3f4f6);
                    border: 2px solid #e5e7eb;
                    border-radius: 20px;
                    margin: 4px;
                }
            """)
            
            logger.info("Tema ultra-premium aplicado exitosamente")
            
        except Exception as e:
            logger.error(f"Error aplicando tema ultra-premium: {e}")
    
    def refresh_ultra_premium_display(self):
        """🚀 Refresca toda la visualización ultra-premium"""
        try:
            # Actualizar datos
            self.apply_filters()
            
            # Actualizar estadísticas
            self.update_ultra_premium_stats()
            
            # Actualizar tema si es necesario
            self.apply_ultra_premium_theme()
            
            logger.info("Display ultra-premium refrescado exitosamente")
            
        except Exception as e:
            logger.error(f"Error refrescando display ultra-premium: {e}")
      # ==================== INTEGRACIÓN CON SISTEMA EXISTENTE ====================
    
    def initialize_ultra_premium_mode(self):
        """🏆 Inicializa el modo ultra-premium completo"""
        try:
            # Aplicar tema ultra-premium
            self.apply_ultra_premium_theme()
            
            # Configurar actualizaciones automáticas
            if hasattr(self, 'mesas') and self.mesas:
                self.update_ultra_premium_stats()
            
            # Establecer modo de vista
            self.view_mode = "ultra-premium"
            
            logger.info("🏆 Modo ultra-premium inicializado exitosamente")
            
        except Exception as e:
            logger.error(f"Error inicializando modo ultra-premium: {e}")
    
    def toggle_ultra_premium_mode(self, enable: bool = True):
        """🔄 Activa/desactiva el modo ultra-premium"""
        try:
            if enable:
                self.initialize_ultra_premium_mode()
                logger.info("🏆 Modo ultra-premium ACTIVADO")
            else:
                # Volver al modo estándar
                self.view_mode = "grid"
                logger.info("📋 Modo estándar ACTIVADO")
                
        except Exception as e:
            logger.error(f"Error cambiando modo ultra-premium: {e}")
    
    def resizeEvent(self, event):
        """Maneja el redimensionamiento del widget para recalcular columnas dinámicamente"""
        super().resizeEvent(event)
        
        # Solo proceder si hay mesas para mostrar
        if not hasattr(self, 'filtered_mesas') or not self.filtered_mesas:
            return
        
        # Evitar llamadas excesivas usando un timer con delay
        if hasattr(self, '_resize_timer'):
            self._resize_timer.stop()
        
        from PyQt6.QtCore import QTimer
        self._resize_timer = QTimer()
        self._resize_timer.timeout.connect(self._on_resize_complete)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.start(150)  # 150ms delay para evitar redibujado excesivo
    
    def _on_resize_complete(self):
        """Callback cuando se completa el redimensionamiento - recalcula el grid"""
        try:
            # Verificar si necesitamos recalcular las columnas
            new_cols = self._calculate_optimal_columns()
            
            # Solo repoblar si el número de columnas cambió
            if not hasattr(self, '_last_columns') or self._last_columns != new_cols:
                self._last_columns = new_cols
                self.populate_grid()
                
        except Exception as e:
            logger.error(f"Error en redimensionamiento: {e}")
    
    def _refresh_layout(self):
        """Refresca el layout aplicando los filtros actuales"""
        # Usar el método existente para refrescar las mesas
        self.refresh_mesas()
