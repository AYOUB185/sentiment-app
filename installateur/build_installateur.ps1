<#
.SYNOPSIS
    Construit l'installateur Windows pour sentiment-app.

.DESCRIPTION
    Etapes :
      1. Verification des prerequis (roue, Inno Setup)
      2. Telechargement et configuration du Python embarque
      3. Installation de la roue et de ses dependances
      4. Verification locale (sentiment.cmd)
      5. Compilation de l'installateur via Inno Setup (sauf -SansCompilation)

.PARAMETER Roue
    Chemin de la roue .whl. Par defaut : la plus recente de dist\.

.PARAMETER PythonVersion
    Version du Python embarque. Par defaut : version du venv actif.
    Forcer 3.11.9 si votre Python est 3.11.10 ou plus recent.

.PARAMETER SansCompilation
    Prepare build\app sans lancer Inno Setup.
#>

param(
    [string]$Roue = "",
    [string]$PythonVersion = "",
    [switch]$SansCompilation
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RACINE = Split-Path $PSScriptRoot -Parent
$BUILD_APP = Join-Path $PSScriptRoot "build\app"
$PYTHON_DIR = Join-Path $BUILD_APP "python"
$ISCC = "C:\Users\Hp\AppData\Local\Programs\Inno Setup 6\ISCC.exe"
if (-not (Test-Path $ISCC)) {
    $ISCC = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
}
if (-not (Test-Path $ISCC)) {
    $ISCC = "C:\Program Files\Inno Setup 6\ISCC.exe"
}

function Etape($msg) { Write-Host "`n=== $msg ===" -ForegroundColor Cyan }
function OK($msg)    { Write-Host "OK  $msg" -ForegroundColor Green }
function ECHEC($msg) { Write-Host "ECHEC  $msg" -ForegroundColor Red; exit 1 }

# ── Etape 1 : Verifications ──────────────────────────────────────────────────
Etape "1. Verifications"

# Trouver la roue
if ($Roue -eq "") {
    $roues = @(Get-ChildItem (Join-Path $RACINE "dist") -Filter "sentiment_app-*.whl" -ErrorAction SilentlyContinue |
             Sort-Object LastWriteTime -Descending)
    if ($roues.Count -eq 0) { ECHEC "Aucune roue dans dist\. Lancez : python -m build" }
    $Roue = $roues[0].FullName
}
if (-not (Test-Path $Roue)) { ECHEC "Roue introuvable : $Roue" }
$nomRoue = Split-Path $Roue -Leaf
# Extraire version depuis nom : sentiment_app-1.0.0-py3-none-any.whl
$version = ($nomRoue -split "-")[1]
OK "roue : $nomRoue  (version $version)"

# Trouver Python actif
if ($PythonVersion -eq "") {
    $pyExe = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $pyExe) {
        # Essayer le venv
        $pyExe = Join-Path $RACINE ".venv\Scripts\python.exe"
    }
    if (Test-Path $pyExe) {
        $ver = & $pyExe -c "import sys; v=sys.version_info; print(f'{v.major}.{v.minor}.{v.micro}')"
        $PythonVersion = $ver.Trim()
    } else {
        ECHEC "Python introuvable. Activez le venv ou specifiez -PythonVersion 3.11.9"
    }
}
OK "python : $PythonVersion"

# Inno Setup
if (-not $SansCompilation) {
    if (-not (Test-Path $ISCC)) { ECHEC "Inno Setup introuvable. Installez-le via : winget install JRSoftware.InnoSetup" }
    OK "Inno Setup : $ISCC"
}

# Calculer l'URL du Python embarque
$parts = $PythonVersion -split "\."
$major = $parts[0]; $minor = $parts[1]; $patch = $parts[2]
$pyZipName = "python-$PythonVersion-embed-amd64.zip"
$pyUrl = "https://www.python.org/ftp/python/$PythonVersion/$pyZipName"

# ── Etape 2 : Python embarque ─────────────────────────────────────────────────
Etape "2. Python embarque ($PythonVersion)"

if (Test-Path $BUILD_APP) { Remove-Item $BUILD_APP -Recurse -Force }
New-Item -ItemType Directory -Force -Path $PYTHON_DIR | Out-Null

$zipPath = Join-Path $env:TEMP $pyZipName
if (-not (Test-Path $zipPath)) {
    Write-Host "Telechargement $pyUrl ..."
    Invoke-WebRequest -Uri $pyUrl -OutFile $zipPath -UseBasicParsing
}
Expand-Archive -Path $zipPath -DestinationPath $PYTHON_DIR -Force

