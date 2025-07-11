"""
Ventana principal moderna de la aplicación Hefest.
"""

import logging
import os
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMenuBar,
    QMenu,
    QMessageBox,
    QScrollArea,
)
from PyQt6.QtCore import QTimer, QEvent, QObject
from PyQt6.QtGui import QCloseEvent, QKeyEvent, QResizeEvent
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QDateTime, QPropertyAnimation
from PyQt6.QtGui import QAction

from src.__version__ import __version__
from ..components.main_navigation_sidebar import ModernSidebar

# === SISTEMA VISUAL V3 ULTRA-MODERNO ===
from ..modules.dashboard_admin_v3.ultra_modern_admin_dashboard import (
    UltraModernAdminDashboard,
)


# Importar servicios de autenticación y auditoría
from services.auth_service import AuthService, get_auth_service
from services.audit_service import AuditService
from core.hefest_data_models import Role
from data.db_manager import DatabaseManager

# Importar decorador de roles

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Ventana principal moderna con sidebar animado y efectos visuales"""

    # Señales
    module_changed = pyqtSignal(str)

    def __init__(self, auth_service: Optional[AuthService] = None) -> None:
        super().__init__()
        logger.info("Initializing MainWindow")
        self.setWindowTitle(f"Hefest v{__version__} - Sistema Integral de Hostelería")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)

        # Usar el servicio de autenticación pasado o crear uno nuevo
        self.auth_service = auth_service if auth_service else get_auth_service()

        # Inicializar el gestor de base de datos
        self.db_manager = DatabaseManager()
        # Eliminado DependencyBus: la inyección de db_manager es ahora explícita y obligatoria

        # Variables de estado
        self.current_module = None
        self.module_widgets: Dict[str, QWidget] = {}
        self._module_scroll_positions: Dict[str, int] = (
            {}
        )  # Guardar posición de scroll por módulo
        # Mapping de módulos a roles requeridos
        self.module_permissions = {
            "dashboard": Role.EMPLOYEE,
            "tpv": Role.EMPLOYEE,
            "advanced_tpv": Role.EMPLOYEE,
            "hospederia": Role.EMPLOYEE,
            "inventario": Role.MANAGER,
            "reportes": Role.MANAGER,
            "configuracion": Role.ADMIN,
            "audit": Role.ADMIN,
            "users": Role.ADMIN,
            "user_management": Role.ADMIN,
        }
        # Configurar la interfaz
        self.setup_ui()
        self.setup_connections()
        self.setup_menu()
        # Forzar ventana maximizada
        self.showMaximized()
        # Deshabilitar resize libre (solo minimizar/maximizar)
        self.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint, True)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, True)
        # Cargar módulo inicial después de asegurar que el usuario esté autenticado
        QTimer.singleShot(500, self.load_initial_module)  # type: ignore[reportUnknownMemberType]

    def load_initial_module(self) -> None:
        """Carga el módulo inicial después de verificar que el usuario esté autenticado"""
        if not self.auth_service.is_authenticated:
            logger.warning("Usuario no autenticado aún, reintentando en 500ms...")
            QTimer.singleShot(500, self.load_initial_module)  # type: ignore[reportUnknownMemberType]
            return

        logger.info("Usuario autenticado, cargando dashboard inicial...")
        self.show_module("dashboard")

    def check_module_permission(self, module_id: str) -> bool:
        """Verifica si el usuario tiene permisos para acceder al módulo"""
        if module_id not in self.module_permissions:
            logger.warning(f"El módulo {module_id} no tiene permisos configurados.")
            return False

        required_role = self.module_permissions[module_id]

        has_permission = self.auth_service.has_permission(required_role.value)

        return has_permission

    def create_permission_denied_widget(self, module_id: str) -> QWidget:
        """Crea un widget que muestra mensaje de acceso denegado"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Icono de acceso denegado
        icon_label = QLabel("🔒")
        icon_label.setStyleSheet("font-size: 72px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Título
        title = QLabel("Acceso Denegado")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #7f1d1d;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Mensaje
        message = QLabel(f"No tienes permisos para acceder al módulo '{module_id}'.")
        message.setStyleSheet("font-size: 16px; color: #374151; margin-top: 10px;")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)  # Registro de auditoría
        if self.auth_service.current_user:
            AuditService.log_access_denied(self.auth_service.current_user, module_id)

        layout.addStretch()
        return widget

    def setup_ui(self) -> None:
        """Configura la interfaz principal"""
        logger.info("Setting up modern UI components")

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar - pasar la instancia de AuthService
        self.sidebar = ModernSidebar(auth_service=self.auth_service)
        main_layout.addWidget(self.sidebar)

        # Contenedor de módulos con scroll/clipping
        self.module_container = QWidget()
        self.module_layout = QVBoxLayout(self.module_container)
        self.module_layout.setContentsMargins(0, 0, 0, 0)
        self.module_layout.setSpacing(0)
        # Envolver en QScrollArea para clipping/scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.module_container)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        main_layout.addWidget(self.scroll_area, stretch=1)
        # Botón flotante 'Volver al inicio'
        self.scroll_to_top_btn = QPushButton("↑", self)
        self.scroll_to_top_btn.setToolTip("Volver al inicio")
        self.scroll_to_top_btn.setFixedSize(36, 36)
        self.scroll_to_top_btn.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #38bdf8, stop:1 #a7f3d0);
                color: #222;
                border-radius: 18px;
                border: 2px solid #38bdf8;
                font-size: 20px;
                font-weight: bold;
                box-shadow: 0 2px 8px rgba(56,189,248,0.15);
            }
            QPushButton:hover {
                background: #a7f3d0;
                color: #0ea5e9;
            }
        """
        )
        self.scroll_to_top_btn.hide()
        self.scroll_to_top_btn.clicked.connect(self.animate_scroll_to_top)  # type: ignore[reportUnknownMemberType]
        vbar = self.scroll_area.verticalScrollBar()
        if vbar is not None:
            vbar.valueChanged.connect(self.toggle_scroll_to_top_btn)  # type: ignore[reportUnknownMemberType]
        self.toggle_scroll_to_top_btn()

        # Barra de estado moderna
        self.setup_status_bar()

        # Aplicar estilo visual moderno al scroll a toda la ventana principal
        try:
            with open(
                os.path.join(os.path.dirname(__file__), "qt_scrollarea_custom.qss"),
                "r",
                encoding="utf-8",
            ) as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.warning(
                f"No se pudo aplicar el estilo QSS personalizado al scroll: {e}"
            )

    def setup_status_bar(self):
        """Configura la barra de estado moderna con información del usuario"""
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("modern-statusbar")
        self.setStatusBar(self.status_bar)

        # Información permanente
        self.status_label = QLabel("Listo")

        # Mostrar usuario actual
        current_user = self.auth_service.current_user
        user_text = (
            f"Usuario: {current_user.name} ({current_user.role.value})"
            if current_user
            else "Usuario: No autenticado"
        )
        self.user_label = QLabel(user_text)
        self.user_label.setStyleSheet("font-weight: bold;")

        # Timer para actualizar fecha/hora
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status_bar)  # type: ignore[reportUnknownMemberType]
        self.timer.start(1000)

        # Agregar widgets a la barra de estado
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.user_label)

    def setup_connections(self):
        """Configura las conexiones de señales"""
        self.sidebar.module_selected.connect(self.show_module)  # type: ignore[reportUnknownMemberType]
        self.module_changed.connect(self.on_module_changed)  # type: ignore[reportUnknownMemberType]
        # Conectar la señal de logout del sidebar
        self.sidebar.logout_requested.connect(self.handle_logout)  # type: ignore[reportUnknownMemberType]

    def setup_menu(self):
        """Configura el menú de la aplicación"""
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menú Archivo
        file_menu = QMenu("Archivo", self)
        menu_bar.addMenu(file_menu)

        # Acción de salir
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)  # type: ignore[reportUnknownMemberType]
        file_menu.addAction(exit_action)  # type: ignore[reportUnknownMemberType]

        # Menú Módulos
        modules_menu = QMenu("Módulos", self)
        menu_bar.addMenu(modules_menu)
        # Agregar acciones para cada módulo
        for module_id in [
            "dashboard",
            "hospederia",
            "tpv",
            "advanced_tpv",
            "inventario",
            "reportes",
            "configuracion",
        ]:
            action = QAction(module_id.capitalize().replace("_", " "), self)
            action.setProperty("module_id", module_id)
            action.triggered.connect(self.module_action_triggered)  # type: ignore[reportUnknownMemberType]
            modules_menu.addAction(action)  # type: ignore[reportUnknownMemberType]
        # Menú Ayuda
        help_menu = QMenu("Ayuda", self)
        menu_bar.addMenu(help_menu)

        # Acción de acerca de
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about_dialog)  # type: ignore[reportUnknownMemberType]
        help_menu.addAction(about_action)  # type: ignore[reportUnknownMemberType]

    def module_action_triggered(self):
        """Maneja la activación de acciones de módulo desde el menú"""
        action = self.sender()
        if action:
            module_id = action.property("module_id")
            self.show_module(module_id)

    def show_module(self, module_id: str) -> None:
        """Muestra el módulo especificado si el usuario tiene permisos"""
        # Guardar posición de scroll del módulo actual
        if self.current_module is not None:
            vbar = self.scroll_area.verticalScrollBar()
            if vbar is not None:
                self._module_scroll_positions[self.current_module] = vbar.value()

        if not self.check_module_permission(module_id):
            logger.warning(f"🚨 SHOW_MODULE: Acceso denegado al módulo {module_id}")
            denied_widget = self.create_permission_denied_widget(module_id)
            self.module_layout.addWidget(denied_widget)
            return

        if module_id in self.module_widgets:
            widget = self.module_widgets[module_id]
        else:
            widget = self.create_module_widget(module_id)
            self.module_widgets[module_id] = widget

        # Limpiar el contenedor de módulos
        for i in reversed(range(self.module_layout.count())):
            item = self.module_layout.itemAt(i)
            old_widget = item.widget() if item else None
            if old_widget:
                old_widget.setParent(None)

        self.module_layout.addWidget(widget)
        previous_module = self.current_module
        self.current_module = module_id
        self.module_changed.emit(module_id)
        vbar = self.scroll_area.verticalScrollBar()
        # Restaurar posición previa si existe y es otro módulo
        if previous_module != module_id and module_id in self._module_scroll_positions:
            if vbar is not None:
                vbar.setValue(self._module_scroll_positions[module_id])
        # Si es el mismo módulo, animar scroll al inicio
        elif previous_module == module_id and vbar is not None:
            anim = QPropertyAnimation(vbar, b"value", self)
            anim.setDuration(350)
            anim.setStartValue(vbar.value())
            anim.setEndValue(0)
            anim.start()
            self._scroll_anim = anim

    def create_module_widget(self, module_id: str) -> QWidget:
        """Crea un widget para el módulo especificado"""
        try:
            module_class = self.get_module_class(module_id)

            if module_class:
                # Pasar auth_service y db_manager específicamente al dashboard y advanced_tpv
                if module_id == "dashboard":
                    widget = module_class(
                        auth_service=self.auth_service, db_manager=self.db_manager
                    )
                    return widget
                elif module_id == "advanced_tpv":
                    # TPVAvanzado espera db_manager como argumento
                    widget = module_class(db_manager=self.db_manager)
                    return widget
                elif module_id == "tpv":
                    # TPVModule ahora acepta db_manager por inyección
                    widget = module_class(db_manager=self.db_manager)
                    return widget
                else:
                    return module_class()
            else:
                logger.error(f"Clase del módulo {module_id} no encontrada.")
                return self.create_permission_denied_widget(module_id)
        except Exception as e:
            logger.error(f"Error al crear el widget del módulo {module_id}: {e}")
            return self.create_permission_denied_widget(module_id)

    def get_module_class(self, module_id: str) -> Any:
        """Obtiene la clase del módulo correspondiente al module_id"""
        from ui.modules.tpv_module.tpv_module import TPVModule

        module_classes: dict[str, Any] = {
            # === SISTEMA VISUAL V3 ULTRA-MODERNO ===
            "dashboard": UltraModernAdminDashboard,  # NUEVO: Dashboard V3 Ultra-Moderno
            # Otros módulos (usar sistema antiguo temporalmente)
            "tpv": TPVModule,
            "advanced_tpv": "ui.modules.tpv_module.components.tpv_avanzado.TPVAvanzado",
            "hospederia": "ui.modules.hospederia_module.HospederiaModule",
            "inventario": "ui.modules.inventario_module.InventarioModulePro",
            "audit": "ui.modules.audit_module.AuditModule",
            "users": "ui.modules.user_management_module.UserManagementModule",
            "user_management": "ui.modules.user_management_module.UserManagementModule",
            "configuracion": "ui.modules.configuracion_module.ConfiguracionModule",
            "reportes": "ui.modules.reportes_module.ReportesModule",
        }

        if module_id in module_classes:
            class_path: Any = module_classes[module_id]
            if isinstance(class_path, str):
                # Importar la clase dinámicamente
                module_name, class_name = class_path.rsplit(".", 1)
                module = __import__(module_name, fromlist=[class_name])
                return getattr(module, class_name)  # type: ignore[reportUnknownVariableType]
            else:
                return class_path
        else:
            logger.warning(f"Módulo no encontrado para ID: {module_id}")
            return None

    def handle_logout(self):
        """Maneja el cierre de sesión"""
        if self.auth_service.current_user:
            self.auth_service.logout()

        # Cerrar ventana actual
        self.close()

        # Aquí podrías reiniciar la aplicación o mostrar la pantalla de login
        logger.info("Usuario ha cerrado sesión")

    def update_status_bar(self):
        """Actualiza la información de la barra de estado"""
        current_time = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")
        self.status_bar.showMessage(current_time)

        # Actualizar texto de usuario si cambió
        current_user = self.auth_service.current_user
        if current_user:
            user_text = f"Usuario: {current_user.name} ({current_user.role.value})"
            self.user_label.setText(user_text)

    def on_module_changed(self, module_id: str) -> None:
        """Maneja el cambio de módulo"""
        logger.info(f"Módulo cambiado a: {module_id}")

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        """Maneja el cierre de la ventana"""
        logger.info("Close event triggered")
        if hasattr(self, "timer"):
            self.timer.stop()
        if a0:
            a0.accept()

    def show_about_dialog(self):
        """Muestra el diálogo Acerca de"""
        msg = QMessageBox()
        msg.setWindowTitle("Acerca de Hefest")
        msg.setText(
            f"Hefest v{__version__}\nSistema Integral de Hostelería\n\nDesarrollado para la gestión integral de hoteles y restaurantes"
        )
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        super().keyPressEvent(a0)
        # Atajos de scroll para el área principal
        vbar = self.scroll_area.verticalScrollBar()
        if vbar is not None and a0 is not None:
            if a0.key() == Qt.Key.Key_PageDown:
                vbar.setValue(min(vbar.value() + vbar.pageStep(), vbar.maximum()))
            elif a0.key() == Qt.Key.Key_PageUp:
                vbar.setValue(max(vbar.value() - vbar.pageStep(), 0))
            elif a0.key() == Qt.Key.Key_Home:
                vbar.setValue(0)
            elif a0.key() == Qt.Key.Key_End:
                vbar.setValue(vbar.maximum())

        # Ctrl+Q para salir
        if (
            a0 is not None
            and a0.key() == Qt.Key.Key_Q
            and a0.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self.close()

        # F12 para abrir el menú de depuración (si está disponible)
        if a0 is not None and a0.key() == Qt.Key.Key_F12:
            debug_menu_action = self.findChild(QAction, "debugMenuAction")
            if debug_menu_action:
                debug_menu_action.trigger()

        # Ctrl+Shift+R para recargar el módulo currente
        if (
            a0 is not None
            and a0.key() == Qt.Key.Key_R
            and a0.modifiers() & Qt.KeyboardModifier.ControlModifier
            and a0.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ):
            if self.current_module:
                logger.info("Reloading current module: %s", self.current_module)
                self.show_module(self.current_module)

        # Ctrl+Shift+L para ver el registro de auditoría
        if (
            a0 is not None
            and a0.key() == Qt.Key.Key_L
            and a0.modifiers() & Qt.KeyboardModifier.ControlModifier
            and a0.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ):
            self.show_module("audit")

        # Ctrl+Shift+U para gestionar usuarios y roles
        if (
            a0 is not None
            and a0.key() == Qt.Key.Key_U
            and a0.modifiers() & Qt.KeyboardModifier.ControlModifier
            and a0.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ):
            self.show_module("users")

    def update_scroll_overflow_indicators(self):
        vbar = self.scroll_area.verticalScrollBar()
        hbar = self.scroll_area.horizontalScrollBar()
        overflow_top = vbar.value() > 0 if vbar is not None else False
        overflow_bottom = vbar.value() < vbar.maximum() if vbar is not None else False
        overflow_left = hbar.value() > 0 if hbar is not None else False
        overflow_right = hbar.value() < hbar.maximum() if hbar is not None else False
        self.scroll_area.setProperty("overflow-top", overflow_top)
        self.scroll_area.setProperty("overflow-bottom", overflow_bottom)
        self.scroll_area.setProperty("overflow-left", overflow_left)
        self.scroll_area.setProperty("overflow-right", overflow_right)
        style = self.scroll_area.style()
        if style is not None:
            style.unpolish(self.scroll_area)
            style.polish(self.scroll_area)

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a0 == self.scroll_area and a1 is not None and a1.type() == a1.Type.Resize:
            self.update_scroll_overflow_indicators()
        return super().eventFilter(a0, a1)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        super().resizeEvent(a0)
        # Posicionar el botón flotante en la esquina inferior derecha de la QScrollArea
        if hasattr(self, "scroll_to_top_btn"):
            area = self.scroll_area.geometry()
            x = area.x() + area.width() - self.scroll_to_top_btn.width() - 18
            y = area.y() + area.height() - self.scroll_to_top_btn.height() - 18
            self.scroll_to_top_btn.move(x, y)

    def toggle_scroll_to_top_btn(self):
        vbar = self.scroll_area.verticalScrollBar()
        if vbar is not None and vbar.maximum() > 0 and vbar.value() > 0:
            self.scroll_to_top_btn.show()
        else:
            self.scroll_to_top_btn.hide()

    def animate_scroll_to_top(self):
        vbar = self.scroll_area.verticalScrollBar()
        if vbar is not None:
            anim = QPropertyAnimation(vbar, b"value", self)
            anim.setDuration(350)
            anim.setStartValue(vbar.value())
            anim.setEndValue(0)
            anim.start()
            self._scroll_anim = anim  # Guardar referencia para evitar GC
