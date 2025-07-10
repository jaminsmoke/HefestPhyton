"""
Servicio de auditoría para el sistema Hefest.
Registra y permite consultar acciones realizadas por los usuarios.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from core.hefest_data_models import User
import logging


logger = logging.getLogger(__name__)


class AuditService:
    _logs: List[Dict[str, Any]] = []

    @classmethod
    def log(
        cls,
        action: str,
        user: Optional[User] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Registra una acción en el sistema de auditoría"""
        entry = {
            "timestamp": datetime.now(),
            "action": action,
            "user": user.name if user else "Sistema",
            "user_id": user.id if user else None,
            "role": user.role.value if user else None,
            "details": details or {},
        }
        cls._logs.append(entry)
        logger.info(f"AUDIT: {entry}")

        # En producción, guardar en base de datos aquí

    @classmethod
    def get_recent_logs(cls, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtiene los registros más recientes"""
        return sorted(cls._logs, key=lambda x: x["timestamp"], reverse=True)[:limit]

    @classmethod
    def log_access_denied(cls, user: Optional[User], module_id: str):
        """Registra un evento de acceso denegado"""
        cls.log(action="Acceso Denegado", user=user, details={"module_id": module_id})
