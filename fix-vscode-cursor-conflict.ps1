# Script para configurar VS Code correctamente y solucionar conflictos con Cursor
# fix-vscode-cursor-conflict.ps1

Write-Host "🔧 Configurando VS Code correctamente..." -ForegroundColor Yellow

# 1. Configurar VS Code como editor por defecto de Git
Write-Host "1. Configurando Git para usar VS Code..." -ForegroundColor Cyan
$vscodePath = "C:\Users\$env:USERNAME\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"
git config --global core.editor "$vscodePath --wait"
Write-Host "   ✅ Git configurado para VS Code" -ForegroundColor Green

# 2. Limpiar PATH de conflictos con Cursor
Write-Host "2. Verificando PATH..." -ForegroundColor Cyan
$cursorInPath = $env:PATH -match "cursor"
if ($cursorInPath) {
    Write-Host "   ⚠️  Cursor detectado en PATH - puede causar conflictos" -ForegroundColor Yellow
}
else {
    Write-Host "   ✅ PATH limpio" -ForegroundColor Green
}

# 3. Verificar extensiones problemáticas deshabilitadas
Write-Host "3. Verificando extensiones..." -ForegroundColor Cyan
$extensions = & "$vscodePath" --list-extensions
$problematicas = @(
    "ms-azuretools.vscode-azure-github-copilot",
    "codereviewforgithubcopilot.github-copilot-code-review",
    "ms-vscode.vscode-websearchforcopilot"
)

foreach ($ext in $problematicas) {
    if ($extensions -contains $ext) {
        Write-Host "   ⚠️  $ext aún habilitada - deshabilitando..." -ForegroundColor Yellow
        & "$vscodePath" --disable-extension $ext
    }
    else {
        Write-Host "   ✅ $ext no encontrada o ya deshabilitada" -ForegroundColor Green
    }
}

# 4. Verificar extensiones básicas de Copilot
Write-Host "4. Verificando Copilot básico..." -ForegroundColor Cyan
$copilotBasic = @("github.copilot", "github.copilot-chat")
foreach ($ext in $copilotBasic) {
    if ($extensions -contains $ext) {
        Write-Host "   ✅ $ext habilitada" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ $ext no encontrada" -ForegroundColor Red
    }
}

Write-Host "`n📋 Resumen de cambios:" -ForegroundColor Green
Write-Host "   1. Git configurado para usar VS Code" -ForegroundColor White
Write-Host "   2. Extensiones problemáticas deshabilitadas" -ForegroundColor White
Write-Host "   3. Copilot básico verificado" -ForegroundColor White

Write-Host "`n🎯 Pasos siguientes:" -ForegroundColor Yellow
Write-Host "   1. Reinicia VS Code (cierra todas las ventanas y abre de nuevo)" -ForegroundColor White
Write-Host "   2. Verifica que el menú contextual de Copilot funcione" -ForegroundColor White
Write-Host "   3. Si persiste: File → Preferences → Extensions → busca las extensiones deshabilitadas" -ForegroundColor White

Write-Host "`n✨ Configuración completada!" -ForegroundColor Green
