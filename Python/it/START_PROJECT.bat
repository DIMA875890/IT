@echo off
title AI Translator Suite

cd /d C:\Python\it

echo [1/2] Launching Telegram Bot...

start "Telegram Bot" cmd /k python main.py

echo [2/2] Launching Flask Dashboard...
start "Flask Server" cmd /k python app.py

echo =========================================
echo All systems are starting! 
echo Keep the other windows open while working.
echo Dashboard is at: http://127.0.0.1:5000
echo =========================================
pause