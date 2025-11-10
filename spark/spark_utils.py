
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, lit, year, month, dayofmonth, hour as hour_func
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def add_temporal_features(df: DataFrame, timestamp_col: str = "timestamp") -> DataFrame:

    df_with_features = (df
        .withColumn("date", col(timestamp_col).cast("date"))
        .withColumn("year", year(col(timestamp_col)))
        .withColumn("month", month(col(timestamp_col)))
        .withColumn("day", dayofmonth(col(timestamp_col)))
        .withColumn("hour", hour_func(col(timestamp_col)))
        .withColumn("day_of_week", ((col(timestamp_col).cast("long") / 86400 + 4) % 7).cast("int"))  # 0=Lundi
        .withColumn("is_weekend", when(col("day_of_week").isin([5, 6]), 1).otherwise(0))
    )
    
    logger.info(" Features temporelles added")
    return df_with_features


def detect_anomalies(df: DataFrame, column: str, min_value: float, max_value: float, anomaly_col: str = "is_anomaly") -> DataFrame:
    
    df_with_anomalies = df.withColumn(
        anomaly_col,
        when(
            (col(column).isNull()) | 
            (col(column) < min_value) | 
            (col(column) > max_value),
            1
        ).otherwise(0)
    )
    
    anomaly_count = df_with_anomalies.filter(col(anomaly_col) == 1).count()
    total_count = df_with_anomalies.count()
    anomaly_pct = (anomaly_count / total_count * 100) if total_count > 0 else 0
    
    logger.info(f" {anomaly_count:,} anomalies detected ({anomaly_pct:.2f}%)")
    
    return df_with_anomalies


def remove_duplicates(df: DataFrame, subset: list = None) -> DataFrame:
    initial_count = df.count()    
    df_dedup = df.dropDuplicates(subset=subset)
    
    final_count = df_dedup.count()
    removed = initial_count - final_count
    
    logger.info(f" {removed:,} duplicates removed (final: {final_count:,} lines)")
    
    return df_dedup


def handle_null_values(df: DataFrame, strategy: dict) -> DataFrame:    
    df_cleaned = df
    
    for column, action in strategy.items():
        if column not in df.columns:
            logger.warning(f" Colonne '{column}' not found")
            continue
            
        null_count = df_cleaned.filter(col(column).isNull()).count()
        
        if null_count == 0:
            logger.info(f"✓ '{column}': none null")
            continue
        
        if action == "drop":
            df_cleaned = df_cleaned.filter(col(column).isNotNull())
            logger.info(f"'{column}': {null_count:,} lines deleted")
            
        elif action == "mean":
            mean_value = df_cleaned.select(col(column)).summary("mean").collect()[0][1]
            df_cleaned = df_cleaned.fillna({column: float(mean_value)})
            logger.info(f"✓ '{column}': {null_count:,} nulls replaced per mean ({mean_value})")
            
        else:
            df_cleaned = df_cleaned.fillna({column: action})
            logger.info(f"✓ '{column}': {null_count:,} nulls replaced per {action}")
    
    return df_cleaned


def write_to_parquet(df: DataFrame, path: str, partition_cols: list = None, mode: str = "overwrite") -> None:
    logger.info(f"Mode: {mode}, Partitions: {partition_cols}")
    
    record_count = df.count()
    logger.info(f"Records to write: {record_count:,}")
    
    writer = df.write.mode(mode).format("parquet")
    
    if partition_cols:
        writer = writer.partitionBy(*partition_cols)
    
    writer.save(path)
    
    logger.info(f" {record_count:,} records wroten to {path}")


def read_from_parquet(spark, path: str) -> DataFrame:
    
    df = spark.read.parquet(path)
    
    record_count = df.count()
    logger.info(f" {record_count:,} records read from {path}")
    
    return df


def show_dataframe_info(df: DataFrame, name: str = "DataFrame", sample_rows: int = 5):
    logger.info(f" Informations sur '{name}'")
    
    # Schéma
    logger.info("\n Schema:")
    df.printSchema()
    
    # Statistiques
    count = df.count()
    columns = len(df.columns)
    logger.info(f"\nStatistics:")
    logger.info(f"   lines: {count:,}")
    logger.info(f"   Columns: {columns}")
    
    # Échantillon
    if count > 0:
        logger.info(f"\n Sample ({sample_rows} lines):")
        df.show(sample_rows, truncate=False)
    else:
        logger.warning("Empty DataFrame!")
    

def validate_dataframe(df: DataFrame, required_columns: list, name: str = "DataFrame") -> bool:
    
    missing_cols = set(required_columns) - set(df.columns)
    
    if missing_cols:
        logger.error(f"Missing columns: {missing_cols}")
        return False
    
    return True


if __name__ == "__main__":
    print(" Module utilitaire chargé")
    print("Fonctions disponibles:")
    print("  - add_temporal_features()")
    print("  - detect_anomalies()")
    print("  - remove_duplicates()")
    print("  - handle_null_values()")
    print("  - write_to_parquet()")
    print("  - read_from_parquet()")
    print("  - show_dataframe_info()")
    print("  - validate_dataframe()")