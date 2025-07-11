# Script para limpiar configuraciones problemáticas de Copilot
# clean-copilot-config.ps1

Write-Host "🧹 Limpiando configuraciones problemáticas de Copilot..." -ForegroundColor Yellow

$globalSettingsPath = "$env:APPDATA\Code\User\settings.json"

if (Test-Path $globalSettingsPath) {
    Write-Host "📁 Archivo encontrado: $globalSettingsPath" -ForegroundColor Green

    # Crear backup
    $backupPath = "$globalSettingsPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $globalSettingsPath $backupPath -Force
    Write-Host "💾 Backup creado: $backupPath" -ForegroundColor Cyan

    # Leer contenido actual
    $content = Get-Content $globalSettingsPath -Raw

    # Eliminar configuraciones problemáticas
    Write-Host "🔧 Eliminando configuraciones problemáticas..." -ForegroundColor Yellow

    # Eliminar continue.models
    $content = $content -replace '"continue\.models":\s*\[[\s\S]*?\],?\s*', ''

    # Eliminar thinking tool
    $content = $content -replace '"github\.copilot\.chat\.agent\.thinkingTool":\s*true,?\s*', ''

    # Eliminar allowedModels con modelos no estándar
    $content = $content -replace '"allowedModels":\s*\[[\s\S]*?"claude-sonnet-4"[\s\S]*?\],?\s*', ''

    # Limpiar comas dobles y espacios extra
    $content = $content -replace ',\s*,', ','
    $content = $content -replace ',\s*}', '}'
    $content = $content -replace '{\s*,', '{'

    # Guardar archivo limpio
    $content | Set-Content $globalSettingsPath -Encoding UTF8

    Write-Host "✅ Configuraciones problemáticas eliminadas" -ForegroundColor Green
    Write-Host "🔄 Reinicia VS Code para aplicar cambios" -ForegroundColor Cyan

    # Mostrar qué se eliminó
    Write-Host "`n📋 Configuraciones eliminadas:" -ForegroundColor Yellow
    Write-Host "   • continue.models (gemini-1.5-flash)" -ForegroundColor Red
    Write-Host "   • github.copilot.chat.agent.thinkingTool" -ForegroundColor Red
    Write-Host "   • allowedModels con claude-sonnet-4" -ForegroundColor Red

}
else {
    Write-Host "❌ No se encontró el archivo de configuración global" -ForegroundColor Red
}

Write-Host "`n🎯 Para restaurar si es necesario:" -ForegroundColor Green
Write-Host "   Copy-Item `"$backupPath`" `"$globalSettingsPath`" -Force" -ForegroundColor White

Write-Host "`n✨ Script completado!" -ForegroundColor Green
