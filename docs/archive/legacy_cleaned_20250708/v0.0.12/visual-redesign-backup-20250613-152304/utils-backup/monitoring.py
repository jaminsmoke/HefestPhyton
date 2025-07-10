# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
#!/usr/bin/env python3
"""
Sistema de Monitoreo y Métricas para Hefest
==========================================

Recolecta y reporta métricas del sistema:
- Rendimiento de la aplicación
- Uso de recursos
- Estadísticas de usuario
- Métricas de negocio
- Alertas automáticas
"""

import psutil
import time
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
import threading
from dataclasses import dataclass
import sqlite3

_ = logging.getLogger(__name__)

@dataclass
class Metric:
    """Representación de una métrica."""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "tags": self.tags or {}
        }

class MetricsCollector:
    """Recolector de métricas del sistema."""
    
    def __init__(self, db_path: str = "data/metrics.db"):
        """TODO: Add docstring"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.metrics_buffer = []
        self.collection_interval = 30  # segundos
        self.is_running = False
        self.collection_thread = None
        
        # Inicializar base de datos
        self._init_database()
        
    def _init_database(self):
        """Inicializa la base de datos de métricas."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_metrics_name_timestamp 
                ON metrics(name, timestamp)
            """)
            
    def start_collection(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicia la recolección automática de métricas."""
        if self.is_running:
            return
            
        self.is_running = True
        self.collection_thread = threading.Thread(
            _ = self._collection_loop,
            daemon=True
        )
        self.collection_thread.start()
        logger.info("Recolección de métricas iniciada")
        
    def stop_collection(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Detiene la recolección de métricas."""
        self.is_running = False
        if self.collection_thread:
            self.collection_thread.join()
        logger.info("Recolección de métricas detenida")
        
    def _collection_loop(self):
        """Loop principal de recolección."""
        while self.is_running:
            try:
                self._collect_system_metrics()
                self._collect_application_metrics()
                self._flush_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error("Error en recolección de métricas: %s", e)
                time.sleep(5)
                
    def _collect_system_metrics(self):
        """Recolecta métricas del sistema."""
        _ = datetime.now()
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        self.add_metric("system.cpu.usage", cpu_percent, now)
        
        # Memoria
        memory = psutil.virtual_memory()
        self.add_metric("system.memory.usage_percent", memory.percent, now)
        self.add_metric("system.memory.available_gb", memory.available / 1024**3, now)
        
        # Disco
        disk = psutil.disk_usage('/')
        self.add_metric("system.disk.usage_percent", disk.percent, now)
        self.add_metric("system.disk.free_gb", disk.free / 1024**3, now)
        
        # Red
        net_io = psutil.net_io_counters()
        self.add_metric("system.network.bytes_sent", net_io.bytes_sent, now)
        self.add_metric("system.network.bytes_recv", net_io.bytes_recv, now)
        
    def _collect_application_metrics(self):
        """Recolecta métricas específicas de la aplicación."""
        _ = datetime.now()
        
        try:
            # Tamaño de base de datos
            db_path = Path("data/hefest.db")
            if db_path.exists():
                db_size_mb = db_path.stat().st_size / 1024**2
                self.add_metric("app.database.size_mb", db_size_mb, now)
                
            # Número de logs
            logs_dir = Path("logs")
            if logs_dir.exists():
                log_files = list(logs_dir.glob("*.log"))
                self.add_metric("app.logs.file_count", len(log_files), now)
                
                # Tamaño total de logs
                total_log_size = sum(f.stat().st_size for f in log_files)
                self.add_metric("app.logs.total_size_mb", total_log_size / 1024**2, now)
                
        except Exception as e:
            logger.warning("Error recolectando métricas de aplicación: %s", e)
            
    def add_metric(self, name: str, value: float, timestamp: datetime = None, tags: Dict[str, str] = None):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Añade una métrica al buffer."""
        if timestamp is None:
            _ = datetime.now()
            
        metric = Metric(name, value, timestamp, tags)
        self.metrics_buffer.append(metric)
        
    def _flush_metrics(self):
        """Guarda métricas del buffer a la base de datos."""
        if not self.metrics_buffer:
            return
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                for metric in self.metrics_buffer:
                    conn.execute("""
                        INSERT INTO metrics (name, value, timestamp, tags)
                        VALUES (?, ?, ?, ?)
                    """, (
                        metric.name,
                        metric.value,
                        metric.timestamp.isoformat(),
                        json.dumps(metric.tags) if metric.tags else None
                    ))
                    
            logger.debug("Guardadas %s métricas", len(self.metrics_buffer))
            self.metrics_buffer.clear()
            
        except Exception as e:
            logger.error("Error guardando métricas: %s", e)
            
    def get_metrics(self, name: str = None, hours: int = 24) -> List[Dict[str, Any]]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene métricas de la base de datos."""
        since = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            if name:
                _ = conn.execute("""
                    SELECT * FROM metrics 
                    WHERE name = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                """, (name, since.isoformat()))
            else:
                _ = conn.execute("""
                    SELECT * FROM metrics 
                    WHERE timestamp >= ?
                    ORDER BY timestamp DESC
                """, (since.isoformat(),))
                
            return [dict(row) for row in cursor.fetchall()]
            
    def get_aggregated_metrics(self, name: str, hours: int = 24) -> Dict[str, float]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene métricas agregadas."""
        since = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(self.db_path) as conn:
            _ = conn.execute("""
                SELECT 
                    AVG(value) as avg_value,
                    MIN(value) as min_value,
                    MAX(value) as max_value,
                    COUNT(*) as count
                FROM metrics 
                WHERE name = ? AND timestamp >= ?
            """, (name, since.isoformat()))
            
            _ = cursor.fetchone()
            return {
                "average": row[0] or 0,
                "minimum": row[1] or 0,
                "maximum": row[2] or 0,
                "count": row[3] or 0
            }

class AlertManager:
    """Gestor de alertas basado en métricas."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        """TODO: Add docstring"""
        self.metrics_collector = metrics_collector
        self.alert_rules = []
        self.active_alerts = {}
        
    def add_alert_rule(self, name: str, metric_name: str, condition: str, threshold: float, duration_minutes: int = 5):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Añade una regla de alerta."""
        _ = {
            "name": name,
            "metric_name": metric_name,
            "condition": condition,  # "greater_than", "less_than", "equals"
            "threshold": threshold,
            "duration_minutes": duration_minutes,
            "last_triggered": None
        }
        self.alert_rules.append(rule)
        
    def check_alerts(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica todas las reglas de alerta."""
        for rule in self.alert_rules:
            self._check_single_alert(rule)
            
    def _check_single_alert(self, rule: Dict[str, Any]):
        """Verifica una regla de alerta específica."""
        # Obtener métricas recientes
        _ = self.metrics_collector.get_metrics(
            rule["metric_name"], 
            _ = 1
        )
        
        if not recent_metrics:
            return
            
        # Verificar condición
        _ = recent_metrics[0]["value"]
        condition_met = self._evaluate_condition(
            latest_value, 
            rule["condition"], 
            rule["threshold"]
        )
        
        if condition_met:
            self._trigger_alert(rule, latest_value)
        else:
            self._clear_alert(rule["name"])
            
    def _evaluate_condition(self, value: float, condition: str, threshold: float) -> bool:
        """Evalúa una condición de alerta."""
        if condition == "greater_than":
            return value > threshold
        elif condition == "less_than":
            return value < threshold
        elif condition == "equals":
            return abs(value - threshold) < 0.01
        return False
        
    def _trigger_alert(self, rule: Dict[str, Any], current_value: float):
        """Dispara una alerta."""
        _ = rule["name"]
        now = datetime.now()
        
        if alert_key not in self.active_alerts:
            self.active_alerts[alert_key] = {
                "rule": rule,
                "triggered_at": now,
                "current_value": current_value
            }
            
            # Log de alerta
            logger.warning("ALERTA: {rule['name']} - Valor: {current_value}, Umbral: %s", rule['threshold'])
            
            # Aquí se podría enviar notificación por email, webhook, etc.
            self._send_alert_notification(rule, current_value)
            
    def _clear_alert(self, alert_name: str):
        """Limpia una alerta activa."""
        if alert_name in self.active_alerts:
            del self.active_alerts[alert_name]
            logger.info("Alerta resuelta: %s", alert_name)
            
    def _send_alert_notification(self, rule: Dict[str, Any], current_value: float):
        """Envía notificación de alerta."""
        # Implementar envío de notificaciones (email, webhook, etc.)
        pass

class PerformanceMonitor:
    """Monitor de rendimiento de la aplicación."""
    
    def __init__(self):
        """TODO: Add docstring"""
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager(self.metrics_collector)
        self._setup_default_alerts()
        
    def _setup_default_alerts(self):
        """Configura alertas por defecto."""
        # CPU alto
        self.alert_manager.add_alert_rule(
            "high_cpu_usage",
            "system.cpu.usage",
            "greater_than",
            80.0,
            _ = 5
        )
        
        # Memoria baja
        self.alert_manager.add_alert_rule(
            "low_memory",
            "system.memory.available_gb",
            "less_than",
            1.0,
            _ = 3
        )
        
        # Disco lleno
        self.alert_manager.add_alert_rule(
            "disk_full",
            "system.disk.usage_percent",
            "greater_than",
            90.0,
            _ = 1
        )
        
    def start(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicia el monitoreo."""
        self.metrics_collector.start_collection()
        logger.info("Monitor de rendimiento iniciado")
        
    def stop(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Detiene el monitoreo."""
        self.metrics_collector.stop_collection()
        logger.info("Monitor de rendimiento detenido")
        
    def get_dashboard_data(self) -> Dict[str, Any]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene datos para dashboard de monitoreo."""
        return {
            "cpu_usage": self.metrics_collector.get_aggregated_metrics("system.cpu.usage", 1),
            "memory_usage": self.metrics_collector.get_aggregated_metrics("system.memory.usage_percent", 1),
            "disk_usage": self.metrics_collector.get_aggregated_metrics("system.disk.usage_percent", 1),
            "active_alerts": list(self.alert_manager.active_alerts.keys()),
            "last_updated": datetime.now().isoformat()
        }

# Instancia global
performance_monitor = PerformanceMonitor()

def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Función principal para ejecutar como script independiente."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor de rendimiento Hefest")
    parser.add_argument("--duration", type=int, default=60, help="Duración en segundos")
    parser.add_argument("--interval", type=int, default=10, help="Intervalo de recolección")
    
    _ = parser.parse_args()
    
    monitor = PerformanceMonitor()
    monitor.metrics_collector.collection_interval = args.interval
    
    try:
        monitor.start()
        print("Monitoreando por %s segundos..." % args.duration)
        time.sleep(args.duration)
        
        # Mostrar resumen
        _ = monitor.get_dashboard_data()
        print("\n📊 Resumen de Métricas:")
        print("CPU Promedio: %s%" % dashboard_data['cpu_usage']['average']:.2f)
        print("Memoria Promedio: %s%" % dashboard_data['memory_usage']['average']:.2f)
        print("Disco: %s%" % dashboard_data['disk_usage']['average']:.2f)
        
        if dashboard_data['active_alerts']:
            print("⚠️ Alertas Activas: %s" % ', '.join(dashboard_data['active_alerts']))
        else:
            print("✅ Sin alertas activas")
            
    finally:
        monitor.stop()

if __name__ == "__main__":
    main()
