"""
Servicio de datos específico para el Dashboard Admin v3
Proporciona datos en tiempo real y cálculos de métricas administrativas
"""

import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

logger = logging.getLogger(__name__)


class AdminDataService(QObject):
    """Servicio para obtener y procesar datos administrativos"""
    
    # Señales para notificar cambios en los datos
    data_updated = pyqtSignal(dict)  # Emite dict con todas las métricas
    error_occurred = pyqtSignal(str)  # Emite mensaje de error
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_update = None
        self._cache = {}
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._fetch_data)
        
    def start_auto_update(self, interval_seconds: int = 30):
        """Inicia la actualización automática de datos"""
        logger.info(f"Iniciando actualización automática cada {interval_seconds} segundos")
        self._update_timer.start(interval_seconds * 1000)
        # Realizar primera actualización inmediatamente
        self._fetch_data()
        
    def stop_auto_update(self):
        """Detiene la actualización automática"""
        self._update_timer.stop()
        logger.info("Actualización automática detenida")
        
    def _fetch_data(self):
        """Obtiene datos actualizados (simulados por ahora)"""
        try:
            # Simular datos reales del sistema
            current_data = {
                'users_online': self._simulate_users_online(),
                'daily_revenue': self._simulate_daily_revenue(),
                'system_load': self._simulate_system_load(),
                'database_size': self._simulate_database_size(),
                'active_sessions': self._simulate_active_sessions(),
                'error_rate': self._simulate_error_rate(),
                'response_time': self._simulate_response_time(),
                'storage_used': self._simulate_storage_used(),
                'timestamp': datetime.now()
            }
            
            # Actualizar cache
            self._cache.update(current_data)
            self._last_update = datetime.now()
            
            # Emitir señal con los datos actualizados
            self.data_updated.emit(current_data)
            
            logger.debug(f"Datos actualizados: {len(current_data)} métricas")
            
        except Exception as e:
            error_msg = f"Error al obtener datos: {str(e)}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
    
    def _simulate_users_online(self) -> int:
        """Simula usuarios en línea con variación realista"""
        base = 45
        variation = random.randint(-10, 15)
        return max(0, base + variation)
    
    def _simulate_daily_revenue(self) -> float:
        """Simula ingresos diarios"""
        base = 2500.0
        variation = random.uniform(-500, 800)
        return max(0, base + variation)
    
    def _simulate_system_load(self) -> float:
        """Simula carga del sistema (0-100%)"""
        return random.uniform(15, 85)
    
    def _simulate_database_size(self) -> float:
        """Simula tamaño de la base de datos en MB"""
        base = 156.7
        growth = random.uniform(0, 2.5)
        return base + growth
    
    def _simulate_active_sessions(self) -> int:
        """Simula sesiones activas"""
        return random.randint(12, 28)
    
    def _simulate_error_rate(self) -> float:
        """Simula tasa de errores (0-100%)"""
        return random.uniform(0.1, 4.2)
    
    def _simulate_response_time(self) -> float:
        """Simula tiempo de respuesta en ms"""
        return random.uniform(120, 350)
    
    def _simulate_storage_used(self) -> float:
        """Simula almacenamiento usado (0-100%)"""
        return random.uniform(35, 75)
    
    def get_metric(self, metric_name: str) -> Optional[Any]:
        """Obtiene una métrica específica del cache"""
        return self._cache.get(metric_name)
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Obtiene todas las métricas del cache"""
        return self._cache.copy()
    
    def get_historical_data(self, metric_name: str, hours: int = 24) -> List[Dict]:
        """
        Simula datos históricos para gráficos
        En una implementación real, esto consultaría la base de datos
        """
        if metric_name not in self._cache:
            return []
        
        # Simular datos históricos
        historical = []
        now = datetime.now()
        current_value = self._cache[metric_name]
        
        for i in range(hours):
            timestamp = now - timedelta(hours=i)
            # Simular variación histórica basada en el valor actual
            if isinstance(current_value, (int, float)):
                variation = random.uniform(-0.2, 0.2)
                value = current_value * (1 + variation)
            else:
                value = current_value
                
            historical.append({
                'timestamp': timestamp,
                'value': value
            })
        
        return list(reversed(historical))
    
    def force_refresh(self):
        """Fuerza una actualización inmediata de los datos"""
        logger.info("Forzando actualización de datos")
        self._fetch_data()
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas resumen del sistema"""
        if not self._cache:
            return {}
        
        return {
            'total_users': self._cache.get('users_online', 0),
            'revenue_today': self._cache.get('daily_revenue', 0),
            'system_health': 'Saludable' if self._cache.get('system_load', 0) < 80 else 'Carga Alta',
            'last_update': self._last_update,
            'uptime': '99.8%',  # Simulado
            'active_modules': ['Auth', 'Dashboard', 'Inventory', 'TPV'],
        }
