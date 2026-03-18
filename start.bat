@echo off
REM Invoice Generator — start script for Windows
REM Double-click this file to launch

cd /d "%~dp0"
py -m pip install -r requirements.txt -q
py app.py
pause
