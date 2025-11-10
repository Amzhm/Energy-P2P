
import subprocess
import logging
from pathlib import Path
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class SmartMetersRawIngestion:
    
    def __init__(self, halfhourly_dir):
        self.halfhourly_dir = Path(halfhourly_dir)
        self.hdfs_path = "/data-lake/bronze/smart-meters"
        
    def validate_directory(self):
        if not self.halfhourly_dir.exists():
            logger.error(f" Dossier introuvable: {self.halfhourly_dir}")
            return False
        
        csv_files = list(self.halfhourly_dir.glob("*.csv"))
        
        if len(csv_files) == 0:
            logger.error(f" No CSV file")
            return False
        
        logger.info(f" Find {len(csv_files)} CSV files")
        
        total_size_mb = sum(f.stat().st_size for f in csv_files) / (1024 * 1024)
        logger.info(f" Size: {total_size_mb:.2f} MB")
        
        return True, csv_files
    
    def upload_file_to_hdfs(self, csv_file):

        filename = csv_file.name
        container_tmp = f"/tmp/{filename}"
        
        try:
            subprocess.run(
                f"docker cp {csv_file} namenode:{container_tmp}",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            subprocess.run(
                f"docker exec namenode hdfs dfs -put -f {container_tmp} {self.hdfs_path}/",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            subprocess.run(
                f"docker exec namenode rm {container_tmp}",
                shell=True,
                stderr=subprocess.DEVNULL
            )
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"  Error upload {filename}: {e}")
            return False
    
    def upload_all_files(self, csv_files):        
        logger.info(f"  Upload of {len(csv_files)} files to HDFS...")
        
        success_count = 0
        failed_count = 0
        
        for csv_file in tqdm(csv_files, desc="Upload HDFS"):
            if self.upload_file_to_hdfs(csv_file):
                success_count += 1
            else:
                failed_count += 1
        
        logger.info(f" Succès: {success_count}/{len(csv_files)}")
        if failed_count > 0:
            logger.warning(f"  Échecs: {failed_count}")
    
    def get_hdfs_stats(self):
        
        cmd_count = f"docker exec namenode hdfs dfs -ls {self.hdfs_path} | grep csv | wc -l"
        result = subprocess.run(cmd_count, shell=True, capture_output=True, text=True)
        file_count = result.stdout.strip()
        
        cmd_size = f"docker exec namenode hdfs dfs -du -s -h {self.hdfs_path}"
        result = subprocess.run(cmd_size, shell=True, capture_output=True, text=True)
        
        logger.info(f"\ Statistics HDFS:")
        logger.info(f" CSV files: {file_count}")
        logger.info(f"  {result.stdout.strip()}")
    
    def run(self):
        logger.info(" INGESTION RAW SMART METERS")
        
        result = self.validate_directory()
        if not result:
            return False
        
        valid, csv_files = result
        
        self.upload_all_files(csv_files)
        
        self.get_hdfs_stats()        
        logger.info("\ Ingestion RAW OK!")
        return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("\nExemple:")
        print("  python ingest_smartmeters_raw.py ~/Downloads/halfhourly_dataset/")
        sys.exit(1)
    
    halfhourly_dir = sys.argv[1]
    ingestion = SmartMetersRawIngestion(halfhourly_dir)
    ingestion.run()
