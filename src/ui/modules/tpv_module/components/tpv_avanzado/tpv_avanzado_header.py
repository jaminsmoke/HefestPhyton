"""
TPV Avanzado - Header modularizado
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QComboBox
from services.auth_service import get_auth_service
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def create_header(parent, parent_layout):
    """Crea el header del TPV avanzado, centrado y con título perfectamente legible y elegante"""
    header = QFrame()
    header.setStyleSheet("""
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            border-top-left-radius: 22px;
            border-top-right-radius: 22px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            box-shadow: 0 4px 18px 0 rgba(102,126,234,0.10);
            margin: 0px 0px 12px 0px;
        }
    """)
    header.setFixedHeight(104)

    layout = QVBoxLayout(header)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

    # Título destacado con fondo blanco translúcido y texto morado oscuro
    title = QLabel("🍽️ TPV Avanzado")
    title.setFont(QFont("Segoe UI", 25, QFont.Weight.ExtraBold))
    title.setStyleSheet("""
        background: rgba(255,255,255,0.92);
        color: #4B2991;
        border-radius: 20px;
        padding: 0px 38px 0px 38px;
        margin-top: 2px;
        margin-bottom: 2px;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 12px 0 rgba(102,126,234,0.13);
    """)
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)
    # Selector de usuario (ComboBox)
    user_selector_layout = QHBoxLayout()
    user_selector_layout.setContentsMargins(0, 0, 0, 0)
    user_selector_layout.setSpacing(8)
    user_selector_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    user_label = QLabel("👤 Usuario:")
    user_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
    user_label.setStyleSheet("color: #fff; background: transparent; margin-right: 4px;")
    user_selector_layout.addWidget(user_label)

    user_combo = QComboBox()
    user_combo.setObjectName("user_selector_combo")
    user_combo.setStyleSheet("""
        QComboBox {
            background: rgba(255,255,255,0.92);
            color: #4B2991;
            border-radius: 12px;
            padding: 2px 18px 2px 8px;
            font-size: 15px;
            min-width: 120px;
        }
    """)
    user_combo.setFont(QFont("Segoe UI", 13, QFont.Weight.Normal))

    # Poblar usuarios activos
    auth_service = get_auth_service()
    users = [u for u in auth_service.users if u.is_active]
    for user in users:
        user_combo.addItem(f"{user.name} ({user.role.value})", user.id)

    # Seleccionar usuario actual si existe
    current_user = auth_service.current_user
    if current_user:
        idx = user_combo.findData(current_user.id)
        if idx >= 0:
            user_combo.setCurrentIndex(idx)


    def on_user_changed(index):
        user_id = user_combo.itemData(index)
        selected_user = next((u for u in users if u.id == user_id), None)
        if not selected_user:
            return
        # Si el usuario seleccionado es el mismo, no hacer nada
        if hasattr(parent, 'selected_user') and parent.selected_user and parent.selected_user.id == selected_user.id:
            return

        # Pedir PIN del usuario seleccionado
        from PyQt6.QtWidgets import QInputDialog, QMessageBox, QLineEdit
        pin, ok = QInputDialog.getText(parent, "Autenticación requerida", f"Introduce el PIN de {selected_user.name}:", QLineEdit.EchoMode.Password)
        if not ok:
            # Cancelado, volver al usuario anterior
            if hasattr(parent, 'selected_user') and parent.selected_user:
                idx = user_combo.findData(parent.selected_user.id)
                if idx >= 0:
                    user_combo.blockSignals(True)
                    user_combo.setCurrentIndex(idx)
                    user_combo.blockSignals(False)
            return

        # Validar PIN
        auth_service = get_auth_service()
        # Validar que el id no sea None
        if selected_user.id is None:
            QMessageBox.warning(parent, "Error de autenticación", f"El usuario seleccionado no tiene ID válido. Se mantiene el usuario actual.")
            if hasattr(parent, 'selected_user') and parent.selected_user:
                idx = user_combo.findData(parent.selected_user.id)
                if idx >= 0:
                    user_combo.blockSignals(True)
                    user_combo.setCurrentIndex(idx)
                    user_combo.blockSignals(False)
            return
        if not auth_service.login(int(selected_user.id), pin):
            # Log intento fallido
            import logging
            logging.getLogger(__name__).warning(f"Intento fallido de login para usuario {selected_user.username} desde TPV avanzado.")
            QMessageBox.warning(parent, "Error de autenticación", f"PIN incorrecto para {selected_user.name}. Se mantiene el usuario actual.")
            # Volver al usuario anterior
            if hasattr(parent, 'selected_user') and parent.selected_user:
                idx = user_combo.findData(parent.selected_user.id)
                if idx >= 0:
                    user_combo.blockSignals(True)
                    user_combo.setCurrentIndex(idx)
                    user_combo.blockSignals(False)
            return

        # Autenticación exitosa: cambiar usuario
        parent.selected_user = selected_user
        # Feedback visual: resaltar usuario activo
        user_combo.setStyleSheet(user_combo.styleSheet() + "QComboBox { font-weight: bold; background: #e0e7ff; }")
        # TODO: Propagar cambio de usuario a operaciones relevantes y refrescar UI
        # Mensaje opcional de éxito
        # QMessageBox.information(parent, "Usuario cambiado", f"Ahora operando como {selected_user.name}.")

    user_combo.currentIndexChanged.connect(on_user_changed)
    parent.user_selector_combo = user_combo
    parent.selected_user = current_user if current_user else (users[0] if users else None)
    user_selector_layout.addWidget(user_combo)
    layout.addLayout(user_selector_layout)

    # Información de la mesa, centrada y con mejor contraste
    parent.header_mesa_label = QLabel("Seleccione una mesa")
    if getattr(parent, 'mesa', None):
        parent.header_mesa_label.setText(f"Mesa {parent.mesa.numero} - {parent.mesa.zona}")
    parent.header_mesa_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Medium))
    parent.header_mesa_label.setStyleSheet("color: rgba(255,255,255,0.96); margin-top: 2px; margin-bottom: 10px;")
    parent.header_mesa_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(parent.header_mesa_label)

    parent_layout.addWidget(header)
