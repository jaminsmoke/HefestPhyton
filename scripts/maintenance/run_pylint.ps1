# Script para ejecutar PyLint en el proyecto Hefest
# run_pylint.ps1

param(
    [string]$Path = "src",
    [switch]$AllFiles,
    [switch]$Verbose
)

$VenvPath = "$PSScriptRoot\..\.venv\Scripts\pylint.exe"
$ConfigPath = "$PSScriptRoot\..\development-config\.pylintrc"

Write-Host "🔍 EJECUTANDO PYLINT - ANÁLISIS DE CÓDIGO PYTHON" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Gray

if (-not (Test-Path $VenvPath)) {
    Write-Host "❌ Error: PyLint no encontrado en $VenvPath" -ForegroundColor Red
    Write-Host "💡 Ejecuta: pip install pylint" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $ConfigPath)) {
    Write-Host "⚠️ Warning: Archivo de configuración no encontrado: $ConfigPath" -ForegroundColor Yellow
    Write-Host "Usando configuración por defecto..." -ForegroundColor Yellow
    $ConfigArg = ""
}
else {
    $ConfigArg = "--rcfile=$ConfigPath"
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

# Ejecutar PyLint
try {
    if ($ConfigArg) {
        & $VenvPath $ConfigArg $TargetPath
    }
    else {
        & $VenvPath $TargetPath
    }
    
    $exitCode = $LASTEXITCODE
    Write-Host ""
    Write-Host "✅ PyLint completado. Código de salida: $exitCode" -ForegroundColor Green
    
    if ($exitCode -eq 0) {
        Write-Host "🎉 ¡Código perfecto! Sin errores ni warnings." -ForegroundColor Green
    }
    elseif ($exitCode -lt 5) {
        Write-Host "⚠️ Se encontraron warnings menores." -ForegroundColor Yellow
    }
    else {
        Write-Host "❌ Se encontraron errores importantes." -ForegroundColor Red
    }
    
}
catch {
    Write-Host "❌ Error ejecutando PyLint: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
