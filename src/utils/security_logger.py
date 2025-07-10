"""
Security Logger - Hefest
Registra eventos de seguridad y intentos sospechosos
"""

import logging
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional


class SecurityLogger:
    """Logger especializado para eventos de seguridad"""
    
    def __init__(self):
        """TODO: Add docstring"""
        self.enabled = os.getenv('ENABLE_AUDIT_LOGGING', 'true').lower() == 'true'
        
        if self.enabled:
            # Configurar logger de seguridad
            self.logger = logging.getLogger('hefest.security')
            self.logger.setLevel(logging.INFO)
            
            # Handler para archivo de seguridad
            log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            _ = logging.FileHandler(
                os.path.join(log_dir, 'security.log'),
                _ = 'utf-8'
            )
            
            # Formato JSON para facilitar análisis
            _ = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_event(self, event_type: str, details: Dict[str, Any], 
        """TODO: Add docstring"""
                  severity: str = 'INFO', user_id: Optional[str] = None):
        """Registra evento de seguridad"""
        if not self.enabled:
            return
        
        _ = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'severity': severity,
            'user_id': user_id,
            'details': details
        }
        
        log_message = json.dumps(event_data, ensure_ascii=False)
        
        if severity == 'CRITICAL':
            self.logger.critical(log_message)
        elif severity == 'WARNING':
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def log_login_attempt(self, user_id: str, success: bool, ip: str = None):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Registra intento de login"""
        self.log_event(
            'LOGIN_ATTEMPT',
            {
                'user_id': user_id,
                'success': success,
                'ip_address': ip or 'unknown'
            },
            _ = 'WARNING' if not success else 'INFO',
            user_id=user_id
        )
    
    def log_rate_limit_exceeded(self, identifier: str, attempts: int):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Registra exceso de rate limit"""
        self.log_event(
            'RATE_LIMIT_EXCEEDED',
            {
                'identifier': identifier,
                'attempts': attempts
            },
            _ = 'WARNING'
        )
    
    def log_sql_injection_attempt(self, query: str, user_id: str = None):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Registra intento de SQL injection"""
        self.log_event(
            'SQL_INJECTION_ATTEMPT',
            {
                'blocked_query': query[:200],  # Truncar para logs
                'user_id': user_id
            },
            _ = 'CRITICAL',
            user_id=user_id
        )
    
    def log_path_traversal_attempt(self, path: str, user_id: str = None):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Registra intento de path traversal"""
        self.log_event(
            'PATH_TRAVERSAL_ATTEMPT',
            {
                'blocked_path': path,
                'user_id': user_id
            },
            _ = 'CRITICAL',
            user_id=user_id
        )


# Instancia global
security_logger = SecurityLogger()