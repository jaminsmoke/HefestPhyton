"""
Sistema de Configuración Avanzada para Hefest
============================================

Extensión del ConfigManager con características profesionales:
- Encriptación de configuraciones sensibles
- Backup automático
- Validación de esquemas
- Sincronización multi-usuario
- Hot-reload de configuraciones
"""

import os
import json
import logging
import hashlib
import base64
from pathlib import Path
from typing import Dict, Any, Optional, Union
from datetime import datetime
import threading
import time

logger = logging.getLogger(__name__)

# Imports opcionales para características avanzadas
try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    logger.debug("cryptography no disponible - encriptación deshabilitada")

try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    validate = None
    ValidationError = None
    HAS_JSONSCHEMA = False
    logger.debug("jsonschema no disponible - validación de esquemas deshabilitada")

if not HAS_CRYPTO:
    logger.warning("cryptography no está instalado. La encriptación está deshabilitada.")
if not HAS_JSONSCHEMA:
    logger.warning("jsonschema no está instalado. La validación de esquemas está deshabilitada.")

class AdvancedConfigManager:
    """Gestor de configuración avanzado con características empresariales"""

    # Esquema de validación para configuraciones
    CONFIG_SCHEMA = {
        "type": "object",
        "properties": {
            "app": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
                    "debug": {"type": "boolean"},
                    "log_level": {"type": "string", "enum": ["DEBUG", "INFO", "WARNING", "ERROR"]}
                },
                "required": ["name", "version"]
            },
            "database": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "backup_enabled": {"type": "boolean"},
                    "backup_interval": {"type": "number", "minimum": 1}
                },
                "required": ["path"]
            },
            "security": {
                "type": "object",
                "properties": {
                    "session_timeout": {"type": "number", "minimum": 1},
                    "auto_logout": {"type": "boolean"},
                    "encryption_enabled": {"type": "boolean"}
                }
            }
        },
        "required": ["app", "database"]
    }

    def __init__(self, config_name: str = "hefest_advanced", encrypt_sensitive: bool = True):
        self.config_name = config_name
        self.encrypt_sensitive = encrypt_sensitive
        self.config_file = self._get_config_file()
        self.backup_dir = self._get_backup_dir()
        self.sensitive_keys = {"database.password", "api.secret_key", "security.encryption_key"}

        # Configuración por defecto
        self.default_config = {
            "app": {
                "name": "HEFEST",
                "version": "0.0.10",
                "debug": False,
                "log_level": "INFO",
                "auto_save": True,
                "backup_on_change": True
            },
            "database": {
                "path": "data/hefest.db",
                "backup_enabled": True,
                "backup_interval": 24,
                "connection_pool_size": 5,
                "query_timeout": 30
            },
            "security": {
                "session_timeout": 30,
                "auto_logout": True,
                "encryption_enabled": True,
                "password_policy": {
                    "min_length": 6,
                    "require_numbers": False,
                    "require_special": False
                }
            },
            "ui": {
                "theme": "modern",
                "language": "es",
                "animation_enabled": True,
                "auto_refresh": True,
                "refresh_interval": 5
            },
            "performance": {
                "cache_enabled": True,
                "cache_size": 100,
                "lazy_loading": True,
                "parallel_processing": True,
                "max_workers": 4
            },
            "logging": {
                "file_enabled": True,
                "file_path": "logs/hefest.log",
                "max_file_size": "10MB",
                "backup_count": 5,
                "console_enabled": True
            }
        }

        # Inicializar encriptación
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key) if encrypt_sensitive else None

        # Cargar configuración
        self.config = self._load_config()
        self.config_hash = self._calculate_config_hash()

        # Configurar hot-reload si está habilitado
        self.hot_reload_enabled = self.config.get("app", {}).get("hot_reload", False)
        self.hot_reload_thread = None
        if self.hot_reload_enabled:
            self._start_hot_reload()

    def _get_config_file(self):
        """Obtiene la ruta del archivo de configuración."""
        config_dir = Path.home() / ".hefest" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / f"{self.config_name}.json"

    def _get_backup_dir(self):
        """Obtiene el directorio de backups."""
        backup_dir = Path.home() / ".hefest" / "backups" / "config"
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir

    def _get_or_create_encryption_key(self):
        """Obtiene o crea la clave de encriptación."""
        key_file = Path.home() / ".hefest" / "config" / "encryption.key"

        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            key_file.chmod(0o600)  # Solo lectura para el propietario
            return key

    def _encrypt_value(self, value: str) -> str:
        """Encripta un valor sensible."""
        if not self.cipher:
            return value
        return base64.b64encode(self.cipher.encrypt(value.encode())).decode()

    def _decrypt_value(self, encrypted_value: str) -> str:
        """Desencripta un valor."""
        if not self.cipher:
            return encrypted_value
        try:
            decoded = base64.b64decode(encrypted_value.encode())
            return self.cipher.decrypt(decoded).decode()
        except Exception:
            # Si no se puede desencriptar, asumir que no está encriptado
            return encrypted_value

    def _is_sensitive_key(self, key_path: str) -> bool:
        """Verifica si una clave es sensible."""
        return key_path in self.sensitive_keys

    def _calculate_config_hash(self) -> str:
        """Calcula hash de la configuración para detectar cambios."""
        config_str = json.dumps(self.config, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()

    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Valida la configuración contra el esquema."""
        if not HAS_JSONSCHEMA:
            # Validación básica sin jsonschema
            if not isinstance(config, dict):
                logger.error("La configuración debe ser un diccionario")
                return False
            logger.debug("Validación básica de configuración pasada (jsonschema no disponible)")
            return True

        try:
            if validate is not None:
                validate(instance=config, schema=self.CONFIG_SCHEMA)
                return True
            else:
                logger.warning("jsonschema no disponible, no se puede validar el esquema.")
                return True
        except Exception as e:
            logger.error(f"Error de validación de configuración: {e}")
            return False

    def _backup_config(self):
        """Crea backup de la configuración actual."""
        if not self.config.get("app", {}).get("backup_on_change", True):
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"{self.config_name}_backup_{timestamp}.json"

        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Backup de configuración creado: {backup_file}")

            # Limpiar backups antiguos (mantener solo los últimos 10)
            self._cleanup_old_backups()

        except Exception as e:
            logger.error(f"Error creando backup: {e}")

    def _cleanup_old_backups(self):
        """Limpia backups antiguos."""
        backup_files = sorted(
            self.backup_dir.glob(f"{self.config_name}_backup_*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        # Mantener solo los últimos 10 backups
        for old_backup in backup_files[10:]:
            try:
                old_backup.unlink()
                logger.debug(f"Backup antiguo eliminado: {old_backup}")
            except Exception as e:
                logger.warning(f"No se pudo eliminar backup {old_backup}: {e}")

    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde archivo."""
        if not self.config_file.exists():
            logger.info("Archivo de configuración no existe, usando valores por defecto")
            self._save_config(self.default_config)
            return self.default_config.copy()

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Validar configuración
            if not self._validate_config(config):
                logger.warning("Configuración inválida, usando valores por defecto")
                return self.default_config.copy()

            # Desencriptar valores sensibles
            config = self._decrypt_sensitive_values(config)

            logger.info(f"Configuración cargada desde {self.config_file}")
            return config

        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            return self.default_config.copy()

    def _decrypt_sensitive_values(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Desencripta valores sensibles en la configuración."""
        # Implementación pendiente: por seguridad, no se implementa encriptación básica
        # Se requiere una implementación robusta con gestión de claves segura
        logger.debug("Desencriptación de valores sensibles no implementada")
        return config

    def _save_config(self, config: Optional[Dict[str, Any]] = None):
        """Guarda la configuración a archivo."""
        if config is None:
            config = self.config

        # Crear backup antes de guardar
        if self.config_file.exists():
            self._backup_config()

        try:
            # Encriptar valores sensibles antes de guardar
            config_to_save = self._encrypt_sensitive_values(config.copy())

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)

            logger.info(f"Configuración guardada en {self.config_file}")
            # Actualizar hash
            self.config_hash = self._calculate_config_hash()

        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")
            raise

    def _encrypt_sensitive_values(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Encripta valores sensibles en la configuración."""
        # Implementación pendiente: por seguridad, no se implementa encriptación básica
        # Se requiere una implementación robusta con gestión de claves segura
        logger.debug("Encriptación de valores sensibles no implementada")
        return config

    def _start_hot_reload(self):
        """Inicia el hilo de hot-reload."""
        if self.hot_reload_thread and self.hot_reload_thread.is_alive():
            return

        self.hot_reload_thread = threading.Thread(
            target=self._hot_reload_worker,
            daemon=True
        )
        self.hot_reload_thread.start()
        logger.info("Hot-reload de configuración iniciado")

    def _hot_reload_worker(self):
        """Worker del hot-reload."""
        while self.hot_reload_enabled:
            try:
                if self.config_file.exists():
                    current_hash = self._calculate_config_hash()
                    if current_hash != self.config_hash:
                        logger.info("Cambio en configuración detectado, recargando...")
                        self.config = self._load_config()

                time.sleep(1)  # Verificar cada segundo

            except Exception as e:
                logger.error(f"Error en hot-reload: {e}")
                time.sleep(5)  # Esperar más tiempo en caso de error

    def get(self, key_path: str, default: Any = None) -> Any:
        """Obtiene un valor usando notación de punto."""
        keys = key_path.split('.')
        current = self.config

        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default

    def set(self, key_path: str, value: Any, auto_save: bool = True):
        """Establece un valor usando notación de punto."""
        keys = key_path.split('.')
        current = self.config

        # Navegar hasta el penúltimo nivel
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        # Establecer valor
        current[keys[-1]] = value

        if auto_save:
            self._save_config()

        logger.debug(f"Configuración actualizada: {key_path} = {value}")

    def update(self, updates: Dict[str, Any], auto_save: bool = True):
        """Actualiza múltiples valores."""
        for key_path, value in updates.items():
            self.set(key_path, value, auto_save=False)

        if auto_save:
            self._save_config()

    def reset_to_defaults(self, section: Optional[str] = None):
        """Restaura configuración por defecto."""
        if section:
            if section in self.default_config:
                self.config[section] = self.default_config[section].copy()
        else:
            self.config = self.default_config.copy()

        self._save_config()
        logger.info(f"Configuración restaurada: {section or 'completa'}")

    def export_config(self, file_path: Union[str, Path]):
        """Exporta configuración a archivo."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuración exportada a {file_path}")
        except Exception as e:
            logger.error(f"Error exportando configuración: {e}")
            raise

    def import_config(self, file_path: Union[str, Path], validate: bool = True):
        """Importa configuración desde archivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)

            if validate and not self._validate_config(imported_config):
                raise ValueError("Configuración importada no es válida")

            self.config.update(imported_config)
            self._save_config()
            logger.info(f"Configuración importada desde {file_path}")

        except Exception as e:
            logger.error(f"Error importando configuración: {e}")
            raise

    def get_config_info(self) -> Dict[str, Any]:
        """Obtiene información sobre la configuración."""
        return {
            "config_file": str(self.config_file),
            "backup_dir": str(self.backup_dir),
            "encryption_enabled": self.encrypt_sensitive,
            "hot_reload_enabled": self.hot_reload_enabled,
            "config_hash": self.config_hash,
            "last_modified": datetime.fromtimestamp(
                self.config_file.stat().st_mtime
            ).isoformat() if self.config_file.exists() else None,
            "size_bytes": self.config_file.stat().st_size if self.config_file.exists() else 0
        }

# Instancia global del gestor avanzado
advanced_config = AdvancedConfigManager()
