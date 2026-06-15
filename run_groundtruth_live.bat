@echo off
title GROUNDTRUTH LIVE - results backend + app
echo Starting results backend (needs FOOTBALL_DATA_KEY set)...
start "GROUNDTRUTH backend" cmd /k python "%~dp0server.py"
timeout /t 2 >nul
echo Opening app...
start "" "%~dp0groundtruth.html"
echo.
echo In the app: Scout -^> Settings -^> Results backend URL = http://localhost:8787
exit
