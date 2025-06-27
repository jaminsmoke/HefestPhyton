# Plan Reorganización Tests - Siguiente Fase

## ✅ FASE 1 COMPLETADA

### Tests Migrados y Funcionando:
- **Unit**: `test_inventario_service_basic.py` ✅ (3 tests pasando)
- **Integration**: `test_tpv_module_integration.py` ✅
- **Integration**: `test_inventario_complete.py` ✅  
- **UI**: `test_dashboard_metrics.py` ✅
- **UI**: `test_mesas_area_metrics.py` ✅

### Estructura Creada:
```
tests/
├── unit/           ✅ 1 test migrado
├── integration/    ✅ 2 tests migrados  
├── ui/            ✅ 2 tests migrados
└── utilities/     ✅ Preparado para herramientas
```

## 🎯 FASE 2: REFACTORING Y CONSOLIDACIÓN

### Prioridad Alta - Tests Recuperables:

#### 1. Unit Tests Adicionales
```bash
# Migrar estos tests valiosos:
scripts/testing/test_supplier_corrections.py → tests/unit/test_supplier_service.py
scripts/testing/test_category_manager_quick.py → tests/unit/test_category_service.py  
scripts/testing/test_import_supplier.py → tests/unit/test_import_services.py
scripts/testing/test_import_tpv.py → tests/unit/test_import_services.py (consolidar)
```

#### 2. Integration Tests Adicionales
```bash
# Migrar flujos completos:
scripts/testing/test_flujo_inventario.py → tests/integration/test_inventario_workflow.py
scripts/testing/test_inventory_final_verification.py → tests/integration/test_system_verification.py
test_edicion_nombres_mesa.py (raíz) → tests/integration/test_mesa_editing_workflow.py
```

#### 3. UI Tests Consolidados
```bash
# Consolidar múltiples tests similares:
test_dialog_*.py (múltiples) → tests/ui/test_dialog_components.py
test_header_*.py (múltiples) → tests/ui/test_header_components.py  
test_stats_*.py (múltiples) → tests/ui/test_stats_components.py
test_mesas_*.py (múltiples) → tests/ui/test_mesa_components.py
```

### Prioridad Media - Tests con Refactoring Mayor:

#### Dashboard Tests
```bash
test_dashboard_comparison.py
test_dashboard_debug.py  
test_dashboard_debug_v2.py
→ Consolidar en: tests/ui/test_dashboard_complete.py
```

#### Widget Tests  
```bash
test_mesa_widget_mejoras.py
test_product_dialog_professional.py
test_supplier_dialog_direct.py
→ Consolidar en: tests/ui/test_widget_suite.py
```

## 🗑️ FASE 3: LIMPIEZA Y ELIMINACIÓN

### Tests para Eliminar (Obsoletos):

#### Debug Temporales:
- `debug_categoria.py`
- `debug_inventario_import.py` 
- `test_debug_stats_compactas.py`

#### Duplicados Obvios:
- `test_status_container_optimizado.py` vs `test_status_container_optimized.py`
- `test_dialog_simple.py` vs `test_dialog_corrected.py` vs `test_dialog_integrated.py`

#### Versiones Específicas Obsoletas:
- `test_estilos_tablas_v0_0_12.py`
- Tests con "ultra_premium", "final", "definitivo" en el nombre

#### Tests de Desarrollo Iterativo:
- `test_title_ultra_premium_final.py`
- `test_header_ultra_premium.py`
- `test_stats_ultra_simple.py`

### Utilidades a Conservar:
```bash
# Mover a tests/utilities/:
scripts/testing/check_db_status.py
scripts/testing/check_db_structure.py  
scripts/testing/verify_db.py
```

## 📋 COMANDOS PARA FASE 2

### 1. Migrar Tests Prioritarios:
```bash
# Copiar y adaptar tests valiosos
cp scripts/testing/test_supplier_corrections.py tests/unit/test_supplier_service.py
# Editar imports y estructura

cp scripts/testing/test_flujo_inventario.py tests/integration/test_inventario_workflow.py
# Convertir a unittest estándar
```

### 2. Consolidar Tests Similares:
```bash
# Crear tests consolidados combinando lógica útil
# Ejemplo: Combinar todos los test_dialog_*.py en uno solo
```

### 3. Verificar Funcionamiento:
```bash
# Ejecutar cada test migrado
python tests/unit/test_supplier_service.py
python tests/integration/test_inventario_workflow.py

# Ejecutar suite completa
python -m tests.test_suite
```

## 🎯 OBJETIVOS FASE 2

### Métricas Esperadas:
- **Tests finales**: ~15-20 (de 67 originales)
- **Reducción**: ~75% de archivos
- **Cobertura**: Mantener/mejorar cobertura actual
- **Calidad**: Tests estándar, mantenibles, documentados

### Estructura Final:
```
tests/
├── unit/ (5-7 tests consolidados)
├── integration/ (4-5 tests de flujos)
├── ui/ (4-5 tests de componentes)
├── utilities/ (3 herramientas BD)
└── README.md (actualizado)
```

## ✅ SIGUIENTE ACCIÓN RECOMENDADA

**Continuar con migración de `test_supplier_corrections.py`** - Es un test completo y valioso que debe preservarse en `tests/unit/test_supplier_service.py`.

¿Proceder con Fase 2?