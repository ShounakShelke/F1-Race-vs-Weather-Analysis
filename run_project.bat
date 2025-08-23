@echo off
echo ========================================
echo F1 Weather Analysis Project Runner
echo ========================================
echo.

echo Starting F1 Weather Analysis Project...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found. Checking dependencies...
echo.

REM Install requirements if needed
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages failed to install
    echo Continuing anyway...
)

echo.
echo ========================================
echo STEP 1: Collecting F1 Race Data
echo ========================================
echo.
echo This will collect F1 race data from 2020-2024...
echo.
python scripts/01_collect_f1_data.py
if errorlevel 1 (
    echo ERROR: F1 data collection failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 2: Collecting Weather Data
echo ========================================
echo.
echo This will collect weather data for each race location...
echo.
python scripts/02_collect_weather_data.py
if errorlevel 1 (
    echo ERROR: Weather data collection failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 3: Exporting Data for QGIS
echo ========================================
echo.
echo This will process and export data for QGIS mapping...
echo.
python scripts/03_export_for_qgis.py
if errorlevel 1 (
    echo ERROR: QGIS export failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo PROJECT COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Your F1 weather analysis is ready!
echo.
echo Next steps:
echo 1. Open the Jupyter notebooks in the 'notebooks' folder
echo 2. Run the analysis notebooks for detailed insights
echo 3. Use QGIS to create maps (see qgis_guide.md)
echo 4. Check the 'results' folder for generated plots
echo 5. Review 'data/processed' for cleaned datasets
echo.
echo Files created:
echo - F1 race data: data/raw/f1_races_2020_2024.csv
echo - Weather data: data/raw/f1_weather_data_2020_2024.csv
echo - QGIS exports: data/qgis_export/
echo - Processed data: data/processed/
echo.
echo Happy analyzing! ��️🌧️📊
echo.
pause
