"""
TPV Avanzado - Panel de pedido modularizado
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                            QTableWidgetItem, QLabel, QPushButton, QFrame, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def create_pedido_panel(parent, splitter):
    """Crea el panel de pedido actual y pago"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)


    # Header del pedido
    header_frame = QFrame()
    header_frame.setStyleSheet("""
        QFrame {
            background: #f8f9fa;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 10px;
        }
    """)
    header_layout = QHBoxLayout(header_frame)

    pedido_title = QLabel("📋 Pedido Actual")
    pedido_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    pedido_title.setStyleSheet("color: #374151;")
    header_layout.addWidget(pedido_title)

    header_layout.addStretch()

    clear_btn = QPushButton("🗑️ Limpiar")
    clear_btn.setStyleSheet("""
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
    """)
    clear_btn.clicked.connect(lambda: limpiar_pedido(parent))
    header_layout.addWidget(clear_btn)

    layout.addWidget(header_frame)

    # Estado actual del pedido
    estado_frame = QFrame()
    estado_frame.setStyleSheet("""
        QFrame {
            background: #ede9fe;
            border: 1px solid #a78bfa;
            border-radius: 8px;
            padding: 6px 12px;
            margin-bottom: 4px;
        }
    """)
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
    if hasattr(parent, "current_order") and parent.current_order is not None:
        estado_actual = getattr(parent.current_order, "estado", None)
        estado_valor = estado_actual if estado_actual else "Desconocido"
    estado_valor_label = QLabel(estado_valor.capitalize())
    estado_valor_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
    estado_valor_label.setStyleSheet("color: #4B2991;")
    estado_layout.addWidget(estado_valor_label)

    # ComboBox para cambiar estado
    from PyQt6.QtWidgets import QComboBox
    estado_combo = QComboBox()
    estado_combo.setFixedWidth(140)
    estado_combo.setStyleSheet("background: #ede9fe; color: #4B2991; font-weight: bold;")
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

    def on_estado_combo_changed(idx):
        if idx <= 0:
            return
        nuevo_estado = estado_combo.currentData()
        if not nuevo_estado or not hasattr(parent, "current_order") or parent.current_order is None:
            return
        # Llamar a TPVService para cambiar el estado
        exito = False
        error_msg = None
        if hasattr(parent, "tpv_service"):
            try:
                exito = parent.tpv_service.cambiar_estado_comanda(parent.current_order.id, nuevo_estado)
            except Exception as e:
                error_msg = str(e)
            if exito:
                parent.current_order.estado = nuevo_estado
                # Refrescar UI de estado y combo
                if hasattr(parent, 'refrescar_estado_pedido_ui'):
                    parent.refrescar_estado_pedido_ui()
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
    parent.estado_pedido_label = estado_valor_label
    parent.estado_pedido_combo = estado_combo

    # Tabla de productos del pedido
    parent.pedido_table = QTableWidget()
    parent.pedido_table.setColumnCount(6)
    parent.pedido_table.setHorizontalHeaderLabels(["Producto", "Precio", "Cant.", "Descuento", "Total", "Eliminar"])

    # Configurar tabla
    header = parent.pedido_table.horizontalHeader()
    if header:
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    parent.pedido_table.setStyleSheet("""
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
    """)

    layout.addWidget(parent.pedido_table)

    # Panel de totales
    totales_frame = create_totales_panel(parent)
    layout.addWidget(totales_frame)

    # Botones de acción
    actions_frame = create_actions_panel(parent)
    layout.addWidget(actions_frame)

    # Botón de descuento global
    descuento_global_btn = QPushButton("% Descuento Global")
    descuento_global_btn.setStyleSheet("""
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
    """)
    descuento_global_btn.clicked.connect(lambda: aplicar_descuento_global(parent))
    layout.addWidget(descuento_global_btn)

    # Inicializar método para agregar productos
    parent.agregar_producto_pedido = lambda nombre, precio: agregar_producto_a_pedido(parent, nombre, precio)

    # --- NUEVO: Inicializar tabla con productos de la comanda activa (si existen) ---
    if hasattr(parent, "current_order") and parent.current_order is not None:
        table = parent.pedido_table
        for linea in getattr(parent.current_order, "lineas", []):
            row = table.rowCount()
            table.insertRow(row)
            nombre = getattr(linea, "producto_nombre", "")
            precio = getattr(linea, "precio_unidad", 0.0)
            cantidad = getattr(linea, "cantidad", 1)
            descuento = getattr(linea, "descuento", 0.0)  # Si se implementa descuento por línea
            total_linea = precio * cantidad * (1 - descuento/100)
            table.setItem(row, 0, QTableWidgetItem(nombre))
            table.setItem(row, 1, QTableWidgetItem(f"€{precio:.2f}"))
            cantidad_item = QTableWidgetItem(str(cantidad))
            cantidad_item.setFlags(cantidad_item.flags() | Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 2, cantidad_item)
            table.setItem(row, 3, QTableWidgetItem(f"{descuento:.0f}%"))
            table.setItem(row, 4, QTableWidgetItem(f"€{total_linea:.2f}"))
            eliminar_btn = QPushButton("❌")
            eliminar_btn.setStyleSheet("background: #ef4444; color: white; border: none; border-radius: 4px; font-weight: bold;")
            eliminar_btn.clicked.connect(lambda _, n=nombre: eliminar_producto_de_pedido(parent, n))
            table.setCellWidget(row, 5, eliminar_btn)

    splitter.addWidget(widget)


