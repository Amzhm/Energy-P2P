
import subprocess
import logging
from pathlib import Path
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class SmartMetersRawIngestion:
    
    def __init__(self, halfhourly_dir):
        self.halfhourly_dir = Path(halfhourly_dir)
        self.hdfs_path = "/data-lake/bronze/smart-meters/raw"
        
    def validate_directory(self):
        if not self.halfhourly_dir.exists():
            logger.error(f" Dossier introuvable: {self.halfhourly_dir}")
            return False
        
        csv_files = list(self.halfhourly_dir.glob("*.csv"))
        
        if len(csv_files) == 0:
            logger.error(f" Aucun fichier CSV trouvé")
            return False
        
        logger.info(f" Trouvé {len(csv_files)} fichiers CSV")
        
        total_size_mb = sum(f.stat().st_size for f in csv_files) / (1024 * 1024)
        logger.info(f" Taille totale: {total_size_mb:.2f} MB")
        
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
            logger.warning(f"  Erreur upload {filename}: {e}")
            return False
    
    def upload_all_files(self, csv_files):
        """Upload tous les fichiers CSV vers HDFS"""
        
        logger.info(f"  Upload de {len(csv_files)} fichiers vers HDFS...")
        
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
        
        logger.info(f"\ Statistiques HDFS:")
        logger.info(f"  Fichiers CSV: {file_count}")
        logger.info(f"  {result.stdout.strip()}")
    
    def verify_sample(self):
        """Affiche un échantillon des fichiers uploadés"""
        logger.info("\ Échantillon des fichiers dans HDFS:")
        
        cmd = f"docker exec namenode hdfs dfs -ls {self.hdfs_path} | head -10"
        subprocess.run(cmd, shell=True)
    
    def run(self):
        logger.info(" INGESTION RAW SMART METERS - AUCUN TRAITEMENT")
        
        result = self.validate_directory()
        if not result:
            return False
        
        valid, csv_files = result
        
        self.upload_all_files(csv_files)
        
        self.get_hdfs_stats()
        
        self.verify_sample()
        
        logger.info("\ Ingestion RAW terminée!")
        logger.info(f"  Fichiers disponibles dans: {self.hdfs_path}")
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