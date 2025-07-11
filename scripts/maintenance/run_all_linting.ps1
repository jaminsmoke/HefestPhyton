# Script para ejecutar todas las herramientas de linting
# run_all_linting.ps1

param(
    [string]$Path = "src",
    [switch]$AllFiles,
    [switch]$Verbose
)

Write-Host "🧪 EJECUTANDO TODAS LAS HERRAMIENTAS DE LINTING - PROYECTO HEFEST" -ForegroundColor Magenta
Write-Host "=" * 80 -ForegroundColor Gray
Write-Host ""

$ErrorCount = 0

# Ejecutar PyLint
Write-Host "1️⃣ EJECUTANDO PYLINT..." -ForegroundColor Yellow
Write-Host ""
try {
    if ($AllFiles) {
        & "$PSScriptRoot\run_pylint.ps1" -AllFiles
    } else {
        & "$PSScriptRoot\run_pylint.ps1" -Path $Path
    }
    if ($LASTEXITCODE -ne 0) { $ErrorCount++ }
} catch {
    Write-Host "❌ Error ejecutando PyLint: $($_.Exception.Message)" -ForegroundColor Red
    $ErrorCount++
}

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Gray
Write-Host ""

# Ejecutar Flake8
Write-Host "2️⃣ EJECUTANDO FLAKE8..." -ForegroundColor Yellow
Write-Host ""
try {
    if ($AllFiles) {
        & "$PSScriptRoot\run_flake8.ps1" -AllFiles
    } else {
        & "$PSScriptRoot\run_flake8.ps1" -Path $Path
    }
    if ($LASTEXITCODE -ne 0) { $ErrorCount++ }
} catch {
    Write-Host "❌ Error ejecutando Flake8: $($_.Exception.Message)" -ForegroundColor Red
    $ErrorCount++
}

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Gray
Write-Host ""

# Resumen final
Write-Host "📋 RESUMEN FINAL DEL ANÁLISIS" -ForegroundColor Magenta
Write-Host "=" * 80 -ForegroundColor Gray

if ($ErrorCount -eq 0) {
    Write-Host "🎉 ¡EXCELENTE! Todas las herramientas completaron sin errores." -ForegroundColor Green
    Write-Host "✨ El código cumple con todos los estándares de calidad." -ForegroundColor Green
} else {
    Write-Host "⚠️ Se encontraron problemas en $ErrorCount herramienta(s)." -ForegroundColor Yellow
    Write-Host "📝 Revisa los detalles arriba para corregir los problemas." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💡 TIP: Usa -AllFiles para analizar todo el proyecto" -ForegroundColor Cyan
Write-Host "💡 TIP: Especifica -Path <ruta> para analizar una carpeta específica" -ForegroundColor Cyan
Write-Host ""

exit $ErrorCount
