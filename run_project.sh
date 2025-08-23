#!/bin/bash

echo "========================================"
echo "F1 Weather Analysis Project Runner"
echo "========================================"
echo

echo "Starting F1 Weather Analysis Project..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.8+ and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python found. Checking dependencies..."
echo

# Install requirements if needed
echo "Installing required packages..."
$PYTHON_CMD -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "WARNING: Some packages failed to install"
    echo "Continuing anyway..."
fi

echo
echo "========================================"
echo "STEP 1: Collecting F1 Race Data"
echo "========================================"
echo
echo "This will collect F1 race data from 2020-2024..."
echo
$PYTHON_CMD scripts/01_collect_f1_data.py
if [ $? -ne 0 ]; then
    echo "ERROR: F1 data collection failed"
    exit 1
fi

echo
echo "========================================"
echo "STEP 2: Collecting Weather Data"
echo "========================================"
echo
echo "This will collect weather data for each race location..."
echo
$PYTHON_CMD scripts/02_collect_weather_data.py
if [ $? -ne 0 ]; then
    echo "ERROR: Weather data collection failed"
    exit 1
fi

echo
echo "========================================"
echo "STEP 3: Exporting Data for QGIS"
echo "========================================"
echo
echo "This will process and export data for QGIS mapping..."
echo
$PYTHON_CMD scripts/03_export_for_qgis.py
if [ $? -ne 0 ]; then
    echo "ERROR: QGIS export failed"
    exit 1
fi

echo
echo "========================================"
echo "PROJECT COMPLETED SUCCESSFULLY!"
echo "========================================"
echo
echo "Your F1 weather analysis is ready!"
echo
echo "Next steps:"
echo "1. Open the Jupyter notebooks in the 'notebooks' folder"
echo "2. Run the analysis notebooks for detailed insights"
echo "3. Use QGIS to create maps (see qgis_guide.md)"
echo "4. Check the 'results' folder for generated plots"
echo "5. Review 'data/processed' for cleaned datasets"
echo
echo "Files created:"
echo "- F1 race data: data/raw/f1_races_2020_2024.csv"
echo "- Weather data: data/raw/f1_weather_data_2020_2024.csv"
echo "- QGIS exports: data/qgis_export/"
echo "- Processed data: data/processed/"
echo
echo "Happy analyzing! 🏎️🌧️📊"
echo
