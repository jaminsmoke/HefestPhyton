# Script para ejecutar Flake8 en el proyecto Hefest
# run_flake8.ps1

param(
    [string]$Path = "src",
    [switch]$AllFiles,
    [switch]$Verbose
)

$VenvPath = "$PSScriptRoot\..\.venv\Scripts\flake8.exe"
$ConfigPath = "$PSScriptRoot\..\development-config\.flake8"

Write-Host "🔍 EJECUTANDO FLAKE8 - ANÁLISIS DE ESTILO PEP8" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

if (-not (Test-Path $VenvPath)) {
    Write-Host "❌ Error: Flake8 no encontrado en $VenvPath" -ForegroundColor Red
    Write-Host "💡 Ejecuta: pip install flake8" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $ConfigPath)) {
    Write-Host "⚠️ Warning: Archivo de configuración no encontrado: $ConfigPath" -ForegroundColor Yellow
    Write-Host "Usando configuración por defecto..." -ForegroundColor Yellow
    $ConfigArg = ""
}
else {
    $ConfigArg = "--config=$ConfigPath"
}

# Determinar qué archivos analizar
if ($AllFiles) {
    $TargetPath = "."
    Write-Host "📂 Analizando: Todo el proyecto" -ForegroundColor Green
}
else {
    $TargetPath = $Path
    Write-Host "📂 Analizando: $TargetPath" -ForegroundColor Green
}

Write-Host "⚙️ Configuración: $ConfigPath" -ForegroundColor Green
Write-Host "🚀 Comando: $VenvPath $ConfigArg $TargetPath" -ForegroundColor Gray
Write-Host ""

# Ejecutar Flake8
try {
    if ($ConfigArg) {
        & $VenvPath $ConfigArg $TargetPath
    }
    else {
        & $VenvPath $TargetPath
    }
    
    $exitCode = $LASTEXITCODE
    Write-Host ""
    Write-Host "✅ Flake8 completado. Código de salida: $exitCode" -ForegroundColor Green
    
    if ($exitCode -eq 0) {
        Write-Host "🎉 ¡Código perfecto! Sin errores de estilo." -ForegroundColor Green
    }
    else {
        Write-Host "❌ Se encontraron errores de estilo." -ForegroundColor Red
    }
    
}
catch {
    Write-Host "❌ Error ejecutando Flake8: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
