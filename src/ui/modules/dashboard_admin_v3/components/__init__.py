"""
Componentes específicos del Dashboard Administrativo Ultra Moderno V3.

Este módulo contiene todos los componentes especializados para el dashboard
administrativo, incluyendo:
- Componentes base de métricas (UltraModernMetricCard)
- Especializaciones para hostelería (HospitalityMetricCard)
- Otros componentes específicos del dashboard administrativo

Arquitectura:
- dashboard_metric_components.py: Componentes base de métricas
- hospitality_metric_card.py: Especialización para métricas de hostelería

Versión: v0.0.12
Autor: Hefest Team
"""

from .dashboard_metric_components import UltraModernMetricCard
from .hospitality_metric_card import HospitalityMetricCard

__all__ = ["UltraModernMetricCard", "HospitalityMetricCard"]
