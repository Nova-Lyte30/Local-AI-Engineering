@echo off
setlocal
chcp 65001 >nul
where pwsh >nul 2>&1
if %errorlevel%==0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0llama-oneclick.example.ps1" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0llama-oneclick.example.ps1" %*
)
exit /b %errorlevel%
