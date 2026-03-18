#!/bin/bash
# Invoice Generator — start script for Mac/Linux
# Just double-click this file (or run: bash start.sh)

cd "$(dirname "$0")"
pip install -r requirements.txt -q
python app.py
