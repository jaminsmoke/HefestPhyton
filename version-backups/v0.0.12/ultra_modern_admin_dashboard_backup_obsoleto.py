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
from ...components.dashboard_metric_components import (
    UltraModernTheme, UltraModernDashboard, UltraModernCard, 
    UltraModernMetricCard, UltraModernBaseWidget
)

# Importar el DataManager centralizado  
from utils.real_data_manager import RealDataManager

logger = logging.getLogger(__name__)


class UltraModernAdminDashboard(UltraModernBaseWidget):
    """Dashboard administrativo ultra-moderno V3"""
    
    # Señales para comunicación con la ventana principal
    metric_selected = pyqtSignal(str, dict)  # título, datos
    action_requested = pyqtSignal(str)  # acción
    
    def __init__(self, auth_service=None, db_manager=None, parent=None):
        super().__init__(parent)
        self.theme = UltraModernTheme()
        
        # DIAGNÓSTICO: Verificar que llega al constructor
        logger.warning("🔍 DIAGNÓSTICO DASHBOARD: Iniciando constructor del dashboard")
        logger.warning(f"🔍 DIAGNÓSTICO DASHBOARD: auth_service recibido: {auth_service}")
        logger.warning(f"🔍 DIAGNÓSTICO DASHBOARD: db_manager recibido: {db_manager}")
        
        # Servicios compatibles con la aplicación principal
        self.auth_service = auth_service
        self.db_manager = db_manager
        
        # DIAGNÓSTICO: Verificar usuario actual si hay auth_service
        if self.auth_service:
            current_user = self.auth_service.current_user
            is_authenticated = self.auth_service.is_authenticated
            logger.warning(f"🔍 DIAGNÓSTICO DASHBOARD: Usuario actual: {current_user.name if current_user else 'None'}")
            logger.warning(f"🔍 DIAGNÓSTICO DASHBOARD: Autenticado: {is_authenticated}")
        else:
            logger.warning("🔍 DIAGNÓSTICO DASHBOARD: No se recibió auth_service")        # DataManager centralizado para obtener SOLO datos reales
        self.data_manager = RealDataManager(db_manager)
        self.metric_cards = []  # Lista de tarjetas de métricas
        
        logger.warning("🔍 DIAGNÓSTICO DASHBOARD: Llamando a setup_admin_dashboard")
        self.setup_admin_dashboard()
        logger.warning("🔍 DIAGNÓSTICO DASHBOARD: Llamando a setup_admin_features")
        self.setup_admin_features()
        logger.warning("🔍 DIAGNÓSTICO DASHBOARD: Llamando a setup_centralized_data_refresh")
        self.setup_centralized_data_refresh()
        logger.warning("🔍 DIAGNÓSTICO DASHBOARD: Dashboard inicializado completamente")
        logger.info("Dashboard Admin V3 Ultra-Moderno inicializado con DataManager centralizado")
    
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
          # Styling del dashboard con fondo sofisticado y textura sutil
        self.setStyleSheet(f"""
            UltraModernAdminDashboard {{
                background-color: {self.theme.COLORS['gray_50']};
                background-image: 
                    radial-gradient(circle at 10% 20%, {self.theme.COLORS['gray_100']} 0%, transparent 20%),
                    radial-gradient(circle at 90% 80%, {self.theme.COLORS['gray_200']} 0%, transparent 20%),
                    radial-gradient(circle at 50% 50%, {self.theme.COLORS['white']} 0%, transparent 70%),
                    linear-gradient(#e9ecef 1px, transparent 1px),
                    linear-gradient(90deg, #e9ecef 1px, transparent 1px);
                background-size: 
                    100% 100%, 
                    100% 100%, 
                    100% 100%,
                    40px 40px,
                    40px 40px;
                background-blend-mode: multiply;
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
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-top: none;
                background: {self.theme.COLORS['white']};
                border-bottom-left-radius: {self.theme.RADIUS['lg']}px;
                border-bottom-right-radius: {self.theme.RADIUS['lg']}px;
                margin-top: -1px;
            }}
            QTabBar::tab {{
                background: {self.theme.COLORS['gray_100']};
                color: {self.theme.COLORS['gray_700']};
                padding: 16px 24px;
                margin-right: 2px;
                margin-bottom: 0px;
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-bottom: none;
                border-top-left-radius: {self.theme.RADIUS['lg']}px;
                border-top-right-radius: {self.theme.RADIUS['lg']}px;
                font-size: {self.theme.TYPOGRAPHY['text_base']}px;
                font-weight: {self.theme.TYPOGRAPHY['font_medium'].value};
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                background: {self.theme.COLORS['white']};
                color: {self.theme.COLORS['blue_600']};
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-bottom: 1px solid {self.theme.COLORS['white']};
                font-weight: {self.theme.TYPOGRAPHY['font_semibold'].value};
                margin-bottom: -1px;
            }}
            QTabBar::tab:hover:!selected {{
                background: {self.theme.COLORS['blue_50']};
                color: {self.theme.COLORS['blue_700']};
                border-color: {self.theme.COLORS['blue_200']};
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
        """Crear tab de métricas principales con estructura mejorada"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Contenedor principal con estilo similar a las otras pestañas
        main_card = UltraModernCard(padding=24)
          # Crear sub-pestañas para métricas
        metrics_tab_widget = QTabWidget()
        metrics_tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 2px solid {self.theme.COLORS['gray_200']};
                background: {self.theme.COLORS['gray_50']};
                border-top-left-radius: 0px;
                border-top-right-radius: {self.theme.RADIUS['md']}px;
                border-bottom-left-radius: {self.theme.RADIUS['md']}px;
                border-bottom-right-radius: {self.theme.RADIUS['md']}px;
                margin-top: 0px;
                padding: 0px;
            }}
            QTabBar::tab {{
                background: {self.theme.COLORS['gray_100']};
                color: {self.theme.COLORS['gray_600']};
                padding: 12px 20px;
                margin-right: 0px;
                margin-bottom: -1px;
                margin-left: 0px;
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-bottom: none;
                border-top-left-radius: {self.theme.RADIUS['md']}px;
                border-top-right-radius: {self.theme.RADIUS['md']}px;
                font-size: {self.theme.TYPOGRAPHY['text_sm']}px;
                font-weight: {self.theme.TYPOGRAPHY['font_medium'].value};
                min-width: 100px;
            }}
            QTabBar::tab:first {{
                margin-left: 0px;
                border-top-left-radius: 0px;
                border-top-right-radius: {self.theme.RADIUS['md']}px;
            }}
            QTabBar::tab:!first {{
                margin-left: 0px;
            }}
            QTabBar::tab:selected {{
                background: {self.theme.COLORS['gray_50']};
                color: {self.theme.COLORS['blue_600']};
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-bottom: 1px solid {self.theme.COLORS['gray_50']};
                font-weight: {self.theme.TYPOGRAPHY['font_semibold'].value};
                z-index: 1;
            }}
            QTabBar::tab:hover:!selected {{
                background: {self.theme.COLORS['blue_50']};
                color: {self.theme.COLORS['blue_700']};
                border-color: {self.theme.COLORS['blue_200']};
            }}
            QTabBar {{
                qproperty-drawBase: 0;
            }}
        """)
        
        # Sub-pestaña 1: Vista Resumen
        summary_tab = self.create_summary_view()
        metrics_tab_widget.addTab(summary_tab, "📊 Resumen")
        
        # Sub-pestaña 2: Vista Detallada  
        detailed_tab = self.create_detailed_view()
        metrics_tab_widget.addTab(detailed_tab, "📈 Detalles")        
        # Sub-pestaña 3: Vista Comparativa
        comparison_tab = self.create_comparison_view()
        metrics_tab_widget.addTab(comparison_tab, "🔄 Comparar")
        
        main_card.main_layout.addWidget(metrics_tab_widget)
        layout.addWidget(main_card)
        
        return widget

    def create_summary_view(self):
        """Crear vista de resumen de métricas principales"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area para métricas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{ 
                background: transparent; 
                border: none;
            }}
            QScrollBar:vertical {{
                background: {self.theme.COLORS['gray_100']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme.COLORS['gray_300']};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme.COLORS['gray_500']};
            }}
        """)
        
        # Contenedor de métricas
        metrics_container = QWidget()
        metrics_layout = QGridLayout(metrics_container)
        metrics_layout.setSpacing(self.theme.SPACING['lg'])
        metrics_layout.setContentsMargins(0, 0, 0, 0)
        self.metrics_layout = metrics_layout  # Guardar referencia para resizeEvent
        
        # Datos de métricas hosteleras con objetivos e iconos        # NO usar valores hardcodeados - Solo datos reales del RealDataManager
        # Las métricas se crearán dinámicamente cuando lleguen datos del data_manager
        admin_metrics = []
                "title": "Ventas Diarias", 
                "value": "2,450", 
                "unit": "€", 
                "target": "3,000",
                "trend": "+18.5%", 
                "type": "success",
                "icon": "💰"
            },            {
                "title": "Comandas Activas", 
                "value": "28", 
                "unit": "", 
                "target": "35",
                "trend": "+12.3%", 
                "type": "primary",
                "icon": "📋"
            },            {
                "title": "Mesas Ocupadas", 
                "value": "18", 
                "unit": "/24", 
                "target": "22",
                "trend": "+25.7%", 
                "type": "success",
                "icon": "🪑"
            },            {
                "title": "Ticket Promedio", 
                "value": "24.50", 
                "unit": "€", 
                "target": "28.00",
                "trend": "+8.9%", 
                "type": "info",
                "icon": "🧾"
            },            {
                "title": "Satisfacción Cliente", 
                "value": "4.6", 
                "unit": "★", 
                "target": "4.8",
                "trend": "+2.1%", 
                "type": "success",
                "icon": "⭐"
            },            {
                "title": "Tiempo Servicio", 
                "value": "8.5", 
                "unit": "min", 
                "target": "7.0",
                "trend": "-15.3%", 
                "type": "success",
                "icon": "⏱️"
            },            {
                "title": "Rotación Mesas", 
                "value": "3.2", 
                "unit": "veces", 
                "target": "3.5",
                "trend": "+5.8%", 
                "type": "primary",
                "icon": "�"
            },            {
                "title": "Inventario Bebidas", 
                "value": "87", 
                "unit": "%", 
                "target": "95",
                "trend": "-8.2%", 
                "type": "warning",
                "icon": "🍺"
            },            {
                "title": "Margen Bruto", 
                "value": "68.5", 
                "unit": "%", 
                "target": "70.0",
                "trend": "+2.1%", 
                "type": "success",
                "icon": "📊"
            },]
        
        # Crear tarjetas de métricas con nuevas funcionalidades
        self.metric_cards = []
        for i, metric in enumerate(admin_metrics):
            card = UltraModernMetricCard(
                title=metric["title"],
                value=metric["value"],
                unit=metric["unit"],
                trend=metric["trend"],
                target=metric["target"],
                metric_type=metric["type"],
                icon=metric["icon"]
            )
              # Conectar eventos
            card.clicked.connect(
                lambda checked, title=metric["title"], data=metric: 
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
    
    def create_detailed_view(self):
        """Crear vista detallada con todas las métricas"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area para métricas detalladas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{ 
                background: transparent; 
                border: none;
            }}
            QScrollBar:vertical {{
                background: {self.theme.COLORS['gray_100']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme.COLORS['gray_300']};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme.COLORS['gray_500']};
            }}
        """)
          # Contenedor de métricas detalladas con fondo gris
        metrics_container = QWidget()
        metrics_container.setStyleSheet(f"""
            QWidget {{
                background: {self.theme.COLORS['gray_50']};
                border: none;
            }}
        """)
        metrics_layout = QGridLayout(metrics_container)
        metrics_layout.setSpacing(self.theme.SPACING['md'])
        metrics_layout.setContentsMargins(16, 16, 16, 16)
        
        # Todas las métricas para vista detallada
        detailed_metrics = [
            {"title": "Ventas Diarias", "value": "2,450", "unit": "€", "target": "3,000", "trend": "+18.5%", "type": "success", "icon": "💰"},
            {"title": "Comandas Activas", "value": "28", "unit": "", "target": "35", "trend": "+12.3%", "type": "primary", "icon": "📋"},
            {"title": "Mesas Ocupadas", "value": "18", "unit": "/24", "target": "22", "trend": "+25.7%", "type": "success", "icon": "🪑"},
            {"title": "Ticket Promedio", "value": "24.50", "unit": "€", "target": "28.00", "trend": "+8.9%", "type": "info", "icon": "🧾"},
            {"title": "Satisfacción Cliente", "value": "4.6", "unit": "★", "target": "4.8", "trend": "+2.1%", "type": "success", "icon": "⭐"},
            {"title": "Tiempo Servicio", "value": "8.5", "unit": "min", "target": "7.0", "trend": "-15.3%", "type": "success", "icon": "⏱️"},
            {"title": "Rotación Mesas", "value": "3.2", "unit": "veces", "target": "3.5", "trend": "+5.8%", "type": "primary", "icon": "🔄"},
            {"title": "Inventario Bebidas", "value": "87", "unit": "%", "target": "95", "trend": "-8.2%", "type": "warning", "icon": "🍺"},
            {"title": "Margen Bruto", "value": "68.5", "unit": "%", "target": "70.0", "trend": "+2.1%", "type": "success", "icon": "📊"},
        ]
        
        # Crear tarjetas detalladas (3 columnas)
        for i, metric in enumerate(detailed_metrics):
            card = UltraModernMetricCard(
                title=metric["title"],
                value=metric["value"],
                unit=metric["unit"],
                trend=metric["trend"],
                target=metric["target"],
                metric_type=metric["type"],
                icon=metric["icon"]            )
            
            card.clicked.connect(
                lambda checked, title=metric["title"], data=metric: 
                self.metric_selected.emit(title, data)
            )
            
            row = i // 3  # 3 columnas
            col = i % 3
            metrics_layout.addWidget(card, row, col)
        
        scroll_area.setWidget(metrics_container)
        layout.addWidget(scroll_area)
        
        return widget
    
    def create_comparison_view(self):
        """Crear vista comparativa con gráficos y tendencias"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Placeholder para vista comparativa
        comparison_card = UltraModernCard(padding=32)
        
        content_layout = QVBoxLayout()
        
        title = QLabel("Vista Comparativa")
        title_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        title_font.setPointSize(self.theme.TYPOGRAPHY['text_3xl'])
        title_font.setWeight(self.theme.TYPOGRAPHY['font_bold'])
        title.setFont(title_font)
        title.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel("Análisis comparativo de métricas y tendencias")
        description_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        description_font.setPointSize(self.theme.TYPOGRAPHY['text_lg'])
        description.setFont(description_font)
        description.setStyleSheet(f"color: {self.theme.COLORS['gray_600']};")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Información de funcionalidades futuras
        features_info = QLabel("""
        🔄 Comparación mensual/semanal
        📊 Gráficos de tendencias
        📈 Análisis de crecimiento
        🎯 Seguimiento de objetivos
        📋 Reportes personalizados
        """)
        features_info_font = QFont(self.theme.TYPOGRAPHY['font_family'])
        features_info_font.setPointSize(self.theme.TYPOGRAPHY['text_base'])
        features_info.setFont(features_info_font)
        features_info.setStyleSheet(f"color: {self.theme.COLORS['gray_700']};")
        features_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        content_layout.addWidget(title)
        content_layout.addWidget(description)
        content_layout.addStretch()
        content_layout.addWidget(features_info)
        content_layout.addStretch()
        
        comparison_card.main_layout.addLayout(content_layout)
        layout.addWidget(comparison_card)
        
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
        
    def refresh_admin_data(self):
        """
        Actualizar manualmente todos los datos administrativos
        Método requerido por la interfaz del dashboard
        """
        logger.info("Actualizando datos administrativos manualmente")
        if hasattr(self, 'data_manager'):
            self.data_manager.fetch_all_real_data()
        else:
            logger.warning("DataManager no disponible para actualización manual")
    
    def setup_data_refresh(self):
        """Configurar actualización automática de datos con DataManager centralizado"""
        # Conectar señales del DataManager
        self.data_manager.data_updated.connect(self.on_all_data_updated)
        self.data_manager.metric_updated.connect(self.on_metric_data_updated)
        self.data_manager.error_occurred.connect(self.on_data_error)
        
        # Iniciar monitoreo centralizado
        self.data_manager.start_monitoring(5000)  # 5 segundos
        logger.info("DataManager centralizado configurado (5s)")
    
    def setup_centralized_data_refresh(self):
        """Alias para compatibilidad"""
        self.setup_data_refresh()
    
    def on_all_data_updated(self, data: dict):
        """Callback cuando se actualizan todos los datos"""
        logger.debug(f"Datos actualizados: {len(data)} métricas")
        # Actualizar todas las tarjetas con los nuevos datos
        self.update_all_metric_cards(data)
    
    def on_metric_data_updated(self, metric_name: str, metric_data: dict):
        """Callback cuando se actualiza una métrica específica"""
        # Encontrar y actualizar la tarjeta correspondiente
        for card in self.metric_cards:
            if hasattr(card, 'metric_name') and card.metric_name == metric_name:
                card.update_data(metric_data)
                break
    
    def on_data_error(self, error_message: str):
        """Callback cuando ocurre un error en la obtención de datos"""
        logger.error(f"Error en DataManager: {error_message}")
        # TODO: Mostrar notificación de error al usuario    
    def update_all_metric_cards(self, data: dict):
        """Actualizar todas las tarjetas de métricas con nuevos datos hosteleros"""
        # Mapeo de datos del DataManager a las métricas hosteleras
        data_mapping = {
            'Ventas Diarias': 'ventas_diarias',
            'Comandas Activas': 'comandas_activas', 
            'Mesas Ocupadas': 'mesas_ocupadas',
            'Ticket Promedio': 'ticket_promedio',
            'Satisfacción Cliente': 'satisfaccion_cliente',
            'Tiempo Servicio': 'tiempo_servicio',
            'Rotación Mesas': 'rotacion_mesas',
            'Inventario Bebidas': 'inventario_bebidas',
            'Margen Bruto': 'margen_bruto'
        }
        
        # Actualizar cada tarjeta con datos reales
        for card in self.metric_cards:
            if hasattr(card, 'title'):
                data_key = data_mapping.get(card.title)
                if data_key and data_key in data:
                    metric_data = data[data_key]
                    # Usar las nuevas funcionalidades de las tarjetas mejoradas
                    card.update_metric_data(
                        value=metric_data.get('value', card.value),
                        trend=metric_data.get('trend', card.trend),
                        target=metric_data.get('target', card.target)
                    )                    # Actualizar tooltip dinámico
                    card.update_tooltip()
                    logger.debug(f"Tarjeta '{card.title}' actualizada con datos reales")
                  # Guardar referencia del mapeo para futuras actualizaciones                card.metric_name = data_key
        
    def on_metric_selected(self, title, data):
        """Manejar selección de métrica"""
        logger.info(f"Métrica seleccionada: {title}")
        self.metric_selected.emit(title, data)
    
    def on_action_requested(self, action):
        """Manejar solicitud de acción"""
        logger.info(f"Acción solicitada: {action}")
        self.action_requested.emit(action)
    
    def resizeEvent(self, event):
        """
        Manejo responsivo del dashboard
        Adapta el número de columnas según el ancho disponible
        """
        super().resizeEvent(event)
        
        if hasattr(self, 'metrics_layout'):
            width = event.size().width()
            
            # Determinar número de columnas basado en el ancho
            if width > 1200:
                columns = 3  # Pantalla completa
            elif width > 800:
                columns = 2  # Tablet/pantalla mediana
            else:
                columns = 1  # Móvil/pantalla pequeña
            
            # Reorganizar tarjetas si es necesario
            self.update_grid_columns(columns)
    
    def update_grid_columns(self, columns: int):
        """
        Actualiza el layout de grid para usar el número especificado de columnas
        
        Args:
            columns: Número de columnas a usar
        """
        if not hasattr(self, 'metrics_layout') or not hasattr(self, 'metric_cards'):
            return
        
        # Remover todas las tarjetas del layout actual
        for i in reversed(range(self.metrics_layout.count())):
            item = self.metrics_layout.itemAt(i)
            if item:
                self.metrics_layout.removeItem(item)
        
        # Reorganizar tarjetas en el nuevo grid
        for i, card in enumerate(self.metric_cards):
            row = i // columns
            col = i % columns
            self.metrics_layout.addWidget(card, row, col)
        
        logger.debug(f"Grid reorganizado a {columns} columnas")

    def cleanup(self):
        """Limpieza al cerrar el dashboard"""
        if hasattr(self, 'data_manager'):
            self.data_manager.stop_monitoring()
        logger.info("Dashboard Admin V3 limpiado")
