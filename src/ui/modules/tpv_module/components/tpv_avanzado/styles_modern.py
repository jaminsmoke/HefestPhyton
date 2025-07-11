"""
Estilos modernos para TPV Avanzado v0.0.14
Paleta de colores profesional y sistema de estilos consistente
"""

# 🎨 PALETA DE COLORES MODERNA
COLORS = {
    # Colores primarios
    "primary": "#2563eb",           # Azul moderno
    "primary_dark": "#1d4ed8",      # Azul oscuro
    "primary_light": "#3b82f6",     # Azul claro
    
    # Colores secundarios
    "secondary": "#64748b",         # Gris azulado
    "secondary_light": "#94a3b8",   # Gris claro
    "accent": "#059669",            # Verde para éxito
    "warning": "#d97706",           # Naranja para advertencias
    "danger": "#dc2626",            # Rojo para errores
    
    # Neutrales
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
    
    # Colores especiales para TPV
    "success": "#10b981",           # Verde para ventas completadas
    "pending": "#f59e0b",           # Amarillo para pendientes
    "table_free": "#ecfdf5",        # Verde muy claro para mesas libres
    "table_occupied": "#fef3c7",    # Amarillo claro para mesas ocupadas
    "table_reserved": "#e0e7ff",    # Azul claro para mesas reservadas
}

# 📐 DIMENSIONES Y ESPACIADO
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px",
    "2xl": "32px",
    "3xl": "48px",
}

BORDER_RADIUS = {
    "sm": "6px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "full": "50%",
}

# 🎯 ESTILOS DE COMPONENTES TPV

