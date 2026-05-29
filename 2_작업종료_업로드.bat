@echo off
echo ====================================================
echo [1] Cleaning up completed media files to save space...
echo ====================================================
if exist "D:\antigravity\InsureTech_Labs\creative_assets" (
    rd /s /q "D:\antigravity\InsureTech_Labs\creative_assets"
)
mkdir "D:\antigravity\InsureTech_Labs\creative_assets"
echo Cleanup complete!

echo.
echo ====================================================
echo [2] Uploading today's work to GitHub...
echo ====================================================
git add .
git commit -m "Auto sync and cleanup completed assets"
git push origin main
echo.
echo Upload Complete! You can close this window.
pause
