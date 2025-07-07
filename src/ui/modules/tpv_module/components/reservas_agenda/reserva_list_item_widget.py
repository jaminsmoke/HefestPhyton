"""
Widget visual personalizado para mostrar una reserva en la agenda.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from src.utils.modern_styles import ModernStyles

class ReservaListItemWidget(QWidget):
    def __init__(self, reserva, parent=None):
        super().__init__(parent)
        self.reserva = reserva
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(12)

        # Estado badge
        estado = getattr(self.reserva, 'estado', 'pendiente')
        badge = QLabel(estado.capitalize())
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFixedWidth(80)
        badge.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        badge.setStyleSheet(ModernStyles.get_reserva_badge_style(estado))
        layout.addWidget(badge)

        # Info principal (cliente, hora, mesa)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        # Cliente
        cliente = getattr(self.reserva, 'cliente_nombre', 'Sin nombre')
        label_cliente = QLabel(f"👤 {cliente}")
        label_cliente.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        info_layout.addWidget(label_cliente)
        # Fecha/hora
        fecha = getattr(self.reserva, 'fecha_reserva', None)
        hora = getattr(self.reserva, 'hora_reserva', None)
        if fecha and hora:
            fecha_hora = f"{fecha.strftime('%d/%m/%Y')} {hora}"
        elif fecha:
            fecha_hora = fecha.strftime('%d/%m/%Y')
        else:
            fecha_hora = ''
        label_fecha = QLabel(f"🕒 {fecha_hora}")
        label_fecha.setFont(QFont('Segoe UI', 10))
        info_layout.addWidget(label_fecha)
        # Mesa
        mesa_id = getattr(self.reserva, 'mesa_id', '-')
        alias = getattr(self.reserva, 'alias', '')
        label_mesa = QLabel(f"Mesa {mesa_id}{f' ({alias})' if alias else ''}")
        label_mesa.setFont(QFont('Segoe UI', 10))
        info_layout.addWidget(label_mesa)
        layout.addLayout(info_layout, 2)

        # Detalles secundarios (personas, teléfono, notas)
        detalles_layout = QVBoxLayout()
        detalles_layout.setSpacing(2)
        # Personas
        personas = getattr(self.reserva, 'numero_personas', None)
        if personas:
            label_personas = QLabel(f"👥 {personas} pers.")
            label_personas.setFont(QFont('Segoe UI', 10))
            detalles_layout.addWidget(label_personas)
        # Teléfono
        telefono = getattr(self.reserva, 'cliente_telefono', None)
        if telefono:
            label_tel = QLabel(f"📞 {telefono}")
            label_tel.setFont(QFont('Segoe UI', 10))
            detalles_layout.addWidget(label_tel)
        # Notas
        notas = getattr(self.reserva, 'notas', None)
        if notas:
            label_notas = QLabel(f"📝 {notas}")
            label_notas.setFont(QFont('Segoe UI', 9))
            detalles_layout.addWidget(label_notas)
        layout.addLayout(detalles_layout, 1)

        self.setStyleSheet(ModernStyles.get_reserva_list_item_style())

    def _badge_style(self, estado):
        # DEPRECATED: Usar ModernStyles.get_reserva_badge_style(estado)
        return ModernStyles.get_reserva_badge_style(estado)
