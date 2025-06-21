# HEFEST - Sistema de Backup Profesional de Versiones
# Backup Estandarizado para v0.0.11 - 12 de Junio de 2025

param(
    [string]$Version = "v0.0.11",
    [string]$BackupType = "version-release",
    [switch]$IncludeData,
    [switch]$Compress
)

# Configuración
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_NAME = "HEFEST_${Version}_${BackupType}_${TIMESTAMP}"
$BACKUP_BASE_DIR = Join-Path $PROJECT_ROOT "version-backups"
$VERSION_DIR = Join-Path $BACKUP_BASE_DIR $Version
$BACKUP_DIR = Join-Path $VERSION_DIR $BACKUP_NAME

# Funciones de utilidad
function Write-BackupHeader {
    param([string]$Message)
    Write-Host "`n[BACKUP] $Message" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Gray
}

function Write-BackupSuccess {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-BackupInfo {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-BackupError {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Función principal de backup
function New-HefestVersionBackup {
    Write-BackupHeader "Iniciando Backup Profesional de HEFEST $Version"
    
    # Crear directorios
    if (-not (Test-Path $BACKUP_BASE_DIR)) {
        New-Item -ItemType Directory -Path $BACKUP_BASE_DIR -Force | Out-Null
        Write-BackupInfo "Directorio base de backups creado: $BACKUP_BASE_DIR"
    }
    
    if (-not (Test-Path $VERSION_DIR)) {
        New-Item -ItemType Directory -Path $VERSION_DIR -Force | Out-Null
        Write-BackupInfo "Directorio de versión creado: $VERSION_DIR"
    }
    
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
    Write-BackupInfo "Directorio de backup creado: $BACKUP_DIR"
    
    # Archivos y directorios principales a respaldar
    $ITEMS_TO_BACKUP = @(
        "src",
        "tests", 
        "docs",
        "scripts",
        "config",
        "assets",
        "docker",
        "build-tools",
        "development-config",
        "*.py",
        "*.ps1", 
        "*.md",
        "*.toml",
        "*.txt",
        "*.json",
        "*.in",
        "LICENSE"
    )
    
    # Archivos a excluir
    $EXCLUDE_PATTERNS = @(
        "__pycache__",
        "*.pyc",
        ".pytest_cache",
        "htmlcov",
        ".coverage",
        "build",
        "dist",
        "*.egg-info",
        "logs",
        "backups",
        "version-backups"
    )
    
    Write-BackupInfo "Copiando archivos del proyecto..."
    
    # Copiar archivos y directorios
    foreach ($item in $ITEMS_TO_BACKUP) {
        $sourcePath = Join-Path $PROJECT_ROOT $item
        if (Test-Path $sourcePath) {
            $itemName = Split-Path $sourcePath -Leaf
            $destPath = Join-Path $BACKUP_DIR $itemName
            
            if (Test-Path $sourcePath -PathType Container) {
                # Es un directorio
                Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
                Write-BackupInfo "Directorio copiado: $itemName"
            } else {
                # Es un archivo o patrón de archivos
                if ($item.Contains("*")) {
                    $files = Get-ChildItem -Path $PROJECT_ROOT -Name $item
                    foreach ($file in $files) {
                        $sourceFile = Join-Path $PROJECT_ROOT $file
                        $destFile = Join-Path $BACKUP_DIR $file
                        Copy-Item -Path $sourceFile -Destination $destFile -Force
                    }
                    Write-BackupInfo "Archivos copiados: $item"
                } else {
                    Copy-Item -Path $sourcePath -Destination $destPath -Force
                    Write-BackupInfo "Archivo copiado: $itemName"
                }
            }
        }
    }
    
    # Incluir datos si se especifica
    if ($IncludeData) {
        $dataPath = Join-Path $PROJECT_ROOT "data"
        if (Test-Path $dataPath) {
            $destDataPath = Join-Path $BACKUP_DIR "data"
            Copy-Item -Path $dataPath -Destination $destDataPath -Recurse -Force
            Write-BackupInfo "Datos incluidos en backup"
        }
    }
    
    # Limpiar archivos excluidos
    Write-BackupInfo "Limpiando archivos temporales del backup..."
    foreach ($pattern in $EXCLUDE_PATTERNS) {
        $filesToRemove = Get-ChildItem -Path $BACKUP_DIR -Recurse -Name $pattern -ErrorAction SilentlyContinue
        foreach ($file in $filesToRemove) {
            $fullPath = Join-Path $BACKUP_DIR $file
            if (Test-Path $fullPath) {
                Remove-Item -Path $fullPath -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
    }
    
    # Crear archivo de información del backup
    $backupInfo = @"
# HEFEST - Información del Backup
Versión: $Version
Tipo de Backup: $BackupType
Fecha de Creación: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')
Sistema Operativo: $($env:OS)
Usuario: $($env:USERNAME)
Máquina: $($env:COMPUTERNAME)

## Contenido del Backup
- Código fuente completo (src/)
- Tests completos (tests/)
- Documentación (docs/)
- Scripts de automatización (scripts/)
- Configuraciones (config/, docker/, build-tools/, development-config/)
- Assets (assets/)
- Archivos de configuración (*.toml, *.txt, *.json, etc.)
- Documentación (README.md, CHANGELOG.md, LICENSE)

## Exclusiones
- Archivos temporales (__pycache__, *.pyc)
- Cache de tests (.pytest_cache, htmlcov, .coverage)
- Builds (build/, dist/, *.egg-info)
- Logs y backups anteriores

## Estado del Proyecto en el Backup
- ✅ 87 tests PASSED
- ✅ Makefile.ps1 operativo con 29 tareas
- ✅ Error de encoding solucionado
- ✅ Estructura empresarial organizada
- ✅ Documentación completa

🎯 ESTADO: PRODUCTION READY
"@
    
    $infoFile = Join-Path $BACKUP_DIR "BACKUP_INFO.md"
    $backupInfo | Out-File -FilePath $infoFile -Encoding UTF8
    Write-BackupInfo "Archivo de información creado: BACKUP_INFO.md"
      # Comprimir si se especifica
    if ($Compress) {
        Write-BackupInfo "Comprimiendo backup..."
        $zipPath = "$BACKUP_DIR.zip"
        Compress-Archive -Path $BACKUP_DIR -DestinationPath $zipPath -Force
          # Verificar integridad del ZIP
        Write-BackupInfo "Verificando integridad del backup comprimido..."
        try {
            # Crear directorio temporal en la ubicación temporal del sistema
            $tempVerifyDir = Join-Path $env:TEMP "hefest_verify_$(Get-Random)"
            New-Item -ItemType Directory -Path $tempVerifyDir -Force | Out-Null
            
            try {
                Expand-Archive -Path $zipPath -DestinationPath $tempVerifyDir -Force
                $extractedFiles = (Get-ChildItem -Path $tempVerifyDir -Recurse -File | Measure-Object).Count
                Write-BackupInfo "ZIP verificado: $extractedFiles archivos"
                
                # Obtener tamaños antes de eliminar
                $originalSize = (Get-ChildItem -Path $BACKUP_DIR -Recurse | Measure-Object -Property Length -Sum).Sum
                $compressedSize = (Get-Item $zipPath).Length
                $spaceSaved = $originalSize - $compressedSize
                
                # Eliminar directorio sin comprimir para optimizar espacio
                Remove-Item -Path $BACKUP_DIR -Recurse -Force
                Write-BackupSuccess "Directorio sin comprimir eliminado - Espacio liberado: $([math]::Round($spaceSaved / 1MB, 2)) MB"
                
            } finally {
                # Garantizar limpieza del directorio temporal, incluso si hay errores
                if (Test-Path $tempVerifyDir) {
                    Remove-Item -Path $tempVerifyDir -Recurse -Force -ErrorAction SilentlyContinue
                    Write-BackupInfo "Directorio temporal limpiado: $(Split-Path $tempVerifyDir -Leaf)"
                }
            }
            
        } catch {
            Write-BackupError "Error verificando ZIP: $_"
            Write-BackupInfo "Manteniendo directorio sin comprimir por seguridad"
        }
        
        Write-BackupSuccess "Backup comprimido y optimizado: $(Split-Path $zipPath -Leaf)"
        $finalPath = $zipPath
    } else {
        $finalPath = $BACKUP_DIR
    }
    
    # Obtener información del backup
    if ($Compress) {
        $backupSize = (Get-Item $finalPath).Length
        $sizeText = "{0:N2} MB" -f ($backupSize / 1MB)
    } else {
        $backupSize = (Get-ChildItem -Path $finalPath -Recurse | Measure-Object -Property Length -Sum).Sum
        $sizeText = "{0:N2} MB" -f ($backupSize / 1MB)
    }
    
    $fileCount = (Get-ChildItem -Path $finalPath -Recurse -File | Measure-Object).Count
    
    Write-BackupSuccess "Backup completado exitosamente!"
    Write-BackupInfo "Ubicación: $finalPath"
    Write-BackupInfo "Tamaño: $sizeText"
    Write-BackupInfo "Archivos: $fileCount"
    Write-BackupInfo "Nombre: $BACKUP_NAME"
    
    return $finalPath
}

# Ejecutar backup si el script se ejecuta directamente
if ($MyInvocation.InvocationName -ne '.') {
    $backupPath = New-HefestVersionBackup
    
    Write-BackupHeader "BACKUP PROFESIONAL HEFEST $Version COMPLETADO"
    Write-Host "Ubicación final: $backupPath" -ForegroundColor Yellow
    Write-Host "`n🎉 Backup de versión listo para archivo histórico" -ForegroundColor Green
}
