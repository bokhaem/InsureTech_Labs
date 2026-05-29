@echo off
echo ====================================================
echo [2] Uploading today's work to GitHub...
echo ====================================================
git add .
git commit -m "Auto sync from batch file"
git push origin main
echo.
echo Upload Complete! You can close this window.
pause
