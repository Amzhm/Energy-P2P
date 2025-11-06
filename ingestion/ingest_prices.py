import requests
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "bronze" / "temp"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class PricesIngestion:
    
    def __init__(self):
        self.api_url = "https://api.energy-charts.info/price"
        self.max_retries = 3
        self.retry_delay = 5  # secondes
        self.data_dir = DATA_DIR
        
    def fetch_prices_with_retry(self, start_date, end_date):
        params = {
            "bzn": "DE-LU", 
            "start": start_date,
            "end": end_date
        }
        
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Tentative {attempt}/{self.max_retries}...")
                
                response = requests.get(
                    self.api_url,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                
                data = response.json()
                logger.info(f"{len(data.get('unix_seconds', []))} points recuperated")
                return data
                
            except requests.exceptions.Timeout:
                logger.warning(f" Timeout - Retry in {self.retry_delay}s...")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f" Error: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    logger.error("Price KO")
                    return None
        
        return None
    
    def validate_data(self, data):
        if not data:
            return False
        
        required_fields = ['unix_seconds', 'price']
        
        for field in required_fields:
            if field not in data:
                logger.error(f"Champ manquant: {field}")
                return False
        
        if len(data['unix_seconds']) == 0:
            logger.error("Empty data")
            return False
        
        logger.info("Data validated")
        return True
    
    def save_locally(self, data, filename):
        filepath = self.data_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        size_kb = filepath.stat().st_size / 1024
        logger.info(f"Saved: {filepath} ({size_kb:.1f} KB)")
        
        return filepath
    
    def upload_to_hdfs(self, local_path, hdfs_path):
        filename = local_path.name
        container_tmp = f"/tmp/{filename}"
        
        subprocess.run(
            f"docker cp {local_path} namenode:{container_tmp}",
            shell=True,
            check=True,
            stderr=subprocess.DEVNULL
        )
        
        hdfs_full_path = f"{hdfs_path}/{filename}"
        subprocess.run(
            f"docker exec namenode hdfs dfs -put -f {container_tmp} {hdfs_full_path}",
            shell=True,
            check=True,
            stderr=subprocess.DEVNULL
        )
        
        # Cleanup
        subprocess.run(
            f"docker exec namenode rm {container_tmp}",
            shell=True,
            stderr=subprocess.DEVNULL
        )
        
        logger.info(f"Uploaded: {hdfs_full_path}")
    
    def run(self):
        logger.info(" INGESTION ELECTRICITY PRICES")
        
        # Dates
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Fetch avec retry
        data = self.fetch_prices_with_retry(yesterday, today)
        
        if data is None:
            return False
        
        # 2. Validation
        if not self.validate_data(data):
            return False
        
        filename = f"prices_{yesterday}.json"
        local_path = self.save_locally(data, filename)
        
        # 4. Upload HDFS
        hdfs_path = "/data-lake/bronze/prices/raw"
        self.upload_to_hdfs(local_path, hdfs_path)
        
        logger.info("\nIngestion OK!")
        logger.info(f"File local: {local_path}")
        logger.info(f"File HDFS: {hdfs_path}/{filename}")
        
        return True


if __name__ == "__main__":
    ingestion = PricesIngestion()
    ingestion.run()