# HEFEST - Makefile de PowerShell para Automatización de Tareas

param(
    [string]$Task = "help",
    [switch]$Clean,
    [switch]$Verbose
)

# Configuración
$PYTHON_CMD = "python"
$PIP_CMD = "pip"

# Funciones de utilidad
function Write-TaskHeader {
    param([string]$TaskName)
    Write-Host "`n[INFO] Ejecutando: $TaskName" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Gray
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

# Tareas disponibles
switch ($Task.ToLower()) {
    "help" {        Write-Host @"
HEFEST - Sistema de Gestion de Hosteleria
============================================

Tareas disponibles:

DESARROLLO:
  install      - Instalar dependencias del proyecto
  install-dev  - Instalar dependencias de desarrollo
  dev          - Modo desarrollo (instalar + tests + linter)
  
TESTING:
  test         - Ejecutar todos los tests
  test-unit    - Ejecutar solo tests unitarios
  test-cov     - Ejecutar tests con coverage
  
CALIDAD DE CODIGO:
  lint         - Ejecutar linters (flake8, mypy)
  format       - Formatear codigo con black
  clean        - Limpiar archivos temporales
  
BUILD Y DISTRIBUCION:
  build        - Construir paquete de distribucion
  build-exe    - Crear ejecutable con PyInstaller
  install-pkg  - Instalar paquete en modo editable
  
EJECUCION:
  run          - Ejecutar aplicacion
  debug        - Ejecutar en modo debug
  
UTILIDADES:
  check-db     - Verificar base de datos
  backup       - Crear backup del proyecto
  docs         - Generar documentacion

TAREAS AVANZADAS:
  release      - Crear una nueva version de release
  quality      - Ejecutar analisis de calidad del codigo
  setup-hooks  - Configurar pre-commit hooks
  security-scan - Ejecutar analisis de seguridad
  docker-build  - Construir imagen Docker
  docker-run    - Ejecutar Hefest en Docker
  performance-test - Ejecutar tests de rendimiento
  migration     - Ejecutar migraciones de base de datos
  install-all   - Instalación completa del proyecto

USO:
  .\Makefile.ps1 <tarea>
  .\Makefile.ps1 dev -Clean      # Limpiar antes de ejecutar
  .\Makefile.ps1 test -Verbose   # Output detallado

"@ -ForegroundColor Yellow
    }
    
    "install" {
        Write-TaskHeader "Instalando dependencias del proyecto"
        & $PIP_CMD install -r requirements.txt
        Write-Success "Dependencias instaladas"
    }
    
    "install-dev" {
        Write-TaskHeader "Instalando dependencias de desarrollo"
        & $PIP_CMD install -r requirements-dev.txt
        & $PIP_CMD install -e .
        Write-Success "Dependencias de desarrollo instaladas"
    }
    
    "dev" {
        Write-TaskHeader "Configurando entorno de desarrollo"
        if ($Clean) {
            & .\Makefile.ps1 clean
        }
        & .\Makefile.ps1 install-dev
        & .\Makefile.ps1 test
        & .\Makefile.ps1 lint
        Write-Success "Entorno de desarrollo configurado"
    }
    
    "test" {
        Write-TaskHeader "Ejecutando tests"
        & $PYTHON_CMD -m pytest tests/ -v
        Write-Success "Tests completados"
    }
    
    "test-unit" {
        Write-TaskHeader "Ejecutando tests unitarios"
        & $PYTHON_CMD -m pytest tests/unit/ -v
        Write-Success "Tests unitarios completados"
    }
    
    "test-cov" {
        Write-TaskHeader "Ejecutando tests con coverage"
        & $PYTHON_CMD -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
        Write-Success "Coverage report generado"
    }
    
    "lint" {
        Write-TaskHeader "Ejecutando linters"
        & $PYTHON_CMD -m flake8 src/ tests/
        & $PYTHON_CMD -m mypy src/
        Write-Success "Linting completado"
    }
    
    "format" {
        Write-TaskHeader "Formateando código"
        & $PYTHON_CMD -m black src/ tests/
        & $PYTHON_CMD -m isort src/ tests/
        Write-Success "Código formateado"
    }
    
    "clean" {
        Write-TaskHeader "Limpiando archivos temporales"
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .pytest_cache
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue __pycache__
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue src/__pycache__
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue tests/__pycache__
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue htmlcov
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .coverage
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue build
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue dist
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "*.egg-info"
        Write-Success "Limpieza completada"
    }
    
    "build" {
        Write-TaskHeader "Construyendo paquete de distribución"
        & $PYTHON_CMD -m build
        Write-Success "Paquete construido en dist/"
    }
    
    "build-exe" {
        Write-TaskHeader "Creando ejecutable"
        & $PYTHON_CMD -m PyInstaller --onefile --name hefest src/main.py
        Write-Success "Ejecutable creado en dist/"
    }
    
    "install-pkg" {
        Write-TaskHeader "Instalando paquete en modo editable"
        & $PIP_CMD install -e .
        Write-Success "Paquete instalado"
    }
    
    "run" {
        Write-TaskHeader "Ejecutando aplicación"
        & $PYTHON_CMD src/main.py
    }
    
    "debug" {
        Write-TaskHeader "Ejecutando en modo debug"
        $env:DEBUG = "true"
        & $PYTHON_CMD src/main.py
    }
    
    "check-db" {
        Write-TaskHeader "Verificando base de datos"
        & $PYTHON_CMD -c "from src.database import check_connection; check_connection()"
        Write-Success "Base de datos verificada"
    }
    
    "backup" {
        Write-TaskHeader "Creando backup"
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupName = "hefest_backup_$timestamp.zip"
        Compress-Archive -Path "src", "tests", "requirements*.txt", "README.md" -DestinationPath $backupName
        Write-Success "Backup creado: $backupName"
    }
    
    "docs" {
        Write-TaskHeader "Generando documentación"
        & $PYTHON_CMD -m sphinx.cmd.build -b html docs/ docs/_build/html
        Write-Info "Documentación disponible en docs/_build/html/"
        Write-Success "Documentación generada"
    }
    
    "release" {
        Write-TaskHeader "Creando nueva versión de release"
        $Version = Read-Host "Nueva versión (ej: 0.0.11)"
        if (-not $Version) {
            Write-Error "Versión requerida"
            exit 1
        }
        & $PYTHON_CMD scripts/auto_release.py --version $Version
        Write-Success "Release $Version creado"
    }
    
    "quality" {
        Write-TaskHeader "Ejecutando análisis de calidad"
        & $PYTHON_CMD scripts/quality_analysis.py
        Write-Success "Análisis de calidad completado"
    }
    
    "setup-hooks" {
        Write-TaskHeader "Configurando pre-commit hooks"
        & pre-commit install --config development-config/.pre-commit-config.yaml
        Write-Success "Pre-commit hooks configurados"
    }
    
    "security-scan" {
        Write-TaskHeader "Ejecutando análisis de seguridad"
        & $PYTHON_CMD -m bandit -r src/
        & $PYTHON_CMD -m safety check
        Write-Success "Análisis de seguridad completado"
    }
    
    "docker-build" {
        Write-TaskHeader "Construyendo imagen Docker"
        docker build -f docker/Dockerfile -t hefest:latest .
        Write-Success "Imagen Docker construida"
    }
    
    "docker-run" {
        Write-TaskHeader "Ejecutando Hefest en Docker"
        docker-compose -f docker/docker-compose.yml up -d
        Write-Success "Hefest ejecutándose en Docker"
    }
    
    "performance-test" {
        Write-TaskHeader "Ejecutando tests de rendimiento"
        & $PYTHON_CMD -m pytest tests/performance/ -v
        Write-Success "Tests de rendimiento completados"
    }
    
    "migration" {
        Write-TaskHeader "Ejecutando migraciones de base de datos"
        & $PYTHON_CMD scripts/migrate_db.py
        Write-Success "Migraciones completadas"
    }
    
    "install-all" {
        Write-TaskHeader "Instalación completa del proyecto"
        & .\Makefile.ps1 install-dev
        & .\Makefile.ps1 setup-hooks
        & .\Makefile.ps1 check-db
        & .\Makefile.ps1 test
        Write-Success "Instalación completa finalizada"
    }
    
    default {
        Write-Error "Tarea '$Task' no reconocida"
        Write-Info "Ejecuta '.\Makefile.ps1 help' para ver tareas disponibles"
        exit 1
    }
}