def get_modern_button_style(variant="primary", size="md"):
    """Genera estilos modernos para botones"""
    base_style = f"""
        QPushButton {{
            border: none;
            border-radius: {BORDER_RADIUS['md']};
            font-weight: 600;
            font-family: 'Segoe UI', Arial, sans-serif;
            transition: all 0.2s ease;
        }}
        QPushButton:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        QPushButton:pressed {{
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        QPushButton:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
    """
    
    # Tamaños
    sizes = {
        "sm": f"padding: {SPACING['sm']} {SPACING['md']}; font-size: 13px; min-width: 80px; min-height: 32px;",
        "md": f"padding: {SPACING['md']} {SPACING['lg']}; font-size: 14px; min-width: 100px; min-height: 38px;",
        "lg": f"padding: {SPACING['lg']} {SPACING['xl']}; font-size: 16px; min-width: 120px; min-height: 44px;",
    }
    
    # Variantes de color
    variants = {
        "primary": f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']});
            color: {COLORS['white']};
        """,
        "secondary": f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['gray_100']}, stop:1 {COLORS['gray_200']});
            color: {COLORS['gray_700']};
            border: 1px solid {COLORS['gray_300']};
        """,
        "success": f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['success']}, stop:1 {COLORS['accent']});
            color: {COLORS['white']};
        """,
        "warning": f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['warning']}, stop:1 #b45309);
            color: {COLORS['white']};
        """,
        "danger": f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['danger']}, stop:1 #b91c1c);
            color: {COLORS['white']};
        """,
    }
    
    return base_style + f"QPushButton {{ {sizes[size]} {variants[variant]} }}"

def get_modern_card_style():
    """Genera estilos para tarjetas modernas"""
    return f"""
        QFrame {{
            background: {COLORS['white']};
            border: 1px solid {COLORS['gray_200']};
            border-radius: {BORDER_RADIUS['lg']};
            padding: {SPACING['lg']};
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        QFrame:hover {{
            border-color: {COLORS['primary_light']};
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
        }}
    """

def get_modern_input_style():
    """Genera estilos para inputs modernos"""
    return f"""
        QLineEdit, QComboBox {{
            background: {COLORS['white']};
            border: 2px solid {COLORS['gray_200']};
            border-radius: {BORDER_RADIUS['md']};
            padding: {SPACING['md']};
            font-size: 14px;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: {COLORS['gray_800']};
        }}
        QLineEdit:focus, QComboBox:focus {{
            border-color: {COLORS['primary']};
            outline: none;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }}
        QLineEdit::placeholder {{
            color: {COLORS['gray_400']};
        }}
    """

def get_modern_table_style():
    """Genera estilos para tablas modernas"""
    return f"""
        QTableWidget {{
            background: {COLORS['white']};
            border: 1px solid {COLORS['gray_200']};
            border-radius: {BORDER_RADIUS['md']};
            gridline-color: {COLORS['gray_100']};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        QTableWidget::item {{
            padding: {SPACING['md']};
            border: none;
        }}
        QTableWidget::item:selected {{
            background: {COLORS['primary_light']};
            color: {COLORS['white']};
        }}
        QHeaderView::section {{
            background: {COLORS['gray_50']};
            border: none;
            border-bottom: 2px solid {COLORS['gray_200']};
            padding: {SPACING['md']};
            font-weight: 600;
            color: {COLORS['gray_700']};
        }}
    """

def get_modern_tab_style():
    """Genera estilos para pestañas modernas"""
    return f"""
        QTabWidget::pane {{
            border: 1px solid {COLORS['gray_200']};
            background: {COLORS['white']};
            border-radius: {BORDER_RADIUS['md']};
            margin-top: -1px;
        }}
        QTabBar::tab {{
            background: {COLORS['gray_100']};
            border: 1px solid {COLORS['gray_200']};
            border-bottom: none;
            border-radius: {BORDER_RADIUS['md']} {BORDER_RADIUS['md']} 0 0;
            padding: {SPACING['md']} {SPACING['lg']};
            margin-right: 2px;
            font-weight: 500;
            color: {COLORS['gray_600']};
            min-width: 120px;
        }}
        QTabBar::tab:selected {{
            background: {COLORS['white']};
            border-bottom: 2px solid {COLORS['primary']};
            color: {COLORS['primary']};
            font-weight: 600;
        }}
        QTabBar::tab:hover:!selected {{
            background: {COLORS['gray_200']};
            color: {COLORS['gray_700']};
        }}
    """

def get_product_card_style():
    """Estilos específicos para tarjetas de productos"""
    return f"""
        QPushButton {{
            background: {COLORS['white']};
            border: 2px solid {COLORS['gray_200']};
            border-radius: {BORDER_RADIUS['lg']};
            padding: {SPACING['lg']};
            text-align: center;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: {COLORS['gray_800']};
            min-width: 140px;
            min-height: 100px;
        }}
        QPushButton:hover {{
            border-color: {COLORS['primary']};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['white']}, stop:1 {COLORS['gray_50']});
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15);
        }}
        QPushButton:pressed {{
            background: {COLORS['primary_light']};
            color: {COLORS['white']};
            transform: translateY(0);
        }}
        QPushButton:disabled {{
            background: {COLORS['gray_100']};
            color: {COLORS['gray_400']};
            border-color: {COLORS['gray_200']};
        }}
    """

def get_status_badge_style(status="success"):
    """Genera estilos para badges de estado"""
    status_colors = {
        "success": {"bg": COLORS['success'], "text": COLORS['white']},
        "warning": {"bg": COLORS['warning'], "text": COLORS['white']},
        "danger": {"bg": COLORS['danger'], "text": COLORS['white']},
        "pending": {"bg": COLORS['pending'], "text": COLORS['white']},
        "info": {"bg": COLORS['primary'], "text": COLORS['white']},
    }
    
    colors = status_colors.get(status, status_colors['info'])
    
    return f"""
        QLabel {{
            background: {colors['bg']};
            color: {colors['text']};
            border-radius: {BORDER_RADIUS['full']};
            padding: {SPACING['xs']} {SPACING['md']};
            font-size: 12px;
            font-weight: 600;
            text-align: center;
        }}
    """

# 🎭 ANIMACIONES Y EFECTOS
def get_fade_animation():
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

def get_slide_animation():
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
            animation: slideInUp 0.4s ease-out;
        }
    """

# 🌓 MODO OSCURO (para implementación futura)
DARK_COLORS = {
    "primary": "#3b82f6",
    "background": "#1f2937",
    "surface": "#374151",
    "text": "#f9fafb",
    "text_secondary": "#9ca3af",
    "border": "#4b5563",
}

def get_dark_theme_override():
    """Estilos para modo oscuro"""
    return f"""
        QWidget {{
            background-color: {DARK_COLORS['background']};
            color: {DARK_COLORS['text']};
        }}
        QFrame {{
            background-color: {DARK_COLORS['surface']};
            border-color: {DARK_COLORS['border']};
        }}
    """
