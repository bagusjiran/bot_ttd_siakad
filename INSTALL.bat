@echo off
title SIAKAD Auto Absensi v2 - Setup
color 0A
echo.
echo  =============================================
echo    SIAKAD KPT Auto Absensi Bot v2 - Setup
echo  =============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python tidak ditemukan!
    echo  Download: https://python.org/downloads
    echo  Centang "Add to PATH" saat install!
    pause & exit /b 1
)

echo  [1/3] Install playwright...
pip install playwright -q
if %errorlevel% neq 0 ( echo  [ERROR] Gagal! & pause & exit /b 1 )

echo  [2/3] Download browser Chromium...
playwright install chromium
if %errorlevel% neq 0 ( echo  [ERROR] Gagal download! & pause & exit /b 1 )

echo  [3/3] Semua siap!
echo.
echo  =============================================
echo   Jalankan: python absensi_bot.py
echo   atau klik 2x: JALANKAN.bat
echo  =============================================
pause
