@echo off
REM ============================================================
REM  BALLS FIGHTING Z - launcher
REM  Serves the game with NO-CACHE headers so you never get
REM  stuck on an old version, then opens it in your browser.
REM ============================================================
cd /d "%~dp0"

set PORT=8777
set URL=http://localhost:%PORT%/index.html

REM Kill anything already holding the port
for /f "tokens=5" %%p in ('netstat -ano ^| findstr "127.0.0.1:%PORT%" ^| findstr LISTENING') do (
    taskkill /F /PID %%p >nul 2>nul
)

echo Starting BALLS FIGHTING Z (no-cache)...
echo.

REM Prefer Node, fall back to Python
where node >nul 2>nul
if %errorlevel%==0 (
    start "" /min node "%~dp0server.js"
    goto :wait
)

where py >nul 2>nul
if %errorlevel%==0 (
    start "" /min py "%~dp0server.py"
    goto :wait
)

where python >nul 2>nul
if %errorlevel%==0 (
    start "" /min python "%~dp0server.py"
    goto :wait
)

REM Nothing installed - the game is a single self-contained file,
REM so it still works opened straight from disk.
echo No Python or Node found.
echo Opening index.html directly instead - the game needs no server.
start "" "%~dp0index.html"
exit /b 0

:wait
echo Waiting for the server...
timeout /t 2 /nobreak >nul
start "" "%URL%"
echo.
echo Game opened: %URL%
echo.
echo   L = toggle Lite graphics (fastest)
echo   G = cycle graphics quality
echo.
echo Leave this window open while playing. Close it to stop the server.
echo.
pause