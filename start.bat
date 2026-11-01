@echo off
rem Double-click to open the presentation. Close the server window to stop it.
cd /d "%~dp0"
start "HiLegal deck server (close to stop)" powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\serve.ps1" -Port 8000
timeout /t 2 /nobreak >nul
start "" "http://localhost:8000/"
