import os
from pyspark.sql import SparkSession

STORAGE_MODE = os.environ.get("STORAGE_MODE", "LOCAL")  # LOCAL ou HDFS

# ============================================================================
# Path BASE
# ============================================================================
if STORAGE_MODE == "LOCAL":
    LOCAL_DATA_DIR = os.environ.get("LOCAL_DATA_DIR", "/opt/spark-data")
    
    BASE_PATH = LOCAL_DATA_DIR
    BRONZE_BASE = f"{BASE_PATH}/bronze"
    SILVER_BASE = f"{BASE_PATH}/silver"
    GOLD_BASE = f"{BASE_PATH}/gold"    
else:
    HDFS_BASE = "hdfs://namenode:9000"
    
    BASE_PATH = HDFS_BASE
    BRONZE_BASE = f"{HDFS_BASE}/data-lake/bronze/"
    SILVER_BASE = f"{HDFS_BASE}/data-lake/silver/"
    GOLD_BASE = f"{HDFS_BASE}/data-lake/gold/"
    
# ============================================================================
# Data Path
# ============================================================================

BRONZE_WEATHER = f"{BRONZE_BASE}/weather"
BRONZE_CONSUMPTION = f"{BRONZE_BASE}/consumption"
BRONZE_PRICES = f"{BRONZE_BASE}/prices"

# Chemins Silver (données nettoyées)
SILVER_WEATHER = f"{SILVER_BASE}/weather"
SILVER_CONSUMPTION = f"{SILVER_BASE}/consumption"
SILVER_PRICES = f"{SILVER_BASE}/prices"
SILVER_PRODUCTION = f"{SILVER_BASE}/production"  # Données synthétiques

# Chemins Gold (données agrégées)
GOLD_ENERGY_BALANCE = f"{GOLD_BASE}/energy_balance"
GOLD_USER_PROFILES = f"{GOLD_BASE}/user_profiles"

# Pour compatibilité avec l'ancien code
HDFS_BASE = BASE_PATH
HDFS_BRONZE = BRONZE_BASE
HDFS_SILVER = SILVER_BASE
HDFS_GOLD = GOLD_BASE

# ============================================================================
# CONFIGURATION SPARK
# ============================================================================

def get_spark_session(app_name: str, master: str = None) -> SparkSession:
    """if master is None:
        if STORAGE_MODE == "LOCAL":
            master = "local[*]" 
        else:"""
    master = "spark://spark-master:7077"
    
    builder = (SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.executor.memory", "2g")
        .config("spark.driver.memory", "1g")
        .config("spark.executor.cores", "2")
        
        # Optimisations
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        
        # Format Parquet
        .config("spark.sql.parquet.compression.codec", "snappy")
        .config("spark.sql.parquet.mergeSchema", "false")
        
        # Shuffle
        .config("spark.sql.shuffle.partitions", "8")
    )
    
    # Configuration  HDFS
    if STORAGE_MODE == "HDFS":
        builder = builder.config("spark.hadoop.fs.defaultFS", BASE_PATH)
        builder = builder.enableHiveSupport()
    
    spark = builder.getOrCreate()
    
    # Configuration du niveau de log
    spark.sparkContext.setLogLevel("WARN")
    
    print(f" SparkSession created on mode {STORAGE_MODE}")
    print(f"   Master: {master}")
    print(f"   Path base: {BASE_PATH}")
    
    return spark


def stop_spark_session(spark: SparkSession):
    if spark:
        spark.stop()
        print(" SparkSession terminated")


# ============================================================================
# SCHÉMAS DE DONNÉES
# ============================================================================

from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, 
    IntegerType, TimestampType, DateType
)

# Schéma pour les données météo Silver
SCHEMA_WEATHER_SILVER = StructType([
    StructField("date", DateType(), nullable=False),
    StructField("hour", IntegerType(), nullable=False),
    StructField("timestamp", TimestampType(), nullable=False),
    StructField("location_zone", StringType(), nullable=False),
    StructField("temperature_celsius", DoubleType(), nullable=True),
    StructField("cloud_cover_percent", DoubleType(), nullable=True),
    StructField("solar_irradiance_wm2", DoubleType(), nullable=True),
    StructField("wind_speed_ms", DoubleType(), nullable=True),
    StructField("precipitation_mm", DoubleType(), nullable=True)
])

# Schéma pour les données de consommation Silver
SCHEMA_CONSUMPTION_SILVER = StructType([
    StructField("household_id", StringType(), nullable=False),
    StructField("timestamp", TimestampType(), nullable=False),
    StructField("date", DateType(), nullable=False),
    StructField("hour", IntegerType(), nullable=False),
    StructField("consumption_kwh", DoubleType(), nullable=False),
    StructField("is_anomaly", IntegerType(), nullable=True)
])

# Schéma pour les données de prix Silver
SCHEMA_PRICES_SILVER = StructType([
    StructField("date", DateType(), nullable=False),
    StructField("hour", IntegerType(), nullable=False),
    StructField("timestamp", TimestampType(), nullable=False),
    StructField("spot_price_eur_mwh", DoubleType(), nullable=False),
    StructField("grid_buy_price_eur_kwh", DoubleType(), nullable=True),
    StructField("grid_sell_price_eur_kwh", DoubleType(), nullable=True),
    StructField("price_category", StringType(), nullable=True)  # LOW, MEDIUM, HIGH
])

# Schéma pour la production solaire Silver (synthétique)
SCHEMA_PRODUCTION_SILVER = StructType([
    StructField("household_id", StringType(), nullable=False),
    StructField("timestamp", TimestampType(), nullable=False),
    StructField("date", DateType(), nullable=False),
    StructField("hour", IntegerType(), nullable=False),
    StructField("production_kwh", DoubleType(), nullable=False),
    StructField("panel_size_kwp", DoubleType(), nullable=False),
    StructField("efficiency_factor", DoubleType(), nullable=True)
])


# Paramètres pour la génération de production solaire
SOLAR_PANEL_EFFICIENCY = 0.18  # 18% d'efficacité moyenne
SOLAR_PANEL_AREA_M2 = 1.6      # Surface moyenne d'un panneau en m²
DEFAULT_PANEL_SIZE_KWP = 4.0   # Taille système par défaut: 4 kWp

# Seuils de détection d'anomalies
CONSUMPTION_MIN_KWH = 0.0
CONSUMPTION_MAX_KWH = 50.0
TEMPERATURE_MIN_C = -20.0
TEMPERATURE_MAX_C = 45.0

# Catégories de prix
PRICE_CATEGORY_THRESHOLDS = {
    "LOW": 50.0,      # < 50 EUR/MWh
    "MEDIUM": 100.0,  # 50-100 EUR/MWh
    "HIGH": 150.0     # > 100 EUR/MWh
}


if __name__ == "__main__":
    print(" Test configuration Spark")
    print(f"HDFS Base: {HDFS_BASE}")
    print(f"Bronze Weather: {BRONZE_WEATHER}")
    print(f"Silver Weather: {SILVER_WEATHER}")
    
    try:
        spark = get_spark_session("test-config")
        print(f" SparkSession created: {spark.version}")
        print(f" Master: {spark.sparkContext.master}")
        stop_spark_session(spark)
    except Exception as e:
        print(f" Error: {e}")