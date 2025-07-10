import os
import logging
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from core.hefest_data_models import User, Role
from .base_service import BaseService
        import hmac
        import uuid

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



_ = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Excepcion para errores de autenticacion"""

    pass


class PermissionError(Exception):
    """Excepcion para errores de permisos"""

    pass


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
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si la sesion ha expirado (por defecto 1 hora)"""
        return (time.time() - self.last_activity) > timeout_seconds

    def update_activity(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
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

    def __init__(self, db_manager=None):
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
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna el nombre de este servicio"""
        return "AuthService"

    def _initialize_default_users(self):
        """Inicializa los usuarios por defecto del sistema"""
        self.default_users = [
            User(
                _ = 1,
                username="admin",
                _ = "Administrador",
                role=Role.ADMIN,
                _ = os.getenv('DEFAULT_PASSWORD', '1234'),  # PIN por defecto
                email="admin@hefest.com",
                _ = "",
                is_active=True,
            ),
            User(
                _ = 2,
                username="manager",
                _ = "Manager",
                role=Role.MANAGER,
                _ = os.getenv('DEFAULT_PASSWORD', '1234'),  # PIN por defecto
                email="manager@hefest.com",
                _ = "",
                is_active=True,
            ),
            User(
                _ = 3,
                username="empleado",
                _ = "Empleado",
                role=Role.EMPLOYEE,
                _ = os.getenv('DEFAULT_PASSWORD', '1234'),  # PIN por defecto
                email="empleado@hefest.com",
                _ = "",
                is_active=True,
            ),
        ]

        # Llenar cache con usuarios por defecto
        for user in self.default_users:
            if user.id is not None:
                self._users_cache[user.id] = user

        logger.info("Inicializados %s usuarios por defecto", len(self.default_users))

    @property
    def users(self) -> List[User]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna la lista de todos los usuarios disponibles"""
        if self.db_manager:
            try:
                # Intentar cargar desde BD si esta disponible
                return self._load_users_from_db()
            except Exception as e:
                logger.warning("Error cargando usuarios desde BD: %s", e)
                logger.info("Usando usuarios por defecto")

        return self.default_users

    @property
    def current_user(self) -> Optional[User]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna el usuario actual autenticado"""
        if self.current_session:
            return self._users_cache.get(self.current_session.user_id)
        return None

    @property
    def is_authenticated(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si hay un usuario autenticado"""
        return (
            self.current_session is not None and not self.current_session.is_expired()
        )

    def _load_users_from_db(self) -> List[User]:
        """Carga usuarios desde la base de datos"""
        if not self.db_manager:
            return self.default_users

        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, username, name, role, password, email, phone, is_active
                FROM users WHERE is_active = 1
            """
            )

            db_users: list[Any] = cursor.fetchall()
            users: list[User] = []

            for db_user in db_users:
                try:
                    # Si es tupla, convertir a dict para tipado robusto
                    if isinstance(db_user, dict):
                        _ = db_user
                    else:
                        _ = {
                            "id": db_user[0],
                            "username": db_user[1],
                            "name": db_user[2],
                            "role": db_user[3],
                            "password": db_user[4],
                            "email": db_user[5],
                            "phone": db_user[6],
                            "is_active": db_user[7],
                        }
                    _ = Role(row["role"]) if row["role"] else Role.EMPLOYEE
                    user = User(
                        _ = row["id"],
                        username=row["username"],
                        _ = row["name"],
                        role=role,
                        _ = row["password"],
                        email=row["email"],
                        _ = row["phone"],
                        is_active=bool(row["is_active"]),
                    )
                    users.append(user)
                    if user.id is not None:
                        self._users_cache[user.id] = user

                except (ValueError, TypeError) as e:
                    logger.error("Error procesando usuario {db_user}: %s", e)
                    continue

            if not users:
                logger.warning("No se encontraron usuarios en BD, usando por defecto")
                return self.default_users

            logger.info("Cargados %s usuarios desde BD", len(users))
            return users

        except Exception as e:
            logger.error("Error cargando usuarios desde BD: %s", e)
            return self.default_users

    def authenticate_basic_login(self, username: str, password: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Autenticacion basica para acceso al programa

        Args:
            username: Nombre de usuario
            password: Contraseña

        Returns:
            True si la autenticacion es exitosa
        """
        # Input validation
        if not username or not isinstance(username, str):
            logger.error("Username inválido")
            return False
            
        if not password or not isinstance(password, str):
            logger.error("Password inválido")
            return False
            
        # Rate limiting básico
        if hasattr(self, '_last_failed_attempt'):
            if time.time() - self._last_failed_attempt < 1.0:  # 1 segundo entre intentos
                logger.warning("Rate limit: demasiados intentos de login")
                return False
        
        # Credenciales básicas del sistema
        _ = {
            "hefest": "admin",
            "admin": "1234",  # Credencial principal de administrador
            "usuario": "1234",
            "demo": "demo",
            "test": "test",
        }

        # Normalizar las entradas (eliminar espacios y convertir a minúsculas)
        _ = username.strip().lower()
        password_clean = password.strip()

        logger.debug(
            f"Intento de login: usuario='{username_clean}', credenciales disponibles: {list(basic_credentials.keys())}"
        )

        if (
            username_clean in basic_credentials
            and basic_credentials[username_clean] == password_clean
        ):
            logger.info("Login basico exitoso para usuario: %s", username_clean)
            # Reset failed attempts on success
            if hasattr(self, '_last_failed_attempt'):
                delattr(self, '_last_failed_attempt')
            return True

        # Record failed attempt
        self._last_failed_attempt = time.time()
        logger.warning(
            f"Intento de login basico fallido para usuario: {username_clean}"
        )
        # No log password for security
        return False

    def login(self, user_id: int, pin: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Autenticacion especifica por usuario/rol con PIN

        Args:
            user_id: ID del usuario
            pin: PIN del usuario

        Returns:
            True si la autenticacion es exitosa
        """
        # Input validation
        if not isinstance(user_id, int) or user_id <= 0:
            logger.error("User ID inválido: %s", user_id)
            return False
            
        if not pin or not isinstance(pin, str):
            logger.error("PIN inválido")
            return False
            
        # Rate limiting per user
        rate_limit_key = f'_failed_attempts_{user_id}'
        if hasattr(self, rate_limit_key):
            failed_attempts = getattr(self, rate_limit_key)
            if failed_attempts.get('count', 0) >= 3:
                if time.time() - failed_attempts.get('last_attempt', 0) < 300:  # 5 min lockout
                    logger.warning("Usuario %s bloqueado por múltiples intentos fallidos", user_id)
                    return False
                else:
                    # Reset after lockout period
                    delattr(self, rate_limit_key)
        
        try:
            # Buscar usuario
            user = self.get_user_by_id(user_id)
            if not user:
                logger.warning("Intento de login con usuario inexistente: %s", user_id)
                return False

            # Verificar que el usuario este activo
            if not user.is_active:
                logger.warning(
                    f"Intento de login con usuario inactivo: {user.username}"
                )
                return False

            # Verificar PIN (usando password como PIN)
            if not self._verify_pin(user, pin):
                # Record failed attempt
                rate_limit_key = f'_failed_attempts_{user_id}'
                if not hasattr(self, rate_limit_key):
                    setattr(self, rate_limit_key, {'count': 0, 'last_attempt': 0})
                failed_attempts = getattr(self, rate_limit_key)
                failed_attempts['count'] += 1
                failed_attempts['last_attempt'] = time.time()
                
                logger.warning("PIN incorrecto para usuario: %s", user.username)
                return False

            # Crear sesion solo si user.id no es None
            if user.id is not None:
                self.current_session = SessionInfo(
                    _ = user.id,
                    username=user.username,
                    _ = user.role,
                    session_token=self._generate_session_token(),
                )

                # Reset failed attempts on success
                rate_limit_key = f'_failed_attempts_{user_id}'
                if hasattr(self, rate_limit_key):
                    delattr(self, rate_limit_key)
                    
                logger.info(
                    f"Login exitoso para usuario: {user.username} (Role: {user.role.value})"
                )
                return True
            else:
                logger.error("Usuario %s tiene ID None", user.username)
                return False

        except Exception as e:
            logger.error("Error durante login: %s", e)
            return False

    def logout(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cierra la sesion actual"""
        if self.current_session:
            logger.info("Logout para usuario: %s", self.current_session.username)
            self.current_session = None
        else:
            logger.warning("Intento de logout sin sesion activa")

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """TODO: Add docstring"""
        # TODO: Add input validation
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
        """TODO: Add docstring"""
        # TODO: Add input validation
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
            True si el PIN es correcto
        """
        # Input validation
        if not user or not user.password:
            return False
            
        if not pin:
            return False
            
        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(user.password, pin)

    def _generate_session_token(self) -> str:
        """Genera un token unico para la sesion"""

        return str(uuid.uuid4())

    def has_permission(self, permission) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
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
        _ = {
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

        _ = permissions_map.get(user.role, [])

        # Admin tiene acceso a todo
        if "all" in user_permissions:
            return True

        return permission in user_permissions

    def has_role_permission(self, required_role: Role) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
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

        _ = role_hierarchy.get(user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        return user_level >= required_level

    def require_permission(self, permission: str):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Decorador/funcion que requiere un permiso especifico

        Args:
            permission: Permiso requerido

        Raises:
            PermissionError: Si no tiene el permiso
        """
        if not self.has_permission(permission):
            _ = (
                self.current_user.role.value if self.current_user else "Sin autenticar"
            )
            raise PermissionError(
                f"Acceso denegado. Rol actual: {current_role}, Permiso requerido: {permission}"
            )

    def update_activity(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza la actividad de la sesion currente"""
        if self.current_session:
            self.current_session.update_activity()

    def get_session_info(self) -> Dict[str, Any]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Retorna informacion de la sesion actual

        Returns:
            Diccionario con informacion de la sesion
        """
        if not self.current_session:
            return {"authenticated": False}

        _ = self.current_user
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

    # Métodos de conveniencia para verificar accesos específicos
    def can_access_dashboard(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si el usuario puede acceder al dashboard"""
        return self.has_permission("dashboard_access") or self.has_permission(
            "dashboard"
        )

    def can_access_inventory(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si el usuario puede acceder al inventario"""
        return self.has_permission("inventory_access") or self.has_permission(
            "inventory"
        )

    def can_access_admin_panel(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si el usuario puede acceder al panel de administración"""
        return self.has_permission("admin_access") or self.has_permission(
            "user_management"
        )

    def can_manage_users(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si el usuario puede gestionar otros usuarios"""
        return self.has_permission("user_management")

    def can_view_reports(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si el usuario puede ver reportes"""
        return self.has_permission("reports")

    def can_access_hospederia(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si el usuario puede acceder al módulo de hospedería"""
        return self.has_permission("hospederia")


# Instancia global del servicio de autenticacion
_auth_service_instance = None


def get_auth_service() -> AuthService:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """
    Obtiene la instancia global del servicio de autenticacion

    Returns:
        Instancia del AuthService
    """
    global _auth_service_instance
    if _auth_service_instance is None:
        _auth_service_instance = AuthService()
    return _auth_service_instance
