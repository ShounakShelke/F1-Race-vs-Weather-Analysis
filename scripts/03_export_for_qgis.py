#!/usr/bin/env python3
"""
Data Export Script for QGIS
Exports processed F1 and weather data in formats suitable for QGIS import.

Author: F1 Weather Analysis Project
Date: 2024
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import logging
from datetime import datetime
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QGISDataExporter:
    """Exports data in formats suitable for QGIS"""
    
    def __init__(self):
        self.raw_data_dir = "../data/raw"
        self.processed_data_dir = "../data/processed"
        self.qgis_export_dir = "../data/qgis_export"
        
        # Create directories if they don't exist
        os.makedirs(self.qgis_export_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)
        
    def load_data(self):
        """Load all the collected data"""
        logger.info("Loading collected data...")
        
        try:
            # Load F1 data
            races_df = pd.read_csv(f"{self.raw_data_dir}/f1_races_2020_2024.csv")
            results_df = pd.read_csv(f"{self.raw_data_dir}/f1_results_2020_2024.csv")
            weather_df = pd.read_csv(f"{self.raw_data_dir}/f1_weather_data_2020_2024.csv")
            
            logger.info(f"Loaded: {len(races_df)} races, {len(results_df)} results, {len(weather_df)} weather records")
            
            return races_df, results_df, weather_df
            
        except FileNotFoundError as e:
            logger.error(f"Data file not found: {e}")
            logger.error("Please run the data collection scripts first")
            return None, None, None
    
    def merge_race_weather_data(self, races_df, weather_df):
        """Merge race and weather data"""
        logger.info("Merging race and weather data...")
        
        # Merge on season, round, and circuit
        merged_df = pd.merge(
            races_df, 
            weather_df, 
            on=['season', 'round', 'circuit_id', 'circuit_name'],
            how='left',
            suffixes=('', '_weather')
        )
        
        # Clean up duplicate columns
        duplicate_cols = [col for col in merged_df.columns if col.endswith('_weather')]
        for col in duplicate_cols:
            original_col = col.replace('_weather', '')
            if original_col in merged_df.columns:
                # Use weather data if available, otherwise use original
                merged_df[original_col] = merged_df[original_col].fillna(merged_df[col])
                merged_df = merged_df.drop(columns=[col])
        
        logger.info(f"Merged data shape: {merged_df.shape}")
        return merged_df
    
    def add_race_outcomes(self, merged_df, results_df):
        """Add race outcome analysis to the merged data"""
        logger.info("Adding race outcome analysis...")
        
        # Calculate DNFs and incidents per race
        race_outcomes = results_df.groupby(['season', 'round']).agg({
            'status': lambda x: (x != 'Finished').sum(),  # Count non-finishers
            'laps': 'mean',  # Average laps completed
            'position': 'count'  # Total drivers
        }).reset_index()
        
        race_outcomes.columns = ['season', 'round', 'dnf_count', 'avg_laps', 'total_drivers']
        
        # Add position changes (grid vs final position)
        position_changes = results_df.copy()
        position_changes['position_change'] = position_changes['grid'] - position_changes['position']
        
        # Calculate average position change per race
        avg_position_changes = position_changes.groupby(['season', 'round'])['position_change'].mean().reset_index()
        avg_position_changes.columns = ['season', 'round', 'avg_position_change']
        
        # Merge outcomes with main data
        merged_df = pd.merge(merged_df, race_outcomes, on=['season', 'round'], how='left')
        merged_df = pd.merge(merged_df, avg_position_changes, on=['season', 'round'], how='left')
        
        # Fill missing values
        merged_df['dnf_count'] = merged_df['dnf_count'].fillna(0)
        merged_df['avg_laps'] = merged_df['avg_laps'].fillna(0)
        merged_df['total_drivers'] = merged_df['total_drivers'].fillna(0)
        merged_df['avg_position_change'] = merged_df['avg_position_change'].fillna(0)
        
        logger.info("Race outcomes added successfully")
        return merged_df
    
    def create_weather_analysis_features(self, merged_df):
        """Create additional features for weather analysis"""
        logger.info("Creating weather analysis features...")
        
        # Create binary weather indicators
        merged_df['is_rainy'] = merged_df['weather_category'].isin(['Light Rain', 'Heavy Rain', 'Drizzle'])
        merged_df['is_dry'] = merged_df['weather_category'] == 'Dry'
        merged_df['is_extreme'] = merged_df['weather_category'].isin(['Heavy Rain', 'Cold'])
        
        # Create temperature categories
        merged_df['temp_category'] = pd.cut(
            merged_df['temperature_avg'], 
            bins=[-float('inf'), 10, 20, 30, float('inf')],
            labels=['Cold', 'Cool', 'Warm', 'Hot']
        )
        
        # Create precipitation intensity
        merged_df['precipitation_intensity'] = pd.cut(
            merged_df['precipitation'],
            bins=[-float('inf'), 0, 1, 5, float('inf')],
            labels=['None', 'Light', 'Moderate', 'Heavy']
        )
        
        # Create season categories
        merged_df['season_category'] = pd.cut(
            merged_df['season'],
            bins=[2019, 2021, 2023, 2025],
            labels=['Early 2020s', 'Mid 2020s', 'Late 2020s']
        )
        
        logger.info("Weather analysis features created")
        return merged_df
    
    def export_for_qgis(self, merged_df):
        """Export data in QGIS-compatible formats"""
        logger.info("Exporting data for QGIS...")
        
        # Create GeoDataFrame for QGIS
        geometry = [Point(xy) for xy in zip(merged_df['circuit_lng'], merged_df['circuit_lat'])]
        gdf = gpd.GeoDataFrame(merged_df, geometry=geometry, crs="EPSG:4326")
        
        # Export as GeoJSON (QGIS native format)
        geojson_path = f"{self.qgis_export_dir}/f1_races_weather_analysis.geojson"
        gdf.to_file(geojson_path, driver='GeoJSON')
        logger.info(f"Exported GeoJSON to: {geojson_path}")
        
        # Export as CSV with coordinates (QGIS can import this too)
        csv_path = f"{self.qgis_export_dir}/f1_races_weather_analysis.csv"
        merged_df.to_csv(csv_path, index=False)
        logger.info(f"Exported CSV to: {csv_path}")
        
        # Export as shapefile (alternative format)
        shapefile_path = f"{self.qgis_export_dir}/f1_races_weather_analysis.shp"
        gdf.to_file(shapefile_path, driver='ESRI Shapefile')
        logger.info(f"Exported Shapefile to: {shapefile_path}")
        
        # Create a simplified version for easier QGIS handling
        simple_columns = [
            'season', 'round', 'race_name', 'circuit_name', 'circuit_country',
            'race_date', 'weather_category', 'temperature_avg', 'precipitation',
            'dnf_count', 'avg_position_change', 'is_rainy', 'is_dry',
            'circuit_lat', 'circuit_lng'
        ]
        
        simple_df = merged_df[simple_columns].copy()
        simple_gdf = gpd.GeoDataFrame(
            simple_df, 
            geometry=geometry, 
            crs="EPSG:4326"
        )
        
        simple_geojson_path = f"{self.qgis_export_dir}/f1_races_simple.geojson"
        simple_gdf.to_file(simple_geojson_path, driver='GeoJSON')
        logger.info(f"Exported simplified GeoJSON to: {simple_geojson_path}")
        
        return {
            'geojson': geojson_path,
            'csv': csv_path,
            'shapefile': shapefile_path,
            'simple_geojson': simple_geojson_path
        }
    
    def create_qgis_import_guide(self, export_paths):
        """Create a guide for importing data into QGIS"""
        logger.info("Creating QGIS import guide...")
        
        guide_content = f"""# QGIS Import Guide for F1 Weather Analysis

