#!/bin/bash
# Invoice Generator — start script for Mac/Linux
# Just double-click this file (or run: bash start.sh)

cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt -q
python3 app.py
