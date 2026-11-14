@echo off
rem Lanceur de la commande sentiment.
rem Ce fichier est installe a cote du dossier python\ du Python embarque.
rem Il n'utilise pas le Python du systeme : il appelle explicitement le Python embarque.

set "SCRIPT_DIR=%~dp0"
set "PYTHON=%SCRIPT_DIR%python\python.exe"

if not exist "%PYTHON%" (
    echo ERREUR : Python embarque introuvable dans %SCRIPT_DIR%python\
    exit /b 1
)

"%PYTHON%" -m sentiment_app.cli %*
exit /b %ERRORLEVEL%