## Generated Files
The following files have been created for QGIS import:

### 1. GeoJSON Files (Recommended)
- **Full Dataset**: `{os.path.basename(export_paths['geojson'])}`
  - Contains all weather and race data
  - Best for detailed analysis
  
- **Simplified Dataset**: `{os.path.basename(export_paths['simple_geojson'])}`
  - Contains essential columns only
  - Easier to work with in QGIS

### 2. Alternative Formats
- **CSV**: `{os.path.basename(export_paths['csv'])}`
- **Shapefile**: `{os.path.basename(export_paths['shapefile'])}`

## QGIS Import Instructions

### Method 1: Drag and Drop (Easiest)
1. Open QGIS
2. Drag the `.geojson` file directly into the QGIS map canvas
3. The layer will be automatically added with proper styling

### Method 2: Layer → Add Layer → Add Vector Layer
1. In QGIS, go to Layer → Add Layer → Add Vector Layer
2. Browse to the exported file
3. Select the file and click "Open"

### Method 3: Browser Panel
1. In the Browser panel, navigate to your project folder
2. Right-click on the `.geojson` file
3. Select "Add Layer to Project"

## Data Structure
The exported data contains the following key fields:

- **Location**: `circuit_lat`, `circuit_lng` (coordinates)
- **Race Info**: `season`, `round`, `race_name`, `circuit_name`
- **Weather**: `weather_category`, `temperature_avg`, `precipitation`
- **Outcomes**: `dnf_count`, `avg_position_change`
- **Categories**: `is_rainy`, `is_dry`

