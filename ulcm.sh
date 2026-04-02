#!/bin/bash
# ULCM Cost Dashboard — launch script for Mac/Linux
# Run from Terminal:  bash ulcm.sh
# Or make executable: chmod +x ulcm.sh  then  ./ulcm.sh

cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt -q
OPEN_PATH=/ulcm python3 app.py
