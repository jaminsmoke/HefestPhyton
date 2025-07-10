# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
import logging
from PyQt6.QtWidgets import (QMainWindow, QStatusBar, QWidget, 
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QDateTime
from PyQt6.QtGui import QCloseEvent, QAction
from ui.components.sidebar import ModernSidebar
from ui.modules.dashboard_admin_v3.dashboard_admin_controller import DashboardAdminController
from services.auth_service import AuthService
from services.audit_service import AuditService
from core.models import Role
from data.db_manager import DatabaseManager

"""
Ventana principal moderna de la aplicación Hefest.
"""

                            QVBoxLayout, QHBoxLayout, QFrame,
                            QLabel, QPushButton, QMenuBar, QMenu,
                            QMessageBox)


# Importar servicios de autenticación y auditoría

# Importar decorador de roles

_ = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Ventana principal moderna con sidebar animado y efectos visuales"""
      # Señales
    _ = pyqtSignal(str)
    
    def __init__(self, auth_service=None):
        """TODO: Add docstring"""
        super().__init__()
        logger.info("Initializing MainWindow")
        self.setWindowTitle("Hefest v1.0 - Sistema Integral de Hostelería")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)
        
        # Usar el servicio de autenticación pasado o crear uno nuevo
        self.auth_service = auth_service if auth_service else AuthService()
        
        # Inicializar el gestor de base de datos
        self.db_manager = DatabaseManager()
        
        # Variables de estado
        self.current_module = None
        self.module_widgets = {}
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
            "user_management": Role.ADMIN        }
        
        # Configurar la interfaz
        self.setup_ui()
        self.setup_connections()
        self.setup_menu()
        
        # Cargar módulo inicial
        QTimer.singleShot(100, lambda: self.show_module("dashboard"))

    def check_module_permission(self, module_id):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si el usuario tiene permisos para acceder al módulo"""
        if module_id not in self.module_permissions:
            logger.warning("El módulo %s no tiene permisos configurados.", module_id)
            return False
        
        _ = self.module_permissions[module_id]
        current_user = self.auth_service.current_user
        _ = self.auth_service.is_authenticated
        
        logger.debug("Verificando permisos para módulo: %s", module_id)
        logger.debug("  Rol requerido: %s", required_role.value)
        logger.debug("  Usuario actual: %s", current_user.name if current_user else 'None')
        logger.debug("  Rol usuario: %s", current_user.role.value if current_user else 'None')
        logger.debug("  Autenticado: %s", is_authenticated)
        
        has_permission = self.auth_service.has_permission(required_role)
        logger.debug("  Tiene permiso: %s", has_permission)
        
        return has_permission

    def create_permission_denied_widget(self, module_id):
        """TODO: Add docstring"""
        # TODO: Add input validation
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
        layout.addWidget(message)        # Registro de auditoría
        if self.auth_service.current_user:
            AuditService.log_access_denied(self.auth_service.current_user, module_id)

        layout.addStretch()
        return widget

    def setup_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
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
        
        # Contenedor de módulos
        self.module_container = QWidget()
        self.module_layout = QVBoxLayout(self.module_container)
        self.module_layout.setContentsMargins(0, 0, 0, 0)
        self.module_layout.setSpacing(0)
        main_layout.addWidget(self.module_container, stretch=1)
        
        # Barra de estado moderna
        self.setup_status_bar()
        
    def setup_status_bar(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura la barra de estado moderna con información del usuario"""
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("modern-statusbar")
        self.setStatusBar(self.status_bar)
        
        # Información permanente
        self.status_label = QLabel("Listo")
        
        # Mostrar usuario actual
        current_user = self.auth_service.current_user
        user_text = f"Usuario: {current_user.name} ({current_user.role.value})" if current_user else "Usuario: No autenticado"
        self.user_label = QLabel(user_text)
        self.user_label.setStyleSheet("font-weight: bold;")
        
        # Timer para actualizar fecha/hora
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status_bar)
        self.timer.start(1000)
        
        # Agregar widgets a la barra de estado
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.user_label)
        
    def setup_connections(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura las conexiones de señales"""
        self.sidebar.module_selected.connect(self.show_module)
        self.module_changed.connect(self.on_module_changed)
        # Conectar la señal de logout del sidebar
        self.sidebar.logout_requested.connect(self.handle_logout)
        
    def setup_menu(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura el menú de la aplicación"""
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        
        # Menú Archivo
        file_menu = QMenu("Archivo", self)
        menu_bar.addMenu(file_menu)
        
        # Acción de salir
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Módulos
        modules_menu = QMenu("Módulos", self)
        menu_bar.addMenu(modules_menu)
          # Agregar acciones para cada módulo
        for module_id in ["dashboard", "hospederia", "tpv", "advanced_tpv", "inventario", "reportes", "configuracion"]:
            action = QAction(module_id.capitalize().replace("_", " "), self)
            action.setProperty("module_id", module_id)
            action.triggered.connect(self.module_action_triggered)
            modules_menu.addAction(action)
        
        # Menú Ayuda
        help_menu = QMenu("Ayuda", self)
        menu_bar.addMenu(help_menu)
          # Acción de acerca de
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
    def module_action_triggered(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Maneja la activación de acciones de módulo desde el menú"""
        action = self.sender()
        if action:
            module_id = action.property("module_id")
            self.show_module(module_id)
        
    def show_module(self, module_id):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Muestra el módulo especificado si el usuario tiene permisos"""
        if not self.check_module_permission(module_id):
            logger.info("Acceso denegado al módulo %s", module_id)
            denied_widget = self.create_permission_denied_widget(module_id)
            self.module_layout.addWidget(denied_widget)
            return

        if module_id in self.module_widgets:
            _ = self.module_widgets[module_id]
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
        self.current_module = module_id
        self.module_changed.emit(module_id)

    def create_module_widget(self, module_id):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea un widget para el módulo especificado"""
        try:
            module_class = self.get_module_class(module_id)
            if module_class:
                # Pasar auth_service y db_manager específicamente al dashboard
                if module_id == "dashboard":
                    return module_class(auth_service=self.auth_service, db_manager=self.db_manager)
                else:
                    return module_class()
            else:
                logger.error("Clase del módulo %s no encontrada.", module_id)
                return self.create_permission_denied_widget(module_id)
        except Exception as e:
            logger.error("Error al crear el widget del módulo {module_id}: %s", e)
            return self.create_permission_denied_widget(module_id)
        
    def get_module_class(self, module_id):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene la clase del módulo correspondiente al module_id"""
        _ = {
            "dashboard": DashboardAdminController,
            "tpv": "ui.modules.tpv_module.TPVTab",
            "advanced_tpv": "ui.modules.advanced_tpv_module.AdvancedTPVModule",
            "hospederia": "ui.modules.hospederia_module.HospederiaModule",
            "inventario": "ui.modules.inventario_module.InventarioTab",
            "audit": "ui.modules.audit_module.AuditModule",
            "users": "ui.modules.user_management_module.UserManagementModule",
            "user_management": "ui.modules.user_management_module.UserManagementModule",
            "configuracion": "ui.modules.configuracion_module.ConfiguracionModule",
            "reportes": "ui.modules.reportes_module.ReportesModule"
        }
        
        if module_id in module_classes:
            class_path = module_classes[module_id]
            if isinstance(class_path, str):
                # Importar la clase dinámicamente
                module_name, class_name = class_path.rsplit(".", 1)
                module = __import__(module_name, fromlist=[class_name])
                return getattr(module, class_name)
            else:
                return class_path
        else:
            logger.warning("Módulo no encontrado para ID: %s", module_id)
            return None
    
    def handle_logout(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Maneja el cierre de sesión"""
        if self.auth_service.current_user:
            self.auth_service.logout()
            
        # Cerrar ventana actual
        self.close()
        
        # Aquí podrías reiniciar la aplicación o mostrar la pantalla de login
        logger.info("Usuario ha cerrado sesión")
    
    def update_status_bar(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza la información de la barra de estado"""
        current_time = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")
        self.status_bar.showMessage(current_time)
        
        # Actualizar texto de usuario si cambió
        current_user = self.auth_service.current_user
        if current_user:
            user_text = f"Usuario: {current_user.name} ({current_user.role.value})"
            self.user_label.setText(user_text)
        
        
        
    def on_module_changed(self, module_id):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Maneja el cambio de módulo"""
        logger.info("Módulo cambiado a: %s", module_id)
    
    def closeEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Maneja el cierre de la ventana"""
        logger.info("Close event triggered")
        if hasattr(self, 'timer'):
            self.timer.stop()
        if event:
            event.accept()
    
    def show_about_dialog(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Muestra el diálogo Acerca de"""
        msg = QMessageBox()
        msg.setWindowTitle("Acerca de Hefest")
        msg.setText("Hefest v1.0\nSistema Integral de Hostelería\n\nDesarrollado para la gestión integral de hoteles y restaurantes")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
        
    def keyPressEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Maneja eventos de teclas"""
        super().keyPressEvent(event)
        
        # Ctrl+Q para salir
        if event.key() == Qt.Key.Key_Q and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.close()
          # F12 para abrir el menú de depuración (si está disponible)
        if event.key() == Qt.Key.Key_F12:
            debug_menu_action = self.findChild(QAction, "debugMenuAction")
            if debug_menu_action:
                debug_menu_action.trigger()
        
        # Ctrl+Shift+R para recargar el módulo currente
        if event.key() == Qt.Key.Key_R and event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            if self.current_module:
                logger.info("Reloading current module: %s", self.current_module)
                self.show_module(self.current_module)
        
        # Ctrl+Shift+L para ver el registro de auditoría
        if event.key() == Qt.Key.Key_L and event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.show_module("audit")
        
        # Ctrl+Shift+U para gestionar usuarios y roles
        if event.key() == Qt.Key.Key_U and event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.show_module("users")
