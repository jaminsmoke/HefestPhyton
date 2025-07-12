"""
Sistema de Autenticacion Robusto para Hefest
============================================

Este modulo implementa un sistema de autenticacion de doble nivel:
1. Login basico: Acceso al programa
2. User Selector: Autenticacion por roles (Administrador/Manager/Empleado)

Caracteristicas:
- Gestion segura de usuarios y roles
- Autenticacion por PIN
- Sistema de sesiones
- Logging de auditoria
- Validacion de permisos
"""

import json
import logging
import os
import sqlite3
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from core.hefest_data_models import Role, User

from .base_service import BaseService

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Excepcion para errores de autenticacion"""


class PermissionError(Exception):
    """Excepcion para errores de permisos"""


@dataclass
class SessionInfo:
    """Informacion de la sesion actual"""

    user_id: int
    username: str
    role: Role
    login_time: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    session_token: str = ""

    def is_expired(self, timeout_seconds: int = 3600) -> bool:
        """Verifica si la sesion ha expirado (por defecto 1 hora)"""
        return (time.time() - self.last_activity) > timeout_seconds

    def update_activity(self) -> None:
        """Actualiza el timestamp de la ultima actividad"""
        self.last_activity = time.time()


class AuthService(BaseService):
    """
    Servicio de autenticacion principal

    Maneja:
    - Autenticacion de usuarios (login basico + selector de roles)
    - Gestion de sesiones
    - Verificacion de permisos
    - Usuarios por defecto del sistema
    """

    # Import para type hints
    from typing import TYPE_CHECKING, Any, Optional

    if TYPE_CHECKING:
        from data.db_manager import DatabaseManager

    def __init__(self, db_manager: Optional["DatabaseManager"] = None):
        """
        Inicializa el servicio de autenticacion

        Args:
            db_manager: Gestor de base de datos (opcional)
        """
        super().__init__(db_manager)
        self.current_session: Optional[SessionInfo] = None
        self._users_cache: Dict[int, User] = {}
        self._initialize_default_users()

        self.logger.info("AuthService inicializado correctamente")

    def get_service_name(self) -> str:
        """Retorna el nombre de este servicio"""
        return "AuthService"

    def _initialize_default_users(self) -> None:
        """Inicializa los usuarios por defecto del sistema"""
        default_pin = self._get_default_pin()
        
        self.default_users = [
            User(
                id=1,
                username="admin",
                name="Administrador",
                role=Role.ADMIN,
                password=default_pin,  # PIN desde configuración
                email="admin@hefest.com",
                phone="",
                is_active=True,
            ),
            User(
                id=2,
                username="manager",
                name="Manager",
                role=Role.MANAGER,
                password=default_pin,  # PIN desde configuración
                email="manager@hefest.com",
                phone="",
                is_active=True,
            ),
            User(
                id=3,
                username="empleado",
                name="Empleado",
                role=Role.EMPLOYEE,
                password=default_pin,  # PIN desde configuración
                email="empleado@hefest.com",
                phone="",
                is_active=True,
            ),
        ]

        # Llenar cache con usuarios por defecto
        for user in self.default_users:
            if user.id is not None:
                self._users_cache[user.id] = user

        logger.info(f"Inicializados {len(self.default_users)} usuarios por defecto")

    @property
    def users(self) -> List[User]:
        """Retorna la lista de todos los usuarios disponibles"""
        if self.db_manager:
            try:
                # Intentar cargar desde BD si esta disponible
                return self._load_users_from_db()
            except Exception as e:
                logger.warning(f"Error cargando usuarios desde BD: {e}")
                logger.info("Usando usuarios por defecto")

        return self.default_users

    @property
    def current_user(self) -> Optional[User]:
        """Retorna el usuario actual autenticado"""
        if self.current_session:
            return self._users_cache.get(self.current_session.user_id)
        return None

    @property
    def is_authenticated(self) -> bool:
        """Verifica si hay un usuario autenticado"""
        return (
            self.current_session is not None and not self.current_session.is_expired()
        )

    def _load_users_from_db(self) -> List[User]:
        """Carga usuarios desde la base de datos"""
        if not self.db_manager:
            return self.default_users

        try:
            conn = self.db_manager.get_connection()  # type: ignore
            cursor: sqlite3.Cursor = conn.cursor()  # type: ignore
            cursor.execute(
                """
                SELECT id, username, name, role, password, email, phone, is_active
                FROM users WHERE is_active = 1
            """
            )

            db_users: List[Any] = cursor.fetchall()  # type: ignore
            users: List[User] = []

            for db_user in db_users:
                try:
                    # Si es tupla, convertir a dict para tipado robusto
                    if isinstance(db_user, dict):
                        row: Dict[str, Any] = db_user
                    else:
                        row: Dict[str, Any] = {
                            "id": db_user[0],
                            "username": db_user[1],
                            "name": db_user[2],
                            "role": db_user[3],
                            "password": db_user[4],
                            "email": db_user[5],
                            "phone": db_user[6],
                            "is_active": db_user[7],
                        }
                    role = Role(row["role"]) if row["role"] else Role.EMPLOYEE
                    user = User(
                        id=int(row["id"]) if row["id"] is not None else None,
                        username=str(row["username"]),
                        name=str(row["name"]),
                        role=role,
                        password=str(row["password"]),
                        email=str(row["email"]),
                        phone=str(row["phone"]),
                        is_active=bool(row["is_active"]),
                    )
                    users.append(user)
                    if user.id is not None:
                        self._users_cache[user.id] = user

                except (ValueError, TypeError) as e:
                    logger.error(f"Error procesando usuario {db_user}: {e}")
                    continue

            if not users:
                logger.warning("No se encontraron usuarios en BD, usando por defecto")
                return self.default_users

            logger.info(f"Cargados {len(users)} usuarios desde BD")
            return users

        except Exception as e:
            logger.error(f"Error cargando usuarios desde BD: {e}")
            return self.default_users

    def authenticate_basic_login(self, username: str, password: str) -> bool:
        """
        Autenticacion basica para acceso al programa

        Args:
            username: Nombre de usuario
            password: Contraseña

        Returns:
            True si la autenticacion es exitosa
        """  # Credenciales básicas del sistema
        basic_credentials = {
            "hefest": "admin",
            "admin": "1234",  # Credencial principal de administrador
            "usuario": "1234",
            "demo": "demo",
            "test": "test",
        }

        # Normalizar las entradas (eliminar espacios y convertir a minúsculas)
        username_clean = username.strip().lower()
        password_clean = password.strip()

        logger.debug(
            f"Intento de login: usuario='{username_clean}', credenciales disponibles: {list(basic_credentials.keys())}"
        )

        if (
            username_clean in basic_credentials
            and basic_credentials[username_clean] == password_clean
        ):
            logger.info(f"Login basico exitoso para usuario: {username_clean}")
            return True

        logger.warning(
            f"Intento de login basico fallido para usuario: {username_clean}"
        )
        logger.debug(
            f"Contraseña esperada: '{basic_credentials.get(username_clean, 'USUARIO_NO_EXISTE')}'"
        )
        return False

    def login(self, user_id: int, pin: str) -> bool:
        """
        Autenticacion especifica por usuario/rol con PIN

        Args:
            user_id: ID del usuario
            pin: PIN del usuario

        Returns:
            True si la autenticacion es exitosa
        """
        try:
            # Buscar usuario
            user = self.get_user_by_id(user_id)
            if not user:
                logger.warning(f"Intento de login con usuario inexistente: {user_id}")
                return False

            # Verificar que el usuario este activo
            if not user.is_active:
                logger.warning(
                    f"Intento de login con usuario inactivo: {user.username}"
                )
                return False

            # Verificar PIN (usando password como PIN)
            if not self._verify_pin(user, pin):
                logger.warning(f"PIN incorrecto para usuario: {user.username}")
                return False

            # Crear sesion solo si user.id no es None
            if user.id is not None:
                self.current_session = SessionInfo(
                    user_id=user.id,
                    username=user.username,
                    role=user.role,
                    session_token=self._generate_session_token(),
                )

                logger.info(
                    f"Login exitoso para usuario: {user.username} (Role: {user.role.value})"
                )
                return True
            else:
                logger.error(f"Usuario {user.username} tiene ID None")
                return False

        except Exception as e:
            logger.error(f"Error durante login: {e}")
            return False

    def logout(self) -> None:
        """Cierra la sesion actual"""
        if self.current_session:
            logger.info(f"Logout para usuario: {self.current_session.username}")
            self.current_session = None
        else:
            logger.warning("Intento de logout sin sesion activa")

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID

        Args:
            user_id: ID del usuario

        Returns:
            Usuario encontrado o None
        """
        # Buscar en cache primero
        if user_id in self._users_cache:
            return self._users_cache[user_id]

        # Buscar en la lista de usuarios
        for user in self.users:
            if user.id == user_id:
                self._users_cache[user_id] = user
                return user

        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Obtiene un usuario por su username

        Args:
            username: Nombre de usuario

        Returns:
            Usuario encontrado o None
        """
        for user in self.users:
            if user.username == username:
                return user
        return None

    def _verify_pin(self, user: User, pin: str) -> bool:
        """
        Verifica el PIN del usuario

        Args:
            user: Usuario a verificar
            pin: PIN ingresado

        Returns:
            True si el PIN es correcto"""
        # Por compatibilidad, usamos password como PIN
        return user.password == pin

    def _generate_session_token(self) -> str:
        """Genera un token unico para la sesion"""
        import uuid

        return str(uuid.uuid4())

    def has_permission(self, permission: str) -> bool:
        """
        Verifica si el usuario actual tiene un permiso especifico

        Args:
            permission: Permiso a verificar (string o Role)

        Returns:
            True si tiene el permiso
        """
        if not self.is_authenticated:
            return False

        user = self.current_user
        if not user:
            return False

        # Si se pasa un Role, verificar jerarquía de roles
        if isinstance(permission, Role):
            return self.has_role_permission(permission)
        # Mapeo de permisos por rol (para strings)
        permissions_map = {
            Role.ADMIN: [
                "all",  # Acceso total
                "user_management",
                "system_settings",
                "reports",
                "inventory",
                "sales",
                "audit",
                "hospederia",
                "dashboard",
                "dashboard_access",
                "inventory_access",
                "admin_access",
            ],
            Role.MANAGER: [
                "reports",
                "inventory",
                "sales",
                "audit",
                "hospederia",
                "dashboard",
                "dashboard_access",
                "inventory_access",
                "user_view",  # Solo ver usuarios, no editar
            ],
            Role.EMPLOYEE: [
                "sales",
                "inventory_view",
                "hospederia",
                "dashboard",
                "dashboard_access",
                "basic_operations",  # Operaciones básicas
            ],
        }

        user_permissions = permissions_map.get(user.role, [])

        # Admin tiene acceso a todo
        if "all" in user_permissions:
            return True

        return permission in user_permissions

    def has_role_permission(self, required_role: Role) -> bool:
        """
        Verifica si el usuario actual tiene el rol requerido o uno superior

        Args:
            required_role: Rol mínimo requerido

        Returns:
            True si tiene el rol requerido o superior
        """
        if not self.is_authenticated:
            return False

        user = self.current_user
        if not user:
            return False

        # Jerarquía de roles: ADMIN > MANAGER > EMPLOYEE
        role_hierarchy = {Role.EMPLOYEE: 1, Role.MANAGER: 2, Role.ADMIN: 3}

        user_level = role_hierarchy.get(user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        return user_level >= required_level

    def require_permission(self, permission: str) -> None:
        """
        Decorador/funcion que requiere un permiso especifico

        Args:
            permission: Permiso requerido

        Raises:
            PermissionError: Si no tiene el permiso
        """
        if not self.has_permission(permission):
            current_role = (
                self.current_user.role.value if self.current_user else "Sin autenticar"
            )
            raise PermissionError(
                f"Acceso denegado. Rol actual: {current_role}, Permiso requerido: {permission}"
            )

    def update_activity(self) -> None:
        """Actualiza la actividad de la sesion currente"""
        if self.current_session:
            self.current_session.update_activity()

    def get_session_info(self) -> Dict[str, Any]:
        """
        Retorna informacion de la sesion actual

        Returns:
            Diccionario con informacion de la sesion
        """
        if not self.current_session:
            return {"authenticated": False}

        user = self.current_user
        return {
            "authenticated": True,
            "user_id": self.current_session.user_id,
            "username": self.current_session.username,
            "user_name": user.name if user else "",
            "role": self.current_session.role.value,
            "login_time": self.current_session.login_time,
            "last_activity": self.current_session.last_activity,
            "session_token": self.current_session.session_token,
        }

    def _load_auth_config(self) -> Dict[str, Any]:
        """Carga la configuración de autenticación desde config/default.json"""
        try:
            config_path = os.path.join("config", "default.json")
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("authentication", {})
            return {}
        except Exception as e:
            logger.warning(f"Error cargando configuración de auth: {e}")
            return {}

    def _get_default_pin(self) -> str:
        """Obtiene el PIN por defecto desde configuración"""
        auth_config = self._load_auth_config()
        return auth_config.get("default_pin", "9999")  # Fallback seguro

    # Métodos de conveniencia para verificar accesos específicos
    def can_access_dashboard(self) -> bool:
        """Verifica si el usuario puede acceder al dashboard"""
        return self.has_permission("dashboard_access") or self.has_permission(
            "dashboard"
        )

    def can_access_inventory(self) -> bool:
        """Verifica si el usuario puede acceder al inventario"""
        return self.has_permission("inventory_access") or self.has_permission(
            "inventory"
        )

    def can_access_admin_panel(self) -> bool:
        """Verifica si el usuario puede acceder al panel de administración"""
        return self.has_permission("admin_access") or self.has_permission(
            "user_management"
        )

    def can_manage_users(self) -> bool:
        """Verifica si el usuario puede gestionar otros usuarios"""
        return self.has_permission("user_management")

    def can_view_reports(self) -> bool:
        """Verifica si el usuario puede ver reportes"""
        return self.has_permission("reports")

    def can_access_hospederia(self) -> bool:
        """Verifica si el usuario puede acceder al módulo de hospedería"""
        return self.has_permission("hospederia")


# Instancia global del servicio de autenticacion
_auth_service_instance = None


def get_auth_service() -> AuthService:
    """
    Obtiene la instancia global del servicio de autenticacion

    Returns:
        Instancia del AuthService
    """
    global _auth_service_instance
    if _auth_service_instance is None:
        _auth_service_instance = AuthService()
    return _auth_service_instance
