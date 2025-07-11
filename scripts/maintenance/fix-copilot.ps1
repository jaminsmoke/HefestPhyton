# Script para solucionar problemas de GitHub Copilot
# Ejecutar con: PowerShell -ExecutionPolicy Bypass .\fix-copilot.ps1

Write-Host "🔧 Solucionando problemas de GitHub Copilot..." -ForegroundColor Yellow

# 1. Limpiar caché de VS Code
Write-Host "1. Limpiando caché de VS Code..." -ForegroundColor Cyan
$vscodeCache = "$env:APPDATA\Code\CachedExtensionVSIXs"
if (Test-Path $vscodeCache) {
    Get-ChildItem -Path $vscodeCache -Filter "*copilot*" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "   ✅ Caché limpiada" -ForegroundColor Green
}

# 2. Limpiar logs de Copilot
Write-Host "2. Limpiando logs de Copilot..." -ForegroundColor Cyan
$logsPath = "$env:APPDATA\Code\logs"
if (Test-Path $logsPath) {
    Get-ChildItem -Path $logsPath -Recurse -Filter "*copilot*" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "   ✅ Logs limpiados" -ForegroundColor Green
}

# 3. Limpiar archivos temporales del workspace
Write-Host "3. Limpiando archivos temporales del workspace..." -ForegroundColor Cyan
if (Test-Path ".\.vscode") {
    Remove-Item -Path ".\.vscode\*.tmp" -Force -ErrorAction SilentlyContinue
    Remove-Item -Path ".\.vscode\*.log" -Force -ErrorAction SilentlyContinue
    Write-Host "   ✅ Temporales del workspace limpiados" -ForegroundColor Green
}

# 4. Verificar estado de Git
Write-Host "4. Verificando estado de Git..." -ForegroundColor Cyan
$gitStatus = git status --porcelain 2>$null
if ($gitStatus) {
    $modifiedCount = ($gitStatus | Where-Object { $_ -match "^ M" }).Count
    $untrackedCount = ($gitStatus | Where-Object { $_ -match "^\?\?" }).Count
    Write-Host "   📊 Archivos modificados: $modifiedCount" -ForegroundColor White
    Write-Host "   📊 Archivos sin rastrear: $untrackedCount" -ForegroundColor White
}
else {
    Write-Host "   ✅ Repositorio limpio" -ForegroundColor Green
}

Write-Host "`n🎯 Soluciones aplicadas:" -ForegroundColor Green
Write-Host "   1. Caché de extensiones limpiada" -ForegroundColor White
Write-Host "   2. Logs de Copilot eliminados" -ForegroundColor White
Write-Host "   3. Archivos temporales removidos" -ForegroundColor White
Write-Host "   4. Estado de Git verificado" -ForegroundColor White

Write-Host "`n📋 Pasos manuales recomendados:" -ForegroundColor Yellow
Write-Host "   1. Reinicia VS Code (Ctrl+Shift+P → 'Developer: Reload Window')" -ForegroundColor White
Write-Host "   2. Verifica que Copilot esté habilitado en extensiones" -ForegroundColor White
Write-Host "   3. Si persiste: Ctrl+Shift+P → 'GitHub Copilot: Reset Authentication'" -ForegroundColor White

Write-Host "`n✨ Script completado!" -ForegroundColor Green
