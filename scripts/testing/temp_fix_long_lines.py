#!/usr/bin/env python3
"""
Script temporal para arreglar líneas largas en inventario_service_real.py
"""

import re

def fix_long_lines(file_path: str) -> None:
    """Arregla líneas largas en el archivo especificado"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fixes específicos para líneas largas comunes
    fixes = [
        # Arreglar logger.warning
        (r'logger\.warning\("Sin conexión a base de datos, retornando lista vacía"\)',
         'logger.warning(\n                "Sin conexión a base de datos, retornando lista vacía"\n            )'),
        
        # Arreglar logger.info con líneas largas
        (r'logger\.info\("No se encontraron proveedores en la base de datos"\)',
         'logger.info(\n                "No se encontraron proveedores en la base de datos"\n            )'),
        
        # Arreglar logger.warning largos
        (r'logger\.warning\(f"La categoría \'\{nombre\}\' ya existe y está activa"\)',
         'logger.warning(\n                    f"La categoría \'{nombre}\' ya existe y está activa"\n                )'),
        
        # Arreglar logger.info largos
        (r'logger\.info\(f"Categoría \'\{nombre\}\' reactivada exitosamente"\)',
         'logger.info(\n                    f"Categoría \'{nombre}\' reactivada exitosamente"\n                )'),
        
        # Arreglar listas largas
        (r'return \["General", "Bebidas", "Comida", "Limpieza", "Papelería"\]',
         'return [\n                    "General", "Bebidas", "Comida", "Limpieza", "Papelería"\n                ]'),
        
        # Arreglar docstrings largos
        (r'"""Obtener lista de proveedores desde la tabla proveedores con soporte de categorías"""',
         '"""\n        Obtener lista de proveedores desde la tabla proveedores\n        con soporte de categorías\n        """'),
        
        (r'"""Crear un nuevo proveedor en la tabla proveedores\. Si existe uno inactivo, lo reactiva\."""',
         '"""\n        Crear un nuevo proveedor en la tabla proveedores.\n        Si existe uno inactivo, lo reactiva.\n        """'),
        
        # Arreglar queries largos
        (r'"SELECT id, activa FROM categorias WHERE LOWER\(nombre\) = LOWER\(\?\)"',
         '(\n                "SELECT id, activa FROM categorias "\n                "WHERE LOWER(nombre) = LOWER(?)"\n            )'),
        
        (r'"UPDATE categorias SET activa = 1, descripcion = \? WHERE id = \?"',
         '(\n                        "UPDATE categorias SET activa = 1, "\n                        "descripcion = ? WHERE id = ?"\n                    )'),
        
        (r'INSERT INTO categorias \(nombre, descripcion, fecha_creacion, activa\)',
         'INSERT INTO categorias \n                (nombre, descripcion, fecha_creacion, activa)'),
        
        # Arreglar líneas de cálculo largos
        (r'productos_sin_stock = len\(\[p for p in productos if p\.stock_actual == 0\]\)',
         'productos_sin_stock = len([\n                p for p in productos if p.stock_actual == 0\n            ])'),
        
        (r'producto_mas_caro = max\(productos, key=lambda p: p\.precio, default=None\)',
         'producto_mas_caro = max(\n                productos, key=lambda p: p.precio, default=None\n            )'),
        
        # Arreglar líneas de diccionario largos
        (r'"contacto": contacto\.strip\(\) if contacto else ""',
         '"contacto": (\n                                    contacto.strip() if contacto else ""\n                                )'),
        
        (r'"telefono": telefono\.strip\(\) if telefono else ""',
         '"telefono": (\n                                    telefono.strip() if telefono else ""\n                                )'),
        
        (r'"direccion": direccion\.strip\(\) if direccion else ""',
         '"direccion": (\n                                    direccion.strip() if direccion else ""\n                                )'),
        
        (r'categoria\.strip\(\) if categoria else "General"',
         '(\n                                    categoria.strip() if categoria else "General"\n                                )'),
        
        (r'"activo": bool\(proveedor_dict\.get\("activo", True\)\)',
         '"activo": bool(\n                                    proveedor_dict.get("activo", True)\n                                )'),
        
        (r'proveedor_dict\.get\("categoria", "General"\) or "General"',
         '(\n                            proveedor_dict.get("categoria", "General") \n                            or "General"\n                        )'),
        
        # Arreglar logger.info largos con formato
        (r'logger\.info\(f"Obtenidos \{len\(proveedores\)\} proveedores de la base de datos"\)',
         'logger.info(\n                f"Obtenidos {len(proveedores)} proveedores de la base de datos"\n            )'),
        
        # Arreglar comentarios de docstring largos  
        (r'Crear una nueva categoría en la tabla categorias\. Si existe una inactiva, la reactiva\.',
         'Crear una nueva categoría en la tabla categorias.\n        Si existe una inactiva, la reactiva.'),
        
        # Arreglar "No se encontraron categorías activas..."
        (r'"No se encontraron categorías activas, retornando categorías por defecto"',
         '(\n                    "No se encontraron categorías activas, "\n                    "retornando categorías por defecto"\n                )'),
    ]
    
    # Aplicar todas las correcciones
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content)
    
    # Escribir contenido corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Líneas largas corregidas en {file_path}")

if __name__ == "__main__":
    file_path = "src/services/inventario_service_real.py"
    fix_long_lines(file_path)
    print("¡Correcciones aplicadas!")
