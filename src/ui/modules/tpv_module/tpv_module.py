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
        
        # Dashboard de métricas (refactorizado)
        self.dashboard = TPVDashboard(self.tpv_service)
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
            }        """)
        
        # Pestaña de mesas (refactorizada)
        self.create_mesas_tab_refactored()
        # Pestañas de desarrollo (mantenemos las existentes)
        self.create_venta_rapida_tab()
        self.create_reportes_tab()
        
        layout.addWidget(self.tab_widget, 1)
        
    def create_mesas_tab_refactored(self):
        """Crea la pestaña de mesas con layout contextualizado y grid principal"""
        mesas_widget = QWidget()
        layout = QVBoxLayout(mesas_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Área de mesas como elemento principal (incluye filtros integrados y estadísticas)
        self.mesas_area = MesasArea()        # Conectar señales
        self.mesas_area.mesa_clicked.connect(self._on_mesa_clicked)
        self.mesas_area.nueva_mesa_requested.connect(self.nueva_mesa)
        self.mesas_area.nueva_mesa_con_zona_requested.connect(self.nueva_mesa_con_zona)
        self.mesas_area.eliminar_mesa_requested.connect(self.eliminar_mesa)
        
        # El área de mesas ocupa todo el espacio disponible
        layout.addWidget(self.mesas_area, 1)
        
        # Ya no necesitamos el FiltersPanel separado - ahora está integrado en MesasArea
        
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
            
            # Actualizar área de mesas con los datos actuales
            if hasattr(self, 'mesas_area'):                self.mesas_area.set_mesas(self.mesas)
            
            # Las estadísticas compactas se actualizan automáticamente en MesasArea
                
        except Exception as e:            logger.error(f"Error refrescando componentes: {e}")
    
    # ======= MÉTODOS SIMPLIFICADOS (DELEGADOS AL CONTROLADOR) =======
    
    def nueva_mesa(self):
        """Crea una nueva mesa usando el controlador"""
        try:
            # Usar nomenclatura automática contextualizada
            self.mesa_controller.crear_mesa(4, "Principal")
        except Exception as e:
            logger.error(f"Error creando nueva mesa: {e}")
            QMessageBox.critical(self, "Error", f"Error al crear mesa: {str(e)}")
    
    def nueva_mesa_con_zona(self, capacidad: int, zona: str):
        """Crea una nueva mesa con parámetros específicos usando el controlador"""
        try:
            self.mesa_controller.crear_mesa(capacidad, zona)
            logger.info(f"Mesa creada en zona '{zona}' con capacidad {capacidad}")
        except Exception as e:
            logger.error(f"Error creando nueva mesa con zona: {e}")
            QMessageBox.critical(self, "Error", f"Error al crear mesa: {str(e)}")
    
    def eliminar_mesa(self, mesa_id: int):
        """Elimina una mesa usando el controlador"""
        try:
            if self.mesa_controller.eliminar_mesa(mesa_id):
                logger.info(f"Mesa {mesa_id} eliminada correctamente")
                QMessageBox.information(self, "Éxito", "Mesa eliminada correctamente")
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar la mesa")
        except Exception as e:
            logger.error(f"Error eliminando mesa: {e}")
            QMessageBox.critical(self, "Error", f"Error al eliminar mesa: {str(e)}")
    
    def load_data(self):
        """Carga los datos iniciales usando el controlador"""
        try:
            logger.info("Cargando datos del TPV...")
            self.mesa_controller.cargar_mesas()
            
            if self.tpv_service:
                self.productos = self.tpv_service.get_productos()
                logger.info("Datos del TPV cargados correctamente")                # Cargar datos iniciales en MesasArea si ya está inicializada
                if hasattr(self, 'mesas_area') and self.mesas:
                    self.mesas_area.set_mesas(self.mesas)
                
                # Las estadísticas compactas se actualizan automáticamente en MesasArea
                logger.info("Datos del TPV cargados correctamente")
                    
            else:
                logger.warning("No hay servicio TPV disponible")
        except Exception as e:
            logger.error(f"Error cargando datos del TPV: {e}")    
    # MÉTODO ELIMINADO: on_search_changed - La búsqueda ahora se maneja en el header ultra-premium
    # def on_search_changed(self, text):
    #     """Maneja cambios en el campo de búsqueda"""
    #     if hasattr(self, 'mesas_area'):
    #         self.mesas_area.apply_search(text)
    
    def venta_rapida(self):
        """TODO: Implementar venta rápida"""
        QMessageBox.information(self, "Venta Rápida", "Funcionalidad en desarrollo")
    
    def cerrar_caja(self):
        """TODO: Implementar cierre de caja"""
        QMessageBox.information(self, "Cerrar Caja", "Funcionalidad en desarrollo")
    
    def update_compact_stats(self):
        """Actualiza las estadísticas compactas basadas en datos reales"""
        try:
            if not hasattr(self, 'mesas_area') or not self.mesas_area:
                return
                
            # Obtener datos reales de las mesas
            total_mesas = len(self.mesas)
            mesas_libres = len([m for m in self.mesas if m.estado == "libre"])
            mesas_ocupadas = len([m for m in self.mesas if m.estado == "ocupada"])
            mesas_reservadas = len([m for m in self.mesas if m.estado == "reservada"])
            
            # Obtener zonas únicas
            zonas_activas = len(set(m.zona for m in self.mesas)) if self.mesas else 0
              # Actualizar las estadísticas
            stats_config = [
                ("📍", "Zonas Activas", str(zonas_activas)),
                ("🍽️", "Mesas Totales", str(total_mesas)), 
                ("🟢", "Disponibles", str(mesas_libres)),
                ("🔴", "Ocupadas", str(mesas_ocupadas))
            ]
            
            # TODO: Implementar actualización dinámica de estadísticas cuando sea necesario
                                
        except Exception as e:
            logger.error(f"Error actualizando estadísticas compactas: {e}")

    def calculate_real_stats(self) -> dict:
        """Calcula estadísticas reales basadas en los datos actuales de mesas"""
        try:
            if not self.mesas:
                return {
                    "zonas_activas": "0",
                    "mesas_totales": "0", 
                    "disponibles": "0",
                    "ocupadas": "0"
                }
            
            # Calcular estadísticas reales
            zonas_unicas = set(mesa.zona for mesa in self.mesas)
            mesas_totales = len(self.mesas)
            disponibles = len([m for m in self.mesas if m.estado == "libre"])
            ocupadas = len([m for m in self.mesas if m.estado == "ocupada"])
            
            return {
                "zonas_activas": str(len(zonas_unicas)),
                "mesas_totales": str(mesas_totales),
                "disponibles": str(disponibles), 
                "ocupadas": str(ocupadas)
            }
            
        except Exception as e:
            logger.error(f"Error calculando estadísticas: {e}")
            return {
                "zonas_activas": "0",
                "mesas_totales": "0",                "disponibles": "0",
                "ocupadas": "0"
            }
    
    def create_compact_stat(self, icon: str, label: str, value: str) -> QWidget:
        """Crea una estadística compacta mejorada y más visible"""
        from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        
        # Frame principal con estilos más sólidos
        stat_widget = QFrame()
        stat_widget.setFrameStyle(QFrame.Shape.StyledPanel)
        stat_widget.setLineWidth(1)
        
        # Layout vertical con más espaciado
        layout = QVBoxLayout(stat_widget)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)
        
        # Etiqueta superior (título)
        label_widget = QLabel(f"{icon} {label}")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Font para el título
        title_font = QFont()
        title_font.setPointSize(9)
        title_font.setBold(False)
        label_widget.setFont(title_font)
        label_widget.setStyleSheet("color: #64748b; margin: 0px; padding: 0px;")
        layout.addWidget(label_widget)
        
        # Valor inferior (destacado)
        value_widget = QLabel(value)
        value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)        # Font para el valor
        value_font = QFont()
        value_font.setPointSize(18)  # Aumentar tamaño de fuente
        value_font.setBold(True)
        value_widget.setFont(value_font)
        value_widget.setStyleSheet("color: #1f2937; margin: 0px; padding: 0px; background-color: transparent;")  # Color más oscuro
        layout.addWidget(value_widget)
        
        # Estilo del frame contenedor con más contraste
        stat_widget.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                margin: 2px;
            }
            QFrame:hover {
                border-color: #2563eb;
            }
        """)
        
        # Tamaño fijo más grande para mejor visibilidad
        stat_widget.setFixedSize(130, 70)
        
        return stat_widget

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Crear y mostrar el módulo TPV
    tpv = TPVModule()
    tpv.show()
    tpv.resize(1200, 800)
    
    sys.exit(app.exec())
