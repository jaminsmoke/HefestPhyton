"""
Módulo TPV - Terminal Punto de Venta Profesional (Refactorizado)
Versión: v0.0.14
"""

import logging
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.services.tpv_service import Comanda, Mesa, Producto, TPVService
from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus
from src.ui.modules.module_base_interface import BaseModule

# Importar componentes refactorizados
# TPVDashboard eliminado para evitar métricas duplicadas
# from .components.tpv_dashboard import TPVDashboard
from .components.mesas_area import MesasArea
from .components.reservas_agenda.reserva_service import ReservaService
from .components.reservas_agenda.reservas_agenda_tab import ReservasAgendaTab
from .controllers.mesa_controller import MesaController

logger = logging.getLogger(__name__)


def clear_layout(widget: QWidget) -> None:
    """Elimina el layout existente para evitar warnings de duplicados."""
    old_layout = widget.layout() if hasattr(widget, "layout") else None  # type: ignore
    if old_layout is not None:
        while old_layout.count():  # type: ignore
            item = old_layout.takeAt(0)  # type: ignore
            w = item.widget()  # type: ignore
            if w is not None:
                w.setParent(None)  # type: ignore
        old_layout.deleteLater()  # type: ignore


class TPVModule(BaseModule):
    """Módulo TPV principal con interfaz moderna (Refactorizado)"""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        db_manager: Optional[Any] = None,
    ) -> None:
        # ...existing code...
        super().__init__(parent)  # type: ignore[misc]

        # Inicializar servicios, pasando db_manager si se recibe
        self._init_services(db_manager=db_manager)

        # Inicializar controladores
        self._init_controllers()

        # Configurar UI y cargar datos
        self.setup_ui()
        self.load_data()
        # ...existing code...
        self._connect_event_bus()

    def _connect_event_bus(self) -> None:
        """Conecta las señales del event bus de mesas"""
        # Conectar eventos de mesas
        mesa_event_bus.mesa_actualizada.connect(self._on_mesa_updated)  # type: ignore
        mesa_event_bus.mesas_actualizadas.connect(
            self._on_mesas_updated
        )  # type: ignore
        mesa_event_bus.mesa_clicked.connect(self._on_mesa_clicked)  # type: ignore
        mesa_event_bus.mesa_creada.connect(self._on_mesa_creada)  # type: ignore
        mesa_event_bus.mesa_eliminada.connect(self._on_mesa_eliminada)  # type: ignore
        mesa_event_bus.alias_cambiado.connect(self._on_alias_cambiado)  # type: ignore

        # Forzar emisión inicial para UI
        try:
            pass

            if hasattr(self, "tpv_service") and self.tpv_service:
                mesa_event_bus.mesas_actualizadas.emit(self.tpv_service.get_mesas())
        except Exception:
            pass

    def _init_services(self, db_manager: Optional[Any] = None) -> None:
        """Inicializa los servicios necesarios"""
        try:
            from data.db_manager import DatabaseManager

            if db_manager is not None:
                self.db_manager = db_manager
                # DatabaseManager recibido por inyección
            else:
                self.db_manager = DatabaseManager()
                # DatabaseManager creado internamente
        except Exception as e:
            logger.error(f"TPVModule: Error creando DatabaseManager: {e}")
            self.db_manager = None

        self.tpv_service = TPVService(self.db_manager)
        self.mesas: List[Mesa] = []
        self.productos: List[Producto] = []
        self.current_comanda: Optional[Comanda] = None

    def _init_controllers(self) -> None:
        """Inicializa los controladores"""
        self.mesa_controller = MesaController(self.tpv_service)
        # Conectar señales del controlador
        # Eliminar conexiones directas obsoletas

    def create_module_header(self) -> None:  # type: ignore
        # No usar header base, así el contenido se pega arriba
        return None

    def setup_ui(self) -> None:
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

        # Configuración inicial de estado de mesas
        try:
            if hasattr(self, "mesas_area") and hasattr(
                self.mesas_area, "comprobar_estado_mesas_inicial"
            ):
                self.mesas_area.comprobar_estado_mesas_inicial()
                # EXCEPCIÓN FUNCIONAL: Acceso protegido para sincronización
                # pylint: disable=protected-access
                self.mesas_area._marcar_mesas_ocupadas_por_comanda()  # type: ignore
                self.mesas_area.update_filtered_mesas()
                from .components.mesas_area.mesas_area_grid import (
                    populate_grid,
                )

                populate_grid(self.mesas_area)
        except Exception as e:
            import logging

            logging.getLogger(__name__).error(
                "Error comprobando estado inicial de mesas: %s", e
            )

        # Sincronizar reservas con mesas
        if hasattr(self, "mesas_area") and self.db_manager is not None:
            try:
                reserva_service = ReservaService(
                    getattr(self.db_manager, "db_path", "data/hefest.db")
                )
                self.mesas_area.sync_reservas(
                    reserva_service
                )  # type: ignore[reportAttributeAccessIssue]
            except Exception as e:
                import logging

                logging.getLogger(__name__).error(
                    f"No se pudo sincronizar reservas con mesas: {e}"
                )

    def create_main_tabs(self, layout: QVBoxLayout) -> None:
        """Crea las pestañas principales usando componentes refactorizados"""
        from PyQt6.QtWidgets import QSizePolicy

        self.tab_widget = QTabWidget()
        # Forzar expansión horizontal del QTabWidget
        self.tab_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.tab_widget.setStyleSheet(
            """
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
            }        """
        )

        # Pestaña de mesas (refactorizada)
        self.create_mesas_tab_refactored()
        # Pestaña de agenda de reservas
        self.create_reservas_agenda_tab()
        # Pestañas de desarrollo (mantenemos las existentes)
        self.create_venta_rapida_tab()
        self.create_reportes_tab()

        layout.addWidget(self.tab_widget, 1)

    def create_mesas_tab_refactored(self):
        """Crea la pestaña de mesas con layout y grid principal"""
        from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

        # Widget principal de la pestaña de mesas
        self.mesas_widget = QWidget()
        self.mesas_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        # Refuerzo defensivo: limpiar layout anterior antes de crear
        # nuevo y asignar layout con setLayout

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

        # Área de mesas como elemento principal (filtros y estadísticas)
        self.mesas_area = MesasArea()

        # FIX v0.0.14: Inicializar servicios para funcionalidad
        self.mesas_area.init_with_services(
            tpv_service=self.tpv_service,
            db_manager=self.db_manager,
            parent=self.mesas_widget,
        )

        # Conectar señales de MesasArea
        self.mesas_area.eliminar_mesa_requested.connect(
            self.eliminar_mesa
        )  # type: ignore[misc]
        self.mesas_area.eliminar_mesas_requested.connect(
            self.eliminar_mesas
        )  # type: ignore[misc]
        self.mesas_area.nueva_mesa_con_zona_requested.connect(
            self.nueva_mesa_con_zona
        )  # type: ignore[misc]

        # Añadir el widget MesasArea al layout de la pestaña
        self.mesas_layout.addWidget(self.mesas_area)

        self.tab_widget.addTab(self.mesas_widget, "🍽️ Gestión de Mesas")

    def eliminar_mesas(self, mesa_numeros: List[Any]) -> None:
        """Elimina varias mesas asegurando consistencia en UI y datos."""
        exitos: List[Any] = []
        fallos: List[Any] = []
        for numero in mesa_numeros:
            try:
                resultado = False
                if hasattr(self, "mesa_controller") and self.mesa_controller:
                    resultado = self.mesa_controller.eliminar_mesa(numero)
                elif hasattr(self, "tpv_service") and self.tpv_service:
                    resultado = self.tpv_service.eliminar_mesa(numero)
                if resultado:
                    exitos.append(numero)
                else:
                    fallos.append(numero)
            except Exception:
                fallos.append(numero)
        # Refrescar UI y mostrar mensaje
        if exitos:
            self.mesas = [m for m in self.mesas if m.numero not in exitos]
            if hasattr(self, "tpv_service") and self.tpv_service:
                from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

                mesa_event_bus.mesas_actualizadas.emit(self.tpv_service.get_mesas())
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.information(
                self,
                "Éxito",
                f"Mesas eliminadas: {', '.join(str(e) for e in exitos)}",
            )
        if fallos:
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self,
                "Error",
                f"Error eliminando: {', '.join(str(f) for f in fallos)}. "
                "Pueden estar ocupadas.",
            )
        # Manejo de layout en self.mesas_layout y self.mesas_widget

    def create_reservas_agenda_tab(self):
        """Crea la pestaña de agenda de reservas"""
        reservas_agenda_tab = ReservasAgendaTab(tpv_service=self.tpv_service)
        self.tab_widget.addTab(reservas_agenda_tab, "📅 Agenda Reservas")
        # --- Wiring de sincronización reactiva ---
        if hasattr(self, "mesas_area"):
            try:
                reserva_service = reservas_agenda_tab.agenda_view.reserva_service
                reservas_agenda_tab.agenda_view.reserva_creada.connect(
                    lambda: self.mesas_area.sync_reservas(reserva_service)
                )  # type: ignore[misc]
                reservas_agenda_tab.agenda_view.reserva_cancelada.connect(
                    lambda: self.mesas_area.sync_reservas(reserva_service)
                )  # type: ignore[misc]
            except Exception as e:
                import logging

                logging.getLogger(__name__).error(
                    f"No se pudo conectar señales de reservas: {e}"
                )

    def create_venta_rapida_tab(self):
        """Crea la pestaña de venta rápida"""
        venta_widget = QWidget()
        clear_layout(venta_widget)
        layout = QVBoxLayout(venta_widget)
        layout.setContentsMargins(24, 24, 24, 24)

        # Placeholder para venta rápida
        placeholder = QLabel("🚀 Venta Rápida - En desarrollo")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                color: #666;
                margin: 50px;
            }
        """
        )
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
        placeholder.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                color: #666;
                margin: 50px;
            }
        """
        )
        layout.addWidget(placeholder)

        self.tab_widget.addTab(reportes_widget, "📈 Reportes")

    def create_title_section(self) -> QWidget:
        """Crea sección título/información con fondo gris cohesivo"""
        title_container = QFrame()
        title_container.setObjectName("TitleContainer")

        # Altura igualada visualmente al header gris
        title_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        title_container.setMinimumHeight(120)
        title_container.setMaximumHeight(120)
        title_container.setStyleSheet(
            """
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
        """
        )

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
        main_title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            color: #1e293b;
            font-family: 'Segoe UI', Arial, sans-serif;
        """
        )
        title_info.addWidget(main_title)

        subtitle = QLabel("Sistema de Terminal Punto de Venta")
        subtitle.setStyleSheet(
            """
            font-size: 13px;
            color: #64748b;
            font-weight: 500;
        """
        )
        title_info.addWidget(subtitle)

        layout.addLayout(title_info)
        layout.addStretch()

        # Estado del sistema
        status_container = QVBoxLayout()
        status_container.setSpacing(2)
        status_label = QLabel("● Sistema Activo")
        status_label.setStyleSheet(
            "font-size: 13px; color: #16a34a; font-weight: bold;"
        )
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
            # logger.debug(f"Mesa {mesa.numero} creada exitosamente")
            self.mesas.append(mesa)
            self._refresh_all_components()
            QMessageBox.information(
                self, "Éxito", f"Mesa {mesa.numero} creada correctamente"
            )
        except Exception as e:
            logger.error(f"Error procesando creación de mesa: {e}")

    def _on_mesa_updated(self, mesa: Mesa):
        """Callback cuando se actualiza una mesa"""
        try:
            # logger.debug(f"Mesa {mesa.numero} actualizada exitosamente")
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
            # logger.debug(f"Mesa {mesa_id} eliminada exitosamente")
            self.mesas = [m for m in self.mesas if m.id != mesa_id]
            self._refresh_all_components()
        except Exception as e:
            logger.error(f"Error procesando eliminación de mesa: {e}")

    def _on_mesas_updated(self, mesas: List[Mesa]):
        """Callback cuando se actualiza la lista completa de mesas"""
        try:
            # logger.debug(f"Lista de mesas actualizada: {len(mesas)} mesas")
            self.mesas = mesas
            if hasattr(self, "mesas_area"):
                self.mesas_area.set_mesas(
                    self.mesas,
                    datos_temporales=getattr(
                        self.mesas_area, "_datos_temporales", None
                    ),
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
            # logger.debug(f"Filtros cambiados: {filters}")
            if hasattr(self, "mesas_area"):
                self.mesas_area.set_mesas(self.mesas)
        except Exception as e:
            logger.error(f"Error aplicando filtros: {e}")

    def _on_mesa_clicked(self, mesa: Mesa):
        """Callback cuando se hace clic en una mesa"""
        try:
            # logger.debug(f"Mesa {mesa.numero} seleccionada")
            from .components.reservas_agenda.reserva_service import ReservaService
            from .components.reservas_agenda.reservas_agenda_tab import (
                ReservasAgendaTab,
            )
            from .dialogs.mesa_dialog import MesaDialog

            reserva_service = ReservaService(
                getattr(self.db_manager, "db_path", "data/hefest.db")
            )
            dialog = MesaDialog(mesa, self, reserva_service=reserva_service)
            dialog.iniciar_tpv_requested.connect(
                self._on_iniciar_tpv
            )  # type: ignore[misc]
            dialog.crear_reserva_requested.connect(
                self._on_crear_reserva
            )  # type: ignore[misc]
            dialog.cambiar_estado_requested.connect(
                self._on_cambiar_estado_mesa
            )  # type: ignore[misc]
            # Eliminar cualquier línea como:
            # dialog.mesa_updated.connect(self._on_mesa_updated)
            dialog.reserva_cancelada.connect(  # type: ignore[misc]
                lambda: self.mesas_area.sync_reservas(reserva_service)
            )
            # Conexión directa a la agenda usando isinstance
            reservas_agenda_tab = None
            for i in range(self.tab_widget.count()):
                widget = self.tab_widget.widget(i)
                if isinstance(widget, ReservasAgendaTab):
                    reservas_agenda_tab = widget
                    break
            if reservas_agenda_tab:
                dialog.reserva_creada.connect(  # type: ignore[misc]
                    reservas_agenda_tab.agenda_view.load_reservas
                )
            dialog.exec()
        except Exception as e:
            logger.error(f"Error procesando clic en mesa: {e}")
            QMessageBox.critical(
                self, "Error", f"Error al abrir diálogo de mesa: {str(e)}"
            )

    def _refresh_all_components(self):
        """Refresca todos los componentes después de cambios en los datos"""
        try:
            # Dashboard de métricas duplicadas eliminado
            # if hasattr(self, 'dashboard'):
            #     self.dashboard.update_metrics()

            # Actualizar área de mesas con los datos actuales
            if hasattr(self, "mesas_area"):
                self.mesas_area.set_mesas(self.mesas)

            # Estadísticas compactas se actualizan automáticamente

        except Exception as e:
            logger.error(f"Error refrescando componentes: {e}")

    # ======= MÉTODOS SIMPLIFICADOS (DELEGADOS AL CONTROLADOR) =======

    # Método obsoleto - usar nueva_mesa_con_zona
    # Mantenido para compatibilidad, será eliminado
    # TODO v0.0.14: Eliminar método
    def nueva_mesa(self):
        """[OBSOLETO] Usar nueva_mesa_con_zona en su lugar."""
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.warning(
            self,
            "Obsoleto",
            "Usar 'nueva_mesa_con_zona'.",
        )

    def nueva_mesa_con_zona(self, numero: int, capacidad: int, zona: str):
        """Crea nueva mesa asegurando consistencia en UI y datos."""
        try:
            resultado = False
            if hasattr(self, "mesa_controller") and self.mesa_controller:
                resultado = (
                    self.mesa_controller.crear_mesa_con_numero(numero, capacidad, zona)
                    if hasattr(self.mesa_controller, "crear_mesa_con_numero")
                    else self.mesa_controller.crear_mesa(capacidad, zona)
                )
            elif hasattr(self, "tpv_service") and self.tpv_service:
                resultado = (
                    self.tpv_service.crear_mesa_con_numero(numero, capacidad, zona)
                    if hasattr(self.tpv_service, "crear_mesa_con_numero")
                    else self.tpv_service.crear_mesa(capacidad, zona)
                )
            if resultado:
                # Mesa creada correctamente
                # Emitir evento global para refrescar UI
                mesa_event_bus.mesas_actualizadas.emit(self.tpv_service.get_mesas())
                from PyQt6.QtWidgets import QMessageBox

                QMessageBox.information(
                    self,
                    "Éxito",
                    f"Mesa creada en zona '{zona}' con número {numero}",
                )
            else:
                logger.warning(f"Error al crear mesa en zona '{zona}' número {numero}")
                from PyQt6.QtWidgets import QMessageBox

                QMessageBox.warning(
                    self,
                    "No se pudo crear",
                    f"Mesa {numero} en zona '{zona}' puede que ya exista "
                    f"o haya un error interno.",
                )
        except Exception as e:
            logger.error(f"Error creando nueva mesa con zona: {e}")
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.critical(self, "Error", f"Error al crear mesa: {str(e)}")

    def eliminar_mesa(self, mesa_id: int):
        """Elimina una mesa de forma robusta asegurando consistencia."""
        try:
            resultado = False
            if hasattr(self, "mesa_controller") and self.mesa_controller:
                resultado = self.mesa_controller.eliminar_mesa(
                    str(mesa_id)
                )  # TODO: Refactor global, mesa_id ahora debe ser numero (str)
            elif hasattr(self, "tpv_service") and self.tpv_service:
                # Usar el método correcto que acepta 'numero' (str)
                if hasattr(self.tpv_service, "eliminar_mesa_por_numero"):
                    resultado = self.tpv_service.eliminar_mesa_por_numero(str(mesa_id))
                else:
                    # EXCEPCIÓN FUNCIONAL: fallback legacy
                    resultado = self.tpv_service.eliminar_mesa(mesa_id)
            if resultado:
                # logger.debug(f"Mesa {mesa_id} eliminada correctamente")
                self.mesas = [m for m in self.mesas if m.id != mesa_id]
                # Emitir evento global para refrescar UI
                mesa_event_bus.mesas_actualizadas.emit(self.tpv_service.get_mesas())
                from PyQt6.QtWidgets import QMessageBox

                QMessageBox.information(self, "Éxito", "Mesa eliminada correctamente")
            else:
                logger.warning(f"No se pudo eliminar la mesa {mesa_id}")
                from PyQt6.QtWidgets import QMessageBox

                QMessageBox.warning(
                    self,
                    "No se pudo eliminar",
                    f"Error al eliminar mesa {mesa_id}. "
                    f"Puede que esté ocupada o haya un error interno.",
                )
        except Exception as e:
            logger.error(f"Error eliminando mesa: {e}")
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.critical(self, "Error", f"Error eliminando mesa: {e}")

    def load_data(self):
        """Carga los datos iniciales usando el controlador"""
        try:
            # logger.debug("Cargando datos del TPV...")
            self.mesa_controller.cargar_mesas()

            # FIX v0.0.14: Obtener las mesas del controlador y pasarlas al TPVModule
            self.mesas = self.mesa_controller.mesas

            if self.tpv_service:
                self.productos = self.tpv_service.get_productos()
                # logger.debug("Datos del TPV cargados correctamente")

                # FIX v0.0.14: Asegurar que mesas_area reciba las mesas cargadas
                if hasattr(self, "mesas_area") and self.mesas:
                    self.mesas_area.set_mesas(self.mesas)
                # Las estadísticas compactas se actualizan automáticamente en MesasArea

            else:
                logger.warning("No hay servicio TPV disponible")
        except Exception as e:
            logger.error(f"Error cargando datos del TPV: {e}")

    def _on_iniciar_tpv(self, mesa_id: int):
        """Inicia el TPV para una mesa específica"""
        try:
            mesa = next((m for m in self.mesas if m.id == mesa_id), None)
            if mesa:
                # logger.debug(f"Iniciando TPV para mesa {mesa.numero}")

                # Importar y crear el TPV avanzado
                from PyQt6.QtWidgets import QDialog, QVBoxLayout

                from .components.tpv_avanzado import TPVAvanzado

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
                tpv_widget.pedido_completado.connect(  # type: ignore[misc]
                    lambda mesa_id, total: self._on_pedido_completado(
                        mesa_id, total, dialog
                    )
                )

                layout.addWidget(tpv_widget)
                dialog.exec()

            else:
                QMessageBox.warning(self, "Error", "Mesa no encontrada")
        except Exception as e:
            logger.error(f"Error iniciando TPV: {e}")
            QMessageBox.critical(self, "Error", f"Error al abrir TPV: {str(e)}")

    def _on_pedido_completado(self, mesa_id: int, total: float, dialog: Any) -> None:
        """Maneja la finalización de un pedido"""
        try:
            mesa = next((m for m in self.mesas if m.id == mesa_id), None)
            if mesa:
                QMessageBox.information(
                    self,
                    "Pedido Completado",
                    f"Pedido de Mesa {mesa.numero} completado\nTotal: €{total:.2f}",
                )
                # Cerrar el diálogo del TPV
                dialog.accept()  # type: ignore[misc]
                # Recargar mesas para actualizar estado
                self.mesa_controller.cargar_mesas()
        except Exception as e:
            logger.error(f"Error procesando pedido completado: {e}")

    def _on_crear_reserva(self, mesa_id: int) -> None:
        """Crea una reserva para una mesa específica"""
        try:
            mesa = next((m for m in self.mesas if m.id == mesa_id), None)
            if mesa:
                # logger.debug(f"Creando reserva para mesa {mesa.numero}")
                QMessageBox.information(
                    self, "Reserva", f"Creando reserva para Mesa {mesa.numero}"
                )
                # TODO: Implementar sistema de reservas
            else:
                QMessageBox.warning(self, "Error", "Mesa no encontrada")
        except Exception as e:
            logger.error(f"Error creando reserva: {e}")

    def _on_cambiar_estado_mesa(self, mesa_id: int, nuevo_estado: str) -> None:
        """Cambia el estado de una mesa"""
        try:
            if self.mesa_controller.cambiar_estado_mesa(
                str(mesa_id), nuevo_estado
            ):  # TODO: Refactor global, mesa_id ahora debe ser numero (str)
                # logger.debug(f"Estado de mesa {mesa_id} cambiado a {nuevo_estado}")
                # Recargar mesas para reflejar el cambio
                self.mesa_controller.cargar_mesas()
            else:
                QMessageBox.warning(
                    self, "Error", "No se pudo cambiar el estado de la mesa"
                )
        except Exception as e:
            logger.error(f"Error cambiando estado de mesa: {e}")
            QMessageBox.critical(self, "Error", f"Error al cambiar estado: {str(e)}")

    # MÉTODO ELIMINADO: on_search_changed - La búsqueda ahora se maneja en el header ultra-premium
    # def on_search_changed(self, text):
    #     """Maneja cambios en el campo de búsqueda"""
    #     if hasattr(self, 'mesas_area'):
    #         self.mesas_area.apply_search(text)

    def venta_rapida(self) -> None:
        """TODO: Implementar venta rápida"""
        QMessageBox.information(self, "Venta Rápida", "Funcionalidad en desarrollo")

    def cerrar_caja(self) -> None:
        """TODO: Implementar cierre de caja"""
        QMessageBox.information(self, "Cerrar Caja", "Funcionalidad en desarrollo")

    def update_compact_stats(self) -> None:
        """Actualiza las estadísticas compactas basadas en datos reales"""
        try:
            if not hasattr(self, "mesas_area") or not self.mesas_area:
                return

            # TODO: Implementar actualización dinámica cuando sea necesario

        except Exception as e:
            logger.error("Error actualizando estadísticas compactas: %s", e)

    def calculate_real_stats(self) -> Dict[str, str]:
        """Calcula estadísticas reales basadas en datos de mesas"""
        try:
            if not self.mesas:
                return {
                    "zonas_activas": "0",
                    "mesas_totales": "0",
                    "disponibles": "0",
                    "ocupadas": "0",
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
                "ocupadas": str(ocupadas),
            }

        except Exception as e:
            logger.error("Error calculando estadísticas: %s", e)
            return {
                "zonas_activas": "0",
                "mesas_totales": "0",
                "disponibles": "0",
                "ocupadas": "0",
            }

    def create_compact_stat(self, icon: str, label: str, value: str) -> QWidget:
        """Crea una estadística compacta mejorada y más visible"""

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
        # Font para el valor
        value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_font = QFont()
        value_font.setPointSize(18)  # Aumentar tamaño de fuente
        value_font.setBold(True)
        value_widget.setFont(value_font)
        value_widget.setStyleSheet(
            "color: #1f2937; margin: 0px; padding: 0px; "
            "background-color: transparent;"
        )  # Color más oscuro
        layout.addWidget(value_widget)

        # Estilo del frame contenedor con más contraste
        stat_widget.setStyleSheet(
            """
            QFrame {
                background-color: #ffffff;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                margin: 2px;
            }
            QFrame:hover {
                border-color: #2563eb;
            }
        """
        )

        # Tamaño fijo más grande para mejor visibilidad
        stat_widget.setFixedSize(130, 70)

        return stat_widget

    def _on_mesa_creada(self, mesa: Mesa) -> None:
        """Maneja evento de mesa creada"""
        pass

    def _on_mesa_eliminada(self, mesa_id: str) -> None:
        """Maneja evento de mesa eliminada"""
        pass

    def _on_alias_cambiado(self, mesa: Mesa, nuevo_alias: str) -> None:
        """Maneja evento de cambio de alias de mesa"""
        pass


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Crear y mostrar el módulo TPV
    tpv = TPVModule()
    tpv.show()
    tpv.resize(1200, 800)

    sys.exit(app.exec())
