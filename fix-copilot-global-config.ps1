# Script para deshabilitar temporalmente configuraciones problemáticas de Copilot
# fix-copilot-global-config.ps1

$globalSettingsPath = "$env:APPDATA\Code\User\settings.json"

Write-Host "🔧 Modificando configuración global de Copilot..." -ForegroundColor Yellow

if (Test-Path $globalSettingsPath) {
    # Leer configuración actual
    $content = Get-Content $globalSettingsPath -Raw

    # Reemplazar configuraciones problemáticas
    $newContent = $content `
        -replace '"github\.copilot\.chat\.agent\.thinkingTool":\s*true', '"github.copilot.chat.agent.thinkingTool": false' `
        -replace '"github\.copilot\.nextEditSuggestions\.fixes":\s*true', '"github.copilot.nextEditSuggestions.fixes": false' `
        -replace '"github\.copilot\.chat\.codesearch\.enabled":\s*true', '"github.copilot.chat.codesearch.enabled": false' `
        -replace '"github\.copilot\.chat\.editor\.temporalContext\.enabled":\s*true', '"github.copilot.chat.editor.temporalContext.enabled": false' `
        -replace '"github\.copilot\.chat\.edits\.temporalContext\.enabled":\s*true', '"github.copilot.chat.edits.temporalContext.enabled": false' `
        -replace '"github\.copilot\.nextEditSuggestions\.enabled":\s*true', '"github.copilot.nextEditSuggestions.enabled": false'

    # Guardar nueva configuración
    $newContent | Set-Content $globalSettingsPath -Encoding UTF8

    Write-Host "✅ Configuración global modificada" -ForegroundColor Green
    Write-Host "📝 Cambios aplicados:" -ForegroundColor Cyan
    Write-Host "   - thinkingTool: false" -ForegroundColor White
    Write-Host "   - nextEditSuggestions.fixes: false" -ForegroundColor White
    Write-Host "   - codesearch.enabled: false" -ForegroundColor White
    Write-Host "   - temporalContext: false (ambos)" -ForegroundColor White
    Write-Host "   - nextEditSuggestions.enabled: false" -ForegroundColor White
}
else {
    Write-Host "❌ No se encontró configuración global" -ForegroundColor Red
}

Write-Host "`n🔄 Pasos siguientes:" -ForegroundColor Yellow
Write-Host "   1. Reinicia VS Code completamente (cierra todas las ventanas)" -ForegroundColor White
Write-Host "   2. Abre VS Code de nuevo" -ForegroundColor White
Write-Host "   3. Prueba el menú contextual en Files Changed de Copilot" -ForegroundColor White
Write-Host "   4. Si funciona: problema resuelto ✅" -ForegroundColor White
Write-Host "   5. Si no funciona: restaura backup con restore-backup.ps1" -ForegroundColor White

Write-Host "`n💾 Backup guardado en:" -ForegroundColor Green
Get-ChildItem "$env:APPDATA\Code\User\settings.json.backup*" | Select-Object Name, LastWriteTime | Format-Table
