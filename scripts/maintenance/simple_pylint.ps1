# Script simple para ejecutar PyLint
param([string]$Path = "src")

$VenvPath = "$PSScriptRoot\..\.venv\Scripts\pylint.exe"
$ConfigPath = "$PSScriptRoot\..\development-config\.pylintrc"

Write-Host "Ejecutando PyLint en: $Path" -ForegroundColor Green

if (Test-Path $VenvPath) {
    & $VenvPath --rcfile=$ConfigPath $Path
} else {
    Write-Host "Error: PyLint no encontrado" -ForegroundColor Red
}
