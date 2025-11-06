import requests
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "bronze" / "temp"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class WeatherIngestion:
    
    def __init__(self):
        self.api_url = "https://api.open-meteo.com/v1/forecast"
        self.latitude = 51.5074   # London
        self.longitude = -0.1278
        self.data_dir = DATA_DIR
        
    def fetch_weather_data(self, start_date, end_date):
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "cloud_cover",
                "wind_speed_10m",
                "shortwave_radiation"
            ],
            "timezone": "Europe/London"
        }
        
        logger.info(f"Meteo for {start_date} to {end_date}...")
        
        try:
            response = requests.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f" {len(data['hourly']['time'])} pdata fetched")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f" Erreur API: {e}")
            return None
    
    def save_locally(self, data, filename):
        filepath = self.data_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Stats
        size_kb = filepath.stat().st_size / 1024
        logger.info(f" Saved: {filepath} ({size_kb:.1f} KB)")
        
        return filepath
    
    def upload_to_hdfs(self, local_path, hdfs_path):
        filename = local_path.name
        
        container_tmp = f"/tmp/{filename}"
        cmd_copy = f"docker cp {local_path} namenode:{container_tmp}"
        
        logger.info(f"Copied to the container: {filename}")
        subprocess.run(cmd_copy, shell=True, check=True, stderr=subprocess.DEVNULL)
        
        hdfs_full_path = f"{hdfs_path}/{filename}"
        cmd_hdfs = f"docker exec namenode hdfs dfs -put -f {container_tmp} {hdfs_full_path}"
        
        logger.info(f" Upload to HDFS: {hdfs_full_path}")
        subprocess.run(cmd_hdfs, shell=True, check=True, stderr=subprocess.DEVNULL)
        
        cmd_clean = f"docker exec namenode rm {container_tmp}"
        subprocess.run(cmd_clean, shell=True, stderr=subprocess.DEVNULL)
        
        logger.info(f" Upload succed!")
    
    def verify_hdfs(self, hdfs_path):
        cmd = f"docker exec namenode hdfs dfs -ls {hdfs_path}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("\n File in HDFS:")
            print(result.stdout)
        else:
            logger.error(" Error HDFS")
    
    def run(self):
        logger.info("INGESTION WEATHER DATA")
        logger.info("="*60)
        
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        
        data = self.fetch_weather_data(yesterday, today)
        
        if data is None:
            logger.error("Ingestion KO")
            return False
        
        filename = f"weather_{yesterday}.json"
        local_path = self.save_locally(data, filename)
        
        hdfs_path = "/data-lake/bronze/weather/raw"
        self.upload_to_hdfs(local_path, hdfs_path)
        
        self.verify_hdfs(hdfs_path)
        
        logger.info("\nIngestion OK!")
        logger.info(f"Local file: {local_path}")
        logger.info(f" HDFS FILE: {hdfs_path}/{filename}")
        
        return True


if __name__ == "__main__":
    ingestion = WeatherIngestion()
    ingestion.run()