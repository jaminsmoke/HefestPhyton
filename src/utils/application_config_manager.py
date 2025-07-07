"""
Módulo de configuración global de la aplicación.
Maneja las preferencias del usuario y configuraciones del sistema.
Versión extendida con características avanzadas.
"""

import os
import json
import logging
import hashlib
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# EXCEPCIÓN FUNCIONAL: No configurar logging global aquí para evitar duplicidad de handlers.
# El logging global se configura únicamente en el entrypoint principal (hefest_application.py).
## TODO(v0.0.14): Si se requiere logging específico, usar solo loggers de módulo sin basicConfig ni handlers globales.
logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Gestiona la configuración de la aplicación, cargando y guardando
    las preferencias del usuario y los ajustes del sistema.
    """

    DEFAULT_CONFIG = {
        "app": {"name": "Hefest", "version": "0.0.14", "theme": "light"},
        "database": {"type": "sqlite", "path": "hefest.db"},
        "ui": {"language": "es", "font_size": 10, "show_toolbar": True},
        "tpv": {
            "impresora_tickets": "default",
            "formato_ticket": "standard",
            "mostrar_iva_desglosado": True,
        },
        "hospederia": {
            "check_in_time": "14:00",
            "check_out_time": "12:00",
            "cobro_automatico": False,
        },
        "backup": {
            "auto_backup": True,
            "backup_frequency": "daily",  # daily, weekly, monthly
            "backup_path": "backups/",
        },
    }

    def __init__(self, config_file="config.json"):
        """Inicializa el gestor de configuración"""
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, config_file)

        # Cargar configuración o crear una nueva
        if os.path.exists(self.config_file):
            try:
                self.config = self._load_config()
                logger.info(f"Configuración cargada desde {self.config_file}")
            except Exception as e:
                logger.error(f"Error al cargar configuración: {e}")
                self.config = self.DEFAULT_CONFIG
                self._save_config()
        else:
            logger.info("Archivo de configuración no encontrado. Creando uno nuevo.")
            self.config = self.DEFAULT_CONFIG
            self._save_config()

    def _get_config_dir(self):
        """Obtiene el directorio de configuración"""
        # Determinar directorio según la plataforma
        app_data = os.path.join(str(Path.home()), "AppData", "Local", "Hefest")

        # Crear directorio si no existe
        os.makedirs(app_data, exist_ok=True)

        return app_data

    def _load_config(self):
        """Carga la configuración desde el archivo"""
        with open(self.config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_config(self):
        """Guarda la configuración en el archivo"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
        logger.info(f"Configuración guardada en {self.config_file}")

    def get(self, section, key=None):
        """
        Obtiene una sección completa o un valor específico de la configuración

        Args:
            section: La sección de configuración
            key: La clave específica (opcional)

        Returns:
            dict o valor específico
        """
        if section not in self.config:
            return None

        if key is None:
            return self.config[section]

        if key in self.config[section]:
            return self.config[section][key]

        return None

    def set(self, section, key, value):
        """
        Establece un valor en la configuración

        Args:
            section: La sección de configuración
            key: La clave específica
            value: El valor a establecer
        """
        if section not in self.config:
            self.config[section] = {}

        self.config[section][key] = value
        self._save_config()

    def update_section(self, section, values):
        """
        Actualiza una sección completa de la configuración

        Args:
            section: La sección a actualizar
            values: Diccionario con los valores a establecer
        """
        if section not in self.config:
            self.config[section] = {}

        self.config[section].update(values)
        self._save_config()

    def reset_to_default(self, section=None):
        """
        Restablece la configuración a los valores predeterminados

        Args:
            section: La sección específica a restablecer (opcional)
        """
        if section is None:
            self.config = self.DEFAULT_CONFIG
        elif section in self.DEFAULT_CONFIG:
            self.config[section] = self.DEFAULT_CONFIG[section]

        self._save_config()

    def get_all_config(self):
        """
        Retorna toda la configuración actual como un diccionario plano

        Returns:
            dict: Configuración completa en formato plano
        """
        flat_config = {}

        def flatten_dict(d, parent_key="", sep="_"):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)

        return flatten_dict(self.config)

    def set_config(self, key, value):
        """
        Establece un valor de configuración usando notación de punto

        Args:
            key (str): Clave de configuración (ej: 'app.theme')
            value: Valor a establecer
        """
        keys = key.split(".")
        current = self.config

        # Navegar hasta el penúltimo nivel
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        # Establecer el valor
        current[keys[-1]] = value
        self._save_config()

    def get_config(self, key, default=None):
        """
        Obtiene un valor de configuración usando notación de punto

        Args:
            key (str): Clave de configuración (ej: 'app.theme')
            default: Valor por defecto si no se encuentra la clave

        Returns:
            Valor de configuración o valor por defecto
        """
        keys = key.split(".")
        current = self.config

        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default

    def export_config(self, file_path):
        """
        Exporta la configuración actual a un archivo

        Args:
            file_path (str): Ruta del archivo de destino
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            logger.info(f"Configuración exportada a: {file_path}")
        except Exception as e:
            logger.error(f"Error al exportar configuración: {e}")
            raise

    def import_config(self, file_path):
        """
        Importa configuración desde un archivo

        Args:
            file_path (str): Ruta del archivo de origen
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                imported_config = json.load(f)

            # Validar y aplicar configuración importada
            self.config.update(imported_config)
            self._save_config()
            logger.info(f"Configuración importada desde: {file_path}")
        except Exception as e:
            logger.error(f"Error al importar configuración: {e}")
            raise

    # === CARACTERÍSTICAS AVANZADAS ===

    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """Crea un backup de la configuración actual"""
        if backup_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"config_backup_{timestamp}.json"

        backup_dir = os.path.join(self.config_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)

        backup_path = os.path.join(backup_dir, backup_name)

        try:
            with open(backup_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            logger.info(f"Backup creado: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Error creando backup: {e}")
            raise

    def restore_backup(self, backup_path: str) -> bool:
        """Restaura la configuración desde un backup"""
        try:
            with open(backup_path, "r", encoding="utf-8") as f:
                backup_config = json.load(f)

            # Crear backup de la configuración actual antes de restaurar
            self.create_backup("pre_restore_backup.json")

            self.config = backup_config
            self._save_config()
            logger.info(f"Configuración restaurada desde: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error restaurando backup: {e}")
            return False

    def get_config_hash(self) -> str:
        """Obtiene un hash de la configuración actual para detectar cambios"""
        config_str = json.dumps(self.config, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()

    def validate_config(self) -> List[str]:
        """Valida la configuración y retorna lista de errores encontrados"""
        errors = []

        # Validaciones básicas
        required_sections = ["app", "database", "ui"]
        for section in required_sections:
            if section not in self.config:
                errors.append(f"Sección requerida '{section}' no encontrada")

        # Validar tipos de datos específicos
        if "app" in self.config:
            app_config = self.config["app"]
            if "version" in app_config and not isinstance(app_config["version"], str):
                errors.append("app.version debe ser una cadena de texto")

        if "ui" in self.config:
            ui_config = self.config["ui"]
            if "font_size" in ui_config and not isinstance(ui_config["font_size"], int):
                errors.append("ui.font_size debe ser un número entero")

        return errors

    def reset_to_defaults(self, section: Optional[str] = None) -> None:
        """Restaura la configuración por defecto (toda o una sección específica)"""
        if section:
            if section in self.DEFAULT_CONFIG:
                self.config[section] = self.DEFAULT_CONFIG[section].copy()
                logger.info(f"Sección '{section}' restaurada a valores por defecto")
            else:
                logger.warning(
                    f"Sección '{section}' no existe en configuración por defecto"
                )
        else:
            self.config = self.DEFAULT_CONFIG.copy()
            logger.info("Configuración completa restaurada a valores por defecto")

        self._save_config()

    def get_user_settings(self) -> Dict[str, Any]:
        """Obtiene solo las configuraciones modificadas por el usuario"""
        user_settings = {}

        def compare_configs(default: Dict, current: Dict, path: str = ""):
            for key, value in current.items():
                current_path = f"{path}.{key}" if path else key

                if key not in default:
                    user_settings[current_path] = value
                elif isinstance(value, dict) and isinstance(default[key], dict):
                    compare_configs(default[key], value, current_path)
                elif value != default[key]:
                    user_settings[current_path] = value

        compare_configs(self.DEFAULT_CONFIG, self.config)
        return user_settings

    def get_config_info(self) -> Dict[str, Any]:
        """Obtiene información sobre la configuración actual"""
        config_info = {
            "config_file": self.config_file,
            "config_dir": self.config_dir,
            "last_modified": None,
            "file_size": 0,
            "config_hash": self.get_config_hash(),
            "validation_errors": self.validate_config(),
            "user_settings_count": len(self.get_user_settings()),
        }

        try:
            if os.path.exists(self.config_file):
                stat = os.stat(self.config_file)
                config_info["last_modified"] = datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat()
                config_info["file_size"] = stat.st_size
        except Exception as e:
            logger.warning(f"No se pudo obtener información del archivo: {e}")

        return config_info


# Instancia global para usar en toda la aplicación
config_manager = ConfigManager()
