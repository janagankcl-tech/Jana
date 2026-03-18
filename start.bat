@echo off
REM Invoice Generator — start script for Windows
REM Double-click this file to launch

cd /d "%~dp0"
pip install -r requirements.txt -q
python app.py
pause
