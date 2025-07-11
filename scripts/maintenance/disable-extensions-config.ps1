# Script para deshabilitar extensiones problemáticas directamente en la configuración
# disable-extensions-config.ps1

Write-Host "🔧 Deshabilitando extensiones problemáticas..." -ForegroundColor Yellow

# Ruta del archivo de configuración de VS Code
$configPath = "$env:APPDATA\Code\User\settings.json"

if (Test-Path $configPath) {
    Write-Host "1. Leyendo configuración actual..." -ForegroundColor Cyan

    $config = Get-Content $configPath -Raw | ConvertFrom-Json

    # Agregar extensiones deshabilitadas
    $disabledExtensions = @(
        "ms-azuretools.vscode-azure-github-copilot",
        "codereviewforgithubcopilot.github-copilot-code-review",
        "ms-vscode.vscode-websearchforcopilot"
    )

    if (-not $config.'extensions.ignoreRecommendations') {
        $config | Add-Member -Type NoteProperty -Name 'extensions.ignoreRecommendations' -Value $true -Force
    }

    # Crear lista de extensiones deshabilitadas
    $config | Add-Member -Type NoteProperty -Name 'extensions.disabled' -Value $disabledExtensions -Force

    # Guardar configuración
    $config | ConvertTo-Json -Depth 10 | Set-Content $configPath

    Write-Host "2. ✅ Configuración actualizada" -ForegroundColor Green
    Write-Host "3. 🔄 Reinicia VS Code para aplicar cambios" -ForegroundColor Yellow
}
else {
    Write-Host "❌ No se encontró el archivo de configuración de VS Code" -ForegroundColor Red
}

Write-Host "`n📋 Extensiones deshabilitadas:" -ForegroundColor Green
foreach ($ext in $disabledExtensions) {
    Write-Host "   - $ext" -ForegroundColor White
}

Write-Host "`n🎯 Para aplicar los cambios:" -ForegroundColor Yellow
Write-Host "   1. Guarda todos tus archivos abiertos" -ForegroundColor White
Write-Host "   2. Cierra completamente VS Code" -ForegroundColor White
Write-Host "   3. Vuelve a abrir VS Code" -ForegroundColor White
Write-Host "   4. Verifica el menú contextual en Source Control" -ForegroundColor White
