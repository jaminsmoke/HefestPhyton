"""
HEFEST - DASHBOARD ADMIN V3 ULTRA-MODERNO
Rediseño completo del dashboard administrativo con arquitectura visual V3
Sin dependencias del sistema antiguo, componentes modernos desde cero
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QTabWidget, QPushButton, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import logging
from datetime import datetime

# Importar el nuevo sistema ultra-moderno
from ...components.ultra_modern_system_v3 import (
    UltraModernTheme, UltraModernDashboard, UltraModernCard, 
    UltraModernMetricCard, UltraModernBaseWidget
)

logger = logging.getLogger(__name__)


class UltraModernAdminDashboard(UltraModernBaseWidget):
    """Dashboard administrativo ultra-moderno V3"""
    
    # Señales para comunicación con la ventana principal
    metric_selected = pyqtSignal(str, dict)  # título, datos
    action_requested = pyqtSignal(str)  # acción
    
    def __init__(self, auth_service=None, db_manager=None, parent=None):
        super().__init__(parent)
        self.theme = UltraModernTheme()
        
        # Servicios compatibles con la aplicación principal
        self.auth_service = auth_service
        self.db_manager = db_manager
        
        self.setup_admin_dashboard()
        self.setup_admin_features()
        self.setup_data_refresh()
        logger.info("Dashboard Admin V3 Ultra-Moderno inicializado")
    
    def setup_admin_dashboard(self):
        """Configurar estructura del dashboard administrativo"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(self.theme.SPACING['lg'])
        
        # Header del dashboard
        header = self.create_dashboard_header()
        main_layout.addWidget(header)
        
        # Contenido principal con tabs
        content_tabs = self.create_admin_tabs()
        main_layout.addWidget(content_tabs, 1)  # Expandir
        
        # Footer con información de estado
        footer = self.create_dashboard_footer()
        main_layout.addWidget(footer)
        
        # Styling del dashboard
        self.setStyleSheet(f"""
            UltraModernAdminDashboard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.theme.COLORS['gray_50']},
                    stop:1 {self.theme.COLORS['white']});
            }}
        """)
    
    def create_dashboard_header(self):
        """Crear header del dashboard"""
        header = UltraModernBaseWidget()
        header.setFixedHeight(100)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Título principal
        title_layout = QVBoxLayout()
        
        main_title = QLabel("Dashboard Administrativo")
        main_title_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        main_title_font.setPointSize(self.theme.TYPOGRAPHY['text_5xl'])
        main_title_font.setWeight(self.theme.TYPOGRAPHY['font_bold'])
        main_title.setFont(main_title_font)
        main_title.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")
        
        subtitle = QLabel("Sistema de gestión ultra-moderno V3")
        subtitle_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        subtitle_font.setPointSize(self.theme.TYPOGRAPHY['text_lg'])
        subtitle_font.setWeight(self.theme.TYPOGRAPHY['font_normal'])
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet(f"color: {self.theme.COLORS['gray_600']};")
        
        title_layout.addWidget(main_title)
        title_layout.addWidget(subtitle)
        
        # Botones de acción rápida
        actions_layout = QHBoxLayout()
        
        action_buttons = [
            ("🔄 Actualizar", "refresh"),
            ("⚙️ Configurar", "settings"),
            ("📊 Reportes", "reports"),
            ("🔔 Alertas", "alerts"),
        ]
        
        for text, action in action_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {self.theme.COLORS['blue_500']},
                        stop:1 {self.theme.COLORS['blue_600']});
                    color: {self.theme.COLORS['white']};
                    border: none;
                    border-radius: {self.theme.RADIUS['md']}px;
                    padding: {self.theme.SPACING['sm']}px {self.theme.SPACING['md']}px;
                    font-size: {self.theme.TYPOGRAPHY['text_sm']}px;
                    font-weight: {self.theme.TYPOGRAPHY['font_medium'].value};
                    min-width: 100px;
                }}
                QPushButton:hover {{
                    background: {self.theme.COLORS['blue_600']};
                }}
                QPushButton:pressed {{
                    background: {self.theme.COLORS['blue_700']};
                }}
            """)
            btn.clicked.connect(lambda checked, a=action: self.action_requested.emit(a))
            actions_layout.addWidget(btn)
        
        # Layout del header
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addLayout(actions_layout)
        
        # Styling del header
        header.setStyleSheet(f"""
            UltraModernBaseWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.theme.COLORS['white']},
                    stop:1 {self.theme.COLORS['blue_50']});
                border: 1px solid {self.theme.COLORS['blue_200']};
                border-radius: {self.theme.RADIUS['xl']}px;
            }}
        """)
        
        header.add_shadow('md')
        
        return header
    
    def create_admin_tabs(self):
        """Crear tabs administrativos"""
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background: transparent;
            }}
            QTabBar::tab {{
                background: {self.theme.COLORS['white']};
                color: {self.theme.COLORS['gray_700']};
                padding: 16px 24px;
                margin-right: 4px;
                border-top-left-radius: {self.theme.RADIUS['lg']}px;
                border-top-right-radius: {self.theme.RADIUS['lg']}px;
                font-size: {self.theme.TYPOGRAPHY['text_base']}px;
                font-weight: {self.theme.TYPOGRAPHY['font_medium'].value};
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.theme.COLORS['blue_500']},
                    stop:1 {self.theme.COLORS['blue_600']});
                color: {self.theme.COLORS['white']};
            }}
            QTabBar::tab:hover {{
                background: {self.theme.COLORS['blue_100']};
                color: {self.theme.COLORS['blue_700']};
            }}
        """)
        
        # Tab 1: Métricas Principales
        self.metrics_tab = self.create_metrics_tab()
        tab_widget.addTab(self.metrics_tab, "📊 Métricas")
        
        # Tab 2: Análisis Avanzado
        self.analytics_tab = self.create_analytics_tab()
        tab_widget.addTab(self.analytics_tab, "📈 Análisis")
        
        # Tab 3: Gestión de Sistema
        self.system_tab = self.create_system_tab()
        tab_widget.addTab(self.system_tab, "⚙️ Sistema")
        
        return tab_widget
    
    def create_metrics_tab(self):
        """Crear tab de métricas principales"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setSpacing(self.theme.SPACING['lg'])
        
        # Scroll area para métricas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background: transparent; }")
        
        # Contenedor de métricas
        metrics_container = QWidget()
        metrics_layout = QGridLayout(metrics_container)
        metrics_layout.setSpacing(self.theme.SPACING['lg'])
        metrics_layout.setContentsMargins(0, 0, 0, 0)
        
        # Datos de métricas administrativas
        admin_metrics = [
            {"title": "Ventas Totales", "value": "245,892", "unit": "€", "trend": "+18.5%", "type": "success"},
            {"title": "Pedidos Activos", "value": "1,847", "unit": "", "trend": "+12.3%", "type": "primary"},
            {"title": "Usuarios Registrados", "value": "15,234", "unit": "", "trend": "+25.7%", "type": "success"},
            {"title": "Inventario Valorado", "value": "892,451", "unit": "€", "trend": "+8.9%", "type": "info"},
            {"title": "Satisfacción Cliente", "value": "4.8", "unit": "★", "trend": "+2.1%", "type": "success"},
            {"title": "Tiempo Respuesta", "value": "1.2", "unit": "s", "trend": "-15.3%", "type": "success"},
            {"title": "Conversiones", "value": "12.4", "unit": "%", "trend": "+5.8%", "type": "primary"},
            {"title": "Abandono Carrito", "value": "23.1", "unit": "%", "trend": "-8.2%", "type": "success"},
            {"title": "Retorno Inversión", "value": "345", "unit": "%", "trend": "+22.1%", "type": "success"},
        ]
        
        # Crear tarjetas de métricas
        self.metric_cards = []
        for i, metric in enumerate(admin_metrics):
            card = UltraModernMetricCard(
                title=metric["title"],
                value=metric["value"],
                unit=metric["unit"],
                trend=metric["trend"],
                metric_type=metric["type"]
            )
            
            # Conectar eventos
            card.clicked.connect(
                lambda title=metric["title"], data=metric: 
                self.metric_selected.emit(title, data)
            )
            
            row = i // 3  # 3 columnas
            col = i % 3
            metrics_layout.addWidget(card, row, col)
            self.metric_cards.append(card)
        
        scroll_area.setWidget(metrics_container)
        layout.addWidget(scroll_area)
        
        return widget
    
    def create_analytics_tab(self):
        """Crear tab de análisis avanzado"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Placeholder para análisis avanzado
        placeholder = UltraModernCard(padding=32)
        
        content_layout = QVBoxLayout()
        
        title = QLabel("Análisis Avanzado")
        title_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        title_font.setPointSize(self.theme.TYPOGRAPHY['text_4xl'])
        title_font.setWeight(self.theme.TYPOGRAPHY['font_bold'])
        title.setFont(title_font)
        title.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel("Módulo de análisis de datos avanzado en desarrollo")
        description_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        description_font.setPointSize(self.theme.TYPOGRAPHY['text_lg'])
        description.setFont(description_font)
        description.setStyleSheet(f"color: {self.theme.COLORS['gray_600']};")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        content_layout.addWidget(title)
        content_layout.addWidget(description)
        content_layout.addStretch()
        
        placeholder.main_layout.addLayout(content_layout)
        layout.addWidget(placeholder)
        
        return widget
    
    def create_system_tab(self):
        """Crear tab de gestión del sistema"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Información del sistema
        system_info_card = UltraModernCard(padding=24)
        
        info_layout = QVBoxLayout()
        
        title = QLabel("Información del Sistema")
        title_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        title_font.setPointSize(self.theme.TYPOGRAPHY['text_3xl'])
        title_font.setWeight(self.theme.TYPOGRAPHY['font_bold'])
        title.setFont(title_font)
        title.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")
        
        system_details = QLabel(f"""
        🚀 Hefest Dashboard Admin V3 Ultra-Moderno
        
        📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        🎨 Sistema Visual: V3 Ultra-Moderno
        ⚡ Motor: PyQt6 nativo
        🔧 Estado: Operativo
        
        ✅ Características activas:
        • Dashboard con métricas en tiempo real
        • Componentes ultra-modernos sin filtros destructivos
        • Animaciones suaves y efectos visuales
        • Grid responsivo y adaptativo
        • Simulación de datos automática
        • Arquitectura modular y escalable
        """)
        
        system_details_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        system_details_font.setPointSize(self.theme.TYPOGRAPHY['text_base'])
        system_details.setFont(system_details_font)
        system_details.setStyleSheet(f"color: {self.theme.COLORS['gray_700']};")
        
        info_layout.addWidget(title)
        info_layout.addWidget(system_details)
        info_layout.addStretch()
        
        system_info_card.main_layout.addLayout(info_layout)
        layout.addWidget(system_info_card)
        
        return widget
    
    def create_dashboard_footer(self):
        """Crear footer del dashboard"""
        footer = UltraModernBaseWidget()
        footer.setFixedHeight(50)
        
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(20, 12, 20, 12)
        
        # Estado del sistema
        status_label = QLabel("🟢 Sistema Operativo")
        status_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        status_font.setPointSize(self.theme.TYPOGRAPHY['text_sm'])
        status_font.setWeight(self.theme.TYPOGRAPHY['font_medium'])
        status_label.setFont(status_font)
        status_label.setStyleSheet(f"color: {self.theme.COLORS['green_600']};")
        
        # Información de actualización
        update_label = QLabel(f"Última actualización: {datetime.now().strftime('%H:%M:%S')}")
        update_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        update_font.setPointSize(self.theme.TYPOGRAPHY['text_xs'])
        update_label.setFont(update_font)
        update_label.setStyleSheet(f"color: {self.theme.COLORS['gray_500']};")
        
        layout.addWidget(status_label)
        layout.addStretch()
        layout.addWidget(update_label)
        
        # Styling del footer
        footer.setStyleSheet(f"""
            UltraModernBaseWidget {{
                background: {self.theme.COLORS['gray_100']};
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-radius: {self.theme.RADIUS['md']}px;
            }}
        """)
        
        return footer
    
    def setup_admin_features(self):
        """Configurar características administrativas"""
        logger.info("Configurando características administrativas avanzadas")
    
    def setup_data_refresh(self):
        """Configurar actualización automática de datos"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_admin_data)
        self.refresh_timer.start(30000)  # Actualizar cada 30 segundos
        logger.info("Actualización automática de datos configurada (30s)")
    
    def refresh_admin_data(self):
        """Actualizar datos administrativos"""
        logger.debug("Actualizando datos administrativos...")
        # Los datos se actualizan automáticamente en cada tarjeta
        
    def on_metric_selected(self, title, data):
        """Manejar selección de métrica"""
        logger.info(f"Métrica seleccionada: {title}")
        self.metric_selected.emit(title, data)
    
    def on_action_requested(self, action):
        """Manejar solicitud de acción"""
        logger.info(f"Acción solicitada: {action}")
        self.action_requested.emit(action)
