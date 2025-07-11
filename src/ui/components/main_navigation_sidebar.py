"""
Sidebar moderno para la aplicación Hefest.
"""

import logging
from typing import Optional, Any, Dict
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal

# Importar servicios de autenticación
from services.auth_service import get_auth_service
from services.audit_service import AuditService
from core.hefest_data_models import Role

logger = logging.getLogger(__name__)


class ModernSidebar(QFrame):
    """Sidebar moderno con navegación y efectos visuales"""

    # Señales
    module_selected = pyqtSignal(str)
    logout_requested = pyqtSignal()

    def __init__(
        self, parent: Optional[QWidget] = None, auth_service: Optional[Any] = None
    ) -> None:
        super().__init__(parent)
        logger.info("Inicializando ModernSidebar")
        # logger.debug("Constructor de ModernSidebar inicializado correctamente.")

        # Usar el servicio de autenticación pasado o crear uno nuevo
        self.auth_service: Any = auth_service if auth_service else get_auth_service()
        self.current_active: Optional[str] = None
        self.nav_buttons: Dict[str, QPushButton] = {}

        # Configurar el sidebar
        self.setup_ui()

    def setup_ui(self) -> None:
        """Configura la interfaz del sidebar"""
        self.setFixedWidth(300)
        self.setFrameStyle(QFrame.Shape.NoFrame)

        # Estilo básico del sidebar (fondo más oscuro y borde más marcado)
        self.setStyleSheet(
            """
            ModernSidebar {
                background: #e5e7eb;
                border-right: 2px solid #cbd5e1;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.create_header(layout)

        # Navegación
        self.create_navigation(layout)

        # Footer
        layout.addStretch()
        self.create_footer(layout)

    def create_header(self, layout: QVBoxLayout) -> None:
        """Crea el header del sidebar"""
        header = QFrame()
        header.setFixedHeight(120)
        header.setStyleSheet(
            """
            QFrame {
                background: #d1d5db;
                border-bottom: 1.5px solid #cbd5e1;
            }
            """
        )

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 20)
        header_layout.setSpacing(5)

        # Logo y título
        title_label = QLabel("HEFEST")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #111827;
                letter-spacing: 1px;
            }
            """
        )

        subtitle_label = QLabel("Sistema Integral")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet(
            """
            QLabel {
                font-size: 11px;
                color: #374151;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            """
        )
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        layout.addWidget(header)  # type: ignore

    def create_navigation(self, layout: QVBoxLayout) -> None:
        """Crea los botones de navegación según los permisos del usuario"""
        # logger.debug("Método create_navigation llamado correctamente.")

        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(10, 20, 10, 10)
        nav_layout.setSpacing(8)

        # Módulos disponibles y sus permisos requeridos
        modules = [
            (
                "dashboard",
                "📊",
                "Dashboard",
                "Vista general del sistema",
                Role.EMPLOYEE,
            ),
            ("tpv", "🏪", "TPV", "Terminal Punto de Venta", Role.EMPLOYEE),
            (
                "hospederia",
                "🏨",
                "Hospedería",
                "Gestión de habitaciones",
                Role.EMPLOYEE,
            ),
            ("inventario", "📦", "Inventario", "Control de stock", Role.MANAGER),
            ("reportes", "📊", "Reportes", "Informes y estadísticas", Role.MANAGER),
            ("configuracion", "⚙️", "Configuración", "Ajustes del sistema", Role.ADMIN),
            ("audit", "📋", "Auditoría", "Registro de actividades", Role.ADMIN),
            ("users", "👥", "Usuarios", "Gestión de usuarios", Role.ADMIN),
        ]

        # logger.debug("Lista de módulos configurados en el sidebar:")
        for module_id, icon, title, description, required_role in modules:
            pass  # Eliminado debug duplicado

        # Filtrar módulos según permisos del usuario
        current_user = self.auth_service.current_user
        if current_user:
            # logger.debug(
            #     f"Usuario actual: {current_user.name} ({current_user.role.value})"
            # )
            # logger.debug("Módulos disponibles según permisos:")
            # logger.debug("Iniciando evaluación de módulos para la barra lateral...")
            for module_id, icon, title, description, required_role in modules:
                has_permission = self.auth_service.has_permission(required_role.value)

                if has_permission:
                    btn = self.create_nav_button(module_id, icon, title, description)
                    nav_layout.addWidget(btn)
                    self.nav_buttons[module_id] = btn
                else:
                    logger.warning(f"Acceso denegado al módulo: {module_id}")

        layout.addWidget(nav_container)  # type: ignore

    def create_nav_button(
        self, module_id: str, icon: str, title: str, description: str
    ) -> QPushButton:
        """Crea un botón de navegación moderno"""
        btn = QPushButton()
        btn.setObjectName(f"nav_btn_{module_id}")
        btn.setFixedHeight(60)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Layout del botón
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(15, 10, 15, 10)
        btn_layout.setSpacing(15)

        # Icono
        icon_label = QLabel(icon)
        icon_label.setFixedSize(24, 24)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 18px;")

        # Contenedor de texto
        text_container = QVBoxLayout()
        text_container.setContentsMargins(0, 0, 0, 0)
        text_container.setSpacing(2)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #374151;
            }
        """
        )

        desc_label = QLabel(description)
        desc_label.setStyleSheet(
            """
            QLabel {
                font-size: 11px;
                color: #6b7280;
            }
        """
        )

        text_container.addWidget(title_label)
        text_container.addWidget(desc_label)

        # Widget contenedor
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(icon_label)
        content_layout.addLayout(text_container)
        content_layout.addStretch()

        # Layout principal del botón
        main_layout = QVBoxLayout(btn)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(content_widget)

        # Estilo del botón
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
            }
            QPushButton:pressed {
                background-color: #e2e8f0;
            }
        """
        )

        # Conectar señal
        def log_and_emit():
            logger.info(f"[SIDEBAR] Botón pulsado: {module_id}")
            if module_id == "tpv":
                logger.info(
                    "[SIDEBAR] Entrando al módulo TPV desde sidebar (log explícito)"
                )
            self.module_selected.emit(module_id)

        btn.clicked.connect(log_and_emit)  # type: ignore

        # Tooltip
        btn.setToolTip(f"{title}\n{description}")

        return btn

    def create_footer(self, layout: QVBoxLayout) -> None:
        """Crea el footer del sidebar con información del usuario y botón de logout"""
        footer = QFrame()
        footer.setFixedHeight(80)
        footer.setStyleSheet(
            """
            QFrame {
                background: #d1d5db;
                border-top: 1.5px solid #cbd5e1;
            }
            """
        )

        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(15, 10, 15, 10)
        footer_layout.setSpacing(5)

        # Información del usuario
        current_user = self.auth_service.current_user  # type: ignore
        if current_user:
            user_label = QLabel(f"👤 {getattr(current_user, 'name', 'Usuario')}")  # type: ignore
            user_label.setStyleSheet(
                """
                QLabel {
                    font-size: 12px;
                    font-weight: 500;
                    color: #374151;
                }
            """
            )

            role_label = QLabel(f"Rol: {getattr(getattr(current_user, 'role', None), 'value', 'Sin rol')}")  # type: ignore
            role_label.setStyleSheet(
                """
                QLabel {
                    font-size: 10px;
                    color: #6b7280;
                }
            """
            )

            footer_layout.addWidget(user_label)
            footer_layout.addWidget(role_label)

        # Botón de logout
        logout_btn = QPushButton("🚪 Cerrar Sesión")
        logout_btn.setFixedHeight(25)
        logout_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 500;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
            QPushButton:pressed {
                background-color: #b91c1c;
            }
        """
        )

        logout_btn.clicked.connect(self.logout_clicked)  # type: ignore
        footer_layout.addWidget(logout_btn)

        layout.addWidget(footer)  # type: ignore

    def logout_clicked(self) -> None:
        """Maneja el clic en el botón de logout"""
        reply = QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Está seguro de que desea cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Registrar en auditoría
            if self.auth_service.current_user:
                AuditService.log("Cierre de sesión", self.auth_service.current_user)

            self.logout_requested.emit()

    def set_active_module(self, module_id: str) -> None:
        """Establece el módulo activo visualmente"""
        # Resetear todos los botones
        for btn_id, btn in self.nav_buttons.items():
            if btn_id == module_id:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #3b82f6;
                        border: none;
                        border-radius: 8px;
                        color: white;
                        text-align: left;
                        padding: 0px;
                    }
                    QPushButton:hover {
                        background-color: #2563eb;
                    }
                """
                )
                # Actualizar color del texto para el botón activo
                for child in btn.findChildren(QLabel):
                    child.setStyleSheet(
                        child.styleSheet()
                        .replace("color: #374151", "color: white")
                        .replace("color: #6b7280", "color: #e5e7eb")
                    )
            else:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        border-radius: 8px;
                        text-align: left;
                        padding: 0px;
                    }
                    QPushButton:hover {
                        background-color: #f1f5f9;
                    }
                    QPushButton:pressed {
                        background-color: #e2e8f0;
                    }
                """
                )
                # Resetear color del texto para botones inactivos
                for child in btn.findChildren(QLabel):
                    if "font-weight: 600" in child.styleSheet():
                        child.setStyleSheet(
                            child.styleSheet().replace("color: white", "color: #374151")
                        )
                    else:
                        child.setStyleSheet(
                            child.styleSheet().replace(
                                "color: #e5e7eb", "color: #6b7280"
                            )
                        )
