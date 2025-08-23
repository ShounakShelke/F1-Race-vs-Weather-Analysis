#!/usr/bin/env python3
"""
F1 Race Data Collection Script
Collects Formula 1 race results, driver information, and circuit data from Ergast API
for the 2020-2024 seasons.

Author: F1 Weather Analysis Project
Date: 2024
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime
import os
from tqdm import tqdm
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class F1DataCollector:
    """Collects F1 data from Ergast API"""
    
    def __init__(self):
        self.base_url = "http://ergast.com/api/f1"
        self.seasons = [2020, 2021, 2022, 2023, 2024]
        self.output_dir = "../data/raw"
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
    def make_request(self, endpoint, params=None):
        """Make API request with rate limiting"""
        url = f"{self.base_url}/{endpoint}.json"
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Rate limiting - be respectful to the API
            time.sleep(0.5)
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {endpoint}: {e}")
            return None
    
    def get_seasons(self):
        """Get basic season information"""
        logger.info("Collecting season information...")
        
        seasons_data = []
        for season in self.seasons:
            data = self.make_request(f"{season}")
            if data and 'MRData' in data:
                season_info = data['MRData']['RaceTable']
                seasons_data.append({
                    'season': season,
                    'total_races': len(season_info.get('Races', [])),
                    'collected_at': datetime.now().isoformat()
                })
        
        # Save seasons summary
        seasons_df = pd.DataFrame(seasons_data)
        seasons_df.to_csv(f"{self.output_dir}/seasons_summary.csv", index=False)
        logger.info(f"Collected data for {len(seasons_data)} seasons")
        
        return seasons_data
    
    def get_races(self, season):
        """Get all races for a specific season"""
        logger.info(f"Collecting races for season {season}...")
        
        data = self.make_request(f"{season}")
        if not data or 'MRData' not in data:
            return []
        
        races = data['MRData']['RaceTable']['Races']
        races_data = []
        
        for race in races:
            race_info = {
                'season': season,
                'round': race.get('round'),
                'race_name': race.get('raceName'),
                'circuit_id': race.get('Circuit', {}).get('circuitId'),
                'circuit_name': race.get('Circuit', {}).get('circuitName'),
                'circuit_location': race.get('Circuit', {}).get('Location', {}).get('locality'),
                'circuit_country': race.get('Circuit', {}).get('Location', {}).get('country'),
                'circuit_lat': race.get('Circuit', {}).get('Location', {}).get('lat'),
                'circuit_lng': race.get('Circuit', {}).get('Location', {}).get('lng'),
                'race_date': race.get('date'),
                'race_time': race.get('time'),
                'url': race.get('url')
            }
            races_data.append(race_info)
        
        return races_data
    
    def get_race_results(self, season, round_num):
        """Get race results for a specific race"""
        data = self.make_request(f"{season}/{round_num}/results")
        if not data or 'MRData' not in data:
            return []
        
        results = data['MRData']['RaceTable']['Races'][0].get('Results', [])
        results_data = []
        
        for result in results:
            result_info = {
                'season': season,
                'round': round_num,
                'position': result.get('position'),
                'position_text': result.get('positionText'),
                'driver_number': result.get('Driver', {}).get('driverId'),
                'driver_code': result.get('Driver', {}).get('code'),
                'driver_name': f"{result.get('Driver', {}).get('givenName', '')} {result.get('Driver', {}).get('familyName', '')}".strip(),
                'constructor_id': result.get('Constructor', {}).get('constructorId'),
                'constructor_name': result.get('Constructor', {}).get('name'),
                'grid': result.get('grid'),
                'laps': result.get('laps'),
                'status': result.get('status'),
                'points': result.get('points'),
                'fastest_lap_rank': result.get('FastestLap', {}).get('rank') if result.get('FastestLap') else None,
                'fastest_lap_time': result.get('FastestLap', {}).get('Time', {}).get('time') if result.get('FastestLap') else None
            }
            results_data.append(result_info)
        
        return results_data
    
    def get_drivers(self, season):
        """Get all drivers for a specific season"""
        logger.info(f"Collecting drivers for season {season}...")
        
        data = self.make_request(f"{season}/drivers")
        if not data or 'MRData' not in data:
            return []
        
        drivers = data['MRData']['DriverTable']['Drivers']
        drivers_data = []
        
        for driver in drivers:
            driver_info = {
                'season': season,
                'driver_id': driver.get('driverId'),
                'driver_code': driver.get('code'),
                'driver_number': driver.get('permanentNumber'),
                'given_name': driver.get('givenName'),
                'family_name': driver.get('familyName'),
                'date_of_birth': driver.get('dateOfBirth'),
                'nationality': driver.get('nationality'),
                'url': driver.get('url')
            }
            drivers_data.append(driver_info)
        
        return drivers_data
    
    def get_constructors(self, season):
        """Get all constructors for a specific season"""
        logger.info(f"Collecting constructors for season {season}...")
        
        data = self.make_request(f"{season}/constructors")
        if not data or 'MRData' not in data:
            return []
        
        constructors = data['MRData']['ConstructorTable']['Constructors']
        constructors_data = []
        
        for constructor in constructors:
            constructor_info = {
                'season': season,
                'constructor_id': constructor.get('constructorId'),
                'name': constructor.get('name'),
                'nationality': constructor.get('nationality'),
                'url': constructor.get('url')
            }
            constructors_data.append(constructor_info)
        
        return constructors_data
    
    def collect_all_data(self):
        """Collect all F1 data for the specified seasons"""
        logger.info("Starting comprehensive F1 data collection...")
        
        all_races = []
        all_results = []
        all_drivers = []
        all_constructors = []
        
        # Collect data for each season
        for season in tqdm(self.seasons, desc="Collecting seasons"):
            logger.info(f"Processing season {season}...")
            
            # Get races for this season
            races = self.get_races(season)
            all_races.extend(races)
            
            # Get results for each race
            for race in races:
                if race['round']:
                    results = self.get_race_results(season, race['round'])
                    all_results.extend(results)
            
            # Get drivers and constructors for this season
            drivers = self.get_drivers(season)
            all_drivers.extend(drivers)
            
            constructors = self.get_constructors(season)
            all_constructors.extend(constructors)
        
        # Convert to DataFrames and save
        races_df = pd.DataFrame(all_races)
        results_df = pd.DataFrame(all_results)
        drivers_df = pd.DataFrame(all_drivers)
        constructors_df = pd.DataFrame(all_constructors)
        
        # Save data
        races_df.to_csv(f"{self.output_dir}/f1_races_2020_2024.csv", index=False)
        results_df.to_csv(f"{self.output_dir}/f1_results_2020_2024.csv", index=False)
        drivers_df.to_csv(f"{self.output_dir}/f1_drivers_2020_2024.csv", index=False)
        constructors_df.to_csv(f"{self.output_dir}/f1_constructors_2020_2024.csv", index=False)
        
        # Save summary statistics
        summary = {
            'total_seasons': len(self.seasons),
            'total_races': len(all_races),
            'total_results': len(all_results),
            'total_drivers': len(all_drivers),
            'total_constructors': len(all_constructors),
            'collection_date': datetime.now().isoformat(),
            'seasons_covered': self.seasons
        }
        
        with open(f"{self.output_dir}/collection_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info("Data collection completed successfully!")
        logger.info(f"Collected: {len(all_races)} races, {len(all_results)} results")
        
        return summary

def main():
    """Main execution function"""
    logger.info("Starting F1 Data Collection...")
    
    collector = F1DataCollector()
    
    try:
        summary = collector.collect_all_data()
        print("\n" + "="*50)
        print("COLLECTION SUMMARY")
        print("="*50)
        print(f"Seasons: {summary['total_seasons']}")
        print(f"Races: {summary['total_races']}")
        print(f"Results: {summary['total_results']}")
        print(f"Drivers: {summary['total_drivers']}")
        print(f"Constructors: {summary['total_constructors']}")
        print(f"Collection Date: {summary['collection_date']}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Error during data collection: {e}")
        raise

if __name__ == "__main__":
    main()
