# Script de limpieza para mejorar rendimiento de VS Code
# Ejecutar: .\scripts\clean_vscode_performance.ps1

param(
    [switch]$Deep = $false
)

Write-Host "🧹 Limpiando archivos que ralentizan VS Code..." -ForegroundColor Cyan

# Limpieza básica
Write-Host "📁 Eliminando carpetas __pycache__..." -ForegroundColor Yellow
Get-ChildItem -Path "." -Recurse -Directory -Name "__pycache__" | ForEach-Object { 
    Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "🐍 Eliminando archivos .pyc..." -ForegroundColor Yellow
Get-ChildItem -Path "." -Recurse -File | Where-Object { $_.Extension -eq ".pyc" } | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "📊 Limpiando logs antiguos..." -ForegroundColor Yellow
Get-ChildItem -Path "logs" -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | Remove-Item -Force -ErrorAction SilentlyContinue

if ($Deep) {
    Write-Host "🔍 Limpieza profunda activada..." -ForegroundColor Magenta
    
    # Limpiar cache de herramientas
    if (Test-Path ".pytest_cache") {
        Remove-Item ".pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    if (Test-Path ".coverage") {
        Remove-Item ".coverage" -Force -ErrorAction SilentlyContinue
    }
    
    # Limpiar archivos temporales
    Get-ChildItem -Path "." -Recurse -File | Where-Object { 
        $_.Extension -in @(".tmp", ".temp", ".swp", ".swo") -or $_.Name -like "*~" 
    } | Remove-Item -Force -ErrorAction SilentlyContinue
}

# Estadísticas finales
$pycacheCount = (Get-ChildItem -Path "." -Recurse -Directory -Name "__pycache__" | Measure-Object).Count
$pycCount = (Get-ChildItem -Path "." -Recurse -File | Where-Object { $_.Extension -eq ".pyc" } | Measure-Object).Count

Write-Host "✅ Limpieza completada:" -ForegroundColor Green
Write-Host "   📁 Carpetas __pycache__ restantes: $pycacheCount" -ForegroundColor White
Write-Host "   🐍 Archivos .pyc restantes: $pycCount" -ForegroundColor White

if ($pycacheCount -eq 0 -and $pycCount -eq 0) {
    Write-Host "🚀 ¡VS Code debería funcionar más rápido ahora!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Algunos archivos no se pudieron eliminar (podrían estar en uso)" -ForegroundColor Yellow
}

Write-Host "`n💡 Consejos adicionales:" -ForegroundColor Cyan
Write-Host "   - Reinicia VS Code para ver mejoras" -ForegroundColor White
Write-Host "   - Ejecuta este script regularmente: .\scripts\clean_vscode_performance.ps1" -ForegroundColor White
Write-Host "   - Para limpieza profunda: .\scripts\clean_vscode_performance.ps1 -Deep" -ForegroundColor White
