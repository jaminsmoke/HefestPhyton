"""
TPV Avanzado - Panel de productos modernizado con búsqueda inteligente
"""

from typing import Any, Optional, Dict, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTabWidget, 
    QGridLayout, QPushButton, QLabel, QFrame, QScrollArea,
    QCompleter, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QStringListModel, QTimer
from PyQt6.QtGui import QFont, QPalette

from .styles_modern import (
    get_product_card_style,
    get_modern_input_style, 
    get_modern_tab_style,
    COLORS, 
    SPACING,
    BORDER_RADIUS
)


class ModernProductCard(QPushButton):
    """Tarjeta moderna de producto con información completa"""
    
    product_selected = pyqtSignal(dict)  # Señal con datos del producto
    
    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setup_card()
        
    def setup_card(self):
        """Configura la tarjeta del producto"""
        # Aplicar estilos modernos
        self.setStyleSheet(get_product_card_style())
        
        # Configurar tamaño
        self.setFixedSize(160, 120)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Configurar contenido
        self.update_content()
        
        # Conectar señal
        self.clicked.connect(self.on_card_clicked)
    
    def update_content(self):
        """Actualiza el contenido de la tarjeta"""
        nombre = self.product_data.get('nombre', 'Producto')
        precio = self.product_data.get('precio', 0.0)
        stock = self.product_data.get('stock', None)
        
        # Texto principal
        text_lines = [
            f"💎 {nombre}",
            f"💰 €{precio:.2f}"
        ]
        
        # Información de stock
        if stock is not None:
            if stock > 0:
                text_lines.append(f"📦 Stock: {stock}")
            else:
                text_lines.append("❌ Sin stock")
                self.setEnabled(False)
        
        self.setText("\n".join(text_lines))
        
        # Tooltip con información adicional
        tooltip_text = f"""
        <b>{nombre}</b><br>
        Precio: €{precio:.2f}<br>
        Stock: {stock if stock is not None else 'No disponible'}
        """
        self.setToolTip(tooltip_text)
    
    def on_card_clicked(self):
        """Maneja el clic en la tarjeta"""
        self.product_selected.emit(self.product_data)
    
    def set_highlighted(self, highlighted=True):
        """Resalta la tarjeta temporalmente"""
        if highlighted:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {COLORS['primary_light']}, 
                        stop:1 {COLORS['primary']});
                    color: {COLORS['white']};
                    border: 2px solid {COLORS['primary_dark']};
                    border-radius: {BORDER_RADIUS['lg']};
                    font-weight: bold;
                }}
            """)
        else:
            self.setStyleSheet(get_product_card_style())


class ModernSearchWidget(QWidget):
    """Widget de búsqueda inteligente moderna"""
    
    search_changed = pyqtSignal(str)  # Señal cuando cambia la búsqueda
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_search_functionality()
    
    def setup_ui(self):
        """Configura la interfaz de búsqueda"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Frame contenedor
        search_frame = QFrame()
        search_frame.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['white']};
                border: 2px solid {COLORS['gray_200']};
                border-radius: {BORDER_RADIUS['lg']};
                padding: {SPACING['sm']};
            }}
            QFrame:focus-within {{
                border-color: {COLORS['primary']};
                box-shadow: 0 0 0 3px {COLORS['primary']}33;
            }}
        """)
        
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(12, 8, 12, 8)
        search_layout.setSpacing(8)
        
        # Icono de búsqueda
        search_icon = QLabel("🔍")
        search_icon.setFont(QFont("Segoe UI", 14))
        search_icon.setStyleSheet(f"color: {COLORS['gray_400']};")
        search_layout.addWidget(search_icon)
        
        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar productos por nombre, código...")
        self.search_input.setStyleSheet(get_modern_input_style())
        self.search_input.setFont(QFont("Segoe UI", 13))
        search_layout.addWidget(self.search_input)
        
        # Botón de limpiar
        self.clear_btn = QPushButton("✖")
        self.clear_btn.setFixedSize(28, 28)
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['gray_200']};
                border: none;
                border-radius: 14px;
                color: {COLORS['gray_600']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {COLORS['danger']};
                color: {COLORS['white']};
            }}
        """)
        self.clear_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(self.clear_btn)
        
        layout.addWidget(search_frame)
        
        # Sugerencias de búsqueda rápida
        self.suggestions_widget = self.create_suggestions_widget()
        layout.addWidget(self.suggestions_widget)
    
    def create_suggestions_widget(self):
        """Crea widget de sugerencias rápidas"""
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['gray_50']};
                border-radius: {BORDER_RADIUS['md']};
                padding: {SPACING['sm']};
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Etiqueta
        label = QLabel("Búsqueda rápida:")
        label.setFont(QFont("Segoe UI", 10))
        label.setStyleSheet(f"color: {COLORS['gray_600']};")
        layout.addWidget(label)
        
        # Botones de sugerencias
        suggestions = ["Bebidas", "Entrantes", "Principales", "Postres"]
        for suggestion in suggestions:
            btn = QPushButton(suggestion)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {COLORS['white']};
                    border: 1px solid {COLORS['gray_300']};
                    border-radius: {BORDER_RADIUS['sm']};
                    padding: 4px 8px;
                    font-size: 10px;
                    color: {COLORS['gray_700']};
                }}
                QPushButton:hover {{
                    background: {COLORS['primary']};
                    color: {COLORS['white']};
                    border-color: {COLORS['primary']};
                }}
            """)
            btn.clicked.connect(lambda checked, s=suggestion: self.set_search(s))
            layout.addWidget(btn)
        
        layout.addStretch()
        return widget
    
    def setup_search_functionality(self):
        """Configura la funcionalidad de búsqueda"""
        # Timer para búsqueda con delay
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.emit_search_changed)
        
        # Conectar eventos
        self.search_input.textChanged.connect(self.on_text_changed)
        
        # Lista de productos para autocompletar
        self.product_names = []
        self.completer = QCompleter()
        self.search_input.setCompleter(self.completer)
    
    def on_text_changed(self, text):
        """Maneja cambios en el texto de búsqueda"""
        # Reiniciar timer para búsqueda con delay
        self.search_timer.stop()
        self.search_timer.start(300)  # 300ms delay
        
        # Mostrar/ocultar botón de limpiar
        self.clear_btn.setVisible(bool(text.strip()))
    
    def emit_search_changed(self):
        """Emite la señal de cambio de búsqueda"""
        text = self.search_input.text().strip()
        self.search_changed.emit(text)
    
    def set_search(self, text):
        """Establece el texto de búsqueda"""
        self.search_input.setText(text)
        self.search_input.setFocus()
    
    def clear_search(self):
        """Limpia la búsqueda"""
        self.search_input.clear()
        self.search_input.setFocus()
    
    def update_completions(self, product_names):
        """Actualiza las sugerencias de autocompletado"""
        self.product_names = product_names
        model = QStringListModel(product_names)
        self.completer.setModel(model)


class ModernProductsPanel(QWidget):
    """Panel moderno de productos con búsqueda y categorías"""
    
    product_selected = pyqtSignal(dict)  # Señal cuando se selecciona producto
    
    def __init__(self, parent_tpv, parent=None):
        super().__init__(parent)
        self.parent_tpv = parent_tpv
        self.all_products = []  # Cache de todos los productos
        self.filtered_products = []  # Productos filtrados
        self.product_cards = {}  # Cache de tarjetas de productos
        
        self.setup_ui()
        self.load_products()
    
    def setup_ui(self):
        """Configura la interfaz del panel"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)
        
        # Header del panel
        header = self.create_panel_header()
        layout.addWidget(header)
        
        # Widget de búsqueda
        self.search_widget = ModernSearchWidget()
        self.search_widget.search_changed.connect(self.filter_products)
        layout.addWidget(self.search_widget)
        
        # Pestañas de categorías
        self.tabs_widget = self.create_categories_tabs()
        layout.addWidget(self.tabs_widget)
        
        # Aplicar estilos
        self.apply_panel_styles()
    
    def create_panel_header(self):
        """Crea el header del panel"""
        header = QFrame()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título
        title = QLabel("🛍️ Productos")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['gray_800']};")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Contador de productos
        self.product_count = QLabel("0 productos")
        self.product_count.setFont(QFont("Segoe UI", 12))
        self.product_count.setStyleSheet(f"color: {COLORS['gray_600']};")
        layout.addWidget(self.product_count)
        
        return header
    
    def create_categories_tabs(self):
        """Crea las pestañas de categorías"""
        tabs = QTabWidget()
        tabs.setStyleSheet(get_modern_tab_style())
        
        # Categorías principales
        categorias = ["Todos", "Bebidas", "Entrantes", "Principales", "Postres"]
        
        for categoria in categorias:
            tab_widget = self.create_category_tab(categoria)
            tabs.addTab(tab_widget, categoria)
        
        # Conectar cambio de pestaña
        tabs.currentChanged.connect(self.on_category_changed)
        
        return tabs
    
    def create_category_tab(self, categoria):
        """Crea una pestaña para una categoría"""
        # Scroll area para muchos productos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Widget contenedor
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(8, 8, 8, 8)
        
        # Grid para productos
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(12)
        
        container_layout.addWidget(grid_widget)
        container_layout.addStretch()
        
        scroll.setWidget(container)
        
        # Guardar referencia al grid para actualizar después
        setattr(scroll, 'grid_layout', grid_layout)
        setattr(scroll, 'categoria', categoria)
        
        return scroll
    
    def apply_panel_styles(self):
        """Aplica estilos al panel"""
        self.setStyleSheet(f"""
            ModernProductsPanel {{
                background: {COLORS['white']};
                border-radius: {BORDER_RADIUS['lg']};
            }}
        """)
    
    def load_products(self):
        """Carga los productos desde el servicio"""
        try:
            if hasattr(self.parent_tpv, 'tpv_service') and self.parent_tpv.tpv_service:
                # Obtener todos los productos
                categorias = ["Bebidas", "Entrantes", "Principales", "Postres"]
                all_products = []
                
                for categoria in categorias:
                    productos = self.parent_tpv.tpv_service.get_productos_por_categoria(categoria)
                    for p in productos:
                        product_data = {
                            "id": getattr(p, "id", None),
                            "nombre": getattr(p, "nombre", "Producto"),
                            "precio": getattr(p, "precio", 0.0),
                            "categoria": categoria,
                            "stock": getattr(p, "stock", None),
                            "codigo": getattr(p, "codigo", ""),
                            "descripcion": getattr(p, "descripcion", "")
                        }
                        all_products.append(product_data)
                
                self.all_products = all_products
                self.filtered_products = all_products.copy()
                
                # Actualizar autocompletado
                product_names = [p["nombre"] for p in all_products]
                self.search_widget.update_completions(product_names)
                
                # Actualizar tabs
                self.update_all_tabs()
                
                # Actualizar contador
                self.update_product_count()
                
        except Exception as e:
            print(f"Error cargando productos: {e}")
            # Productos de ejemplo para desarrollo
            self.load_example_products()
    
    def load_example_products(self):
        """Carga productos de ejemplo para desarrollo"""
        example_products = [
            {"id": 1, "nombre": "Cerveza", "precio": 3.50, "categoria": "Bebidas", "stock": 50},
            {"id": 2, "nombre": "Vino Tinto", "precio": 15.00, "categoria": "Bebidas", "stock": 20},
            {"id": 3, "nombre": "Patatas Bravas", "precio": 6.50, "categoria": "Entrantes", "stock": 30},
            {"id": 4, "nombre": "Jamón Ibérico", "precio": 18.00, "categoria": "Entrantes", "stock": 15},
            {"id": 5, "nombre": "Paella", "precio": 24.00, "categoria": "Principales", "stock": 10},
            {"id": 6, "nombre": "Solomillo", "precio": 28.00, "categoria": "Principales", "stock": 8},
            {"id": 7, "nombre": "Tiramisú", "precio": 7.50, "categoria": "Postres", "stock": 12},
            {"id": 8, "nombre": "Flan", "precio": 5.00, "categoria": "Postres", "stock": 20}
        ]
        
        self.all_products = example_products
        self.filtered_products = example_products.copy()
        
        # Actualizar autocompletado
        product_names = [p["nombre"] for p in example_products]
        self.search_widget.update_completions(product_names)
        
        # Actualizar tabs
        self.update_all_tabs()
        
        # Actualizar contador
        self.update_product_count()
    
    def filter_products(self, search_text):
        """Filtra productos según el texto de búsqueda"""
        if not search_text:
            self.filtered_products = self.all_products.copy()
        else:
            search_lower = search_text.lower()
            self.filtered_products = [
                p for p in self.all_products
                if (search_lower in p["nombre"].lower() or
                    search_lower in p.get("codigo", "").lower() or
                    search_lower in p["categoria"].lower())
            ]
        
        # Actualizar tabs y contador
        self.update_all_tabs()
        self.update_product_count()
    
    def update_all_tabs(self):
        """Actualiza todas las pestañas con productos filtrados"""
        for i in range(self.tabs_widget.count()):
            tab_widget = self.tabs_widget.widget(i)
            categoria = getattr(tab_widget, 'categoria', 'Todos')
            self.update_tab_products(tab_widget, categoria)
    
    def update_tab_products(self, tab_widget, categoria):
        """Actualiza los productos en una pestaña específica"""
        grid_layout = getattr(tab_widget, 'grid_layout', None)
        if not grid_layout:
            return
        
        # Limpiar grid actual
        self.clear_grid_layout(grid_layout)
        
        # Filtrar productos por categoría
        if categoria == "Todos":
            products = self.filtered_products
        else:
            products = [p for p in self.filtered_products if p["categoria"] == categoria]
        
        # Añadir productos al grid
        row, col = 0, 0
        max_cols = 3  # Máximo 3 columnas
        
        for product in products:
            # Crear o reutilizar tarjeta
            card_key = f"{product['id']}_{categoria}"
            if card_key in self.product_cards:
                card = self.product_cards[card_key]
            else:
                card = ModernProductCard(product)
                card.product_selected.connect(self.on_product_selected)
                self.product_cards[card_key] = card
            
            grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def clear_grid_layout(self, layout):
        """Limpia un grid layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
    
    def update_product_count(self):
        """Actualiza el contador de productos"""
        count = len(self.filtered_products)
        self.product_count.setText(f"{count} productos")
    
    def on_category_changed(self, index):
        """Maneja el cambio de categoría"""
        # La actualización se hace automáticamente en update_all_tabs
        pass
    
    def on_product_selected(self, product_data):
        """Maneja la selección de un producto"""
        # Resaltar temporalmente la tarjeta
        sender = self.sender()
        if isinstance(sender, ModernProductCard):
            sender.set_highlighted(True)
            QTimer.singleShot(200, lambda: sender.set_highlighted(False))
        
        # Emitir señal
        self.product_selected.emit(product_data)
    
    def refresh_products(self):
        """Refresca la lista de productos"""
        self.load_products()


def create_modern_productos_panel(parent_tpv) -> ModernProductsPanel:
    """
    Función factory para crear el panel de productos moderno
    
    Args:
        parent_tpv: Instancia del TPV principal
        
    Returns:
        ModernProductsPanel: Panel de productos configurado
    """
    return ModernProductsPanel(parent_tpv)
