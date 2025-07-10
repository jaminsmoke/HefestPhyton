"""
TPV Avanzado - Panel de pedido modularizado
"""

from typing import Any
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QFrame,
    QHeaderView,
    QSplitter,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def create_pedido_panel(parent: QWidget, splitter: QSplitter) -> QWidget:
    """Crea el panel de pedido actual y pago"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)

    # Header del pedido
    header_frame = QFrame()
    header_frame.setStyleSheet(
        """
        QFrame {
            background: #f8f9fa;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 10px;
        }
    """
    )
    header_layout = QHBoxLayout(header_frame)

    pedido_title = QLabel("📋 Pedido Actual")
    pedido_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    pedido_title.setStyleSheet("color: #374151;")
    header_layout.addWidget(pedido_title)

    header_layout.addStretch()

    clear_btn = QPushButton("🗑️ Limpiar")
    clear_btn.setStyleSheet(
        """
        QPushButton {
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #dc2626;
        }
    """
    )
    clear_btn.clicked.connect(lambda: limpiar_pedido(parent))
    header_layout.addWidget(clear_btn)

    layout.addWidget(header_frame)

    # Estado actual del pedido
    estado_frame = QFrame()
    estado_frame.setStyleSheet(
        """
        QFrame {
            background: #ede9fe;
            border: 1px solid #a78bfa;
            border-radius: 8px;
            padding: 6px 12px;
            margin-bottom: 4px;
        }
    """
    )
    estado_layout = QHBoxLayout(estado_frame)
    estado_layout.setContentsMargins(0, 0, 0, 0)
    estado_layout.setSpacing(6)

    estado_label = QLabel("Estado:")
    estado_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
    estado_label.setStyleSheet("color: #4B2991;")
    estado_layout.addWidget(estado_label)

    # Obtener estado actual de la comanda
    estado_valor = "Sin pedido"
    estado_actual = None
    if hasattr(parent, "current_order") and getattr(parent, "current_order") is not None:  # type: ignore
        current_order = getattr(parent, "current_order")  # type: ignore
        estado_actual = getattr(current_order, "estado", None)  # type: ignore
        estado_valor = estado_actual if estado_actual else "Desconocido"
    estado_valor_label = QLabel(estado_valor.capitalize())
    estado_valor_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
    estado_valor_label.setStyleSheet("color: #4B2991;")
    estado_layout.addWidget(estado_valor_label)

    # ComboBox para cambiar estado
    from PyQt6.QtWidgets import QComboBox

    estado_combo = QComboBox()
    estado_combo.setFixedWidth(140)
    estado_combo.setStyleSheet(
        "background: #ede9fe; color: #4B2991; font-weight: bold;"
    )
    # Definir transiciones válidas
    TRANSICIONES_VALIDAS = {
        "abierta": ["en_proceso", "cancelada"],
        "en_proceso": ["pagada", "cancelada"],
        "pagada": ["cerrada"],
        # "cerrada": []
    }
    # Opciones según estado actual
    opciones = []
    if estado_actual in TRANSICIONES_VALIDAS:
        opciones = TRANSICIONES_VALIDAS[estado_actual]
    estado_combo.addItem("Seleccionar...")
    for op in opciones:
        estado_combo.addItem(op.capitalize(), op)
    estado_combo.setEnabled(bool(opciones))

    def on_estado_combo_changed(idx: int) -> None:
        if idx <= 0:
            return
        nuevo_estado = estado_combo.currentData()
        if (
            not nuevo_estado
            or not hasattr(parent, "current_order")
            or getattr(parent, "current_order") is None  # type: ignore
        ):
            return
        # Llamar a TPVService para cambiar el estado
        exito = False
        error_msg = None
        if hasattr(parent, "tpv_service"):
            try:
                current_order = getattr(parent, "current_order")  # type: ignore
                tpv_service = getattr(parent, "tpv_service")  # type: ignore
                exito = tpv_service.cambiar_estado_comanda(  # type: ignore
                    current_order.id, nuevo_estado  # type: ignore
                )
            except Exception as e:
                error_msg = str(e)
            if exito:
                current_order = getattr(parent, "current_order")  # type: ignore
                setattr(current_order, "estado", nuevo_estado)  # type: ignore
                # Refrescar UI de estado y combo
                if hasattr(parent, "refrescar_estado_pedido_ui"):
                    refrescar_func = getattr(parent, "refrescar_estado_pedido_ui")  # type: ignore
                    refrescar_func()  # type: ignore
            else:
                from PyQt6.QtWidgets import QMessageBox

                msg = error_msg or f"No se pudo cambiar el estado a '{nuevo_estado}'."
                QMessageBox.warning(parent, "Error de transición de estado", msg)
        estado_combo.setCurrentIndex(0)

    estado_combo.currentIndexChanged.connect(on_estado_combo_changed)
    estado_layout.addWidget(estado_combo)

    estado_layout.addStretch()
    layout.addWidget(estado_frame)

    # Guardar referencia para futuras actualizaciones
    setattr(parent, "estado_pedido_label", estado_valor_label)  # type: ignore
    setattr(parent, "estado_pedido_combo", estado_combo)  # type: ignore

    # Tabla de productos del pedido
    pedido_table = QTableWidget()
    setattr(parent, "pedido_table", pedido_table)  # type: ignore
    pedido_table.setColumnCount(6)
    pedido_table.setHorizontalHeaderLabels(
        ["Producto", "Precio", "Cant.", "Descuento", "Total", "Eliminar"]
    )

    # Configurar tabla
    header = pedido_table.horizontalHeader()
    if header:
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    pedido_table.setStyleSheet(
        """
        QTableWidget {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            background: white;
            gridline-color: #f3f4f6;
        }
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f3f4f6;
        }
        QTableWidget::item:selected {
            background: #eff6ff;
            color: #1d4ed8;
        }
        QHeaderView::section {
            background: #f9fafb;
            padding: 10px;
            border: none;
            border-bottom: 2px solid #e5e7eb;
            font-weight: bold;
            color: #374151;
        }
    """
    )

    layout.addWidget(pedido_table)

    # Panel de totales
    totales_frame = create_totales_panel(parent)
    layout.addWidget(totales_frame)

    # Botones de acción
    actions_frame = create_actions_panel(parent)
    layout.addWidget(actions_frame)

    # Botón de descuento global
    descuento_global_btn = QPushButton("% Descuento Global")
    descuento_global_btn.setStyleSheet(
        """
        QPushButton {
            background: #f59e0b;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #d97706;
        }
    """
    )
    descuento_global_btn.clicked.connect(lambda: aplicar_descuento_global(parent))
    layout.addWidget(descuento_global_btn)

    # Inicializar método para agregar productos
    setattr(parent, "agregar_producto_pedido",
            lambda nombre, precio: agregar_producto_a_pedido(parent, nombre, precio))  # type: ignore

    # --- NUEVO: Inicializar tabla con productos de la comanda activa (si existen) ---
    if hasattr(parent, "current_order") and getattr(parent, "current_order") is not None:  # type: ignore
        table = getattr(parent, "pedido_table")  # type: ignore
        current_order = getattr(parent, "current_order")  # type: ignore
        for linea in getattr(current_order, "lineas", []):  # type: ignore
            row = table.rowCount()  # type: ignore
            table.insertRow(row)  # type: ignore
            nombre = getattr(linea, "producto_nombre", "")  # type: ignore
            precio = getattr(linea, "precio_unidad", 0.0)  # type: ignore
            cantidad = getattr(linea, "cantidad", 1)  # type: ignore
            descuento = getattr(linea, "descuento", 0.0)  # type: ignore
            total_linea = precio * cantidad * (1 - descuento / 100)
            table.setItem(row, 0, QTableWidgetItem(nombre))  # type: ignore
            table.setItem(row, 1, QTableWidgetItem(f"€{precio:.2f}"))  # type: ignore
            cantidad_item = QTableWidgetItem(str(cantidad))
            cantidad_item.setFlags(cantidad_item.flags() | Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 2, cantidad_item)  # type: ignore
            table.setItem(row, 3, QTableWidgetItem(f"{descuento:.0f}%"))  # type: ignore
            table.setItem(row, 4, QTableWidgetItem(f"€{total_linea:.2f}"))  # type: ignore
            eliminar_btn = QPushButton("❌")
            eliminar_btn.setStyleSheet(
                "background: #ef4444; color: white; border: none; border-radius: 4px; font-weight: bold;"
            )
            eliminar_btn.clicked.connect(
                lambda _, n=nombre: eliminar_producto_de_pedido(parent, n)
            )
            table.setCellWidget(row, 5, eliminar_btn)  # type: ignore

    splitter.addWidget(widget)
    return widget


def create_totales_panel(parent: Any) -> QFrame:
    """Crea el panel de totales"""
    frame = QFrame()
    frame.setStyleSheet(
        """
        QFrame {
            background: #f8f9fa;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 10px;
        }
    """
    )
    layout = QVBoxLayout(frame)

    subtotal_label = QLabel("Subtotal: €0.00")
    subtotal_label.setFont(QFont("Segoe UI", 12))
    setattr(parent, "subtotal_label", subtotal_label)  # type: ignore

    iva_label = QLabel("IVA (21%): €0.00")
    iva_label.setFont(QFont("Segoe UI", 12))
    setattr(parent, "iva_label", iva_label)  # type: ignore

    total_label = QLabel("TOTAL: €0.00")
    total_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    total_label.setStyleSheet("color: #059669;")
    setattr(parent, "total_label", total_label)  # type: ignore

    layout.addWidget(subtotal_label)
    layout.addWidget(iva_label)
    layout.addWidget(total_label)

    return frame


def create_actions_panel(parent: Any) -> QFrame:
    """Crea el panel de botones de acción"""
    frame = QFrame()
    layout = QHBoxLayout(frame)

    # Botón de pago
    pago_btn = QPushButton("💳 Pagar")
    pago_btn.setStyleSheet(
        """
        QPushButton {
            background: #059669;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background: #047857;
        }
    """
    )
    pago_btn.clicked.connect(lambda: procesar_pago(parent))
    layout.addWidget(pago_btn)

    # Botón de descuento
    descuento_btn = QPushButton("% Descuento")
    descuento_btn.setStyleSheet(
        """
        QPushButton {
            background: #f59e0b;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #d97706;
        }
    """
    )
    descuento_btn.clicked.connect(lambda: aplicar_descuento_global(parent))
    layout.addWidget(descuento_btn)

    # Botón de nota
    nota_btn = QPushButton("📝 Nota")
    nota_btn.setStyleSheet(
        """
        QPushButton {
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #4f46e5;
        }
    """
    )
    setattr(parent, "NOTA_BTN_STYLE_NORMAL", nota_btn.styleSheet())  # type: ignore
    setattr(parent, "NOTA_BTN_STYLE_CON_NOTA",
            nota_btn.styleSheet().replace("#6366f1", "#dc2626"))  # type: ignore
    setattr(parent, "nota_btn", nota_btn)  # type: ignore
    nota_btn.clicked.connect(lambda: editar_nota_pedido(parent))
    layout.addWidget(nota_btn)

    return frame


def agregar_producto_a_pedido(parent: Any, nombre: str, precio: float) -> None:
    """Agrega un producto al pedido actual"""
    table = getattr(parent, "pedido_table", None)  # type: ignore
    if not table:
        return

    # Buscar si el producto ya existe
    for row in range(table.rowCount()):  # type: ignore
        item = table.item(row, 0)  # type: ignore
        if item and item.text() == nombre:  # type: ignore
            # Incrementar cantidad
            cantidad_item = table.item(row, 2)  # type: ignore
            if cantidad_item:
                cantidad_actual = int(cantidad_item.text())  # type: ignore
                nueva_cantidad = cantidad_actual + 1
                cantidad_item.setText(str(nueva_cantidad))  # type: ignore

                # Actualizar total de la línea
                precio_item = table.item(row, 1)  # type: ignore
                if precio_item:
                    precio_texto = precio_item.text().replace("€", "")  # type: ignore
                    precio_unitario = float(precio_texto)
                    nuevo_total = precio_unitario * nueva_cantidad
                    total_item = table.item(row, 4)  # type: ignore
                    if total_item:
                        total_item.setText(f"€{nuevo_total:.2f}")  # type: ignore

                actualizar_totales(parent)
                return

    # Si no existe, agregar nueva fila
    row = table.rowCount()  # type: ignore
    table.insertRow(row)  # type: ignore

    table.setItem(row, 0, QTableWidgetItem(nombre))  # type: ignore
    table.setItem(row, 1, QTableWidgetItem(f"€{precio:.2f}"))  # type: ignore

    cantidad_item = QTableWidgetItem("1")
    cantidad_item.setFlags(cantidad_item.flags() | Qt.ItemFlag.ItemIsEditable)
    table.setItem(row, 2, cantidad_item)  # type: ignore

    table.setItem(row, 3, QTableWidgetItem("0%"))  # type: ignore
    table.setItem(row, 4, QTableWidgetItem(f"€{precio:.2f}"))  # type: ignore

    # Botón eliminar
    eliminar_btn = QPushButton("❌")
    eliminar_btn.setStyleSheet(
        "background: #ef4444; color: white; border: none; border-radius: 4px; font-weight: bold;"
    )
    eliminar_btn.clicked.connect(lambda: eliminar_producto_de_pedido(parent, nombre))
    table.setCellWidget(row, 5, eliminar_btn)  # type: ignore

    # Conectar edición de cantidad
    def on_cantidad_editada(row_idx: int = row, col_idx: int = 2) -> None:
        item = table.item(row_idx, col_idx)  # type: ignore
        if item:
            try:
                nueva_cantidad = int(item.text())  # type: ignore
                if nueva_cantidad <= 0:
                    eliminar_producto_de_pedido(parent, nombre)
                else:
                    cambiar_cantidad_producto_pedido(parent, nombre, nueva_cantidad)
            except ValueError:
                item.setText("1")  # type: ignore

    table.itemChanged.connect(  # type: ignore
        lambda item: on_cantidad_editada() if item.column() == 2 else None
    )

    actualizar_totales(parent)


def eliminar_producto_de_pedido(parent: Any, producto_nombre: str) -> None:
    """Elimina un producto individual del pedido y lo persiste en backend"""
    table = getattr(parent, "pedido_table", None)  # type: ignore
    if not table:
        return
    row_to_remove = None
    for row in range(table.rowCount()):  # type: ignore
        item = table.item(row, 0)  # type: ignore
        if item and item.text() == producto_nombre:  # type: ignore
            row_to_remove = row
            break
    if row_to_remove is not None:
        table.removeRow(row_to_remove)  # type: ignore
        actualizar_totales(parent)
        # Persistir en backend
        if (
            hasattr(parent, "current_order")
            and getattr(parent, "current_order") is not None  # type: ignore
            and hasattr(parent, "tpv_service")
        ):
            current_order = getattr(parent, "current_order")  # type: ignore
            tpv_service = getattr(parent, "tpv_service")  # type: ignore
            producto = next(
                (
                    p
                    for p in tpv_service.get_todos_productos()  # type: ignore
                    if p.nombre == producto_nombre  # type: ignore
                ),
                None,
            )
            if producto:
                tpv_service.eliminar_producto_de_comanda(  # type: ignore
                    current_order.id, producto.id  # type: ignore
                )


def cambiar_cantidad_producto_pedido(parent: Any, producto_nombre: str, nueva_cantidad: int) -> None:
    """Cambia la cantidad de un producto y lo persiste en backend"""
    table = getattr(parent, "pedido_table", None)  # type: ignore
    if not table:
        return
    for row in range(table.rowCount()):  # type: ignore
        item = table.item(row, 0)  # type: ignore
        if item and item.text() == producto_nombre:  # type: ignore
            # Actualizar cantidad y total
            cantidad_item = table.item(row, 2)  # type: ignore
            precio_item = table.item(row, 1)  # type: ignore
            total_item = table.item(row, 4)  # type: ignore

            if cantidad_item and precio_item and total_item:
                cantidad_item.setText(str(nueva_cantidad))  # type: ignore
                precio_texto = precio_item.text().replace("€", "")  # type: ignore
                precio = float(precio_texto)
                nuevo_total = precio * nueva_cantidad
                total_item.setText(f"€{nuevo_total:.2f}")  # type: ignore

            actualizar_totales(parent)
            break


def actualizar_totales(parent: Any) -> None:
    """Actualiza los totales del pedido"""
    table = getattr(parent, "pedido_table", None)  # type: ignore
    if not table:
        return

    subtotal = 0.0
    for row in range(table.rowCount()):  # type: ignore
        total_item = table.item(row, 4)  # type: ignore
        if total_item:
            total_texto = total_item.text().replace("€", "")  # type: ignore
            subtotal += float(total_texto)

    iva = subtotal * 0.21
    total = subtotal + iva

    subtotal_label = getattr(parent, "subtotal_label", None)  # type: ignore
    iva_label = getattr(parent, "iva_label", None)  # type: ignore
    total_label = getattr(parent, "total_label", None)  # type: ignore

    if subtotal_label:
        subtotal_label.setText(f"Subtotal: €{subtotal:.2f}")  # type: ignore
    if iva_label:
        iva_label.setText(f"IVA (21%): €{iva:.2f}")  # type: ignore
    if total_label:
        total_label.setText(f"TOTAL: €{total:.2f}")  # type: ignore


def limpiar_pedido(parent: Any) -> None:
    """Limpia el pedido actual"""
    pedido_table = getattr(parent, "pedido_table", None)  # type: ignore
    if pedido_table:
        pedido_table.setRowCount(0)  # type: ignore
    actualizar_totales(parent)
    # Persistir limpieza en backend
    if (
        hasattr(parent, "current_order")
        and getattr(parent, "current_order") is not None  # type: ignore
        and hasattr(parent, "tpv_service")
    ):
        current_order = getattr(parent, "current_order")  # type: ignore
        tpv_service = getattr(parent, "tpv_service")  # type: ignore
        # Eliminar todas las líneas de la comanda
        for linea in list(getattr(current_order, "lineas", [])):  # type: ignore
            tpv_service.eliminar_producto_de_comanda(  # type: ignore
                current_order.id, linea.producto_id  # type: ignore
            )


def procesar_pago(parent: Any) -> None:
    """Procesa el pago del pedido"""
    table = getattr(parent, "pedido_table", None)  # type: ignore
    if not table or table.rowCount() == 0:  # type: ignore
        return

    total_label = getattr(parent, "total_label", None)  # type: ignore
    if not total_label:
        return

    total_text = total_label.text().replace("TOTAL: €", "")  # type: ignore
    try:
        total = float(total_text)
    except ValueError:
        return

    # Procesar pago en backend
    exito = False
    if (
        hasattr(parent, "current_order")
        and getattr(parent, "current_order") is not None  # type: ignore
        and hasattr(parent, "tpv_service")
    ):
        current_order = getattr(parent, "current_order")  # type: ignore
        tpv_service = getattr(parent, "tpv_service")  # type: ignore
        exito = tpv_service.pagar_comanda(  # type: ignore
            current_order.id, getattr(parent, "selected_user", -1)  # type: ignore
        )
    if exito:
        # Limpiar pedido después del pago
        limpiar_pedido(parent)
        # Refrescar UI de estado y grid de mesas
        if hasattr(parent, "refrescar_estado_pedido_ui"):
            refrescar_func = getattr(parent, "refrescar_estado_pedido_ui")  # type: ignore
            refrescar_func()  # type: ignore
        # Opcional: mostrar mensaje de éxito
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(
            parent,  # type: ignore
            "Pago realizado",
            "El pago se ha procesado y la mesa ha sido liberada.",
        )
    else:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.warning(
            parent,  # type: ignore
            "Error de pago",
            "No se pudo procesar el pago. Verifique los datos.",
        )


def aplicar_descuento_global(parent: Any) -> None:
    """Solicita y aplica un descuento global a todas las líneas"""
    from PyQt6.QtWidgets import QInputDialog

    descuento, ok = QInputDialog.getDouble(
        parent, "Descuento global", "Porcentaje de descuento (%):", 0, 0, 100, 1  # type: ignore
    )
    if ok:
        table = getattr(parent, "pedido_table", None)  # type: ignore
        if not table:
            return
        for row in range(table.rowCount()):  # type: ignore
            table.setItem(row, 3, QTableWidgetItem(f"{descuento:.0f}%"))  # type: ignore
        actualizar_totales(parent)
        # Persistir descuentos en backend
        if (
            hasattr(parent, "current_order")
            and getattr(parent, "current_order") is not None  # type: ignore
            and hasattr(parent, "tpv_service")
        ):
            for row in range(table.rowCount()):  # type: ignore
                item = table.item(row, 0)  # type: ignore
                if not item:
                    continue
                producto_nombre = item.text()  # type: ignore
                tpv_service = getattr(parent, "tpv_service")  # type: ignore
                producto = next(
                    (
                        p
                        for p in tpv_service.get_todos_productos()  # type: ignore
                        if p.nombre == producto_nombre  # type: ignore
                    ),
                    None,
                )
                if producto:
                    # Aquí podrías extender para guardar el descuento en la línea si el modelo lo soporta
                    pass  # TODO: persistir descuento por línea si se implementa en el modelo


def editar_nota_pedido(parent: Any) -> None:
    """Permite añadir o editar una nota al pedido actual"""
    from PyQt6.QtWidgets import QInputDialog

    nota_actual = getattr(parent, "nota_pedido", "")  # type: ignore
    nota, ok = QInputDialog.getMultiLineText(
        parent, "Nota del pedido", "Ingrese una nota para el pedido:", nota_actual  # type: ignore
    )
    if ok:
        setattr(parent, "nota_pedido", nota)  # type: ignore
        # Mostrar visualmente que hay nota
        if hasattr(parent, "nota_btn"):
            nota_btn = getattr(parent, "nota_btn")  # type: ignore
            if nota.strip():
                nota_btn.setToolTip(f"Nota: {nota}")  # type: ignore
                style_con_nota = getattr(parent, "NOTA_BTN_STYLE_CON_NOTA", "")  # type: ignore
                nota_btn.setStyleSheet(style_con_nota)  # type: ignore
            else:
                nota_btn.setToolTip("")  # type: ignore
                style_normal = getattr(parent, "NOTA_BTN_STYLE_NORMAL", "")  # type: ignore
                nota_btn.setStyleSheet(style_normal)  # type: ignore
