@echo off
echo ========================================================
echo                 IMAGE WATERMARKING TOOL
echo ========================================================
echo.
echo HOW TO USE:
echo 1. Place your images in the "To be watermarked" folder
echo 2. This script will add watermarks to all images
echo 3. Watermarked images will be saved in the "Watermarked" folder
echo.
echo --------------------------------------------------------
echo Running Watermark Script...
echo --------------------------------------------------------
echo.

python watermark.py

echo.
echo --------------------------------------------------------
echo Watermarking process completed!
echo.
echo Press any key to exit...
pause > nul 