# Réécrire python3xx._pth pour activer site-packages
$pthFile = Get-ChildItem $PYTHON_DIR -Filter "python3*._pth" | Select-Object -First 1
if (-not $pthFile) { ECHEC "Fichier .pth introuvable dans le Python embarque" }
$pthName = $pthFile.Name
$shortVer = "python$($major)$($minor)"  # e.g. python311
# Ecrire SANS BOM (ASCII) : le BOM corrompt le chemin de python311.zip
[System.IO.File]::WriteAllText($pthFile.FullName, "$shortVer.zip`r`n.`r`nLib\site-packages`r`n", [System.Text.Encoding]::ASCII)
OK "$pthName : $shortVer.zip ; . ; Lib\site-packages"

# ── Etape 3 : Installation des dependances ────────────────────────────────────
Etape "3. Installation (pip install --target)"

$sitePackages = Join-Path $PYTHON_DIR "Lib\site-packages"
New-Item -ItemType Directory -Force -Path $sitePackages | Out-Null

# Utiliser le pip du venv pour installer vers --target (pas besoin de pip dans le Python embarque)
$venvPip = Join-Path $RACINE ".venv\Scripts\pip.exe"
if (-not (Test-Path $venvPip)) { ECHEC "pip du venv introuvable : activez le venv" }

# Lire les versions exactes du venv actif
$freeze = & $venvPip freeze 2>$null
$skVerLine  = $freeze | Where-Object { $_ -match "^scikit.learn==" } | Select-Object -First 1
$joblibLine = $freeze | Where-Object { $_ -match "^joblib==" }       | Select-Object -First 1
$npLine     = $freeze | Where-Object { $_ -match "^numpy==" }        | Select-Object -First 1
$skVer     = if ($skVerLine)  { ($skVerLine  -split "==")[1].Trim() } else { "1.5.2" }
$joblibVer = if ($joblibLine) { ($joblibLine -split "==")[1].Trim() } else { "1.4.2" }
$npVer     = if ($npLine)     { ($npLine     -split "==")[1].Trim() } else { "" }

Write-Host "Contraintes : scikit-learn==$skVer  joblib==$joblibVer  numpy==$npVer"

# Installer vers site-packages du Python embarque
& $venvPip install `
    --target $sitePackages `
    --platform win_amd64 `
    --python-version 3.11 `
    --only-binary=:all: `
    --upgrade `
    "scikit-learn==$skVer" "joblib==$joblibVer" $Roue

if ($LASTEXITCODE -ne 0) { ECHEC "pip install a echoue (code $LASTEXITCODE)" }
OK "dependances installees dans $sitePackages"

# ── Etape 4 : Lanceur sentiment.cmd ──────────────────────────────────────────
Etape "4. Lanceur sentiment.cmd"

$cmdSrc = Join-Path $PSScriptRoot "sentiment.cmd"
$cmdDst = Join-Path $BUILD_APP "sentiment.cmd"
Copy-Item $cmdSrc $cmdDst
OK "sentiment.cmd copie"

# LISEZMOI.txt
$lisezmoi = Join-Path $PSScriptRoot "LISEZMOI.txt"
if (Test-Path $lisezmoi) {
    Copy-Item $lisezmoi (Join-Path $BUILD_APP "LISEZMOI.txt")
    OK "LISEZMOI.txt copie"
}

# Verification locale
Write-Host "Test local..."
$testCmd = Join-Path $BUILD_APP "sentiment.cmd"
$result = & cmd /c `"$testCmd`" --version 2>&1
if ($LASTEXITCODE -eq 0) { OK "sentiment --version : $result" } else { ECHEC "sentiment.cmd --version a echoue : $result" }

$result2 = & cmd /c `"$testCmd`" --json "Livraison rapide tres satisfait" 2>&1
if ($result2 -match '"label"') { OK "predict OK : $result2" } else { ECHEC "predict a echoue : $result2" }

$tailleMo = [math]::Round((Get-ChildItem $BUILD_APP -Recurse | Measure-Object Length -Sum).Sum / 1MB, 1)
OK "dossier build\app : ${tailleMo} Mo"

if ($SansCompilation) {
    Write-Host "`nMode -SansCompilation : build\app pret, Inno Setup non lance." -ForegroundColor Yellow
    exit 0
}

# ── Etape 5 : Compilation Inno Setup ─────────────────────────────────────────
Etape "5. Compilation Inno Setup"

$issFile = Join-Path $PSScriptRoot "sentiment.iss"
& $ISCC $issFile
if ($LASTEXITCODE -ne 0) { ECHEC "Inno Setup a echoue (code $LASTEXITCODE)" }

$outputExe = Join-Path $PSScriptRoot "Output\sentiment-app-$version-setup.exe"
if (Test-Path $outputExe) {
    OK "Installateur : $outputExe"
} else {
    # Chercher l'exe genere
    $exes = Get-ChildItem (Join-Path $PSScriptRoot "Output") -Filter "*.exe" -ErrorAction SilentlyContinue
    if ($exes.Count -gt 0) { OK "Installateur : $($exes[0].FullName)" }
    else { ECHEC "Fichier setup.exe introuvable dans Output\" }
}
Write-Host "`nTermine !" -ForegroundColor Green
