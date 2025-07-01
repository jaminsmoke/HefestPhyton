# HEFEST - Sistema Integral de Hostelería

## Políticas de Organización y Estandarización

- No se permite la existencia de archivos sueltos en la raíz del proyecto, salvo los esenciales (README.md, main.py, requirements.txt, pyproject.toml, LICENSE, MANIFEST.in, Makefile.ps1, .gitignore, .editorconfig, .env).
- Toda carpeta debe tener un README propio que explique su propósito, las políticas contextuales y la información relevante sobre su contenido.
- La documentación de implementaciones, progreso, decisiones técnicas o migraciones debe estar en la carpeta `docs/` y sus subcarpetas, nunca en los README de la raíz ni de las carpetas técnicas.
- La estructura de carpetas debe reflejarse y mantenerse actualizada en este README. Cualquier cambio en la estructura real debe reflejarse aquí.
- La nomenclatura de archivos y carpetas debe seguir el estándar definido en `docs/README.md` y los README de cada área.
- No se permite documentación de implementaciones específicas, progreso de tareas ni detalles de limpieza en los README de la raíz ni de carpetas técnicas.
- Todo README de carpeta debe crearse siguiendo la plantilla oficial incluida en este README (ver sección "Plantilla oficial para README de carpetas"). Esta plantilla define la estructura, el tipo de información permitida y las prohibiciones para mantener la estandarización.

## Estructura de Carpetas (actualizada a 28/06/2025)

```
Hefest/
├── assets/           # Recursos visuales y multimedia
├── build-tools/      # Herramientas de build y automatización
├── config/           # Configuración por entorno
├── data/             # Base de datos y backups
├── docs/             # Documentación y logs
│   ├── analysis/
│   ├── archive/
│   ├── changelog/
│   ├── development/
│   ├── logs/
│   └── ...
├── logs/             # Logs y reportes de pruebas
├── logs_debug/       # Logs temporales de depuración puntual (no producción)
├── scripts/          # Scripts de utilidad, análisis, testing, migración
│   ├── analysis/
│   ├── maintenance/
│   ├── migration/
│   ├── testing/
│   └── ...
├── src/              # Código fuente principal
├── tests/            # Tests automatizados (unit, integration, ui, utilities)
├── version-backups/  # Backups versionados
├── main.py           # Punto de entrada principal
├── README.md         # Este archivo
├── requirements.txt  # Dependencias Python
├── pyproject.toml    # Configuración del proyecto
├── LICENSE           # Licencia
├── MANIFEST.in       # Manifest para packaging
├── Makefile.ps1      # Automatización de tareas
├── .gitignore        # Git ignore
├── .editorconfig     # Editor config
├── .env              # Variables de entorno
└── ...
```

---

## 📑 Plantilla oficial para README de carpetas

Toda carpeta debe tener un README siguiendo esta estructura visual y profesional:

---

# [ICONO] [NOMBRE DE LA CARPETA] - [Propósito]

Breve descripción del propósito de la carpeta y su rol en la estructura del proyecto.

---

## 📋 Índice de Contenidos

| Sección                                             | Descripción                              |
| --------------------------------------------------- | ---------------------------------------- |
| [🗂️ Estructura](#estructura)                         | Organización interna y tipos de archivos |
| [📁 Políticas y Estándares](#políticas-y-estándares) | Qué se permite y qué no                  |
| [🚀 Uso e Integración](#uso-e-integración)           | Cómo se usa la carpeta (opcional)        |
| [📖 Información relevante](#información-relevante)   | Enlaces y notas (opcional)               |

---

## 🗂️ Estructura

```
[nombre_carpeta]/
├── archivo1.ext   # Descripción breve
├── subcarpeta/    # Propósito
└── ...
```

- Explica brevemente la función de los principales archivos y subcarpetas.

---

## 📁 Políticas y Estándares

- Qué tipo de archivos/documentos se permiten aquí.
- Nomenclatura esperada (si aplica).
- Prohibiciones (ej: no código fuente, no documentación de progreso, etc).
- Referencia a la política general en el README raíz.

---

## 🚀 Uso e Integración (opcional)

- Cómo se usa la carpeta o sus archivos (si aplica).
- Ejemplos de comandos, integración o dependencias.

---

## 📖 Información relevante (opcional)

- Enlaces a documentación adicional en `docs/` si es necesario.
- Notas, advertencias o recomendaciones visuales.

---

> **Nota:** No incluir aquí detalles de progreso, migraciones, ni implementaciones específicas. Toda esa información debe estar en `docs/`.

---

**Cumple con la política de estandarización y organización definida en el README raíz.**

---

Para políticas y detalles de cada área, consulta el README de la carpeta correspondiente y la documentación en `docs/`.
