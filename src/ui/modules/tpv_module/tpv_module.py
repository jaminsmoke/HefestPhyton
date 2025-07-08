"""
Módulo TPV - Terminal Punto de Venta Profesional (Refactorizado)
Versión: v0.0.14
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
from .components.reservas_agenda.reserva_service import ReservaService
from .mesa_event_bus import mesa_event_bus

# Importar componentes refactorizados
# TPVDashboard eliminado para evitar métricas duplicadas
# from .components.tpv_dashboard import TPVDashboard
from .components.mesas_area import MesasArea
from .widgets.filters_panel import FiltersPanel
from .widgets.statistics_panel import StatisticsPanel
from .controllers.mesa_controller import MesaController
from .components.reservas_agenda.reservas_agenda_tab import ReservasAgendaTab

logger = logging.getLogger(__name__)



def clear_layout(widget):
    """Elimina el layout existente de un widget, si lo tiene, para evitar warnings de layouts duplicados."""
    old_layout = widget.layout() if hasattr(widget, 'layout') else None
    if old_layout is not None:
        while old_layout.count():
            item = old_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
        old_layout.deleteLater()

class TPVModule(BaseModule):
    """Módulo TPV principal con interfaz moderna y profesional (Refactorizado)"""

    def __init__(self, parent=None, db_manager=None):
        # ...existing code...
        super().__init__(parent)

        # Inicializar servicios, pasando db_manager si se recibe
        self._init_services(db_manager=db_manager)

        # Inicializar controladores
        self._init_controllers()

        # Configurar UI y cargar datos
        self.setup_ui()
        self.load_data()
        # ...existing code...
        self._connect_event_bus()

    def _connect_event_bus(self):
        mesa_event_bus.mesa_actualizada.connect(self._on_mesa_updated)
        mesa_event_bus.mesas_actualizadas.connect(self._on_mesas_updated)
        mesa_event_bus.mesa_clicked.connect(self._on_mesa_clicked)
        mesa_event_bus.mesa_creada.connect(self._on_mesa_creada)
        mesa_event_bus.mesa_eliminada.connect(self._on_mesa_eliminada)
        mesa_event_bus.alias_cambiado.connect(self._on_alias_cambiado)
        # Forzar emisión de mesas tras conectar señales para asegurar que la UI reciba la lista inicial
        try:
            from services.tpv_service import TPVService
            if hasattr(self, 'tpv_service') and self.tpv_service:
                mesa_event_bus.mesas_actualizadas.emit(self.tpv_service.get_mesas())
        except Exception:
            pass

    def _init_services(self, db_manager=None):
        """Inicializa los servicios necesarios"""
        try:
            from data.db_manager import DatabaseManager
            if db_manager is not None:
                self.db_manager = db_manager
                logger.info("TPVModule: DatabaseManager recibido por inyección")
            else:
                self.db_manager = DatabaseManager()
                logger.info("TPVModule: DatabaseManager creado internamente")
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
        # Eliminar las líneas de conexión directa a self.mesa_controller.mesa_updated.connect, self.mesa_controller.mesas_updated.connect, self.mesas_area.mesa_clicked.connect, etc.

    def create_module_header(self):
        # No usar header base, así el contenido se pega arriba
        return None

    def setup_ui(self):
        # Usar el layout de contenido, no el main_layout
        layout = self.content_layout
        layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
        layout.setSpacing(0)
        # Añadir el título pegado arriba
        title_section = self.create_title_section()
        layout.addWidget(title_section)
        # Separador visual después del título
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setLineWidth(1)
        separator.setStyleSheet("color: #e0e0e0; background-color: #e0e0e0;")
        layout.addWidget(separator)

        # Restablecer espaciado normal para el resto de elementos
        layout.setSpacing(8)
        # Área principal con pestañas refactorizada
        self.create_main_tabs(layout)
        # --- Sincronizar reservas con mesas ---
        # Si existe MesasArea y ReservaService, sincronizar reservas al iniciar
        if hasattr(self, 'mesas_area') and self.db_manager is not None:
            try:
                reserva_service = ReservaService(getattr(self.db_manager, 'db_path', 'data/hefest.db'))
                self.mesas_area.sync_reservas(reserva_service)  # type: ignore[reportAttributeAccessIssue]
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"No se pudo sincronizar reservas con mesas: {e}")

    def create_main_tabs(self, layout: QVBoxLayout):
        """Crea las pestañas principales usando componentes refactorizados"""
        from PyQt6.QtWidgets import QSizePolicy
        self.tab_widget = QTabWidget()
        # Forzar expansión horizontal del QTabWidget
        self.tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
        # Pestaña de agenda de reservas
        self.create_reservas_agenda_tab()
        # Pestañas de desarrollo (mantenemos las existentes)
        self.create_venta_rapida_tab()
        self.create_reportes_tab()

        layout.addWidget(self.tab_widget, 1)

    def create_mesas_tab_refactored(self):
        """Crea la pestaña de mesas con layout contextualizado y grid principal (usa referencias globales, el layout interno es de MesasArea)"""
        from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout
        # Widget principal de la pestaña de mesas
        self.mesas_widget = QWidget()
        self.mesas_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        # Refuerzo defensivo: limpiar layout anterior antes de crear uno nuevo y asignar layout con setLayout
        import logging
        clear_layout(self.mesas_widget)
        old_layout = self.mesas_widget.layout()
        if old_layout is not None:
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            try:
                old_layout.deleteLater()
            except Exception:
                pass
        self.mesas_layout = QVBoxLayout()
        self.mesas_layout.setContentsMargins(16, 16, 16, 16)
        self.mesas_layout.setSpacing(12)
        self.mesas_widget.setLayout(self.mesas_layout)

        # Área de mesas como elemento principal (incluye filtros integrados y estadísticas)
        self.mesas_area = MesasArea(db_manager=self.db_manager)
        self.mesas_area.eliminar_mesa_requested.connect(self.eliminar_mesa)
        self.mesas_area.eliminar_mesas_requested.connect(self.eliminar_mesas)
        self.mesas_area.nueva_mesa_con_zona_requested.connect(self.nueva_mesa_con_zona)

        # Añadir el widget MesasArea al layout de la pestaña
        self.mesas_layout.addWidget(self.mesas_area)

        self.tab_widget.addTab(self.mesas_widget, "🍽️ Gestión de Mesas")

    def eliminar_mesas(self, mesa_ids: list):
        """Elimina varias mesas de forma robusta y global, asegurando consistencia en UI y datos."""
        exitos = []
        fallos = []
        for mesa_id in mesa_ids:
            try:
                resultado = False
                if hasattr(self, 'mesa_controller') and self.mesa_controller:
                    resultado = self.mesa_controller.eliminar_mesa(mesa_id)
                elif hasattr(self, 'tpv_service') and self.tpv_service:
                    resultado = self.tpv_service.eliminar_mesa(mesa_id)
                if resultado:
                    exitos.append(mesa_id)
                else:
                    fallos.append(mesa_id)
            except Exception as e:
                fallos.append(mesa_id)
        # Refrescar UI y mostrar mensaje
        if exitos:
            self.mesas = [m for m in self.mesas if m.id not in exitos]
            if hasattr(self, 'tpv_service') and self.tpv_service:
                from .mesa_event_bus import mesa_event_bus
                mesa_event_bus.mesas_actualizadas.emit(self.tpv_service.get_mesas())
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Éxito", f"Mesas eliminadas correctamente: {', '.join(str(e) for e in exitos)}")
        if fallos:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "No se pudo eliminar", f"No se pudo eliminar alguna mesa: {', '.join(str(f) for f in fallos)}. Puede que estén ocupadas o haya un error interno.")
        self.mesas_area.nueva_mesa_con_zona_requested.connect(self.nueva_mesa_con_zona)
        # Todo el manejo de layout y tab está ahora en self.mesas_layout y self.mesas_widget

    def create_reservas_agenda_tab(self):
        """Crea la pestaña de agenda de reservas"""
        reservas_agenda_tab = ReservasAgendaTab(tpv_service=self.tpv_service)
        self.tab_widget.addTab(reservas_agenda_tab, "📅 Agenda Reservas")
        # --- Wiring de sincronización reactiva ---
        if hasattr(self, 'mesas_area'):
            try:
                reserva_service = reservas_agenda_tab.agenda_view.reserva_service
                reservas_agenda_tab.agenda_view.reserva_creada.connect(lambda: self.mesas_area.sync_reservas(reserva_service))
                reservas_agenda_tab.agenda_view.reserva_cancelada.connect(lambda: self.mesas_area.sync_reservas(reserva_service))
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"No se pudo conectar señales de reservas: {e}")

    def create_venta_rapida_tab(self):
        """Crea la pestaña de venta rápida"""
        venta_widget = QWidget()
        clear_layout(venta_widget)
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
        clear_layout(reportes_widget)
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

    def create_title_section(self) -> QWidget:
        """Crea una sección de título/información con fondo y efecto visual cohesivo con el header gris de HEFEST"""
        title_container = QFrame()
        title_container.setObjectName("TitleContainer")

        # Altura igualada visualmente al header gris
        title_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        title_container.setMinimumHeight(120)
        title_container.setMaximumHeight(120)
        title_container.setStyleSheet("""
            QFrame#TitleContainer {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f3f4f6, stop:1 #e5e7eb);
                border: none;
                border-radius: 0px;
                margin: 0px;
                padding: 0px;
                box-shadow: 0px 4px 16px 0px rgba(60,60,60,0.04);
                border-bottom: 2px solid #e0e0e0;
            }
        """)

        layout = QHBoxLayout(title_container)
        layout.setContentsMargins(32, 0, 32, 0)
        layout.setSpacing(20)

        # Icono y título principal
        icon_label = QLabel("🍽️")
        icon_label.setStyleSheet("font-size: 32px; margin-right: 16px;")
        layout.addWidget(icon_label)

        title_info = QVBoxLayout()
        title_info.setSpacing(2)

        main_title = QLabel("GESTIÓN DE MESAS - TPV")
        main_title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #1e293b;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        title_info.addWidget(main_title)

        subtitle = QLabel("Sistema de Terminal Punto de Venta")
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #64748b;
            font-weight: 500;
        """)
        title_info.addWidget(subtitle)

        layout.addLayout(title_info)
        layout.addStretch()

        # Estado del sistema
        status_container = QVBoxLayout()
        status_container.setSpacing(2)
        status_label = QLabel("● Sistema Activo")
        status_label.setStyleSheet("font-size: 13px; color: #16a34a; font-weight: bold;")
        status_container.addWidget(status_label)
        time_label = QLabel("Actualizado en tiempo real")
        time_label.setStyleSheet("font-size: 11px; color: #6b7280; font-style: italic;")
        status_container.addWidget(time_label)
        layout.addLayout(status_container)

        return title_container

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
            if hasattr(self, 'mesas_area'):
                self.mesas_area.set_mesas(
                    self.mesas,
                    datos_temporales=getattr(self.mesas_area, '_datos_temporales', None)
                )
            else:
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
                self.mesas_area.set_mesas(self.mesas)
        except Exception as e:
            logger.error(f"Error aplicando filtros: {e}")

    def _on_mesa_clicked(self, mesa: Mesa):
        """Callback cuando se hace clic en una mesa"""
        try:
            logger.info(f"Mesa {mesa.numero} seleccionada")
            from .dialogs.mesa_dialog import MesaDialog
            from .components.reservas_agenda.reserva_service import ReservaService
            from .components.reservas_agenda.reservas_agenda_tab import ReservasAgendaTab
            reserva_service = ReservaService(getattr(self.db_manager, 'db_path', 'data/hefest.db'))
            dialog = MesaDialog(mesa, self, reserva_service=reserva_service)
            dialog.iniciar_tpv_requested.connect(self._on_iniciar_tpv)
            dialog.crear_reserva_requested.connect(self._on_crear_reserva)
            dialog.cambiar_estado_requested.connect(self._on_cambiar_estado_mesa)
            # Eliminar cualquier línea como:
            # dialog.mesa_updated.connect(self._on_mesa_updated)
            dialog.reserva_cancelada.connect(lambda: self.mesas_area.sync_reservas(reserva_service))
            # Conexión directa a la agenda usando isinstance
            reservas_agenda_tab = None
            for i in range(self.tab_widget.count()):
                widget = self.tab_widget.widget(i)
                if isinstance(widget, ReservasAgendaTab):
                    reservas_agenda_tab = widget
                    break
            if reservas_agenda_tab:
                dialog.reserva_creada.connect(reservas_agenda_tab.agenda_view.load_reservas)
            dialog.exec()
        except Exception as e:
            logger.error(f"Error procesando clic en mesa: {e}")
            QMessageBox.critical(self, "Error", f"Error al abrir diálogo de mesa: {str(e)}")

    def _refresh_all_components(self):
        """Refresca todos los componentes después de cambios en los datos"""
        try:
            # Dashboard de métricas duplicadas eliminado
            # if hasattr(self, 'dashboard'):
            #     self.dashboard.update_metrics()

            # Actualizar área de mesas con los datos actuales
            if hasattr(self, 'mesas_area'):
                self.mesas_area.set_mesas(self.mesas)

            # Las estadísticas compactas se actualizan automáticamente en MesasArea

        except Exception as e:
            logger.error(f"Error refrescando componentes: {e}")

    # ======= MÉTODOS SIMPLIFICADOS (DELEGADOS AL CONTROLADOR) =======

    # MÉTODO OBSOLETO: La creación de mesas debe hacerse siempre vía nueva_mesa_con_zona
    # Se mantiene solo para compatibilidad, pero no debe usarse. Será eliminado en futuras versiones.
    # TODO v0.0.14: Eliminar este método y actualizar todos los llamados a nueva_mesa_con_zona
    def nueva_mesa(self):
        """[OBSOLETO] Crea una nueva mesa usando el controlador. Usar nueva_mesa_con_zona en su lugar."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Obsoleto", "El método 'nueva_mesa' está obsoleto. Usa 'nueva_mesa_con_zona'.")
        # No realiza ninguna acción

    def nueva_mesa_con_zona(self, numero: int, capacidad: int, zona: str):
        """Crea una nueva mesa de forma robusta y global, asegurando consistencia en UI y datos."""
        try:
            resultado = False
            if hasattr(self, 'mesa_controller') and self.mesa_controller:
                resultado = self.mesa_controller.crear_mesa_con_numero(numero, capacidad, zona) if hasattr(self.mesa_controller, 'crear_mesa_con_numero') else self.mesa_controller.crear_mesa(capacidad, zona)
            elif hasattr(self, 'tpv_service') and self.tpv_service:
                resultado = self.tpv_service.crear_mesa_con_numero(numero, capacidad, zona) if hasattr(self.tpv_service, 'crear_mesa_con_numero') else self.tpv_service.crear_mesa(capacidad, zona)
            if resultado:
                logger.info(f"Mesa creada en zona '{zona}' con número {numero} y capacidad {capacidad}")
                # Emitir evento global para refrescar UI
                mesa_event_bus.mesas_actualizadas.emit(self.tpv_service.get_mesas())
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Éxito", f"Mesa creada correctamente en zona '{zona}' con número {numero}")
            else:
                logger.warning(f"No se pudo crear la mesa en zona '{zona}' con número {numero}")
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "No se pudo crear", f"No se pudo crear la mesa en zona '{zona}' con número {numero}. Puede que ya exista o haya un error interno.")
        except Exception as e:
            logger.error(f"Error creando nueva mesa con zona: {e}")
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al crear mesa: {str(e)}")

    def eliminar_mesa(self, mesa_id: int):
        """Elimina una mesa de forma robusta y global, asegurando consistencia en UI y datos."""
        try:
            resultado = False
            if hasattr(self, 'mesa_controller') and self.mesa_controller:
                resultado = self.mesa_controller.eliminar_mesa(mesa_id)
            elif hasattr(self, 'tpv_service') and self.tpv_service:
                resultado = self.tpv_service.eliminar_mesa(mesa_id)
            if resultado:
                logger.info(f"Mesa {mesa_id} eliminada correctamente")
                self.mesas = [m for m in self.mesas if m.id != mesa_id]
                # Emitir evento global para refrescar UI
                mesa_event_bus.mesas_actualizadas.emit(self.tpv_service.get_mesas())
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Éxito", "Mesa eliminada correctamente")
            else:
                logger.warning(f"No se pudo eliminar la mesa {mesa_id}")
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "No se pudo eliminar", f"No se pudo eliminar la mesa {mesa_id}. Puede que esté ocupada o haya un error interno.")
        except Exception as e:
            logger.error(f"Error eliminando mesa: {e}")
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error eliminando mesa: {e}")

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

    def _on_iniciar_tpv(self, mesa_id: int):
        """Inicia el TPV para una mesa específica"""
        try:
            mesa = next((m for m in self.mesas if m.id == mesa_id), None)
            if mesa:
                logger.info(f"Iniciando TPV para mesa {mesa.numero}")

                # Importar y crear el TPV avanzado
                from .components.tpv_avanzado import TPVAvanzado
                from PyQt6.QtWidgets import QDialog, QVBoxLayout

                # Crear diálogo para el TPV
                dialog = QDialog(self)
                dialog.setWindowTitle(f"TPV - Mesa {mesa.numero}")
                dialog.setModal(True)
                dialog.resize(900, 700)

                layout = QVBoxLayout(dialog)
                layout.setContentsMargins(0, 0, 0, 0)

                # Crear el componente TPV avanzado
                tpv_widget = TPVAvanzado(mesa, self.tpv_service, dialog)

                # Conectar señales
                tpv_widget.pedido_completado.connect(
                    lambda mesa_id, total: self._on_pedido_completado(mesa_id, total, dialog)
                )

                layout.addWidget(tpv_widget)
                dialog.exec()

            else:
                QMessageBox.warning(self, "Error", "Mesa no encontrada")
        except Exception as e:
            logger.error(f"Error iniciando TPV: {e}")
            QMessageBox.critical(self, "Error", f"Error al abrir TPV: {str(e)}")

    def _on_pedido_completado(self, mesa_id: int, total: float, dialog):
        """Maneja la finalización de un pedido"""
        try:
            mesa = next((m for m in self.mesas if m.id == mesa_id), None)
            if mesa:
                QMessageBox.information(
                    self, "Pedido Completado",
                    f"Pedido de Mesa {mesa.numero} completado\nTotal: €{total:.2f}"
                )
                # Cerrar el diálogo del TPV
                dialog.accept()
                # Recargar mesas para actualizar estado
                self.mesa_controller.cargar_mesas()
        except Exception as e:
            logger.error(f"Error procesando pedido completado: {e}")

    def _on_crear_reserva(self, mesa_id: int):
        """Crea una reserva para una mesa específica"""
        try:
            mesa = next((m for m in self.mesas if m.id == mesa_id), None)
            if mesa:
                logger.info(f"Creando reserva para mesa {mesa.numero}")
                QMessageBox.information(self, "Reserva", f"Creando reserva para Mesa {mesa.numero}")
                # TODO: Implementar sistema de reservas
            else:
                QMessageBox.warning(self, "Error", "Mesa no encontrada")
        except Exception as e:
            logger.error(f"Error creando reserva: {e}")

    def _on_cambiar_estado_mesa(self, mesa_id: int, nuevo_estado: str):
        """Cambia el estado de una mesa"""
        try:
            if self.mesa_controller.cambiar_estado_mesa(mesa_id, nuevo_estado):
                logger.info(f"Estado de mesa {mesa_id} cambiado a {nuevo_estado}")
                # Recargar mesas para reflejar el cambio
                self.mesa_controller.cargar_mesas()
            else:
                QMessageBox.warning(self, "Error", "No se pudo cambiar el estado de la mesa")
        except Exception as e:
            logger.error(f"Error cambiando estado de mesa: {e}")
            QMessageBox.critical(self, "Error", f"Error al cambiar estado: {str(e)}")
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

    def _on_mesa_creada(self, mesa):
        pass
    def _on_mesa_eliminada(self, mesa_id):
        pass
    def _on_alias_cambiado(self, mesa, nuevo_alias):
        pass

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Crear y mostrar el módulo TPV
    tpv = TPVModule()
    tpv.show()
    tpv.resize(1200, 800)

    sys.exit(app.exec())
