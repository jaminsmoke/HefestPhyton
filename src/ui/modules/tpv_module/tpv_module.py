"""
Módulo TPV - Terminal Punto de Venta Profesional (Refactorizado)
Versión: v0.0.13
"""

import logging
from typing import List, Optional, Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSplitter,
    QLabel, QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QTabWidget, QFrame, QScrollArea, QGroupBox, QSizePolicy, QHeaderView,
    QSpacerItem, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

from ui.modules.module_base_interface import BaseModule
from services.tpv_service import TPVService, Mesa, Producto, Comanda, LineaComanda

# Importar componentes refactorizados
from .components.tpv_dashboard import TPVDashboard
from .components.mesas_area import MesasArea
from .widgets.filters_panel import FiltersPanel
from .widgets.statistics_panel import StatisticsPanel
from .controllers.mesa_controller import MesaController

logger = logging.getLogger(__name__)



class TPVModule(BaseModule):
    """Módulo TPV principal con interfaz moderna y profesional (Refactorizado)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Inicializar servicios
        self._init_services()
        
        # Inicializar controladores
        self._init_controllers()
        
        # Configurar UI y cargar datos
        self.setup_ui()
        self.load_data()
        
    def _init_services(self):
        """Inicializa los servicios necesarios"""
        try:
            from data.db_manager import DatabaseManager
            
            self.db_manager = DatabaseManager()
            logger.info("TPVModule: DatabaseManager creado correctamente")
        except Exception as e:
            logger.error(f"TPVModule: Error creando DatabaseManager: {e}")
            self.db_manager = None
            
        self.tpv_service = TPVService(self.db_manager)
        self.mesas: List[Mesa] = []
        self.productos: List[Producto] = []
        self.current_comanda: Optional[Comanda] = None
        
    def _init_controllers(self):
        """Inicializa los controladores"""
        self.mesa_controller = MesaController(self.tpv_service)
        
        # Conectar señales del controlador
        self.mesa_controller.mesa_created.connect(self._on_mesa_created)
        self.mesa_controller.mesa_updated.connect(self._on_mesa_updated)  
        self.mesa_controller.mesa_deleted.connect(self._on_mesa_deleted)
        self.mesa_controller.mesas_updated.connect(self._on_mesas_updated)
        self.mesa_controller.error_occurred.connect(self._on_controller_error)
        
    def setup_ui(self):
        """Configura la interfaz principal refactorizada"""
        layout = self.main_layout
        
        # Header profesional
        self.create_header(layout)
        
        # Dashboard de métricas (refactorizado)
        self.dashboard = TPVDashboard(self.tpv_service)
        layout.addWidget(self.dashboard)
        layout.addWidget(self.dashboard)
        
        # Línea separadora
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setLineWidth(1)
        separator.setStyleSheet("color: #e0e0e0; background-color: #e0e0e0;")
        layout.addWidget(separator)
        
        # Área principal con pestañas refactorizada
        self.create_main_tabs(layout)
        
        # Barra de estado
        self.create_status_bar(layout)
        
    def create_header(self, layout: QVBoxLayout):
        """Crea el header principal con gradiente azul"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2196f3, stop:1 #1976d2);
                border: none;
            }
        """)
        header_frame.setFixedHeight(80)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        # Título principal
        title_label = QLabel("🍽️ Terminal Punto de Venta")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Barra de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar mesa, producto, comanda...")
        self.search_input.setFixedWidth(280)
        self.search_input.setFixedHeight(34)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 17px;
                padding: 6px 14px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                background-color: white;
                color: #333;
                border-color: rgba(255, 255, 255, 0.8);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.7);
            }
        """)
        self.search_input.textChanged.connect(self.on_search_changed)
        header_layout.addWidget(self.search_input)
        
        # Botones de acción rápida
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        quick_actions = [
            ("🆕 Nueva Mesa", self.nueva_mesa),
            ("⚡ Venta Rápida", self.venta_rapida),
            ("💰 Cerrar Caja", self.cerrar_caja)
        ]
        
        for text, callback in quick_actions:
            btn = QPushButton(text)
            btn.setFixedHeight(34)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 17px;
                    color: white;
                    font-weight: bold;
                    padding: 6px 14px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                    border-color: rgba(255, 255, 255, 0.6);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.1);
                }
            """)
            btn.clicked.connect(callback)
            actions_layout.addWidget(btn)
        
        header_layout.addLayout(actions_layout)
        layout.addWidget(header_frame)
    
    def create_main_tabs(self, layout: QVBoxLayout):
        """Crea las pestañas principales usando componentes refactorizados"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #fafafa;
            }
            QTabBar::tab {
                background-color: #e8e8e8;
                color: #555;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background-color: #2196f3;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #1976d2;
                color: white;
            }
        """)
        
        # Pestaña de mesas (refactorizada)
        self.create_mesas_tab_refactored()
        
        # Pestañas de desarrollo (mantenemos las existentes)
        self.create_venta_rapida_tab()
        self.create_reportes_tab()
        
        layout.addWidget(self.tab_widget, 1)
        
    def create_mesas_tab_refactored(self):
        """Crea la pestaña de mesas usando componentes refactorizados"""
        mesas_widget = QWidget()
        layout = QVBoxLayout(mesas_widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Panel de filtros (refactorizado)
        self.filters_panel = FiltersPanel()
        self.filters_panel.filters_changed.connect(self._on_filters_changed)
        layout.addWidget(self.filters_panel)
        
        # Panel de estadísticas (refactorizado)
        self.statistics_panel = StatisticsPanel(self.tpv_service)
        layout.addWidget(self.statistics_panel)
          # Área de mesas (refactorizada)
        self.mesas_area = MesasArea()
        # Conectar señales
        self.mesas_area.mesa_clicked.connect(self._on_mesa_clicked)
        self.mesas_area.nueva_mesa_requested.connect(self.nueva_mesa)
        layout.addWidget(self.mesas_area, 1)
        
        self.tab_widget.addTab(mesas_widget, "🍽️ Gestión de Mesas")
    
    def create_venta_rapida_tab(self):
        """Crea la pestaña de venta rápida"""
        venta_widget = QWidget()
        layout = QVBoxLayout(venta_widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Placeholder para venta rápida
        placeholder = QLabel("🚀 Venta Rápida - En desarrollo")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #666;
                margin: 50px;
            }
        """)
        layout.addWidget(placeholder)
        
        self.tab_widget.addTab(venta_widget, "⚡ Venta Rápida")
    
    def create_reportes_tab(self):
        """Crea la pestaña de reportes"""
        reportes_widget = QWidget()
        layout = QVBoxLayout(reportes_widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Placeholder para reportes
        placeholder = QLabel("📊 Reportes - En desarrollo")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #666;
                margin: 50px;
            }
        """)
        layout.addWidget(placeholder)
        
        self.tab_widget.addTab(reportes_widget, "📈 Reportes")
    
    def create_status_bar(self, layout: QVBoxLayout):
        """Crea la barra de estado"""
        status_frame = QFrame()
        status_frame.setFixedHeight(30)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
                padding: 4px 16px;
            }
        """)
        
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(8, 4, 8, 4)
        
        # Estado de conexión
        self.status_label = QLabel("✅ Conectado")
        self.status_label.setStyleSheet("color: #28a745; font-size: 12px;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        # Información del usuario
        user_label = QLabel("👤 Usuario: Admin")
        user_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        status_layout.addWidget(user_label)
        
        layout.addWidget(status_frame)

    # ======= CALLBACKS DEL CONTROLADOR =======
    
    def _on_mesa_created(self, mesa: Mesa):
        """Callback cuando se crea una mesa"""
        try:
            logger.info(f"Mesa {mesa.numero} creada exitosamente")
            self.mesas.append(mesa)
            self._refresh_all_components()
            QMessageBox.information(self, "Éxito", f"Mesa {mesa.numero} creada correctamente")
        except Exception as e:
            logger.error(f"Error procesando creación de mesa: {e}")
    
    def _on_mesa_updated(self, mesa: Mesa):
        """Callback cuando se actualiza una mesa"""
        try:
            logger.info(f"Mesa {mesa.numero} actualizada exitosamente")
            # Actualizar en la lista local
            for i, m in enumerate(self.mesas):
                if m.id == mesa.id:
                    self.mesas[i] = mesa
                    break
            self._refresh_all_components()
        except Exception as e:
            logger.error(f"Error procesando actualización de mesa: {e}")
    
    def _on_mesa_deleted(self, mesa_id: int):
        """Callback cuando se elimina una mesa"""
        try:
            logger.info(f"Mesa {mesa_id} eliminada exitosamente")
            self.mesas = [m for m in self.mesas if m.id != mesa_id]
            self._refresh_all_components()
        except Exception as e:
            logger.error(f"Error procesando eliminación de mesa: {e}")
    
    def _on_mesas_updated(self, mesas: List[Mesa]):
        """Callback cuando se actualiza la lista completa de mesas"""
        try:
            logger.info(f"Lista de mesas actualizada: {len(mesas)} mesas")
            self.mesas = mesas
            self._refresh_all_components()
        except Exception as e:
            logger.error(f"Error procesando actualización de mesas: {e}")
    
    def _on_controller_error(self, error_message: str):
        """Callback cuando ocurre un error en el controlador"""
        logger.error(f"Error del controlador: {error_message}")
        QMessageBox.critical(self, "Error", error_message)
    
    def _on_filters_changed(self, filters: Dict[str, Any]):
        """Callback cuando cambian los filtros"""
        try:
            logger.info(f"Filtros cambiados: {filters}")
            if hasattr(self, 'mesas_area'):
                self.mesas_area.apply_filters(filters)
        except Exception as e:
            logger.error(f"Error aplicando filtros: {e}")
    
    def _on_mesa_clicked(self, mesa: Mesa):
        """Callback cuando se hace clic en una mesa"""
        try:
            logger.info(f"Mesa {mesa.numero} seleccionada")
            # TODO: Abrir diálogo de gestión de mesa o menú contextual
            QMessageBox.information(self, "Mesa Seleccionada", 
                                  f"Mesa {mesa.numero} - Estado: {mesa.estado}")
        except Exception as e:
            logger.error(f"Error procesando clic en mesa: {e}")
    
    def _refresh_all_components(self):
        """Refresca todos los componentes después de cambios en los datos"""
        try:
            # Actualizar dashboard
            if hasattr(self, 'dashboard'):
                self.dashboard.update_metrics()
            
            # Actualizar panel de estadísticas
            if hasattr(self, 'statistics_panel'):
                self.statistics_panel.refresh_statistics()
            
            # Actualizar área de mesas
            if hasattr(self, 'mesas_area'):
                self.mesas_area.refresh_mesas()
                
        except Exception as e:
            logger.error(f"Error refrescando componentes: {e}")
    
    # ======= MÉTODOS SIMPLIFICADOS (DELEGADOS AL CONTROLADOR) =======
    
    def nueva_mesa(self):
        """Crea una nueva mesa usando el controlador"""
        try:
            # Por ahora, valores por defecto - en el futuro se abriría un diálogo
            numero = len(self.mesas) + 1
            self.mesa_controller.crear_mesa(numero, 4, "Principal")
        except Exception as e:
            logger.error(f"Error creando nueva mesa: {e}")
            QMessageBox.critical(self, "Error", f"Error al crear mesa: {str(e)}")
    
    def load_data(self):
        """Carga los datos iniciales usando el controlador"""
        try:
            logger.info("Cargando datos del TPV...")
            self.mesa_controller.cargar_mesas()
            
            if self.tpv_service:
                self.productos = self.tpv_service.get_productos()
                logger.info("Datos del TPV cargados correctamente")
            else:
                logger.warning("No hay servicio TPV disponible")
        except Exception as e:
            logger.error(f"Error cargando datos del TPV: {e}")
    
    def on_search_changed(self, text):
        """Maneja cambios en el campo de búsqueda"""
        if hasattr(self, 'mesas_area'):
            self.mesas_area.apply_search(text)
    
    def venta_rapida(self):
        """TODO: Implementar venta rápida"""
        QMessageBox.information(self, "Venta Rápida", "Funcionalidad en desarrollo")
    
    def cerrar_caja(self):
        """TODO: Implementar cierre de caja"""
        QMessageBox.information(self, "Cerrar Caja", "Funcionalidad en desarrollo")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Crear y mostrar el módulo TPV
    tpv = TPVModule()
    tpv.show()
    tpv.resize(1200, 800)
    
    sys.exit(app.exec())
