"""
Estilos modernos para TPV Avanzado v0.0.14
Paleta de colores profesional y sistema de estilos consistente
"""

# 🎨 PALETA DE COLORES MODERNA
COLORS = {
    # Colores primarios
    "primary": "#2563eb",           # Azul moderno
    "primary_dark": "#1d4ed8",      # Azul oscuro
    "primary_light": "#60a5fa",     # Azul claro
    
    # Colores de estado
    "success": "#10b981",           # Verde éxito
    "warning": "#f59e0b",           # Amarillo advertencia
    "danger": "#ef4444",            # Rojo peligro
    "info": "#3b82f6",              # Azul información
    
    # Escala de grises
    "white": "#ffffff",
    "gray_50": "#f9fafb",
    "gray_100": "#f3f4f6",
    "gray_200": "#e5e7eb",
    "gray_300": "#d1d5db",
    "gray_400": "#9ca3af",
    "gray_500": "#6b7280",
    "gray_600": "#4b5563",
    "gray_700": "#374151",
    "gray_800": "#1f2937",
    "gray_900": "#111827",
    "black": "#000000",
    
    # Colores de fondo
    "background": "#f8fafc",
    "surface": "#ffffff",
    "card": "#ffffff",
}

# 📏 SISTEMA DE ESPACIADO
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "20px",
    "2xl": "24px",
    "3xl": "32px",
}

# 🔄 BORDER RADIUS
BORDER_RADIUS = {
    "none": "0px",
    "sm": "4px",
    "md": "6px",
    "lg": "8px",
    "xl": "12px",
    "full": "50%",
}


# 🎯 ESTILOS DE COMPONENTES TPV


def get_modern_button_style(variant: str = "primary",
                            size: str = "md") -> str:
    """Genera estilos modernos para botones"""
    base_style = f"""
        QPushButton {{
            border: none;
            border-radius: {BORDER_RADIUS['md']};
            font-weight: 600;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        QPushButton:hover {{
            opacity: 0.9;
        }}
        QPushButton:pressed {{
            opacity: 0.8;
        }}
        QPushButton:disabled {{
            opacity: 0.5;
        }}
    """
    
    # Tamaños
    sizes = {
        "sm": (f"padding: {SPACING['sm']} {SPACING['md']}; "
               f"font-size: 13px; min-width: 80px; min-height: 32px;"),
        "md": (f"padding: {SPACING['md']} {SPACING['lg']}; "
               f"font-size: 14px; min-width: 100px; min-height: 38px;"),
        "lg": (f"padding: {SPACING['lg']} {SPACING['xl']}; "
               f"font-size: 16px; min-width: 120px; min-height: 44px;"),
    }
    
    # Variantes de color
    variants = {
        "primary": f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']});
            color: {COLORS['white']};
        """,
        "secondary": f"""
            background: {COLORS['gray_100']};
            color: {COLORS['gray_800']};
            border: 1px solid {COLORS['gray_300']};
        """,
        "success": f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['success']}, stop:1 #059669);
            color: {COLORS['white']};
        """,
        "warning": f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['warning']}, stop:1 #d97706);
            color: {COLORS['white']};
        """,
        "danger": f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['danger']}, stop:1 #b91c1c);
            color: {COLORS['white']};
        """,
    }
    
    return base_style + f"QPushButton {{ {sizes[size]} {variants[variant]} }}"


def get_modern_card_style() -> str:
    """Genera estilos para tarjetas modernas"""
    return f"""
        QFrame {{
            background: {COLORS['white']};
            border: 1px solid {COLORS['gray_200']};
            border-radius: {BORDER_RADIUS['lg']};
            padding: {SPACING['lg']};
        }}
        QFrame:hover {{
            border-color: {COLORS['primary_light']};
            background: {COLORS['gray_50']};
        }}
    """


def get_modern_input_style() -> str:
    """Genera estilos para inputs modernos"""
    return f"""
        QLineEdit, QComboBox {{
            background: {COLORS['white']};
            border: 2px solid {COLORS['gray_200']};
            border-radius: {BORDER_RADIUS['md']};
            padding: {SPACING['sm']} {SPACING['md']};
            font-size: 14px;
            color: {COLORS['gray_800']};
        }}
        QLineEdit:focus, QComboBox:focus {{
            border-color: {COLORS['primary']};
            outline: none;
        }}
        QLineEdit:hover, QComboBox:hover {{
            border-color: {COLORS['gray_300']};
        }}
        QSpinBox {{
            background: {COLORS['white']};
            border: 2px solid {COLORS['gray_200']};
            border-radius: {BORDER_RADIUS['md']};
            padding: {SPACING['sm']};
            font-size: 14px;
        }}
    """


