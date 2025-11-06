
import subprocess
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def run_hdfs_cmd(cmd):
    full_cmd = f"docker exec namenode {cmd}"
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error: {e.stderr}")
        return False, e.stderr


def create_bronze_structure():
    
    folders = [
        "/data-lake/bronze/weather/raw",
        "/data-lake/bronze/weather/archive",
        "/data-lake/bronze/prices/raw",
        "/data-lake/bronze/prices/archive",
        "/data-lake/bronze/solar/raw",
        "/data-lake/bronze/solar/archive",
        "/data-lake/bronze/smart-meters/raw",
        "/data-lake/bronze/smart-meters/partitioned",
        "/data-lake/bronze/_metadata"
    ]
    
    logger.info("Creation of Bronze in HDFS...")
    
    for folder in folders:
        success, _ = run_hdfs_cmd(f"hdfs dfs -mkdir -p {folder}")
        if success:
            logger.info(f"{folder} created")
    logger.info("\n Structure created:")
    success, output = run_hdfs_cmd("hdfs dfs -ls -R /data-lake/bronze")
    if success:
        print(output)
    
    logger.info("\n Setup HDFS!")

def create_local_structure():    
    local_folders = [
        DATA_DIR / "bronze" / "temp",
        DATA_DIR / "bronze" / "archive",
        DATA_DIR / "logs"
    ]
    
    logger.info("\n Creation of locale structure...")
    
    for folder in local_folders:
        folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ {folder}")
    
    logger.info("Locale structure created!")


if __name__ == "__main__":
    logger.info(" INITIALISATION DE L'INFRASTRUCTURE")
    
    create_local_structure()
    
    create_bronze_structure()
    
    logger.info(" Setup finished!")