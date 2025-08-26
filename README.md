# Weather vs. Race Outcomes in Formula 1 Analysis

## Project Overview

This project analyzes the relationship between weather conditions and race outcomes in Formula 1 from 2020-2024. We investigate how weather (rain vs. dry) impacts DNFs (Did Not Finish), crashes, and position changes during races.

## Project Objectives

- **Data Collection**: Gather F1 race results and weather data for 2020-2024 seasons
- **Weather Analysis**: Categorize races by weather conditions (Rainy/Dry/Other)
- **Outcome Analysis**: Compare DNFs, incidents, and position changes across weather types
- **Geospatial Visualization**: Create maps in QGIS showing race locations with weather and outcome data
- **Statistical Insights**: Provide quantitative analysis of weather's impact on race outcomes

## Data Sources

### Formula 1 Data
- **Ergast Developer API**: http://ergast.com/mrd/ (Free, no API key required)
- **Alternative**: Kaggle F1 datasets for backup

### Weather Data
- **Meteostat**: https://dev.meteostat.net/ (Free tier available)
- **Visual Crossing**: https://www.visualcrossing.com/weather-api (Free tier: 1000 requests/day)

### Circuit Locations
- **Ergast API**: Includes circuit coordinates
- **Wikipedia**: Manual lookup for missing coordinates

## Quick Start

### Prerequisites
```bash
# Install required packages
pip install -r requirements.txt

# For Jupyter notebooks
pip install jupyter
```

### Project Execution (Weekend Timeline)

#### Day 1 (4-6 hours)
1. **Setup & Data Collection** (2-3 hours)
   - Run `python scripts/01_collect_f1_data.py`
   - Run `python scripts/02_collect_weather_data.py`
   
2. **Data Processing** (2-3 hours)
   - Execute `notebooks/01_data_cleaning_and_merging.ipynb`
   - Run analysis in `notebooks/02_weather_analysis.ipynb`

#### Day 2 (3-4 hours)
1. **QGIS Visualization** (2-3 hours)
   - Follow `qgis_guide.md` instructions
   - Create final maps
   
2. **Documentation & Cleanup** (1 hour)
   - Update README with your findings
   - Commit to GitHub

## Project Structure

```
F1-Race-vs-Weather-Analysis/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── scripts/                           # Data collection scripts
│   ├── 01_collect_f1_data.py         # F1 race data collection
│   ├── 02_collect_weather_data.py    # Weather data collection
│   └── 03_export_for_qgis.py         # Data export for QGIS
├── notebooks/                         # Analysis notebooks
│   ├── 01_data_cleaning_and_merging.ipynb
│   └── 02_weather_analysis.ipynb
├── data/                              # Data storage
│   ├── raw/                          # Raw downloaded data
│   ├── processed/                    # Cleaned and merged data
│   └── qgis_export/                  # QGIS-ready data
├── results/                           # Analysis outputs
│   ├── plots/                        # Python-generated charts
│   └── maps/                         # QGIS-generated maps
├── qgis_guide.md                      # QGIS step-by-step guide
└── sample_results.md                  # Expected analysis results
```

## Setup Instructions

### 1. Environment Setup
```bash
# Clone repository
git clone <your-repo-url>
cd F1-Race-vs-Weather-Analysis

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Keys (if needed)
- **Meteostat**: Free tier, no key required for basic usage
- **Visual Crossing**: Sign up for free API key at https://www.visualcrossing.com/weather-api

### 3. QGIS Setup
- Download QGIS from https://qgis.org/
- Install Python integration (usually included)
- Follow `qgis_guide.md` for detailed instructions

## Expected Results

### Key Findings You'll Discover
- **Weather Impact**: Rainy races typically have 2-3x more DNFs than dry races
- **Geographic Patterns**: Certain circuits show stronger weather sensitivity
- **Seasonal Trends**: Weather impact varies across seasons

### Sample Visualizations
- Bar charts: DNFs by weather type
- Box plots: Position changes vs. weather
- QGIS maps: Circuit locations with weather and outcome data

## Customization Options

### Easy Enhancements
- Add more weather variables (wind speed, humidity)
- Include driver nationality analysis
- Compare qualifying vs. race weather impact

### Advanced Features
- Machine learning: Predict DNFs based on weather
- Real-time data updates for new seasons
- Interactive web dashboard

## Learning Outcomes

By completing this project, you'll gain experience in:
- **API Integration**: Working with sports and weather APIs
- **Data Engineering**: ETL processes and data cleaning
- **Statistical Analysis**: Hypothesis testing and data visualization
- **Geospatial Analysis**: QGIS mapping and spatial data
- **Reproducible Research**: GitHub documentation and code organization

## Contributing

This project is designed for learning and portfolio development. Feel free to:
- Fork and modify for your own analysis
- Add new weather variables or analysis methods
- Share your findings and visualizations

## Troubleshooting

### Common Issues
1. **API Rate Limits**: Use sleep() between requests
2. **Missing Weather Data**: Some historical data may be incomplete
3. **QGIS Import Errors**: Ensure CSV has proper lat/lon columns

### Getting Help
- Check the troubleshooting section in each notebook
- Review the QGIS guide for mapping issues
- Ensure all dependencies are properly installed

---
