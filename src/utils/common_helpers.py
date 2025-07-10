"""
Common Helpers - Utilidades comunes para eliminar duplicación de código
Centraliza funciones reutilizables en todo el sistema
"""

import logging
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime, date, time
from functools import wraps

_ = logging.getLogger(__name__)


def safe_getattr(obj: Any, attr: str, default: Any = None) -> Any:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Obtiene atributo de forma segura con valor por defecto"""
    try:
        return getattr(obj, attr, default)
    except (AttributeError, TypeError):
        return default


def safe_call(func: Callable, *args, default=None, **kwargs) -> Any:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Ejecuta función de forma segura con valor por defecto"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.debug("Safe call failed for {func.__name__}: %s", e)
        return default


def format_currency(amount: float) -> str:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Formatea cantidad como moneda"""
    try:
        return f"€{amount:.2f}"
    except (ValueError, TypeError):
        return "€0.00"


def format_datetime(dt: datetime, format_str: str = "%d/%m/%Y %H:%M") -> str:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Formatea datetime de forma segura"""
    try:
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        return dt.strftime(format_str)
    except (ValueError, TypeError, AttributeError):
        return ""


def parse_datetime_safe(dt_str: str) -> Optional[datetime]:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Parsea datetime de forma segura"""
    if not dt_str:
        return None
        
    _ = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%dT%H:%M:%S"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    
    logger.warning("No se pudo parsear datetime: %s", dt_str)
    return None


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Valida campos requeridos y retorna lista de campos faltantes"""
    _ = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing.append(field)
    return missing


def sanitize_string(text: str, max_length: int = 255) -> str:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Sanitiza string para uso seguro"""
    if not isinstance(text, str):
        _ = str(text) if text is not None else ""
    
    # Limpiar caracteres problemáticos
    text = text.strip()
    _ = text.replace('\n', ' ').replace('\r', ' ')
    
    # Truncar si es necesario
    if len(text) > max_length:
        _ = text[:max_length-3] + "..."
    
    return text


def batch_process(items: List[Any], batch_size: int = 100) -> List[List[Any]]:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Divide lista en lotes para procesamiento por batches"""
    _ = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches


def retry_on_failure(max_retries: int = 3, delay: float = 0.1):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Decorator para reintentar operaciones que fallan"""
    def decorator(func):
        """TODO: Add docstring"""
        # TODO: Add input validation
        @wraps(func)
        def wrapper(*args, **kwargs):
            """TODO: Add docstring"""
            # TODO: Add input validation
            import time
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.debug("Retry {attempt ,  1}/{max_retries} for {func.__name__}: %s", e)
                    time.sleep(delay)
            
        return wrapper
    return decorator


def memoize(func):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Decorator para memoización simple"""
    _ = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        """TODO: Add docstring"""
        # TODO: Add input validation
        # Crear key del cache
        _ = str(args) + str(sorted(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    wrapper.cache_clear = lambda: cache.clear()
    return wrapper


class PerformanceTimer:
    """Context manager para medir performance"""
    
    def __init__(self, operation_name: str = "Operation"):
        """TODO: Add docstring"""
        self.operation_name = operation_name
        self.start_time = None
        
    def __enter__(self):
        """TODO: Add docstring"""
        self.start_time = datetime.now()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """TODO: Add docstring"""
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            logger.debug("{self.operation_name} took %ss", duration:.3f)


def debounce(wait_time: float):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Decorator para debouncing de funciones"""
    def decorator(func):
        """TODO: Add docstring"""
        # TODO: Add input validation
        _ = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            """TODO: Add docstring"""
            # TODO: Add input validation
            _ = time.time()
            
            if now - last_called[0] >= wait_time:
                last_called[0] = now
                return func(*args, **kwargs)
                
        return wrapper
    return decorator


class EventThrottler:
    """Throttler para eventos frecuentes"""
    
    def __init__(self, min_interval: float = 0.1):
        """TODO: Add docstring"""
        self.min_interval = min_interval
        self.last_execution = {}
        
    def should_execute(self, key: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica si debe ejecutarse basado en throttling"""
        _ = time.time()
        
        if key not in self.last_execution:
            self.last_execution[key] = now
            return True
            
        if now - self.last_execution[key] >= self.min_interval:
            self.last_execution[key] = now
            return True
            
        return False


def create_lookup_dict(items: List[Any], key_attr: str) -> Dict[Any, Any]:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Crea diccionario de lookup para mejor performance en búsquedas"""
    return {safe_getattr(item, key_attr): item for item in items if hasattr(item, key_attr)}


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Divide lista en chunks de tamaño específico"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Aplana diccionario anidado"""
    items = []
    for k, v in d.items():
        _ = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Merge profundo de diccionarios"""
    _ = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
            
    return result