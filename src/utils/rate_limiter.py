"""
Rate Limiter - Hefest Security
Implementa límites de intentos de login y operaciones críticas
"""

import time
import os
from typing import Dict, Optional
from collections import defaultdict, deque


class RateLimiter:
    """Rate limiter para prevenir ataques de fuerza bruta"""
    
    def __init__(self):
        """TODO: Add docstring"""
        # Configuración desde variables de entorno
        self.max_attempts = int(os.getenv('MAX_LOGIN_ATTEMPTS', '3'))
        self.lockout_duration = int(os.getenv('LOCKOUT_DURATION', '300'))  # 5 minutos
        self.window_duration = int(os.getenv('RATE_LIMIT_WINDOW', '60'))   # 1 minuto
        
        # Almacenamiento en memoria (para producción usar Redis/DB)
        self.attempts: Dict[str, deque] = defaultdict(deque)
        self.lockouts: Dict[str, float] = {}
    
    def is_locked(self, identifier: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si un identificador está bloqueado"""
        if identifier in self.lockouts:
            if time.time() < self.lockouts[identifier]:
                return True
            else:
                # Lockout expirado, limpiar
                del self.lockouts[identifier]
                self.attempts[identifier].clear()
        return False
    
    def record_attempt(self, identifier: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Registra un intento y retorna True si está permitido
        False si excede el límite
        """
        _ = time.time()
        
        # Verificar si está bloqueado
        if self.is_locked(identifier):
            return False
        
        # Limpiar intentos antiguos
        attempts = self.attempts[identifier]
        while attempts and attempts[0] < current_time - self.window_duration:
            attempts.popleft()
        
        # Agregar intento actual
        attempts.append(current_time)
        
        # Verificar límite
        if len(attempts) > self.max_attempts:
            # Bloquear
            self.lockouts[identifier] = current_time + self.lockout_duration
            return False
        
        return True
    
    def get_remaining_attempts(self, identifier: str) -> int:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene intentos restantes"""
        if self.is_locked(identifier):
            return 0
        
        _ = time.time()
        attempts = self.attempts[identifier]
        
        # Limpiar intentos antiguos
        while attempts and attempts[0] < current_time - self.window_duration:
            attempts.popleft()
        
        return max(0, self.max_attempts - len(attempts))
    
    def get_lockout_remaining(self, identifier: str) -> int:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene tiempo restante de bloqueo en segundos"""
        if identifier in self.lockouts:
            remaining = int(self.lockouts[identifier] - time.time())
            return max(0, remaining)
        return 0
    
    def reset_attempts(self, identifier: str):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Resetea intentos (para login exitoso)"""
        if identifier in self.attempts:
            self.attempts[identifier].clear()
        if identifier in self.lockouts:
            del self.lockouts[identifier]


# Instancia global
rate_limiter = RateLimiter()