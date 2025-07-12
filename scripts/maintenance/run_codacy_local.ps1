# Script para ejecutar análisis local de Codacy usando Docker
# Este script ejecuta el CLI de Codacy en la rama actual

Write-Host "🔍 ANÁLISIS LOCAL DE CODACY - RAMA ACTUAL" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Verificar que Docker esté ejecutándose
Write-Host "📋 Verificando Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker version --format "{{.Client.Version}}"
    Write-Host "✅ Docker versión: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker no está ejecutándose. Iniciando Docker Desktop..." -ForegroundColor Red
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    Write-Host "⏳ Esperando que Docker se inicie..." -ForegroundColor Yellow
    Start-Sleep 30
}

# Información de la rama actual
$currentBranch = git branch --show-current
$currentCommit = git rev-parse HEAD

Write-Host "🌿 Rama actual: $currentBranch" -ForegroundColor Green
Write-Host "📝 Commit: $($currentCommit.Substring(0,8))" -ForegroundColor Green

# Crear directorio para resultados
$resultsDir = "codacy-results"
if (-not (Test-Path $resultsDir)) {
    New-Item -ItemType Directory -Path $resultsDir
}

Write-Host "🔍 Ejecutando análisis de Codacy..." -ForegroundColor Yellow

# Ejecutar análisis de duplicación específicamente
Write-Host "📊 Analizando duplicación de código..." -ForegroundColor Cyan
try {
    docker run --rm -v "${PWD}:/src" codacy/codacy-analysis-cli:latest analyze `
        --directory /src `
        --tool duplication `
        --format json `
        --output /src/codacy-results/duplication-analysis.json `
        --verbose
        
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Análisis de duplicación completado" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Análisis completado con warnings" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error en análisis de duplicación: $_" -ForegroundColor Red
}

# Ejecutar análisis completo
Write-Host "🔍 Ejecutando análisis completo..." -ForegroundColor Cyan
try {
    docker run --rm -v "${PWD}:/src" codacy/codacy-analysis-cli:latest analyze `
        --directory /src `
        --format json `
        --output /src/codacy-results/full-analysis.json `
        --max-allowed-issues 5000 `
        --verbose
        
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Análisis completo completado" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Análisis completado con warnings" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error en análisis completo: $_" -ForegroundColor Red
}

Write-Host "📁 Resultados guardados en: $resultsDir" -ForegroundColor Cyan
Write-Host "🎉 Análisis local completado" -ForegroundColor Green
