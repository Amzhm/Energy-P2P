#  Energy P2P Trading Platform - Data Engineering Project

[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)
[![Apache Spark](https://img.shields.io/badge/Apache-Spark_3.5-E25A1C?logo=apachespark)](https://spark.apache.org/)
[![Apache Airflow](https://img.shields.io/badge/Apache-Airflow_2.7-017CEE?logo=apacheairflow)](https://airflow.apache.org/)
[![Kafka](https://img.shields.io/badge/Apache-Kafka-231F20?logo=apachekafka)](https://kafka.apache.org/)

A comprehensive **Data Engineering portfolio project** demonstrating end-to-end data pipeline development for an energy peer-to-peer (P2P) trading platform.

---

##  Project Overview

This project simulates a marketplace where residential solar producers can sell their energy surplus to neighboring consumers. The focus is on demonstrating expertise in:

-  Multi-source data ingestion (batch + streaming)
-  Medallion architecture (Bronze/Silver/Gold layers)
-  Data Warehousing with dimensional modeling
-  Big Data processing (Hadoop HDFS + Apache Spark)
-  Real-time streaming (Kafka + Spark Structured Streaming)
-  Pipeline orchestration (Apache Airflow)
-  Machine Learning pipelines (SparkML)
-  Data Quality & Observability (Great Expectations, Prometheus, Grafana)
-  Business Intelligence visualization (Apache Superset, Streamlit)

---

##  Architecture

```
┌─────────────────────────────────────────────────────┐
│              VISUALIZATION LAYER                    │
│  Grafana (Monitoring) | Superset (BI) | Streamlit   │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────┴───────────────────────────────────────┐
│           DATA PROCESSING LAYER                     │
│  Airflow (Orchestration) | Spark (Batch + Stream)   │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────┴───────────────────────────────────────┐
│              STORAGE LAYER                          │
│  HDFS | PostgreSQL | MongoDB | Cassandra | Redis    │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────┴───────────────────────────────────────┐
│             INGESTION LAYER                         │
│  Kafka | Python API Clients | Bash Scripts          │
└─────────────────────────────────────────────────────┘
```

---

##  Technology Stack

### Storage
- **HDFS (Hadoop)**: Data Lake (Bronze/Silver/Gold)
- **PostgreSQL**: Data Warehouse (Star Schema)
- **MongoDB**: Document store (user profiles, transactions)
- **Cassandra**: Time-series data (IoT metrics)
- **Redis**: Caching layer

### Processing
- **Apache Spark**: Batch & streaming processing
- **SparkSQL**: Analytical queries
- **SparkML**: Machine learning

### Orchestration & Streaming
- **Apache Airflow**: Workflow automation
- **Apache Kafka**: Event streaming
- **Zookeeper**: Kafka coordination

### Visualization & Monitoring
- **Apache Superset**: Business intelligence
- **Grafana**: Monitoring dashboards
- **Prometheus**: Metrics collection
- **Jupyter**: Data exploration

---

##  Prerequisites

- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+
- **RAM**: Minimum 16GB (32GB recommended)
- **Disk Space**: Minimum 50GB free
- **CPU**: 4+ cores recommended

---

##  Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Amzhm/Energy-P2P.git
cd ENERGY P2P
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your preferred passwords (optional)
nano .env
```

### 3. Start All Services

```bash
# Start all containers
docker-compose up -d

# Check that all services are running
docker-compose ps

# View logs (optional)
docker-compose logs -f
```

 **First startup takes 5-10 minutes** as Docker downloads all images and initializes databases.

### 4. Verify Services

Wait for all services to be healthy (check with `docker-compose ps`), then access:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Hadoop NameNode** | http://localhost:9870 | - |
| **Spark Master** | http://localhost:8080 | - |
| **Kafka UI** | http://localhost:8090 | - |
| **Airflow** | http://localhost:8085 | admin / admin123 |
| **Superset** | http://localhost:8088 | admin / admin123 |
| **Grafana** | http://localhost:3000 | admin / admin123 |
| **Jupyter** | http://localhost:8888 | Token: energy123 |
| **Prometheus** | http://localhost:9090 | - |
| **Mongo Express** | http://localhost:8091 | admin / admin123 |

---

##  Database Initialization

### PostgreSQL

The PostgreSQL container automatically:
- Creates 3 databases: `energy_dwh`, `airflow_db`, `superset_db`
- Creates schemas: `bronze`, `silver`, `gold`, `staging`
- Installs extensions: `uuid-ossp`, `pg_stat_statements`

**Connect to PostgreSQL:**
```bash
docker exec -it postgres psql -U energy_user -d energy_dwh
```

### MongoDB

The MongoDB container automatically:
- Creates collections: `user_profiles`, `energy_transactions`, `anomalies`, `alerts`, `system_logs`
- Creates indexes for performance
- Inserts sample data

**Connect to MongoDB:**
```bash
docker exec -it mongodb mongosh -u mongo_admin -p mongo_password
```

Or use Mongo Express UI: http://localhost:8091

### Cassandra

The Cassandra container automatically:
- Creates keyspace: `energy_timeseries`
- Creates tables for time-series data
- Creates materialized views

**Connect to Cassandra:**
```bash
docker exec -it cassandra cqlsh
```

Then execute:
```cql
USE energy_timeseries;
DESCRIBE TABLES;
```

---

##  HDFS Setup

### Access HDFS

**Via Web UI:** http://localhost:9870

**Via CLI:**
```bash
# Enter namenode container
docker exec -it namenode bash

# List HDFS contents
hdfs dfs -ls /

# Create directories
hdfs dfs -mkdir -p /data/bronze
hdfs dfs -mkdir -p /data/silver
hdfs dfs -mkdir -p /data/gold

# Upload file to HDFS
hdfs dfs -put /data/local-file.csv /data/bronze/

# Download file from HDFS
hdfs dfs -get /data/bronze/file.csv /tmp/
```

### Create Medallion Architecture

```bash
docker exec -it namenode bash

# Create Bronze/Silver/Gold structure
hdfs dfs -mkdir -p /data/bronze/weather
hdfs dfs -mkdir -p /data/bronze/consumption
hdfs dfs -mkdir -p /data/bronze/prices
hdfs dfs -mkdir -p /data/bronze/solar_potential

hdfs dfs -mkdir -p /data/silver/weather
hdfs dfs -mkdir -p /data/silver/consumption
hdfs dfs -mkdir -p /data/silver/energy_flow

hdfs dfs -mkdir -p /data/gold/aggregates
hdfs dfs -mkdir -p /data/gold/features
hdfs dfs -mkdir -p /data/gold/ml_datasets
```

---

##  Apache Spark

### Submit Spark Job

```bash
# Submit via spark-submit
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  /opt/spark-jobs/your-job.py

# Submit with dependencies
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /opt/spark-jobs/streaming-job.py
```

### Access Spark Shell

```bash
# PySpark shell
docker exec -it spark-master pyspark --master spark://spark-master:7077

# Scala shell
docker exec -it spark-master spark-shell --master spark://spark-master:7077
```

---

##  Apache Kafka

### Create Topics

```bash
docker exec -it kafka kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 3 \
  --topic energy-meters

docker exec -it kafka kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic spot-prices

docker exec -it kafka kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 2 \
  --topic anomalies
```

### List Topics

```bash
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Produce Messages

```bash
docker exec -it kafka kafka-console-producer \
  --bootstrap-server localhost:9092 \
  --topic energy-meters
```

### Consume Messages

```bash
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic energy-meters \
  --from-beginning
```
---
##  Apache Superset Setup

### First Login

1. Go to http://localhost:8088
2. Login: `admin` / `admin123`

### Connect to Data Warehouse

1. Settings → Database Connections → + Database
2. Select "PostgreSQL"
3. Connection details:
   - Host: `postgres`
   - Port: `5432`
   - Database: `energy_dwh`
   - Username: `energy_user`
   - Password: `energy_password`