def create_totales_panel(parent):
    """Crea el panel de totales"""
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f0f9ff, stop:1 #e0f2fe);
            border: 2px solid #0ea5e9;
            border-radius: 10px;
            padding: 15px;
        }
    """)

    layout = QVBoxLayout(frame)

    # Labels de totales
    parent.subtotal_label = QLabel("Subtotal: €0.00")
    parent.subtotal_label.setFont(QFont("Segoe UI", 12))
    parent.subtotal_label.setStyleSheet("color: #374151;")
    layout.addWidget(parent.subtotal_label)

    parent.iva_label = QLabel("IVA (21%): €0.00")
    parent.iva_label.setFont(QFont("Segoe UI", 12))
    parent.iva_label.setStyleSheet("color: #374151;")
    layout.addWidget(parent.iva_label)

    parent.total_label = QLabel("TOTAL: €0.00")
    parent.total_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
    parent.total_label.setStyleSheet("color: #059669; margin-top: 5px;")
    layout.addWidget(parent.total_label)

    return frame


def create_actions_panel(parent):
    """Crea el panel de botones de acción"""
    frame = QFrame()
    layout = QVBoxLayout(frame)
    layout.setSpacing(10)

    # Botón de procesar pago
    pago_btn = QPushButton("💳 Procesar Pago")
    pago_btn.setFixedHeight(50)
    pago_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    pago_btn.setStyleSheet("""
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #34d399, stop:1 #10b981);
            color: white;
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #10b981, stop:1 #059669);
            transform: translateY(-1px);
        }
        QPushButton:pressed {
            background: #047857;
        }
    """)
    pago_btn.clicked.connect(lambda: procesar_pago(parent))
    layout.addWidget(pago_btn)

    # Fila de botones secundarios
    secondary_layout = QHBoxLayout()

    descuento_btn = QPushButton("🏷️ Descuento Global")
    descuento_btn.setStyleSheet("""
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
    """)
    descuento_btn.clicked.connect(lambda: aplicar_descuento_global(parent))
    secondary_layout.addWidget(descuento_btn)

    # Definir estilos para el botón de nota
    NOTA_BTN_STYLE_NORMAL = """
        QPushButton {
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #4f46e5;
        }
    """
    NOTA_BTN_STYLE_CON_NOTA = """
        QPushButton {
            background: #fbbf24;
            color: #222;
            border: 2px solid #f59e0b;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #fde68a;
        }
    """
    nota_btn = QPushButton("📝 Nota")
    nota_btn.setStyleSheet(NOTA_BTN_STYLE_NORMAL)
    nota_btn.clicked.connect(lambda: editar_nota_pedido(parent))
    parent.nota_btn = nota_btn
    parent.NOTA_BTN_STYLE_NORMAL = NOTA_BTN_STYLE_NORMAL
    parent.NOTA_BTN_STYLE_CON_NOTA = NOTA_BTN_STYLE_CON_NOTA
    secondary_layout.addWidget(nota_btn)

    layout.addLayout(secondary_layout)

    return frame


def agregar_producto_a_pedido(parent, nombre, precio):
    """Agrega un producto al pedido actual con soporte de descuento por línea"""
    table = parent.pedido_table
    # --- NUEVO: Crear comanda si no existe ---
    if not hasattr(parent, "current_order") or parent.current_order is None:
        if hasattr(parent, "tpv_service") and hasattr(parent, "mesa") and parent.tpv_service and parent.mesa:
            usuario = getattr(parent, "selected_user", -1)
            # Extraer usuario_id de forma segura (evita errores de tipo)
            if isinstance(usuario, int):
                usuario_id = usuario
            elif hasattr(usuario, "id") and isinstance(usuario.id, int):
                usuario_id = usuario.id
            elif hasattr(usuario, "usuario_id") and isinstance(usuario.usuario_id, int):
                usuario_id = usuario.usuario_id
            else:
                usuario_id = -1
            parent.current_order = parent.tpv_service.crear_comanda(parent.mesa.id, usuario_id=usuario_id)
            # Refrescar estado en la UI
            if hasattr(parent, "refrescar_estado_pedido_ui"):
                parent.refrescar_estado_pedido_ui()

    # Buscar si el producto ya existe
    for row in range(table.rowCount()):
        if table.item(row, 0) and table.item(row, 0).text() == nombre:
            # Incrementar cantidad
            cantidad_item = table.item(row, 2)
            cantidad_actual = int(cantidad_item.text())
            nueva_cantidad = cantidad_actual + 1
            cantidad_item.setText(str(nueva_cantidad))

            # Mantener descuento existente
            descuento_item = table.item(row, 3)
            descuento = float(descuento_item.text().replace('%','')) if descuento_item else 0.0
            # Actualizar total de la línea considerando descuento
            total_linea = precio * nueva_cantidad * (1 - descuento/100)
            table.setItem(row, 4, QTableWidgetItem(f"€{total_linea:.2f}"))

            actualizar_totales(parent)
            # Persistir en backend
            if hasattr(parent, "current_order") and parent.current_order is not None and hasattr(parent, "tpv_service"):
                producto = next((p for p in parent.tpv_service.get_todos_productos() if p.nombre == nombre), None)
                if producto:
                    parent.tpv_service.cambiar_cantidad_producto(parent.current_order.id, producto.id, nueva_cantidad)
            return

    # Si no existe, agregar nueva fila
    row = table.rowCount()
    table.insertRow(row)

    table.setItem(row, 0, QTableWidgetItem(nombre))
    table.setItem(row, 1, QTableWidgetItem(f"€{precio:.2f}"))
    cantidad_item = QTableWidgetItem("1")
    cantidad_item.setFlags(cantidad_item.flags() | Qt.ItemFlag.ItemIsEditable)
    table.setItem(row, 2, cantidad_item)
    table.setItem(row, 3, QTableWidgetItem("0%"))  # Descuento por línea
    table.setItem(row, 4, QTableWidgetItem(f"€{precio:.2f}"))
    # Botón eliminar
    from PyQt6.QtWidgets import QPushButton
    eliminar_btn = QPushButton("❌")
    eliminar_btn.setStyleSheet("background: #ef4444; color: white; border: none; border-radius: 4px; font-weight: bold;")
    eliminar_btn.clicked.connect(lambda _, n=nombre: eliminar_producto_de_pedido(parent, n))
    table.setCellWidget(row, 5, eliminar_btn)

    actualizar_totales(parent)
    # Persistir en backend
    if hasattr(parent, "current_order") and parent.current_order is not None and hasattr(parent, "tpv_service"):
        producto = next((p for p in parent.tpv_service.get_todos_productos() if p.nombre == nombre), None)
        if producto:
            parent.tpv_service.agregar_producto_a_comanda(parent.current_order.id, producto.id, producto.nombre, producto.precio, 1)

    # Refrescar estado en la UI tras agregar el primer producto
    if hasattr(parent, "refrescar_estado_pedido_ui"):
        parent.refrescar_estado_pedido_ui()

    # Conectar edición de cantidad
    def on_cantidad_editada(row_idx=row, col_idx=2):
        item = table.item(row_idx, col_idx)
        if item:
            try:
                nueva_cantidad = int(item.text())
                if nueva_cantidad <= 0:
                    eliminar_producto_de_pedido(parent, nombre)
                else:
                    cambiar_cantidad_producto_pedido(parent, nombre, nueva_cantidad)
            except Exception:
                pass
    table.itemChanged.connect(lambda item, n=nombre, r=row: on_cantidad_editada(r, 2) if item.column() == 2 and item.row() == r else None)

def eliminar_producto_de_pedido(parent, producto_nombre):
    """Elimina un producto individual del pedido y lo persiste en backend"""
    table = parent.pedido_table
    row_to_remove = None
    for row in range(table.rowCount()):
        if table.item(row, 0) and table.item(row, 0).text() == producto_nombre:
            row_to_remove = row
            break
    if row_to_remove is not None:
        table.removeRow(row_to_remove)
        actualizar_totales(parent)
        # Persistir en backend
        if hasattr(parent, "current_order") and parent.current_order is not None and hasattr(parent, "tpv_service"):
            producto = next((p for p in parent.tpv_service.get_todos_productos() if p.nombre == producto_nombre), None)
            if producto:
                parent.tpv_service.eliminar_producto_de_comanda(parent.current_order.id, producto.id)

def cambiar_cantidad_producto_pedido(parent, producto_nombre, nueva_cantidad):
    """Cambia la cantidad de un producto y lo persiste en backend"""
    table = parent.pedido_table
    for row in range(table.rowCount()):
        if table.item(row, 0) and table.item(row, 0).text() == producto_nombre:
            table.setItem(row, 2, QTableWidgetItem(str(nueva_cantidad)))
            actualizar_totales(parent)
            # Persistir en backend
            if hasattr(parent, "current_order") and parent.current_order is not None and hasattr(parent, "tpv_service"):
                producto = next((p for p in parent.tpv_service.get_todos_productos() if p.nombre == producto_nombre), None)
                if producto:
                    parent.tpv_service.cambiar_cantidad_producto(parent.current_order.id, producto.id, nueva_cantidad)
            break

# NOTA: Para integración completa, conectar estas funciones a acciones de la UI (botón eliminar, edición de cantidad, etc.)


def actualizar_totales(parent):
    """Actualiza los totales del pedido considerando descuentos"""
    table = parent.pedido_table
    subtotal = 0.0

    for row in range(table.rowCount()):
        precio_item = table.item(row, 1)
        cantidad_item = table.item(row, 2)
        descuento_item = table.item(row, 3)
        if precio_item and cantidad_item and descuento_item:
            precio = float(precio_item.text().replace('€',''))
            cantidad = int(cantidad_item.text())
            descuento = float(descuento_item.text().replace('%',''))
            total_linea = precio * cantidad * (1 - descuento/100)
            table.setItem(row, 4, QTableWidgetItem(f"€{total_linea:.2f}"))
            subtotal += total_linea

    iva = subtotal * 0.21
    total = subtotal + iva

    parent.subtotal_label.setText(f"Subtotal: €{subtotal:.2f}")
    parent.iva_label.setText(f"IVA (21%): €{iva:.2f}")
    parent.total_label.setText(f"TOTAL: €{total:.2f}")


def limpiar_pedido(parent):
    """Limpia el pedido actual"""
    parent.pedido_table.setRowCount(0)
    actualizar_totales(parent)
    # Persistir limpieza en backend
    if hasattr(parent, "current_order") and parent.current_order is not None and hasattr(parent, "tpv_service"):
        # Eliminar todas las líneas de la comanda
        for linea in list(parent.current_order.lineas):
            parent.tpv_service.eliminar_producto_de_comanda(parent.current_order.id, linea.producto_id)


def procesar_pago(parent):
    """Procesa el pago del pedido"""
    table = parent.pedido_table
    if table.rowCount() == 0:
        return

    total_text = parent.total_label.text().replace('TOTAL: €', '')
    total = float(total_text)

    # Procesar pago en backend
    exito = False
    if hasattr(parent, "current_order") and parent.current_order is not None and hasattr(parent, "tpv_service"):
        exito = parent.tpv_service.pagar_comanda(parent.current_order.id, getattr(parent, "selected_user", -1))
    if exito:
        # Limpiar pedido después del pago
        limpiar_pedido(parent)
        # Refrescar UI de estado y grid de mesas
        if hasattr(parent, 'refrescar_estado_pedido_ui'):
            parent.refrescar_estado_pedido_ui()
        # Opcional: mostrar mensaje de éxito
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(parent, "Pago realizado", "El pago se ha procesado y la mesa ha sido liberada.")
    else:
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.warning(parent, "Error de pago", "No se pudo procesar el pago. Verifique la conexión o el estado de la comanda.")


def aplicar_descuento_global(parent):
    """Solicita y aplica un descuento global a todas las líneas"""
    from PyQt6.QtWidgets import QInputDialog
    descuento, ok = QInputDialog.getDouble(parent, "Descuento global", "Porcentaje de descuento (%):", 0, 0, 100, 1)
    if ok:
        table = parent.pedido_table
        for row in range(table.rowCount()):
            table.setItem(row, 3, QTableWidgetItem(f"{descuento:.0f}%"))
        actualizar_totales(parent)
        # Persistir descuentos en backend
        if hasattr(parent, "current_order") and parent.current_order is not None and hasattr(parent, "tpv_service"):
            for row in range(table.rowCount()):
                producto_nombre = table.item(row, 0).text()
                producto = next((p for p in parent.tpv_service.get_todos_productos() if p.nombre == producto_nombre), None)
                if producto:
                    # Aquí podrías extender para guardar el descuento en la línea si el modelo lo soporta
                    pass  # TODO: persistir descuento por línea si se implementa en el modelo


def editar_nota_pedido(parent):
    """Permite añadir o editar una nota al pedido actual"""
    from PyQt6.QtWidgets import QInputDialog
    nota_actual = getattr(parent, 'nota_pedido', "")
    nota, ok = QInputDialog.getMultiLineText(parent, "Nota del pedido", "Ingrese una nota para el pedido:", nota_actual)
    if ok:
        parent.nota_pedido = nota
        # Mostrar visualmente que hay nota
        if hasattr(parent, 'nota_btn'):
            if nota.strip():
                parent.nota_btn.setToolTip(f"Nota: {nota}")
                parent.nota_btn.setStyleSheet(parent.NOTA_BTN_STYLE_CON_NOTA)
            else:
                parent.nota_btn.setToolTip("")
                parent.nota_btn.setStyleSheet(parent.NOTA_BTN_STYLE_NORMAL)