## Styling Recommendations
1. **Color by Weather**: Use `weather_category` for point colors
2. **Size by DNFs**: Use `dnf_count` for point sizes
3. **Labels**: Display `circuit_name` or `race_name`

## Troubleshooting
- If coordinates don't display correctly, check the CRS is set to EPSG:4326
- For large datasets, consider using the simplified version
- Ensure all required columns are present before import

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        guide_path = f"{self.qgis_export_dir}/QGIS_IMPORT_GUIDE.md"
        with open(guide_path, 'w') as f:
            f.write(guide_content)
        
        logger.info(f"QGIS import guide created: {guide_path}")
        return guide_path
    
    def create_data_summary(self, merged_df):
        """Create a summary of the exported data"""
        logger.info("Creating data summary...")
        
        summary = {
            'export_date': datetime.now().isoformat(),
            'total_records': len(merged_df),
            'seasons_covered': sorted(merged_df['season'].unique().tolist()),
            'circuits_covered': len(merged_df['circuit_id'].unique()),
            'weather_categories': merged_df['weather_category'].value_counts().to_dict(),
            'data_quality': {
                'missing_coordinates': merged_df[['circuit_lat', 'circuit_lng']].isnull().sum().to_dict(),
                'missing_weather': merged_df['weather_category'].isnull().sum(),
                'missing_outcomes': merged_df['dnf_count'].isnull().sum()
            },
            'statistical_summary': {
                'avg_temperature': merged_df['temperature_avg'].mean(),
                'avg_precipitation': merged_df['precipitation'].mean(),
                'avg_dnfs': merged_df['dnf_count'].mean(),
                'total_rainy_races': merged_df['is_rainy'].sum(),
                'total_dry_races': merged_df['is_dry'].sum()
            }
        }
        
        summary_path = f"{self.qgis_export_dir}/data_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Data summary created: {summary_path}")
        return summary

def main():
    """Main execution function"""
    logger.info("Starting QGIS Data Export...")
    
    exporter = QGISDataExporter()
    
    try:
        # Load data
        races_df, results_df, weather_df = exporter.load_data()
        if races_df is None:
            return
        
        # Process and merge data
        merged_df = exporter.merge_race_weather_data(races_df, weather_df)
        merged_df = exporter.add_race_outcomes(merged_df, results_df)
        merged_df = exporter.create_weather_analysis_features(merged_df)
        
        # Save processed data
        processed_path = f"{exporter.processed_data_dir}/f1_weather_merged_data.csv"
        merged_df.to_csv(processed_path, index=False)
        logger.info(f"Processed data saved to: {processed_path}")
        
        # Export for QGIS
        export_paths = exporter.export_for_qgis(merged_df)
        
        # Create guides and summaries
        guide_path = exporter.create_qgis_import_guide(export_paths)
        summary = exporter.create_data_summary(merged_df)
        
        print("\n" + "="*50)
        print("QGIS EXPORT COMPLETED")
        print("="*50)
        print(f"Total Records: {summary['total_records']}")
        print(f"Seasons: {summary['seasons_covered']}")
        print(f"Circuits: {summary['circuits_covered']}")
        print(f"Rainy Races: {summary['statistical_summary']['total_rainy_races']}")
        print(f"Dry Races: {summary['statistical_summary']['total_dry_races']}")
        print(f"Average DNFs: {summary['statistical_summary']['avg_dnfs']:.2f}")
        print("\nExported Files:")
        for format_type, path in export_paths.items():
            print(f"  {format_type.upper()}: {os.path.basename(path)}")
        print(f"\nQGIS Guide: {os.path.basename(guide_path)}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Error during QGIS export: {e}")
        raise

if __name__ == "__main__":
    main()
