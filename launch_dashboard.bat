@echo off
echo ========================================
echo   GANDI COMMAND CENTER - Starting...
echo ========================================
echo.

REM Navigate to dashboard folder
cd /d "C:\Users\gandi\.claude\dashboard\streamlit"

REM Launch Streamlit using full path
echo Starting Streamlit dashboard...
echo.
echo Dashboard will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

"C:\Users\gandi\AppData\Roaming\Python\Python314\Scripts\streamlit.exe" run gandi_command_center.py --server.port 8501

pause
