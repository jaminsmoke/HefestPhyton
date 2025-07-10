# Script para resetear específicamente el panel de Copilot Chat
# reset-copilot-chat-panel.ps1

Write-Host "🔧 Reseteando panel de Copilot Chat..." -ForegroundColor Yellow

# 1. Limpiar datos de Copilot Chat en AppData
Write-Host "1. Limpiando datos de Copilot Chat..." -ForegroundColor Cyan
$copilotChatPath = "$env:APPDATA\Code\User\workspaceStorage"
if (Test-Path $copilotChatPath) {
    Get-ChildItem -Path $copilotChatPath -Recurse -Filter "*copilot*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "   ✅ Datos de Copilot Chat limpiados" -ForegroundColor Green
}

# 2. Limpiar estado de ventana de Copilot
Write-Host "2. Limpiando estado de ventana..." -ForegroundColor Cyan
$windowStatePath = "$env:APPDATA\Code\User\globalStorage\state.vscdb"
if (Test-Path $windowStatePath) {
    # No eliminamos el archivo completo, solo hacemos backup
    Copy-Item $windowStatePath "$windowStatePath.backup" -Force -ErrorAction SilentlyContinue
    Write-Host "   ✅ Estado de ventana respaldado" -ForegroundColor Green
}

# 3. Resetear configuración específica de Copilot Chat
Write-Host "3. Reseteando configuración de Copilot Chat..." -ForegroundColor Cyan
$currentPath = Get-Location
$settingsPath = Join-Path $currentPath ".vscode\settings.json"

if (Test-Path $settingsPath) {
    Write-Host "   📝 Configuración encontrada en: $settingsPath" -ForegroundColor White
    Write-Host "   ⚠️  Eliminar manualmente estas configuraciones problemáticas:" -ForegroundColor Yellow
    Write-Host "      - github.copilot.chat.welcomeMessage" -ForegroundColor Red
    Write-Host "      - github.copilot.editor.iterativeEditing" -ForegroundColor Red
    Write-Host "      - github.copilot.chat.localeOverride" -ForegroundColor Red
    Write-Host "      - github.copilot.renameSuggestions.triggerAutomatically" -ForegroundColor Red
}
else {
    Write-Host "   ❌ No se encontró archivo de configuración" -ForegroundColor Red
}

Write-Host "`n🎯 Comandos manuales para probar en Copilot Chat:" -ForegroundColor Green
Write-Host "   1. /clear - Limpiar lista completa" -ForegroundColor White
Write-Host "   2. /reset - Resetear sesión de chat" -ForegroundColor White
Write-Host "   3. Ctrl+Shift+P → 'GitHub Copilot: Reset Authentication'" -ForegroundColor White

Write-Host "`n📋 Pasos siguientes:" -ForegroundColor Yellow
Write-Host "   1. Reinicia VS Code completamente" -ForegroundColor White
Write-Host "   2. Abre el panel de Copilot Chat" -ForegroundColor White
Write-Host "   3. Verifica si aparece el menú contextual en 'Files Changed'" -ForegroundColor White
Write-Host "   4. Si no funciona: deshabilita extensiones una por una" -ForegroundColor White

Write-Host "`n✨ Script completado!" -ForegroundColor Green
