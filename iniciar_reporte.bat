@echo off
title Entrega de Turno ASRS v2
echo ========================================================
echo   Iniciando Servidor Entrega de Turno ASRS v2
echo ========================================================
cd /d "%~dp0"
start "" http://localhost:8050
python server.py
pause
