# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from ..base_module import BaseModule
from .admin_metrics_widgets import AdminMetricsSection
        from core.models import Role

"""
Dashboard Admin Controller v3 - Versión limpia y funcional
"""

                             QFrame, QTabWidget, QPushButton, QSizePolicy)


_ = logging.getLogger(__name__)


class DashboardAdminController(BaseModule):
    """Controlador principal del Dashboard Admin v3 - Versión limpia"""
      # Señales básicas
    _ = pyqtSignal(str, float)
    
    def __init__(self, auth_service=None, db_manager=None, parent=None):
        """TODO: Add docstring"""
        self.auth_service = auth_service
        self.db_manager = db_manager
        super().__init__(parent)
        
        self.setup_admin_dashboard()
        
        # Forzar visibilidad después de construcción completa
        QTimer.singleShot(50, self.force_all_visibility)
    
    def setup_admin_dashboard(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura el dashboard básico"""
        _ = self.main_layout
        
        # Título principal
        title = QLabel("📊 Dashboard Admin v3")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #0f172a;
                padding: 20px;
                background: white;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
                margin-bottom: 20px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)        # Layout principal horizontal (2+1)
        main_content_layout = QHBoxLayout()
        main_content_layout.setSpacing(20)
        
        # Contenedor izquierdo: métricas + análisis (vertical)
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        
        # Añadir métricas al contenedor izquierdo
        metrics_container = self.create_metrics_container()
        left_layout.addWidget(metrics_container)
        
        # Añadir análisis visual al contenedor izquierdo
        charts_container = self.create_charts_container()
        left_layout.addWidget(charts_container)
        
        # Contenedor de alertas (lado derecho)
        _ = self.create_alerts_container()
        
        # Añadir contenedores al layout horizontal
        main_content_layout.addWidget(left_container, 70)     # 70% del ancho
        main_content_layout.addWidget(alerts_container, 30)   # 30% del ancho
        
        # Widget contenedor principal
        main_content_widget = QWidget()
        main_content_widget.setLayout(main_content_layout)
        layout.addWidget(main_content_widget)
          # Espaciador
        layout.addStretch()
    
    def create_metrics_container(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea el contenedor de métricas"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
                padding: 20px;
            }        """)
        container.setMinimumHeight(450)  # Altura mínima suficiente para 2 filas
        # REMOVIDO: setMaximumHeight para permitir expansión completa
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        container.setVisible(True)  # Asegurar visibilidad
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Sección de métricas (ya incluye su propio título)
        self.metrics_section = AdminMetricsSection()
        self.metrics_section.setVisible(True)  # Asegurar visibilidad
        layout.addWidget(self.metrics_section)
        
        return container
    
    def create_charts_container(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea el contenedor de análisis visual"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
                padding: 20px;
            }
        """)
        container.setMinimumHeight(250)
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Título
        title = QLabel("📊 Análisis Visual")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 16px;
            }
        """)
        layout.addWidget(title)
        
        # Placeholder para gráficos
        charts_placeholder = QLabel("🚧 Gráficos en desarrollo...")
        charts_placeholder.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #6b7280;
                background: #f8fafc;
                border: 2px dashed #d1d5db;
                border-radius: 8px;
                padding: 40px;
                text-align: center;
            }
        """)
        charts_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(charts_placeholder)
        
        return container
    
    def create_alerts_container(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea el contenedor de alertas vertical"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
                padding: 20px;
            }
        """)
        container.setMinimumWidth(250)
        container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Título
        title = QLabel("🔔 Alertas")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 16px;
            }
        """)
        layout.addWidget(title)
        
        # Lista de alertas
        alerts_content = QLabel("""
<div style="line-height: 1.8;">
<div style="color: #10b981; margin: 8px 0;">🟢 Sistema operativo normal</div>
<div style="color: #f59e0b; margin: 8px 0;">🟡 Memoria: 78% (Atención)</div>
<div style="color: #10b981; margin: 8px 0;">🟢 CPU: 45% (Normal)</div>
<div style="color: #10b981; margin: 8px 0;">🟢 Conectividad BD: Estable</div>
<div style="color: #f59e0b; margin: 8px 0;">🟡 Disco: 85% (Atención)</div>
<div style="color: #10b981; margin: 8px 0;">🟢 Servicios: Activos</div>
<div style="color: #6b7280; margin: 16px 0; font-size: 12px;">📊 Última actualización: Hace 30s</div>
</div>
        """)
        alerts_content.setStyleSheet("""
            QLabel {
                background-color: #f8fafc;
                border-radius: 6px;
                border-left: 4px solid #f59e0b;
                padding: 15px;
                font-size: 13px;
            }
        """)
        alerts_content.setWordWrap(True)
        layout.addWidget(alerts_content)
        
        # Espaciador
        layout.addStretch()
        
        return container

    def get_module_name(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "Dashboard Admin"
    
    def get_icon_path(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return "📊"
    
    def get_required_permissions(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        return [Role.ADMIN]
    
    def cleanup(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Limpieza al cerrar"""
        logger.info("Dashboard admin v3 cerrado")
    
    def force_all_visibility(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Forzar visibilidad de todos los elementos después de construcción"""
        try:
            logger.debug("Forzando visibilidad de todos los elementos del dashboard")
            
            # 1. Dashboard principal
            self.setVisible(True)
            self.show()
            self.update()
            
            # 2. Metrics section
            if hasattr(self, 'metrics_section'):
                metrics = self.metrics_section
                metrics.setVisible(True)
                metrics.show()
                metrics.update()                # 3. Forzar visibilidad del parent (container) con casting seguro
                container = metrics.parent()
                if container and isinstance(container, QWidget):
                    container.setVisible(True)
                    container.show()
                    container.update()
                
                # 4. Forzar visibilidad de todas las tarjetas
                if hasattr(metrics, 'metric_cards'):
                    for name, card in metrics.metric_cards.items():
                        card.setVisible(True)
                        card.show()
                        card.raise_()
                        card.update()
                        logger.debug("Tarjeta %s forzada como visible", name)
            
            # 5. Actualizar toda la interfaz
            self.update()
            self.repaint()
            
            logger.info("✅ Visibilidad forzada completada para todas las tarjetas")
            
        except Exception as e:
            logger.error("Error forzando visibilidad: %s", e)
