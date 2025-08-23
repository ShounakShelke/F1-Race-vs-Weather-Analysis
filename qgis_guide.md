# QGIS Guide for F1 Weather Analysis

## 🗺️ Overview

This guide will walk you through importing and visualizing your F1 weather analysis data in QGIS. You'll create professional maps showing race locations, weather conditions, and race outcomes.

## 📋 Prerequisites

- **QGIS Installed**: Download from [qgis.org](https://qgis.org/)
- **Data Ready**: Ensure you've run the data collection and analysis scripts
- **Exported Files**: Check that QGIS export files exist in `data/qgis_export/`

## 🚀 Quick Start (5 minutes)

### Method 1: Drag and Drop (Easiest)
1. Open QGIS
2. Navigate to your project folder: `data/qgis_export/`
3. Drag `f1_races_simple.geojson` into the QGIS map canvas
4. Your F1 race data is now loaded and ready!

### Method 2: Layer Menu
1. In QGIS: **Layer → Add Layer → Add Vector Layer**
2. Browse to `data/qgis_export/f1_races_simple.geojson`
3. Click "Open"

## 📊 Understanding Your Data

The exported data contains these key fields:

| Field | Description | Example |
|-------|-------------|---------|
| `circuit_lat` | Latitude coordinate | 51.5139 |
| `circuit_lng` | Longitude coordinate | -0.1776 |
| `circuit_name` | Race circuit name | "Silverstone Circuit" |
| `weather_category` | Weather condition | "Light Rain", "Dry" |
| `dnf_count` | DNFs in the race | 3 |
| `temperature_avg` | Average temperature | 18.5 |
| `precipitation` | Rainfall amount (mm) | 2.3 |
| `is_rainy` | Binary rainy indicator | True/False |

## 🎨 Creating Your First Map

### Step 1: Basic Styling
1. **Right-click** on your layer in the Layers panel
2. Select **"Properties"**
3. Go to **"Symbology"** tab
4. Choose **"Categorized"** renderer
5. Set **"Value"** to `weather_category`
6. Click **"Classify"**
7. **Apply** and **OK**

### Step 2: Color by Weather
- **Dry**: Green (representing good conditions)
- **Light Rain**: Light Blue (moderate impact)
- **Heavy Rain**: Dark Blue (high impact)
- **Drizzle**: Sky Blue (minimal impact)
- **Cold**: Gray (temperature impact)

### Step 3: Size by DNFs
1. Go to **"Symbology"** → **"Size"**
2. Choose **"Graduated"**
3. Set **"Size"** to `dnf_count`
4. Set range: 0-5 DNFs
5. **Apply**

## 🗺️ Advanced Mapping Techniques

### 1. Layer Labels
1. **Properties** → **"Labels"** tab
2. Check **"Single labels"**
3. Set **"Label with"** to `circuit_name`
4. **Font**: Arial, 10pt
5. **Color**: Dark Blue
6. **Buffer**: White, 1mm

### 2. Popup Information
1. **Properties** → **"Fields"** tab
2. Check **"Index"** for fields you want visible
3. **Apply** and **OK**
4. Use **"Identify Features"** tool to click on points

### 3. Attribute Table
1. **Right-click** layer → **"Open Attribute Table"**
2. View all data in spreadsheet format
3. **Filter** by weather type or season
4. **Select** specific races for analysis

## 🌍 Adding Base Maps

### OpenStreetMap (Free)
1. **Layer** → **Add Layer** → **Add XYZ Layer**
2. **URL**: `https://tile.openstreetmap.org/{z}/{x}/{y}.png`
3. **Name**: "OpenStreetMap"
4. **Click OK**

### Satellite Imagery
1. **Layer** → **Add Layer** → **Add XYZ Layer**
2. **URL**: `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`
3. **Name**: "Satellite"
4. **Click OK**

## 📈 Creating Analysis Maps

### Map 1: Weather Impact Overview
- **Title**: "F1 Weather Impact Analysis 2020-2024"
- **Subtitle**: "Race locations colored by weather, sized by DNFs"
- **Legend**: Weather categories and DNF ranges
- **Scale Bar**: Kilometers
- **North Arrow**: Standard orientation

### Map 2: Circuit Sensitivity
- **Focus**: Circuits most affected by weather
- **Styling**: Color by DNF difference (rainy vs dry)
- **Labels**: Circuit names and DNF statistics

### Map 3: Seasonal Patterns
- **Filter**: By season (2020, 2021, 2022, 2023, 2024)
- **Styling**: Consistent color scheme across seasons
- **Analysis**: Compare weather patterns over time

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Coordinates Not Displaying
- **Problem**: Points appear in wrong location
- **Solution**: Check CRS is set to EPSG:4326 (WGS84)
- **Fix**: Right-click layer → **"Set Layer CRS"** → **"EPSG:4326"**

#### 2. Missing Data
- **Problem**: Some races don't show up
- **Solution**: Check for missing coordinates in your data
- **Fix**: Filter out records with NULL lat/lng values

#### 3. Slow Performance
- **Problem**: Large dataset causes lag
- **Solution**: Use the simplified dataset (`f1_races_simple.geojson`)
- **Fix**: Filter by season or weather type

#### 4. Styling Not Applied
- **Problem**: Changes don't appear on map
- **Solution**: Click **"Apply"** before **"OK"**
- **Fix**: Refresh the map view

### Data Quality Checks
1. **Coordinate Range**: Lat: -90 to 90, Lng: -180 to 180
2. **Missing Values**: Check for NULL in key fields
3. **File Size**: Large files may need simplification
4. **Format**: Ensure GeoJSON is valid

## 📊 Exporting Your Maps

### Print Layout
1. **Project** → **New Print Layout**
2. **Add Map**: Drag map canvas to layout
3. **Add Legend**: Include weather categories
4. **Add Title**: Descriptive map title
5. **Export**: PNG, PDF, or SVG format

### Web Maps
1. **Project** → **Import/Export** → **Export Maps to Web**
2. **QGIS2Web** plugin (if available)
3. **Export**: HTML with interactive features

## 🎯 Pro Tips

### 1. Layer Organization
- Group related layers together
- Use descriptive names
- Set appropriate transparency levels
- Order layers logically (base maps at bottom)

### 2. Color Schemes
- Use colorblind-friendly palettes
- Maintain consistency across maps
- Consider cultural color associations
- Test in both light and dark themes

### 3. Performance Optimization
- Use simplified datasets for overview maps
- Apply filters to large datasets
- Cache frequently used layers
- Close unused projects

### 4. Data Updates
- Refresh data after new race results
- Maintain consistent naming conventions
- Version control your QGIS projects
- Document data sources and dates

## 📚 Additional Resources

### QGIS Learning
- [QGIS Official Documentation](https://docs.qgis.org/)
- [QGIS Tutorials](https://www.qgistutorials.com/)
- [YouTube QGIS Channels](https://www.youtube.com/results?search_query=qgis+tutorial)

### F1 Data Sources
- [Ergast Developer API](http://ergast.com/mrd/)
- [Formula 1 Official](https://www.formula1.com/)
- [F1 Statistics](https://www.statsf1.com/)

### Weather Data
- [Meteostat](https://dev.meteostat.net/)
- [Visual Crossing](https://www.visualcrossing.com/weather-api)
- [OpenWeatherMap](https://openweathermap.org/api)

## 🏁 Next Steps

1. **Create Your First Map**: Start with the basic weather impact map
2. **Experiment with Styling**: Try different color schemes and sizes
3. **Add Base Maps**: Include context with satellite or street maps
4. **Create Multiple Views**: Build seasonal and circuit-specific maps
5. **Share Your Work**: Export and present your findings

## 📞 Getting Help

- **QGIS Community**: [forum.qgis.org](https://forum.qgis.org/)
- **Stack Overflow**: Tag questions with `qgis`
- **GitHub Issues**: Report bugs in QGIS repository
- **Local User Groups**: Find QGIS users in your area

---

**Happy Mapping! 🗺️🏎️**

Your F1 weather analysis is now ready for professional visualization in QGIS. Create compelling maps that tell the story of how weather impacts Formula 1 racing!
