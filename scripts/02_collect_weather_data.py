#!/usr/bin/env python3
"""
Weather Data Collection Script for F1 Races
Collects weather data for Formula 1 race locations and dates using Meteostat API.

Author: F1 Weather Analysis Project
Date: 2024
"""

import pandas as pd
import numpy as np
from meteostat import Point, Daily
from datetime import datetime, timedelta
import time
import os
import logging
from tqdm import tqdm
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeatherDataCollector:
    """Collects weather data for F1 race locations"""
    
    def __init__(self):
        self.output_dir = "../data/raw"
        self.races_file = f"{self.output_dir}/f1_races_2020_2024.csv"
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Weather categorization thresholds
        self.rain_threshold = 1.0  # mm of precipitation
        self.temp_threshold = 15.0  # Celsius
        
    def load_race_data(self):
        """Load the collected F1 race data"""
        try:
            races_df = pd.read_csv(self.races_file)
            logger.info(f"Loaded {len(races_df)} races from {self.races_file}")
            return races_df
        except FileNotFoundError:
            logger.error(f"Race data file not found: {self.races_file}")
            logger.error("Please run 01_collect_f1_data.py first")
            return None
    
    def get_weather_data(self, lat, lng, date, days_range=3):
        """Get weather data for a specific location and date"""
        try:
            # Create a point for the location
            location = Point(lat, lng)
            
            # Get weather data for the race date and surrounding days
            start_date = date - timedelta(days=days_range)
            end_date = date + timedelta(days=days_range)
            
            # Fetch daily weather data
            weather_data = Daily(location, start_date, end_date)
            weather_data = weather_data.fetch()
            
            if weather_data.empty:
                logger.warning(f"No weather data found for {date} at lat={lat}, lng={lng}")
                return None
            
            # Find the race day weather (closest to the actual race date)
            race_day_weather = None
            min_date_diff = float('inf')
            
            for idx, row in weather_data.iterrows():
                date_diff = abs((idx - date).days)
                if date_diff < min_date_diff:
                    min_date_diff = date_diff
                    race_day_weather = row
            
            if race_day_weather is not None:
                return {
                    'date': race_day_weather.name.strftime('%Y-%m-%d'),
                    'tavg': race_day_weather.get('tavg'),  # Average temperature
                    'tmin': race_day_weather.get('tmin'),  # Minimum temperature
                    'tmax': race_day_weather.get('tmax'),  # Maximum temperature
                    'prcp': race_day_weather.get('prcp'),  # Precipitation
                    'snow': race_day_weather.get('snow'),  # Snow
                    'wdir': race_day_weather.get('wdir'),  # Wind direction
                    'wspd': race_day_weather.get('wspd'),  # Wind speed
                    'wpgt': race_day_weather.get('wpgt'),  # Peak wind gust
                    'pres': race_day_weather.get('pres'),  # Pressure
                    'tsun': race_day_weather.get('tsun')   # Sunshine duration
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching weather data for {date} at lat={lat}, lng={lng}: {e}")
            return None
    
    def categorize_weather(self, weather_data):
        """Categorize weather conditions based on precipitation and temperature"""
        if weather_data is None:
            return 'Unknown'
        
        prcp = weather_data.get('prcp', 0)
        tavg = weather_data.get('tavg', 20)
        
        # Simple categorization
        if prcp > self.rain_threshold:
            if prcp > 5.0:
                return 'Heavy Rain'
            else:
                return 'Light Rain'
        elif prcp > 0.1:
            return 'Drizzle'
        else:
            if tavg > self.temp_threshold:
                return 'Dry'
            else:
                return 'Cold'
    
    def collect_weather_for_races(self):
        """Collect weather data for all F1 races"""
        logger.info("Starting weather data collection for F1 races...")
        
        # Load race data
        races_df = self.load_race_data()
        if races_df is None:
            return
        
        # Filter races with valid coordinates
        valid_races = races_df.dropna(subset=['circuit_lat', 'circuit_lng'])
        logger.info(f"Found {len(valid_races)} races with valid coordinates")
        
        weather_data_list = []
        failed_races = []
        
        # Process each race
        for idx, race in tqdm(valid_races.iterrows(), total=len(valid_races), desc="Collecting weather data"):
            try:
                # Parse race date
                race_date = datetime.strptime(race['race_date'], '%Y-%m-%d')
                
                # Get weather data
                weather = self.get_weather_data(
                    float(race['circuit_lat']), 
                    float(race['circuit_lng']), 
                    race_date
                )
                
                if weather:
                    # Combine race and weather data
                    combined_data = {
                        'season': race['season'],
                        'round': race['round'],
                        'race_name': race['race_name'],
                        'circuit_id': race['circuit_id'],
                        'circuit_name': race['circuit_name'],
                        'circuit_location': race['circuit_location'],
                        'circuit_country': race['circuit_country'],
                        'circuit_lat': race['circuit_lat'],
                        'circuit_lng': race['circuit_lng'],
                        'race_date': race['race_date'],
                        'weather_date': weather['date'],
                        'temperature_avg': weather['tavg'],
                        'temperature_min': weather['tmin'],
                        'temperature_max': weather['tmax'],
                        'precipitation': weather['prcp'],
                        'snow': weather['snow'],
                        'wind_direction': weather['wdir'],
                        'wind_speed': weather['wspd'],
                        'wind_gust': weather['wpgt'],
                        'pressure': weather['pres'],
                        'sunshine': weather['tsun'],
                        'weather_category': self.categorize_weather(weather)
                    }
                    
                    weather_data_list.append(combined_data)
                else:
                    failed_races.append({
                        'race': race['race_name'],
                        'date': race['race_date'],
                        'circuit': race['circuit_name']
                    })
                
                # Rate limiting - be respectful to the API
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing race {race['race_name']}: {e}")
                failed_races.append({
                    'race': race['race_name'],
                    'date': race['race_date'],
                    'circuit': race['circuit_name'],
                    'error': str(e)
                })
        
        # Convert to DataFrame and save
        if weather_data_list:
            weather_df = pd.DataFrame(weather_data_list)
            weather_df.to_csv(f"{self.output_dir}/f1_weather_data_2020_2024.csv", index=False)
            logger.info(f"Saved weather data for {len(weather_data_list)} races")
        else:
            logger.warning("No weather data collected")
        
        # Save failed races for debugging
        if failed_races:
            failed_df = pd.DataFrame(failed_races)
            failed_df.to_csv(f"{self.output_dir}/failed_weather_collection.csv", index=False)
            logger.warning(f"Failed to collect weather data for {len(failed_races)} races")
        
        # Generate summary statistics
        summary = {
            'total_races': len(valid_races),
            'successful_collections': len(weather_data_list),
            'failed_collections': len(failed_races),
            'success_rate': len(weather_data_list) / len(valid_races) * 100 if len(valid_races) > 0 else 0,
            'collection_date': datetime.now().isoformat()
        }
        
        # Weather category breakdown
        if weather_data_list:
            weather_categories = pd.DataFrame(weather_data_list)['weather_category'].value_counts()
            summary['weather_breakdown'] = weather_categories.to_dict()
        
        # Save summary
        with open(f"{self.output_dir}/weather_collection_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info("Weather data collection completed!")
        return summary
    
    def create_weather_summary(self):
        """Create a summary of weather patterns across races"""
        weather_file = f"{self.output_dir}/f1_weather_data_2020_2024.csv"
        
        if not os.path.exists(weather_file):
            logger.error("Weather data file not found. Run collection first.")
            return
        
        weather_df = pd.read_csv(weather_file)
        
        # Basic statistics
        summary_stats = {
            'total_races_with_weather': len(weather_df),
            'temperature_stats': {
                'avg_temp': weather_df['temperature_avg'].mean(),
                'min_temp': weather_df['temperature_min'].min(),
                'max_temp': weather_df['temperature_max'].max()
            },
            'precipitation_stats': {
                'avg_precipitation': weather_df['precipitation'].mean(),
                'max_precipitation': weather_df['precipitation'].max(),
                'races_with_rain': len(weather_df[weather_df['precipitation'] > 0])
            },
            'weather_categories': weather_df['weather_category'].value_counts().to_dict()
        }
        
        # Save weather summary
        with open(f"{self.output_dir}/weather_analysis_summary.json", 'w') as f:
            json.dump(summary_stats, f, indent=2)
        
        logger.info("Weather summary created successfully!")
        return summary_stats

def main():
    """Main execution function"""
    logger.info("Starting Weather Data Collection for F1 Races...")
    
    collector = WeatherDataCollector()
    
    try:
        # Collect weather data
        summary = collector.collect_weather_for_races()
        
        if summary:
            # Create weather summary
            weather_summary = collector.create_weather_summary()
            
            print("\n" + "="*50)
            print("WEATHER COLLECTION SUMMARY")
            print("="*50)
            print(f"Total Races: {summary['total_races']}")
            print(f"Successful Collections: {summary['successful_collections']}")
            print(f"Failed Collections: {summary['failed_collections']}")
            print(f"Success Rate: {summary['success_rate']:.1f}%")
            print(f"Collection Date: {summary['collection_date']}")
            
            if 'weather_breakdown' in summary:
                print("\nWeather Categories:")
                for category, count in summary['weather_breakdown'].items():
                    print(f"  {category}: {count}")
            
            print("="*50)
        
    except Exception as e:
        logger.error(f"Error during weather data collection: {e}")
        raise

if __name__ == "__main__":
    main()