def get_modern_table_style() -> str:
    """Genera estilos para tablas modernas"""
    return f"""
        QTableWidget {{
            background: {COLORS['white']};
            border: 1px solid {COLORS['gray_200']};
            border-radius: {BORDER_RADIUS['md']};
            gridline-color: {COLORS['gray_200']};
            font-size: 14px;
        }}
        QTableWidget::item {{
            padding: {SPACING['md']};
            border-bottom: 1px solid {COLORS['gray_100']};
        }}
        QTableWidget::item:selected {{
            background: {COLORS['primary_light']};
            color: {COLORS['white']};
        }}
        QTableWidget::item:hover {{
            background: {COLORS['gray_50']};
        }}
        QHeaderView::section {{
            background: {COLORS['gray_100']};
            color: {COLORS['gray_700']};
            padding: {SPACING['md']};
            border: none;
            font-weight: 600;
        }}
    """


def get_modern_tab_style() -> str:
    """Genera estilos para pestañas modernas"""
    return f"""
        QTabWidget::pane {{
            border: 1px solid {COLORS['gray_200']};
            background: {COLORS['white']};
            border-radius: {BORDER_RADIUS['md']};
        }}
        
        QTabWidget::tab-bar {{
            alignment: center;
        }}
        
        QTabBar::tab {{
            background: {COLORS['gray_100']};
            color: {COLORS['gray_600']};
            border: 1px solid {COLORS['gray_200']};
            padding: {SPACING['sm']} {SPACING['md']};
            margin-right: 2px;
            border-top-left-radius: {BORDER_RADIUS['md']};
            border-top-right-radius: {BORDER_RADIUS['md']};
        }}
        
        QTabBar::tab:selected {{
            background: {COLORS['primary']};
            color: {COLORS['white']};
            border-bottom: 2px solid {COLORS['primary']};
        }}
        
        QTabBar::tab:hover {{
            background: {COLORS['gray_200']};
        }}
    """


def get_product_card_style() -> str:
    """Estilos específicos para tarjetas de productos"""
    return f"""
        QPushButton {{
            background: {COLORS['white']};
            border: 2px solid {COLORS['gray_200']};
            border-radius: {BORDER_RADIUS['lg']};
            padding: {SPACING['lg']};
            text-align: left;
            font-size: 14px;
            color: {COLORS['gray_800']};
        }}
        QPushButton:hover {{
            border-color: {COLORS['primary']};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['white']}, stop:1 {COLORS['gray_50']});
        }}
        QPushButton:pressed {{
            background: {COLORS['primary_light']};
            color: {COLORS['white']};
        }}
    """


def get_status_badge_style(status: str = "success") -> str:
    """Genera estilos para badges de estado"""
    status_colors = {
        "success": {"bg": COLORS['success'], "text": COLORS['white']},
        "warning": {"bg": COLORS['warning'], "text": COLORS['white']},
        "danger": {"bg": COLORS['danger'], "text": COLORS['white']},
        "info": {"bg": COLORS['info'], "text": COLORS['white']},
        "default": {"bg": COLORS['gray_100'], "text": COLORS['gray_800']},
    }
    
    colors = status_colors.get(status, status_colors["default"])
    
    return f"""
        QLabel {{
            background: {colors['bg']};
            color: {colors['text']};
            padding: {SPACING['xs']} {SPACING['sm']};
            border-radius: {BORDER_RADIUS['full']};
            font-size: 12px;
            font-weight: 600;
        }}
    """


def get_fade_animation() -> str:
    """CSS para animaciones de fade"""
    return """
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .fade-in {
            animation: fadeIn 0.3s ease-in-out;
        }
    """


def get_slide_animation() -> str:
    """CSS para animaciones de slide"""
    return """
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .slide-in-up {
            animation: slideInUp 0.3s ease-out;
        }
    """


# 🌙 TEMA OSCURO

DARK_COLORS = {
    "background": "#1a1a1a",
    "surface": "#2d2d2d",
    "text": "#ffffff",
    "text_secondary": "#b3b3b3",
}


def get_dark_theme_override() -> str:
    """Estilos para modo oscuro"""
    return f"""
        QWidget {{
            background-color: {DARK_COLORS['background']};
            color: {DARK_COLORS['text']};
        }}
        QFrame {{
            background-color: {DARK_COLORS['surface']};
            border-color: #404040;
        }}
        QLineEdit, QComboBox {{
            background-color: {DARK_COLORS['surface']};
            color: {DARK_COLORS['text']};
            border-color: #404040;
        }}
    """
