@echo off
title Estudio de Criativos
chcp 65001 >nul
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
  "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -I "%~dp0app.py"
) else (
  py -3.12 -I "%~dp0app.py"
)
pause
