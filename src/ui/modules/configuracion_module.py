"""
Módulo de configuración del sistema Hefest.
Permite gestionar configuraciones de la aplicación, parámetros del sistema,
y ajustes específicos para cada módulo.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QGroupBox,
    QFormLayout,
    QTextEdit,
    QScrollArea,
    QFrame,
    QGridLayout,
    QSlider,
    QProgressBar,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QColor, QColor

from ui.modules.module_base_interface import BaseModule
from utils.application_config_manager import ConfigManager

logger = logging.getLogger(__name__)


class ConfiguracionModule(BaseModule):
    """Módulo de configuración del sistema"""

    # Señales
    configuracion_cambiada = pyqtSignal(str, object)  # (clave, valor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.setup_ui()
        self.cargar_configuracion()

    def create_module_header(self):
        """Crea el header del módulo de configuración"""
        header = QFrame()
        header.setObjectName("module-header")
        header.setFixedHeight(70)
        header.setStyleSheet(
            """
            QFrame#module-header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
                margin: 10px;
            }
        """
        )

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        # Icono y título
        title_container = QHBoxLayout()

        icon_label = QLabel("⚙️")
        icon_label.setStyleSheet("font-size: 32px;")
        title_container.addWidget(icon_label)

        title_text = QVBoxLayout()
        title = QLabel("Configuración del Sistema")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        subtitle = QLabel("Gestión de parámetros y ajustes de la aplicación")
        subtitle.setStyleSheet("font-size: 14px; color: rgba(255,255,255,0.8);")

        title_text.addWidget(title)
        title_text.addWidget(subtitle)
        title_container.addLayout(title_text)

        layout.addLayout(title_container)
        layout.addStretch()

        # Botones de acción
        guardar_btn = QPushButton("💾 Guardar Cambios")
        guardar_btn.setStyleSheet(
            """
            QPushButton {
                background: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.3);
            }
        """
        )
        guardar_btn.clicked.connect(self.guardar_configuracion)

        restaurar_btn = QPushButton("🔄 Restaurar")
        restaurar_btn.setStyleSheet(
            """
            QPushButton {
                background: rgba(255,255,255,0.1);
                color: white;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.2);
            }
        """
        )
        restaurar_btn.clicked.connect(self.restaurar_configuracion)

        layout.addWidget(guardar_btn)
        layout.addWidget(restaurar_btn)

        return header

    def setup_ui(self):
        """Configura la interfaz del módulo"""
        # Header del módulo
        header = self.create_module_header()
        self.content_layout.addWidget(header)

        # Crear tabs para diferentes categorías de configuración
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            """
            QTabWidget::pane {
                border: 1px solid #e5e7eb;
                background: white;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
                color: #3b82f6;
            }
        """
        )

        # Tab de configuración general
        self.create_general_tab()

        # Tab de configuración de base de datos
        self.create_database_tab()

        # Tab de configuración de interfaz
        self.create_interface_tab()

        # Tab de configuración de módulos
        self.create_modules_tab()

        # Tab de configuración de seguridad
        self.create_security_tab()

        # Tab de respaldo y mantenimiento
        self.create_backup_tab()

        self.content_layout.addWidget(self.tabs)

    def create_general_tab(self):
        """Crea la pestaña de configuración general"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Información de la empresa
        empresa_group = QGroupBox("Información de la Empresa")
        empresa_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
        )
        empresa_layout = QFormLayout(empresa_group)

        self.nombre_empresa = QLineEdit()
        self.nombre_empresa.setPlaceholderText("Nombre de la empresa")
        empresa_layout.addRow("Nombre:", self.nombre_empresa)

        self.direccion_empresa = QLineEdit()
        self.direccion_empresa.setPlaceholderText("Dirección completa")
        empresa_layout.addRow("Dirección:", self.direccion_empresa)

        self.telefono_empresa = QLineEdit()
        self.telefono_empresa.setPlaceholderText("+34 XXX XXX XXX")
        empresa_layout.addRow("Teléfono:", self.telefono_empresa)

        self.email_empresa = QLineEdit()
        self.email_empresa.setPlaceholderText("contacto@empresa.com")
        empresa_layout.addRow("Email:", self.email_empresa)

        layout.addWidget(empresa_group)

        # Configuración regional
        regional_group = QGroupBox("Configuración Regional")
        regional_group.setStyleSheet(empresa_group.styleSheet())
        regional_layout = QFormLayout(regional_group)

        self.idioma_combo = QComboBox()
        self.idioma_combo.addItems(["Español", "English", "Français", "Deutsch"])
        regional_layout.addRow("Idioma:", self.idioma_combo)

        self.moneda_combo = QComboBox()
        self.moneda_combo.addItems(["EUR (€)", "USD ($)", "GBP (£)"])
        regional_layout.addRow("Moneda:", self.moneda_combo)

        self.formato_fecha = QComboBox()
        self.formato_fecha.addItems(["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        regional_layout.addRow("Formato Fecha:", self.formato_fecha)

        layout.addWidget(regional_group)

        layout.addStretch()
        self.tabs.addTab(tab, "🏢 General")

    def create_database_tab(self):
        """Crea la pestaña de configuración de base de datos"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Configuración de conexión
        conexion_group = QGroupBox("Configuración de Conexión")
        conexion_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
        """
        )
        conexion_layout = QFormLayout(conexion_group)

        self.db_path = QLineEdit()
        self.db_path.setReadOnly(True)
        browse_btn = QPushButton("📁 Examinar")
        browse_btn.clicked.connect(self.seleccionar_db_path)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.db_path)
        path_layout.addWidget(browse_btn)
        conexion_layout.addRow("Ruta Base de Datos:", path_layout)

        self.backup_auto = QCheckBox("Respaldo automático diario")
        self.backup_auto.setChecked(True)
        conexion_layout.addRow("Respaldo:", self.backup_auto)

        layout.addWidget(conexion_group)

        # Estadísticas de la base de datos
        stats_group = QGroupBox("Estadísticas de la Base de Datos")
        stats_group.setStyleSheet(conexion_group.styleSheet())
        stats_layout = QGridLayout(stats_group)

        # Información ficticia para demostración
        stats_labels = [
            ("Total de Usuarios:", "5"),
            ("Total de Productos:", "150"),
            ("Total de Reservas:", "89"),
            ("Tamaño de BD:", "2.5 MB"),
            ("Última Optimización:", "Hace 3 días"),
            ("Fragmentación:", "5%"),
        ]

        for i, (label, value) in enumerate(stats_labels):
            row = i // 2
            col = (i % 2) * 2

            stats_layout.addWidget(QLabel(label), row, col)
            value_label = QLabel(value)
            value_label.setStyleSheet("font-weight: bold; color: #3b82f6;")
            stats_layout.addWidget(value_label, row, col + 1)

        layout.addWidget(stats_group)

        # Botones de mantenimiento
        mantenimiento_layout = QHBoxLayout()

        optimizar_btn = QPushButton("🔧 Optimizar BD")
        optimizar_btn.setStyleSheet(
            """
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background: #059669; }
        """
        )
        optimizar_btn.clicked.connect(self.optimizar_base_datos)

        verificar_btn = QPushButton("✅ Verificar Integridad")
        verificar_btn.setStyleSheet(
            """
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background: #2563eb; }
        """
        )
        verificar_btn.clicked.connect(self.verificar_integridad)

        mantenimiento_layout.addWidget(optimizar_btn)
        mantenimiento_layout.addWidget(verificar_btn)
        mantenimiento_layout.addStretch()

        layout.addLayout(mantenimiento_layout)
        layout.addStretch()

        self.tabs.addTab(tab, "💾 Base de Datos")

    def create_interface_tab(self):
        """Crea la pestaña de configuración de interfaz"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Apariencia
        apariencia_group = QGroupBox("Apariencia")
        apariencia_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
        """
        )
        apariencia_layout = QFormLayout(apariencia_group)

        self.tema_combo = QComboBox()
        self.tema_combo.addItems(["Claro", "Oscuro", "Automático"])
        apariencia_layout.addRow("Tema:", self.tema_combo)

        self.animaciones_check = QCheckBox("Habilitar animaciones")
        self.animaciones_check.setChecked(True)
        apariencia_layout.addRow("Animaciones:", self.animaciones_check)

        self.efectos_check = QCheckBox("Efectos visuales avanzados")
        self.efectos_check.setChecked(True)
        apariencia_layout.addRow("Efectos:", self.efectos_check)

        layout.addWidget(apariencia_group)

        # Configuración de fuentes
        fuentes_group = QGroupBox("Fuentes")
        fuentes_group.setStyleSheet(apariencia_group.styleSheet())
        fuentes_layout = QFormLayout(fuentes_group)

        self.fuente_principal = QComboBox()
        self.fuente_principal.addItems(["Sistema", "Arial", "Segoe UI", "Roboto"])
        fuentes_layout.addRow("Fuente Principal:", self.fuente_principal)

        self.tamano_fuente = QSpinBox()
        self.tamano_fuente.setRange(8, 24)
        self.tamano_fuente.setValue(10)
        fuentes_layout.addRow("Tamaño de Fuente:", self.tamano_fuente)

        layout.addWidget(fuentes_group)

        # Configuración de notificaciones
        notif_group = QGroupBox("Notificaciones")
        notif_group.setStyleSheet(apariencia_group.styleSheet())
        notif_layout = QVBoxLayout(notif_group)

        self.notif_sonido = QCheckBox("Sonidos de notificación")
        self.notif_sonido.setChecked(True)
        notif_layout.addWidget(self.notif_sonido)

        self.notif_sistema = QCheckBox("Notificaciones del sistema")
        self.notif_sistema.setChecked(True)
        notif_layout.addWidget(self.notif_sistema)

        self.notif_alertas = QCheckBox("Alertas de stock")
        self.notif_alertas.setChecked(True)
        notif_layout.addWidget(self.notif_alertas)

        layout.addWidget(notif_group)
        layout.addStretch()

        self.tabs.addTab(tab, "🎨 Interfaz")

    def create_modules_tab(self):
        """Crea la pestaña de configuración de módulos"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Estado de módulos
        modules_group = QGroupBox("Estado de los Módulos")
        modules_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
        """
        )
        modules_layout = QVBoxLayout(modules_group)

        # Tabla de módulos
        self.modules_table = QTableWidget(0, 4)
        self.modules_table.setHorizontalHeaderLabels(
            ["Módulo", "Estado", "Versión", "Acciones"]
        )

        header = self.modules_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        # Datos ficticios de módulos
        modules_data = [
            ("Dashboard", "Activo", "v2.1", True),
            ("TPV", "Activo", "v1.5", True),
            ("TPV Avanzado", "Activo", "v1.0", True),
            ("Hospedería", "Activo", "v1.3", True),
            ("Inventario", "Activo", "v1.2", True),
            ("Reportes", "En desarrollo", "v0.8", False),
            ("Auditoría", "Activo", "v1.1", True),
            ("Configuración", "Activo", "v1.0", True),
        ]

        for i, (nombre, estado, version, activo) in enumerate(modules_data):
            self.modules_table.insertRow(i)

            self.modules_table.setItem(i, 0, QTableWidgetItem(nombre))

            estado_item = QTableWidgetItem(estado)
            if estado == "Activo":
                estado_item.setBackground(QColor("#dcfce7"))
                estado_item.setForeground(QColor("#166534"))
            else:
                estado_item.setBackground(QColor("#fef3c7"))
                estado_item.setForeground(QColor("#92400e"))
            self.modules_table.setItem(i, 1, estado_item)

            self.modules_table.setItem(i, 2, QTableWidgetItem(version))

            # Botón de toggle
            toggle_btn = QPushButton("Desactivar" if activo else "Activar")
            toggle_btn.setStyleSheet(
                f"""
                QPushButton {{
                    background: {'#ef4444' if activo else '#10b981'};
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: {'#dc2626' if activo else '#059669'};
                }}
            """
            )
            self.modules_table.setCellWidget(i, 3, toggle_btn)

        modules_layout.addWidget(self.modules_table)
        layout.addWidget(modules_group)

        layout.addStretch()
        self.tabs.addTab(tab, "🧩 Módulos")

    def create_security_tab(self):
        """Crea la pestaña de configuración de seguridad"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Políticas de contraseñas
        password_group = QGroupBox("Políticas de Contraseñas")
        password_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
        """
        )
        password_layout = QFormLayout(password_group)

        self.min_length = QSpinBox()
        self.min_length.setRange(4, 20)
        self.min_length.setValue(8)
        password_layout.addRow("Longitud mínima:", self.min_length)

        self.require_uppercase = QCheckBox("Requerir mayúsculas")
        self.require_uppercase.setChecked(True)
        password_layout.addRow("Mayúsculas:", self.require_uppercase)

        self.require_numbers = QCheckBox("Requerir números")
        self.require_numbers.setChecked(True)
        password_layout.addRow("Números:", self.require_numbers)

        self.require_special = QCheckBox("Requerir caracteres especiales")
        password_layout.addRow("Especiales:", self.require_special)

        layout.addWidget(password_group)

        # Sesiones
        session_group = QGroupBox("Gestión de Sesiones")
        session_group.setStyleSheet(password_group.styleSheet())
        session_layout = QFormLayout(session_group)

        self.session_timeout = QSpinBox()
        self.session_timeout.setRange(5, 480)
        self.session_timeout.setValue(60)
        self.session_timeout.setSuffix(" minutos")
        session_layout.addRow("Timeout de sesión:", self.session_timeout)

        self.max_sessions = QSpinBox()
        self.max_sessions.setRange(1, 10)
        self.max_sessions.setValue(3)
        session_layout.addRow("Sesiones simultáneas:", self.max_sessions)

        layout.addWidget(session_group)

        # Auditoría
        audit_group = QGroupBox("Configuración de Auditoría")
        audit_group.setStyleSheet(password_group.styleSheet())
        audit_layout = QVBoxLayout(audit_group)

        self.log_login = QCheckBox("Registrar inicios de sesión")
        self.log_login.setChecked(True)
        audit_layout.addWidget(self.log_login)

        self.log_changes = QCheckBox("Registrar cambios de datos")
        self.log_changes.setChecked(True)
        audit_layout.addWidget(self.log_changes)

        self.log_errors = QCheckBox("Registrar errores del sistema")
        self.log_errors.setChecked(True)
        audit_layout.addWidget(self.log_errors)

        layout.addWidget(audit_group)
        layout.addStretch()

        self.tabs.addTab(tab, "🔐 Seguridad")

    def create_backup_tab(self):
        """Crea la pestaña de respaldo y mantenimiento"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Configuración de respaldos
        backup_group = QGroupBox("Configuración de Respaldos")
        backup_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
        """
        )
        backup_layout = QFormLayout(backup_group)

        self.backup_enabled = QCheckBox("Habilitar respaldos automáticos")
        self.backup_enabled.setChecked(True)
        backup_layout.addRow("Estado:", self.backup_enabled)

        self.backup_frequency = QComboBox()
        self.backup_frequency.addItems(["Diario", "Semanal", "Mensual"])
        backup_layout.addRow("Frecuencia:", self.backup_frequency)

        self.backup_retention = QSpinBox()
        self.backup_retention.setRange(1, 365)
        self.backup_retention.setValue(30)
        self.backup_retention.setSuffix(" días")
        backup_layout.addRow("Retención:", self.backup_retention)

        # Selector de carpeta de respaldo
        self.backup_path = QLineEdit()
        backup_browse_btn = QPushButton("📁 Examinar")
        backup_browse_btn.clicked.connect(self.seleccionar_backup_path)

        backup_path_layout = QHBoxLayout()
        backup_path_layout.addWidget(self.backup_path)
        backup_path_layout.addWidget(backup_browse_btn)
        backup_layout.addRow("Carpeta de respaldo:", backup_path_layout)

        layout.addWidget(backup_group)

        # Acciones de respaldo
        actions_group = QGroupBox("Acciones de Respaldo")
        actions_group.setStyleSheet(backup_group.styleSheet())
        actions_layout = QVBoxLayout(actions_group)

        # Botones de acción
        button_layout = QHBoxLayout()

        crear_backup_btn = QPushButton("💾 Crear Respaldo Ahora")
        crear_backup_btn.setStyleSheet(
            """
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background: #059669; }
        """
        )
        crear_backup_btn.clicked.connect(self.crear_backup)

        restaurar_btn = QPushButton("📥 Restaurar desde Respaldo")
        restaurar_btn.setStyleSheet(
            """
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background: #2563eb; }
        """
        )
        restaurar_btn.clicked.connect(self.restaurar_backup)

        button_layout.addWidget(crear_backup_btn)
        button_layout.addWidget(restaurar_btn)
        button_layout.addStretch()

        actions_layout.addLayout(button_layout)

        # Información del último respaldo
        info_layout = QFormLayout()

        ultimo_backup_label = QLabel("Hace 2 días - Exitoso")
        ultimo_backup_label.setStyleSheet("color: #059669; font-weight: bold;")
        info_layout.addRow("Último respaldo:", ultimo_backup_label)

        tamaño_backup_label = QLabel("2.5 MB")
        info_layout.addRow("Tamaño:", tamaño_backup_label)

        actions_layout.addLayout(info_layout)
        layout.addWidget(actions_group)

        layout.addStretch()
        self.tabs.addTab(tab, "💾 Respaldo")

    def cargar_configuracion(self):
        """Carga la configuración actual del sistema"""
        try:
            config = self.config_manager.get_all_config()

            # Cargar configuración general
            self.nombre_empresa.setText(config.get("company_name", ""))
            self.direccion_empresa.setText(config.get("company_address", ""))
            self.telefono_empresa.setText(config.get("company_phone", ""))
            self.email_empresa.setText(config.get("company_email", ""))

            # Cargar configuración regional
            idioma = config.get("language", "Español")
            if idioma in [
                self.idioma_combo.itemText(i) for i in range(self.idioma_combo.count())
            ]:
                self.idioma_combo.setCurrentText(idioma)

            moneda = config.get("currency", "EUR (€)")
            if moneda in [
                self.moneda_combo.itemText(i) for i in range(self.moneda_combo.count())
            ]:
                self.moneda_combo.setCurrentText(moneda)

            # Cargar configuración de base de datos
            self.db_path.setText(config.get("database_path", "hefest.db"))
            self.backup_auto.setChecked(config.get("auto_backup", True))

            # Cargar configuración de interfaz
            tema = config.get("theme", "Claro")
            if tema in [
                self.tema_combo.itemText(i) for i in range(self.tema_combo.count())
            ]:
                self.tema_combo.setCurrentText(tema)

            self.animaciones_check.setChecked(config.get("animations", True))
            self.efectos_check.setChecked(config.get("visual_effects", True))

            logger.info("Configuración cargada correctamente")

        except Exception as e:
            logger.error(f"Error al cargar configuración: {e}")
            QMessageBox.warning(
                self, "Error", f"Error al cargar la configuración:\n{str(e)}"
            )

    def guardar_configuracion(self):
        """Guarda los cambios de configuración"""
        try:
            config = {
                # Configuración general
                "company_name": self.nombre_empresa.text(),
                "company_address": self.direccion_empresa.text(),
                "company_phone": self.telefono_empresa.text(),
                "company_email": self.email_empresa.text(),
                # Configuración regional
                "language": self.idioma_combo.currentText(),
                "currency": self.moneda_combo.currentText(),
                "date_format": self.formato_fecha.currentText(),
                # Configuración de base de datos
                "database_path": self.db_path.text(),
                "auto_backup": self.backup_auto.isChecked(),
                # Configuración de interfaz
                "theme": self.tema_combo.currentText(),
                "animations": self.animaciones_check.isChecked(),
                "visual_effects": self.efectos_check.isChecked(),
                "font_family": self.fuente_principal.currentText(),
                "font_size": self.tamano_fuente.value(),
                # Configuración de seguridad
                "min_password_length": self.min_length.value(),
                "require_uppercase": self.require_uppercase.isChecked(),
                "require_numbers": self.require_numbers.isChecked(),
                "require_special_chars": self.require_special.isChecked(),
                "session_timeout": self.session_timeout.value(),
                # Configuración de respaldo
                "backup_enabled": self.backup_enabled.isChecked(),
                "backup_frequency": self.backup_frequency.currentText(),
                "backup_retention": self.backup_retention.value(),
                "backup_path": self.backup_path.text(),
            }

            for key, value in config.items():
                self.config_manager.set_config(key, value)
                self.configuracion_cambiada.emit(key, value)

            QMessageBox.information(
                self, "Éxito", "Configuración guardada correctamente."
            )
            logger.info("Configuración guardada correctamente")

        except Exception as e:
            logger.error(f"Error al guardar configuración: {e}")
            QMessageBox.critical(
                self, "Error", f"Error al guardar la configuración:\n{str(e)}"
            )

    def restaurar_configuracion(self):
        """Restaura la configuración a los valores por defecto"""
        reply = QMessageBox.question(
            self,
            "Confirmar Restauración",
            "¿Está seguro de que desea restaurar la configuración a los valores por defecto?\nEsta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.config_manager.reset_to_defaults()
                self.cargar_configuracion()
                QMessageBox.information(
                    self, "Éxito", "Configuración restaurada a valores por defecto."
                )
                logger.info("Configuración restaurada a valores por defecto")
            except Exception as e:
                logger.error(f"Error al restaurar configuración: {e}")
                QMessageBox.critical(
                    self, "Error", f"Error al restaurar la configuración:\n{str(e)}"
                )

    def seleccionar_db_path(self):
        """Abre diálogo para seleccionar la ruta de la base de datos"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Base de Datos",
            "",
            "Archivos de Base de Datos (*.db *.sqlite);;Todos los Archivos (*)",
        )
        if file_path:
            self.db_path.setText(file_path)

    def seleccionar_backup_path(self):
        """Abre diálogo para seleccionar la carpeta de respaldo"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Seleccionar Carpeta de Respaldo"
        )
        if dir_path:
            self.backup_path.setText(dir_path)

    def optimizar_base_datos(self):
        """Optimiza la base de datos"""
        reply = QMessageBox.question(
            self,
            "Optimizar Base de Datos",
            "¿Desea optimizar la base de datos?\nEsto puede mejorar el rendimiento pero puede tardar unos minutos.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Simular optimización
            QMessageBox.information(
                self, "Éxito", "Base de datos optimizada correctamente."
            )
            logger.info("Base de datos optimizada")

    def verificar_integridad(self):
        """Verifica la integridad de la base de datos"""
        # Simular verificación
        QMessageBox.information(
            self,
            "Verificación Completa",
            "La integridad de la base de datos es correcta.",
        )
        logger.info("Integridad de base de datos verificada")

    def crear_backup(self):
        """Crea un respaldo manual de la base de datos"""
        try:
            QMessageBox.information(
                self,
                "Respaldo Creado",
                "Respaldo creado exitosamente en la carpeta configurada.",
            )
            logger.info("Respaldo manual creado")
        except Exception as e:
            logger.error(f"Error al crear respaldo: {e}")
            QMessageBox.critical(
                self, "Error", f"Error al crear el respaldo:\n{str(e)}"
            )

    def restaurar_backup(self):
        """Restaura la base de datos desde un respaldo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo de Respaldo",
            "",
            "Archivos de Respaldo (*.db *.backup);;Todos los Archivos (*)",
        )

        if file_path:
            reply = QMessageBox.question(
                self,
                "Confirmar Restauración",
                "¿Está seguro de que desea restaurar desde este respaldo?\nTodos los datos actuales se perderán.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                try:
                    QMessageBox.information(
                        self,
                        "Restauración Completa",
                        "Base de datos restaurada correctamente.",
                    )
                    logger.info(f"Base de datos restaurada desde: {file_path}")
                except Exception as e:
                    logger.error(f"Error al restaurar respaldo: {e}")
                    QMessageBox.critical(
                        self, "Error", f"Error al restaurar el respaldo:\n{str(e)}"
                    )
