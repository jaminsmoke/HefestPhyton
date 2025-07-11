# Script para restaurar configuración original si es necesario
# restore-backup.ps1

$globalSettingsPath = "$env:APPDATA\Code\User\settings.json"
$backups = Get-ChildItem "$env:APPDATA\Code\User\settings.json.backup*" | Sort-Object LastWriteTime -Descending

if ($backups.Count -gt 0) {
    $latestBackup = $backups[0]
    Write-Host "🔄 Restaurando backup más reciente: $($latestBackup.Name)" -ForegroundColor Yellow

    Copy-Item $latestBackup.FullName $globalSettingsPath -Force
    Write-Host "✅ Configuración restaurada" -ForegroundColor Green
    Write-Host "🔄 Reinicia VS Code para aplicar cambios" -ForegroundColor Cyan
} else {
    Write-Host "❌ No se encontraron backups" -ForegroundColor Red
}
