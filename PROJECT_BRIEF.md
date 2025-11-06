# Energy P2P Trading Platform - Data Engineering Project

## 📋 PROJECT OVERVIEW

### Context
This is a comprehensive Data Engineering portfolio project that demonstrates end-to-end data pipeline development for an energy peer-to-peer (P2P) trading platform. The project simulates a marketplace where residential solar producers can sell their energy surplus to neighboring consumers.

**Important**: This is a **DATA ENGINEERING showcase project**, not a full application. The focus is on demonstrating expertise in data pipelines, ETL processes, data warehousing, big data processing, and streaming architectures.

---

## 🎯 PROJECT OBJECTIVES

### Educational Goals
Demonstrate mastery of the complete data engineering lifecycle:
- ✅ Multi-source data ingestion (batch + streaming)
- ✅ Complex ETL/ELT with Medallion architecture (Bronze/Silver/Gold layers)
- ✅ Data Warehousing with dimensional modeling (star schema)
- ✅ Big Data processing (Hadoop HDFS + Apache Spark)
- ✅ Real-time streaming (Apache Kafka + Spark Structured Streaming)
- ✅ Pipeline orchestration (Apache Airflow)
- ✅ Machine Learning pipelines (SparkML)
- ✅ Data Quality & Observability (Great Expectations, Prometheus, Grafana)
- ✅ Business Intelligence visualization (Apache Superset, Streamlit)

### Technical Certifications Alignment
This project validates competencies from IBM Data Engineer certification:
- Python, SQL
- SQL Database Administration
- NoSQL Databases (MongoDB, Cassandra)
- Data Warehousing
- ETL with Bash, Python, Airflow, Kafka
- Big Data with Hadoop and Spark (SparkSQL, SparkML)

---

## 🏗️ TECHNOLOGY STACK

### Data Storage
- **HDFS (Hadoop)**: Data Lake (Bronze/Silver/Gold layers)
- **PostgreSQL**: Data Warehouse (star schema, OLAP)
- **MongoDB**: Document store (user profiles, transactions)
- **Cassandra**: Time-series data (high-frequency IoT metrics)
- **Redis**: Caching layer

### Data Processing
- **Apache Spark**: Batch processing (PySpark)
- **Spark Structured Streaming**: Real-time processing
- **SparkSQL**: Complex analytical queries
- **SparkML**: Machine learning pipelines

### Data Ingestion & Orchestration
- **Apache Kafka**: Event streaming platform
- **Apache Airflow**: Workflow orchestration
- **Python**: ETL scripts, API integrations
- **Bash**: Automation scripts

### Data Quality & Monitoring
- **Great Expectations**: Data validation framework
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards
- **ELK Stack** (optional): Centralized logging

### Visualization
- **Apache Superset**: Business intelligence dashboards
- **Streamlit**: ML predictions interactive interface
- **Grafana**: Technical monitoring dashboards

### DevOps
- **Docker + Docker Compose**: Containerization
- **GitHub Actions**: CI/CD (optional)
- **Terraform**: Infrastructure as Code (optional)

---

## 📊 DATA SOURCES

### 1. London Smart Meters Dataset (Consumption Data)
- **Source**: [Kaggle - Smart Meters in London](https://www.kaggle.com/datasets/jeanmidev/smart-meters-in-london)
- **Description**: Real electricity consumption data from 5,567 London households
- **Period**: 2011-2014
- **Frequency**: Every 30 minutes
- **Size**: ~1.6 GB
- **Format**: CSV
- **Usage**: Real consumption patterns for households

### 2. Open-Meteo API (Weather Data)
- **Source**: [Open-Meteo API](https://open-meteo.com/en/docs)
- **Description**: Historical and forecast weather data
- **Coverage**: Worldwide (focusing on UK for this project)
- **Parameters**: Temperature, solar irradiance, cloud cover, wind
- **Frequency**: Hourly
- **Cost**: Free, no API key required
- **Usage**: Weather correlation with energy production/consumption

### 3. PVGIS API (Solar Production Potential)
- **Source**: [PVGIS - Photovoltaic Geographical Information System](https://re.jrc.ec.europa.eu/pvg_tools/en/)
- **Description**: Solar energy production potential by geographic location
- **Coverage**: Europe complete
- **Data**: Hourly PV production estimates
- **Cost**: Free API
- **Usage**: Baseline model for generating realistic solar production data

### 4. Energy-Charts API (Electricity Spot Prices)
- **Source**: [Energy-Charts.info (Fraunhofer Institute)](https://api.energy-charts.info/)
- **Description**: Real-time electricity spot prices
- **Coverage**: Germany, France
- **Format**: JSON
- **Cost**: Free public API
- **Usage**: Dynamic pricing for energy trading simulation

---

## 🎯 USE CASES & DELIVERABLES

### UC1: Multi-Source Data Ingestion Pipeline
**Objective**: Ingest heterogeneous data sources with error handling, validation, and archiving.

**Tasks**:
- Extract weather data from Open-Meteo API (with retry logic, rate limiting)
- Extract electricity spot prices from Energy-Charts API
- Extract solar production potential from PVGIS API
- Load London Smart Meters CSV dataset (1.6 GB)
- Validate schemas at ingestion (Great Expectations)
- Archive raw data to HDFS Bronze layer
- Stream events to Kafka topics

**Technologies**: Python, Bash, Kafka, HDFS, Airflow

**Deliverables**:
- ✅ 4 data sources ingested into HDFS Bronze layer
- ✅ Reusable Python ingestion scripts with error handling
- ✅ Airflow DAG for daily automated ingestion

---

### UC2: Medallion Architecture Data Lake (Bronze → Silver → Gold)
**Objective**: Transform raw data into analytics-ready datasets through progressive refinement.

**Bronze Layer** (Raw Data):
- Store unmodified source data
- Preserve data lineage
- Format: JSON, CSV as-is

**Silver Layer** (Cleaned & Enriched):
- Clean data: remove duplicates, handle nulls, fix types
- Standardize schemas
- Enrich: join weather data with consumption data
- Add temporal features (hour, day_of_week, is_weekend)
- Detect and flag anomalies
- Format: Parquet (partitioned by date)

**Gold Layer** (Business-Ready):
- Aggregate metrics: daily energy balance per household
- Calculate business KPIs: revenue, savings, CO2 impact
- Create user profiles
- Apply complex transformations (window functions, rolling averages)
- Format: Parquet (optimally partitioned)

**Technologies**: PySpark, HDFS, Great Expectations

**Deliverables**:
- ✅ Complete Medallion architecture in HDFS (50+ GB)
- ✅ Spark transformation jobs with performance optimizations
- ✅ Data quality validation at each layer

---

### UC3: Dimensional Data Warehouse
**Objective**: Star schema optimized for OLAP analytical queries.

**Star Schema Design**:

**Dimension Tables**:
- `dim_users`: User profiles with SCD Type 2 (Slowly Changing Dimensions)
  - user_sk (surrogate key), user_id, location, panel_size_kwp, user_type
  - effective_date, expiration_date, is_current (for historization)

- `dim_time`: Pre-populated time dimension
  - time_sk, date, hour, day_of_week, is_weekend, is_holiday, month, quarter, year

- `dim_weather`: Weather conditions
  - weather_sk, date, hour, location_zone, temperature, cloud_cover, solar_irradiance

- `dim_prices`: Electricity pricing
  - price_sk, date, hour, spot_price, grid_buy_price, grid_sell_price, price_category

**Fact Tables**:
- `fact_energy_flow`: Hourly production/consumption per user
  - Measures: production_kwh, consumption_kwh, self_consumption_kwh, surplus_kwh
  - Foreign keys to all dimensions

- `fact_energy_transactions`: Energy trades between users
  - Measures: energy_kwh, transaction_amount_eur, distance_km, co2_saved_kg
  - Links seller_sk and buyer_sk

- `fact_monthly_summary`: Pre-aggregated monthly metrics (performance optimization)
  - Measures: total_production, total_consumption, total_revenue, total_co2_saved

**Technologies**: PostgreSQL, PySpark (for ETL), SQL (DDL/DML)

**Deliverables**:
- ✅ Complete star schema implemented in PostgreSQL
- ✅ ETL scripts loading from Gold layer to DW
- ✅ Optimized indexes and partitioning
- ✅ SCD Type 2 implementation for historical tracking

---

### UC4: Real-Time Streaming Pipeline
**Objective**: Process event streams with sub-5-second latency.

**Architecture**:

**Kafka Topics**:
- `energy-meters`: Production/consumption events (1000 msg/sec)
- `spot-prices`: Price updates (1 msg/min)
- `weather-alerts`: Weather change notifications (variable)
- `dashboard-updates`: Aggregated metrics for real-time dashboards
- `anomalies`: Detected anomalies

**Spark Streaming Jobs**:

**Job 1: Real-Time Aggregations**
- Read from `energy-meters` topic
- Apply tumbling window (5 minutes)
- Calculate: SUM, AVG, MAX, MIN per household
- Write to Cassandra (time-series storage)
- Publish to `dashboard-updates` topic

**Job 2: Anomaly Detection**
- Detect impossible values (production < 0, consumption > 50 kWh)
- Flag missing data
- Identify statistical outliers (> P99.9)
- Write alerts to MongoDB
- Publish to `anomalies` topic

**Event Simulator**:
- Replay historical data in accelerated time (1 day = 1 minute)
- Generate realistic event stream
- Inject random perturbations (simulate sensor failures)

**Technologies**: Kafka, Spark Structured Streaming, Cassandra, MongoDB, Python

**Deliverables**:
- ✅ Kafka cluster with configured topics
- ✅ Event simulator generating 1000+ msg/min
- ✅ 2 Spark Streaming jobs processing in real-time
- ✅ End-to-end latency < 10 seconds

---

### UC5: Machine Learning Pipelines
**Objective**: Train predictive models and automate inference.

**Feature Engineering**:
- Temporal features: hour, day_of_week, month, season, is_holiday
- Lag features: consumption_lag_1h, consumption_lag_24h, consumption_lag_168h (1 week)
- Rolling features: avg_consumption_7d, std_consumption_7d, max_production_7d
- Weather enrichment: temperature, solar_irradiance, cloud_cover, temp_squared (non-linearity)
- Interaction features: irradiance × temperature
- Categorical encoding: one-hot encoding weather_condition

**Model 1: Solar Production Prediction**
- Algorithm: Gradient Boosting Regressor (SparkML)
- Features: Weather (irradiance, temperature, cloud_cover) + temporal + location
- Target: production_kwh (next 24 hours)
- Training: 2 years historical data (1M+ samples)
- Evaluation: RMSE < 0.5 kWh, R² > 0.90
- Use case: Help users forecast daily production

**Model 2: Consumption Prediction**
- Algorithm: Random Forest or Gradient Boosting (SparkML)
- Features: Historical consumption (lags) + weather + temporal
- Target: consumption_kwh (next 24 hours)
- Training: 2 years historical data (800K+ samples)
- Evaluation: MAPE < 10%, R² > 0.85
- Use case: Predict energy needs for purchase planning

**Model 3: Spot Price Prediction** (Optional)
- Algorithm: LSTM (if time permits) or GBT
- Features: Historical prices + time + demand indicators
- Target: spot_price (next 6 hours)
- Use case: Optimize selling time

**MLOps**:
- Model versioning and tracking
- Hyperparameter tuning with CrossValidator
- Batch inference pipeline (daily predictions)
- Model performance monitoring

**Technologies**: SparkML, PySpark, Python (scikit-learn optionally)

**Deliverables**:
- ✅ 2-3 trained ML models with documented metrics
- ✅ Feature engineering pipeline (1M+ rows)
- ✅ Automated batch inference (Airflow DAG)
- ✅ Predictions stored in PostgreSQL for dashboards

---

### UC6: Workflow Orchestration with Airflow
**Objective**: Automate all pipelines with dependencies, retries, and alerting.

**DAG 1: Daily Data Ingestion**
- Schedule: `@daily` (2:00 AM)
- Tasks:
  - `ingest_weather`: Fetch yesterday's weather data (Open-Meteo API)
  - `ingest_prices`: Fetch electricity prices (Energy-Charts API)
  - `validate_ingestion`: Run Great Expectations checks
  - `archive_to_bronze`: Upload to HDFS
  - `publish_to_kafka`: Stream events
- Error handling: 3 retries with exponential backoff
- Alerting: Email on failure

**DAG 2: Bronze → Silver → Gold Transformations**
- Schedule: `@daily` (3:00 AM, after ingestion)
- Dependencies: Wait for DAG 1 completion (ExternalTaskSensor)
- Tasks:
  - `transform_weather_to_silver`: Clean and standardize
  - `transform_consumption_to_silver`: Clean consumption data
  - `enrich_with_weather`: Join consumption + weather
  - `generate_solar_production`: Simulate production (physics model)
  - `validate_silver`: Great Expectations checks
  - `aggregate_to_gold`: Calculate energy balance and metrics
  - `validate_gold`: Final quality checks
- Parallelization: Independent transformations run in parallel

**DAG 3: Data Warehouse Loading**
- Schedule: `@daily` (5:00 AM, after transformations)
- Tasks:
  - `load_dim_users_scd2`: Update user dimension with SCD Type 2
  - `load_dim_weather`: Load weather dimension
  - `load_dim_prices`: Load price dimension
  - `load_fact_energy_flow`: Load main fact table (with dimension key lookups)
  - `refresh_monthly_aggregates`: Update pre-computed summaries
  - `validate_dw`: Check referential integrity and metrics
- Incremental loading: Only new/updated records

**DAG 4: ML Training Pipeline**
- Schedule: `@weekly` (Sunday 2:00 AM)
- Tasks:
  - `prepare_ml_features`: Feature engineering (Spark job)
  - `train_production_model`: Train solar production model
  - `train_consumption_model`: Train consumption model
  - `evaluate_models`: Calculate RMSE, MAE, R²
  - `register_best_models`: Save if performance improved
  - `generate_ml_report`: Create evaluation notebook
- Conditional: Only register model if metrics improve

**DAG 5: Daily Batch Inference**
- Schedule: `@daily` (6:00 AM, after DW loading)
- Tasks:
  - `load_latest_features`: Prepare input data
  - `predict_production`: Generate next 24h production forecasts
  - `predict_consumption`: Generate next 24h consumption forecasts
  - `calculate_confidence_intervals`: Statistical intervals
  - `save_predictions_to_dw`: Store in PostgreSQL
- Used by: Streamlit dashboard for visualizations

**Advanced Features**:
- Branching: Conditional task execution based on data availability
- Sensors: Wait for external dependencies
- SLAs: Alert if tasks exceed time limits
- Task groups: Logical grouping for clarity
- Callbacks: Slack notifications on success/failure

**Technologies**: Apache Airflow, Python, PySpark

**Deliverables**:
- ✅ 5 production-ready DAGs with complex dependencies
- ✅ Comprehensive error handling and retries
- ✅ Alerting configured (email/Slack)
- ✅ Full pipeline automation (zero manual intervention)

---

### UC7: Data Quality & Observability
**Objective**: Guarantee data quality and full system observability.

**Data Quality (Great Expectations)**:

**Bronze Layer Checks**:
- Schema validation: Expected columns present
- Freshness: Data less than 24 hours old
- Completeness: File not empty

**Silver Layer Checks**:
- No null values in critical columns (household_id, timestamp, kwh)
- Range validation:
  - temperature between -20°C and 45°C
  - consumption_kwh between 0 and 50
  - production_kwh >= 0
- Uniqueness: (household_id, timestamp) combinations are unique
- Statistical: Mean consumption between 1.0 and 10.0 kWh

**Gold Layer Checks**:
- Business logic: production + grid_import = consumption + grid_export
- Referential integrity: All household_ids exist in user_profiles
- Aggregation sanity: daily_production = SUM(hourly_production)

**Data Warehouse Checks**:
- Foreign key constraints validated
- No orphaned records
- Fact table measures sum to expected totals
- SCD Type 2: Only one current record per user

**Expectations Suite**:
- 30+ automated checks
- HTML reports generated (Data Docs)
- Integrated in Airflow DAGs
- Alerting on failures

**Monitoring (Prometheus + Grafana)**:

**Prometheus Metrics**:
- **Kafka**: Consumer lag, message throughput, topic size
- **Spark**: Job duration (P50, P95, P99), records processed, shuffle size
- **Airflow**: DAG success rate, task duration, queue size
- **Databases**: Connection count, query latency, table sizes
- **System**: CPU, RAM, disk usage (Node Exporter)
- **Custom**: Records processed per pipeline, data freshness, error rate

**Grafana Dashboards**:

**Dashboard 1: Pipeline Health**
- Panel: Airflow DAG status (last 7 days)
- Panel: Kafka consumer lag per topic
- Panel: Spark job execution time (line chart)
- Panel: Data volume by layer (Bronze/Silver/Gold)
- Panel: HDFS disk usage
- Panel: PostgreSQL/MongoDB/Cassandra stats

**Dashboard 2: Data Quality**
- Panel: Great Expectations success rate
- Panel: Anomalies detected (count over time)
- Panel: Data freshness by source
- Panel: Records processed per hour
- Panel: Error rate per pipeline stage

**Alerting**:
- Slack webhook integration
- Email notifications
- Alert rules:
  - Kafka lag > 1000 messages
  - DAG failure
  - Data quality check failure
  - Disk usage > 80%
  - Spark job > 30 min duration

**Logging (Optional - ELK Stack)**:
- Centralized logs from all services
- Elasticsearch for storage
- Logstash for parsing
- Kibana for exploration

**Technologies**: Great Expectations, Prometheus, Grafana, Slack API

**Deliverables**:
- ✅ 30+ automated data quality checks
- ✅ 2 comprehensive Grafana dashboards
- ✅ Alerting system operational
- ✅ Data quality reports (HTML)

---

### UC8: Business Intelligence Dashboards
**Objective**: Visualize results through 3 targeted dashboards.

**Dashboard 1: Technical Monitoring (Grafana)**
**Purpose**: For data engineers - monitor system health
**Audience**: Technical team

**Panels**:
- Airflow DAG execution status (success/failure timeline)
- Kafka topics metrics (throughput, lag, partition count)
- Spark jobs performance (duration, stages, memory usage)
- Data volume evolution (Bronze/Silver/Gold GB over time)
- Database sizes (PostgreSQL, MongoDB, Cassandra)
- Data quality checks success rate
- System resources (CPU, RAM, disk per service)

**Refresh**: Auto-refresh every 10 seconds

**Technology**: Grafana connected to Prometheus

---

**Dashboard 2: Business Analytics (Apache Superset)**
**Purpose**: For business users - insights and KPIs
**Audience**: Energy marketplace stakeholders, product managers

**Page 1: Overview**
- **KPI Cards**:
  - Total transactions (last 30 days)
  - Average daily revenue (€)
  - Total energy traded (kWh)
  - Active users count
  - All with % change vs previous period

- **Energy Flow Chart** (Area Chart):
  - X-axis: Hour of day (0-23)
  - Y-axis: kWh
  - Series: Production (green), Consumption (blue), Surplus sold (yellow), Energy bought (red)
  - Aggregation: Average per hour over last 30 days

- **Marketplace Dynamics** (Dual-axis Line Chart):
  - Primary axis: Average price evolution (€/kWh)
  - Secondary axis: Supply vs Demand (kWh)
  - Comparison with grid price (baseline)

**Page 2: Performance Analysis**
- **Top Performers Tables**:
  - Top 10 sellers by volume (kWh)
  - Top 10 buyers by savings (€)
  - Columns: User ID, Total volume/savings, Transaction count

- **Geographic Heatmap**:
  - Map of zones colored by transaction volume
  - Tooltip: Zone name, transaction count, avg price

- **Time Series Analysis**:
  - Daily revenue trend (line chart)
  - Weekly energy volume (bar chart)
  - Monthly growth metrics

**Page 3: Impact Dashboard**
- **CO2 Savings**:
  - Total CO2 saved (kg)
  - Equivalent: km avoided by car, trees planted
  - Progress bar toward monthly goal
  - Trend over time

- **Self-Sufficiency Metrics**:
  - Average self-consumption rate (%)
  - Distribution histogram
  - Top self-sufficient users

**SQL Queries** (examples):
```sql
-- KPI: Total transactions
SELECT COUNT(*) as total_transactions,
       SUM(transaction_amount_eur) as total_revenue,
       SUM(energy_kwh) as total_volume
FROM fact_energy_transactions t
JOIN dim_time dt ON t.time_sk = dt.time_sk
WHERE dt.date >= CURRENT_DATE - INTERVAL '30 days';

-- Energy flow hourly average
SELECT dt.hour,
       AVG(production_kwh) as avg_production,
       AVG(consumption_kwh) as avg_consumption
FROM fact_energy_flow f
JOIN dim_time dt ON f.time_sk = dt.time_sk
WHERE dt.date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY dt.hour
ORDER BY dt.hour;
```

**Refresh**: Auto-refresh every 5 minutes

**Technology**: Apache Superset connected to PostgreSQL DW

---

**Dashboard 3: ML Predictions (Streamlit)**
**Purpose**: Interactive ML predictions demonstration
**Audience**: Technical demonstration, recruiters

**Layout**:

**Sidebar**:
- Dropdown: Select household (from dim_users)
- Date range picker
- Refresh button

**Main Area**:

**Section 1: Solar Production Forecast**
- Line chart (Plotly):
  - X-axis: Timestamp (next 24 hours)
  - Y-axis: kWh
  - Series 1: Predicted production (green solid line)
  - Series 2: Actual production (blue dotted line, if available)
  - Confidence interval: Shaded area (95% confidence)
- Metric cards:
  - Model: "Gradient Boosting Regressor"
  - RMSE: "0.42 kWh"
  - MAE: "0.31 kWh"
  - R² Score: "0.94"

**Section 2: Consumption Forecast**
- Similar line chart for consumption
- Historical pattern overlay (last week, light gray)
- Model metrics:
  - Model: "Random Forest"
  - MAPE: "8.3%"
  - Accuracy: "91.7%"

**Section 3: Energy Surplus Prediction**
- Info box:
  - "Tomorrow 10h-16h: 6.3 kWh surplus expected"
  - Recommended action: SELL / BUY / HOLD
  - Expected revenue: "€0.88 - €1.26"
  - Confidence: "87%"

**Section 4: Spot Price Prediction** (Optional)
- Bar chart: Predicted prices next 6 hours
- Color-coded: Green (low price), Red (high price)
- Annotations: "Best time to sell: 14h (€0.18/kWh)"

**Section 5: Model Performance Tracking**
- Small table:
  - Model name | Version | Last trained | Training samples | Online accuracy
- Link: "View detailed model metrics →" (to notebook)

**Auto-refresh**: Every 30 seconds

**Technology**: Streamlit (Python), Plotly graphs, PostgreSQL connection

**Code structure**:
```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🤖 Energy Prediction Engine")

# Sidebar
household = st.sidebar.selectbox("Select Household", get_households())

# Read predictions from DW
predictions = pd.read_sql(f"""
    SELECT * FROM ml_predictions
    WHERE household_id = '{household}'
""", db_connection)

# Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=predictions['timestamp'],
                         y=predictions['predicted_production'],
                         name='Predicted'))
st.plotly_chart(fig)
```

---

**Dashboard Summary**:

| Dashboard | Tool | Purpose | Audience | Refresh |
|-----------|------|---------|----------|---------|
| Technical Monitoring | Grafana | System health | Data Engineers | 10s |
| Business Analytics | Superset | Business insights | Stakeholders | 5min |
| ML Predictions | Streamlit | Demo ML models | Recruiters | 30s |

**Deliverables**:
- ✅ Grafana: 2 technical dashboards (Pipeline Health, Data Quality)
- ✅ Superset: 3 business dashboards (Overview, Performance, Impact)
- ✅ Streamlit: 1 interactive ML app
- ✅ All dashboards reading from PostgreSQL DW and live systems

---

## 📐 SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                   VISUALIZATION LAYER                    │
│  ┌──────────┐    ┌───────────┐    ┌──────────────┐     │
│  │ Grafana  │    │ Superset  │    │  Streamlit   │     │
│  │(Monitoring)   │(Analytics)│    │(ML Predictions)    │
│  └────┬─────┘    └─────┬─────┘    └──────┬───────┘     │
└───────┼─────────��──────┼──────────────────┼─────────────┘
        │                │                  │
   ┌────┴────┐      ┌────┴────┐       ┌────┴────┐
   │Prometheus│      │PostgreSQL│       │PostgreSQL│
   │ Metrics  │      │   DWH    │       │   DWH   │
   └────▲─────┘      └────▲─────┘       └────▲────┘
        │                 │                  │
┌───────┴─────────────────┴──────────────────┴─────────────┐
│              DATA PROCESSING LAYER                        │
│  ┌──────────────────────────────────────────────────┐    │
│  │          Apache Airflow (Orchestration)          │    │
│  │  DAGs: Ingestion | Transformation | DW | ML      │    │
│  └──────────────────┬───────────────────────────────┘    │
│                     │                                     │
│  ┌──────────────────▼───────────────────────────────┐    │
│  │         Apache Spark (Batch Processing)          │    │
│  │  Bronze→Silver→Gold | Feature Eng | ML Training  │    │
│  └──────────────────────────────────────────────────┘    │
│                                                           │
│  ┌────────────────────────────────────────────────┐      │
│  │  Kafka + Spark Streaming (Real-time)          │      │
│  │  Topics: meters, prices, alerts | CEP | Agg   │      │
│  └────────────────────────────────────────────────┘      │
└───────────────────────┬───────────────────────────────────┘
                        │
┌───────────────────────▼───────────────────────────────────┐
│                  STORAGE LAYER                            │
│  ┌─────────────┐  ┌──────────┐  ┌─────────┐  ┌─────────┐│
│  │    HDFS     │  │PostgreSQL│  │ MongoDB │  │Cassandra││
│  │  Data Lake  │  │   DWH    │  │ Docs    │  │TimeSeries│
│  │Bronze/Silver│  │StarSchema│  │ Users   │  │Streaming││
│  │   /Gold     │  │  OLAP    │  │ Alerts  │  │  Agg    ││
│  └─────────────┘  └──────────┘  └─────────┘  └─────────┘│
└───────────────────────▲───────────────────────────────────┘
                        │
┌───────────────────────┴───────────────────────────────────┐
│                  INGESTION LAYER                          │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │
│  │  Python    │  │   Kafka    │  │  Bash Scripts    │   │
│  │API Clients │  │ Producers  │  │  File Uploads    │   │
│  └────────────┘  └────────────┘  └──────────────────┘   │
└───────────────────────▲───────────────────────────────────┘
                        │
┌───────────────────────┴───────────────────────────────────┐
│                    DATA SOURCES                           │
│  Open-Meteo API | Energy-Charts | PVGIS | Smart Meters   │
└───────────────────────────────────────────────────────────┘
```

---

## 📊 DATA FLOW

### Batch Pipeline (Daily)
1. **Ingestion** (2:00 AM):
   - Airflow triggers API calls (weather, prices)
   - Download to local staging
   - Upload to HDFS `/bronze/`
   - Publish metadata to Kafka

2. **Bronze → Silver** (3:00 AM):
   - Spark reads from Bronze
   - Clean: remove duplicates, handle nulls, type conversion
   - Enrich: join weather + consumption
   - Validate: Great Expectations
   - Write Parquet to `/silver/` (partitioned by date)

3. **Silver → Gold** (4:00 AM):
   - Spark reads from Silver
   - Generate solar production (physics model)
   - Calculate energy balance (production - consumption)
   - Aggregate: daily/monthly metrics
   - Window functions: rolling averages
   - Write Parquet to `/gold/`

4. **Gold → DW** (5:00 AM):
   - Spark reads from Gold
   - Lookup dimension keys
   - SCD Type 2 updates (dim_users)
   - Load facts (incremental)
   - Refresh aggregates (materialized views)
   - Validate referential integrity

5. **ML Training** (Weekly, Sunday 2:00 AM):
   - Feature engineering from Silver
   - Train models (SparkML)
   - Evaluate performance
   - Register if improved

6. **ML Inference** (6:00 AM):
   - Load models
   - Generate predictions (next 24h)
   - Save to PostgreSQL

### Streaming Pipeline (Continuous)
1. **Event Generation**:
   - Simulator replays historical data
   - Produce to Kafka topics (energy-meters, spot-prices)

2. **Spark Streaming Consumption**:
   - Read from Kafka
   - Tumbling window aggregation (5 min)
   - Anomaly detection
   - Write to Cassandra (time-series)
   - Publish to dashboard-updates topic

3. **Real-time Dashboards**:
   - Grafana reads from Prometheus (Kafka metrics)
   - Streamlit reads from Cassandra (latest aggregates)

---

## 🗓️ PROJECT ROADMAP (10 WEEKS)

### Week 1: Infrastructure Setup & Basic Ingestion
- **Day 1-2**: Install Docker Compose, configure all services (Hadoop, Kafka, Airflow, PostgreSQL, MongoDB, Cassandra, Grafana)
- **Day 3**: Load London Smart Meters CSV to HDFS Bronze
- **Day 4-5**: Develop Python ingestion script for Open-Meteo API
- **Day 6-7**: Develop ingestion for Energy-Charts and PVGIS APIs
- **Deliverables**: 4 data sources in HDFS Bronze, reusable scripts

### Week 2: Bronze → Silver Transformations (Spark)
- **Day 1-2**: Setup PySpark, create first Spark job (clean weather data)
- **Day 3**: Transform Smart Meters consumption data
- **Day 4-5**: Generate synthetic solar production data (physics-based model)
- **Day 6-7**: Transform prices, validate Silver layer with Great Expectations
- **Deliverables**: Complete Silver layer (4 cleaned datasets), data quality suite

### Week 3: Silver → Gold + Data Warehouse
- **Day 1-2**: Create Gold aggregations (energy balance, user profiles)
- **Day 3**: Additional Gold metrics (CO2, revenue calculations)
- **Day 4-5**: Design star schema, write DDL scripts, initialize PostgreSQL
- **Day 6-7**: Develop ETL scripts (Gold → DW), implement SCD Type 2
- **Deliverables**: Gold layer complete, PostgreSQL DW populated

### Week 4: Airflow Orchestration
- **Day 1-2**: Create DAG 1 (daily ingestion)
- **Day 3**: Create DAG 2 (Bronze → Silver transformations)
- **Day 4**: Create DAG 3 (Silver → Gold + DW loading)
- **Day 5-7**: Create DAG 4 (ML training), optimize all DAGs (error handling, alerting)
- **Deliverables**: 4 production-ready DAGs

### Week 5: Real-Time Streaming (Kafka + Spark Streaming)
- **Day 1-2**: Configure Kafka topics and producers
- **Day 3-4**: Build event simulator (replay historical data)
- **Day 5-7**: Develop Spark Streaming jobs (aggregations, anomaly detection)
- **Deliverables**: Streaming pipeline operational (1000+ msg/min, <10s latency)

### Week 6: Machine Learning Pipelines
- **Day 1-2**: Feature engineering (lag features, rolling averages, weather interactions)
- **Day 3-4**: Train solar production prediction model (SparkML)
- **Day 5-6**: Train consumption prediction model
- **Day 7**: Batch inference pipeline, integrate with Airflow
- **Deliverables**: 2 trained models (R² > 0.90), automated inference

### Week 7: Data Quality, Monitoring & Documentation
- **Day 1-2**: Implement comprehensive Great Expectations suite (30+ checks)
- **Day 3-4**: Configure Prometheus + Grafana dashboards (pipeline health, data quality)
- **Day 5-7**: Write technical documentation (README, architecture, data dictionary, runbook)
- **Deliverables**: Full observability, professional documentation

### Week 8: Visualization Dashboards
- **Day 1-2**: Finalize Grafana monitoring dashboards
- **Day 3-5**: Create Superset business analytics dashboards (3 dashboards)
- **Day 6-7**: Build Streamlit ML predictions app
- **Deliverables**: 6 dashboards across 3 tools

### Week 9: Testing, Optimization & DevOps
- **Day 1-2**: Write unit tests and integration tests (pytest, 50+ tests)
- **Day 3-4**: Spark performance optimizations (broadcast joins, partitioning, caching)
- **Day 5-6**: Setup CI/CD (GitHub Actions), write Terraform IaC (optional)
- **Day 7**: Code cleanup, final polish
- **Deliverables**: Production-ready codebase, benchmarked optimizations

### Week 10: Demo Preparation & Launch
- **Day 1-2**: Record 10-minute demo video (architecture + live demo)
- **Day 3-4**: Create presentation slide deck (15 slides)
- **Day 5-6**: Practice live demo, prepare Q&A responses
- **Day 7**: Publish GitHub repo, LinkedIn post, portfolio update
- **Deliverables**: Public project ready for recruiters

---

## 📈 PROJECT METRICS & SUCCESS CRITERIA

### Data Volume
- HDFS Data Lake: 50+ GB (Bronze/Silver/Gold combined)
- PostgreSQL DW: 10 tables, 3+ GB
- MongoDB: 10K+ documents (user profiles, alerts)
- Cassandra: 1M+ time-series records

### Pipeline Performance
- Batch ETL: Complete Bronze → DW in < 30 minutes
- Streaming latency: < 10 seconds end-to-end
- Spark job optimization: 80%+ reduction after tuning
- Airflow DAG success rate: > 99%

### Data Quality
- Great Expectations: 30+ automated checks
- Data quality success rate: > 98%
- Zero data loss in pipelines
- Full data lineage documented

### Machine Learning
- Solar production model: R² > 0.90, RMSE < 0.5 kWh
- Consumption model: MAPE < 10%, R² > 0.85
- Predictions generated daily for 5,000+ households
- Model retraining: Weekly automated

### Code Quality
- 50+ unit tests (coverage > 70%)
- All functions documented (docstrings)
- PEP 8 compliant
- CI/CD pipeline operational

### Documentation
- Complete README with architecture diagram
- Data dictionary (all tables/columns documented)
- Operational runbook
- 10-minute demo video
- 15-slide presentation deck

---

## 🎯 KEY LEARNING OUTCOMES

By completing this project, you demonstrate:

1. **Data Engineering Fundamentals**:
   - Multi-source ingestion (APIs, files, streams)
   - ETL/ELT design patterns
   - Data lake architecture (Medallion)
   - Data warehouse dimensional modeling

2. **Big Data Technologies**:
   - Hadoop HDFS for distributed storage
   - Spark for large-scale processing
   - Kafka for event streaming
   - Cassandra for time-series data

3. **Production Best Practices**:
   - Workflow orchestration (Airflow)
   - Data quality validation
   - Monitoring and alerting
   - Error handling and retries

4. **Advanced Spark**:
   - Performance optimization (partitioning, caching, broadcast joins)
   - Structured Streaming (windowing, watermarks)
   - SparkML pipelines

5. **DevOps & MLOps**:
   - Containerization (Docker)
   - CI/CD automation
   - Infrastructure as Code (Terraform)
   - Model versioning and deployment

6. **Communication**:
   - Technical documentation
   - Dashboard design
   - Demo presentation
   - Explaining trade-offs

---

## 🚀 HOW TO USE THIS DOCUMENT

### For Implementation with Claude AI:
When working with Claude on specific tasks, reference the relevant use case:

**Example prompts**:
- "Let's implement UC1: Multi-Source Data Ingestion. Start with the Open-Meteo API script."
- "I'm on Week 3, Day 4-5. Help me design the PostgreSQL star schema."
- "Guide me through setting up the Kafka topics for UC4: Real-Time Streaming."
- "I need help optimizing the Spark job for Silver→Gold transformations."

### For Demonstrations:
- Show this document to explain project scope and architecture
- Reference specific use cases when walking through code
- Use the metrics section to highlight achievements
- Point to the roadmap to show systematic approach

### For Interviews:
- Use the architecture diagram to explain system design
- Discuss trade-offs in technology choices
- Reference specific use cases when asked about experience
- Share metrics as evidence of production-readiness

---

## 📝 IMPORTANT NOTES

### Data Authenticity
- **Real data**: London Smart Meters (consumption), Open-Meteo (weather), Energy-Charts (prices)
- **Simulated data**: Solar production (generated using physics-based model with real weather data)
- **Transparency**: Clearly document what is real vs simulated in all materials

### Scope Management
- This is a DATA ENGINEERING project, not a full application
- Focus 95% effort on pipelines, 5% on visualization
- Dashboards are for demonstrating the data, not the end product
- Prioritize: Architecture > Code Quality > Completeness > UI Polish

### Time Investment
- 10 weeks at 20-25 hours/week = 200-250 hours total
- Suitable as a 3-month side project during work/studies
- Can be shortened to 6-8 weeks with full-time effort

### Cost Considerations
- Local development: Free (Docker on laptop)
- Cloud deployment: Use free tiers (AWS Free Tier, GCP credits)
- Optional: $20-30/month for persistent cloud demo environment

---

## ✅ PROJECT CHECKLIST

Use this checklist to track progress:

**Infrastructure**:
- [ ] Docker Compose with all services running
- [ ] HDFS accessible and configured
- [ ] Kafka topics created
- [ ] Airflow UI accessible
- [ ] All databases initialized

**Data Ingestion**:
- [ ] London Smart Meters loaded to HDFS
- [ ] Open-Meteo API integration working
- [ ] Energy-Charts API integration working
- [ ] PVGIS API integration working
- [ ] Ingestion DAG automated in Airflow

**Data Lake**:
- [ ] Bronze layer populated (raw data)
- [ ] Silver layer implemented (cleaned data)
- [ ] Gold layer implemented (aggregated data)
- [ ] Data quality checks at each layer

**Data Warehouse**:
- [ ] Star schema designed and documented
- [ ] Dimension tables created and populated
- [ ] Fact tables created and populated
- [ ] SCD Type 2 implemented
- [ ] Indexes optimized

**Streaming**:
- [ ] Kafka producers generating events
- [ ] Spark Streaming jobs processing in real-time
- [ ] Cassandra storing time-series aggregates
- [ ] Anomaly detection operational

**Machine Learning**:
- [ ] Feature engineering pipeline complete
- [ ] Solar production model trained (R² > 0.90)
- [ ] Consumption model trained (MAPE < 10%)
- [ ] Batch inference automated
- [ ] Predictions available in dashboards

**Orchestration**:
- [ ] Ingestion DAG operational
- [ ] Transformation DAG operational
- [ ] DW loading DAG operational
- [ ] ML training DAG operational
- [ ] Error handling and alerting configured

**Quality & Monitoring**:
- [ ] Great Expectations suite (30+ checks)
- [ ] Prometheus collecting metrics
- [ ] Grafana dashboards (monitoring)
- [ ] Data quality reports generated

**Visualization**:
- [ ] Grafana: Pipeline health dashboard
- [ ] Grafana: Data quality dashboard
- [ ] Superset: Business overview dashboard
- [ ] Superset: Performance analysis dashboard
- [ ] Superset: Impact dashboard
- [ ] Streamlit: ML predictions app

**Testing & Optimization**:
- [ ] Unit tests written (50+ tests, coverage > 70%)
- [ ] Integration tests for pipelines
- [ ] Spark jobs optimized (benchmarked)
- [ ] Performance documented

**Documentation**:
- [ ] README.md complete with architecture diagram
- [ ] ARCHITECTURE.md detailed
- [ ] DATA_DICTIONARY.md complete
- [ ] RUNBOOK.md for operations
- [ ] Code documented (docstrings)

**Demo Materials**:
- [ ] 10-minute demo video recorded
- [ ] 15-slide presentation deck created
- [ ] GitHub repo public and polished
- [ ] LinkedIn post published
- [ ] Portfolio updated

---

## 🎓 FINAL DELIVERABLES SUMMARY

### Code Repository Structure
```
energy-p2p-data-platform/
├── README.md                          # Project overview
├── docker-compose.yml                 # Infrastructure setup
├── .env.example                       # Environment variables template
├── airflow/
│   ├── dags/
│   │   ├── 01_ingest_daily_data.py
│   │   ├── 02_bronze_to_silver.py
│   │   ├── 03_silver_to_gold_and_dw.py
│   │   ├── 04_ml_training.py
│   │   └── 05_batch_inference.py
│   └── plugins/
├── spark/
│   ├── jobs/
│   │   ├── bronze_to_silver_weather.py
│   │   ├── bronze_to_silver_consumption.py
│   │   ├── generate_solar_production.py
│   │   ├── silver_to_gold_energy_balance.py
│   │   └── load_datawarehouse.py
│   └── ml/
│       ├── train_production_model.py
│       ├── train_consumption_model.py
│       └── batch_inference.py
├── streaming/
│   ├── event_simulator.py
│   ├── spark_aggregations.py
│   └── anomaly_detector.py
├── ingestion/
│   ├── ingest_weather.py
│   ├── ingest_prices.py
│   └── ingest_pvgis.py
├── dashboards/
│   ├── ml_predictions_app.py          # Streamlit app
│   └── grafana/
│       └── dashboards.json
├── sql/
│   ├── ddl/
│   │   ├── create_star_schema.sql
│   │   └── create_indexes.sql
│   └── queries/
│       └── analytics_queries.sql
├── tests/
│   ├── unit/
│   ├── integration/
│   └── great_expectations/
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_evaluation.ipynb
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA_DICTIONARY.md
│   ├── RUNBOOK.md
│   └── images/
│       └── architecture_diagram.png
├── terraform/                         # Optional: IaC
│   ├── main.tf
│   └── variables.tf
└── .github/
    └── workflows/
        └── ci.yml
```

### Documentation Deliverables
1. **README.md**: Project overview, setup instructions, architecture
2. **ARCHITECTURE.md**: Detailed system design, technology justifications
3. **DATA_DICTIONARY.md**: All tables, schemas, column descriptions
4. **RUNBOOK.md**: Operations guide, troubleshooting
5. **Demo video**: 10-minute walkthrough (YouTube)
6. **Presentation deck**: 15 slides (PDF)

### Technical Artifacts
1. **Codebase**: 5,000+ lines of production-quality Python/SQL
2. **Data pipeline**: 5 Airflow DAGs, 20+ Spark jobs
3. **Databases**: PostgreSQL (10 tables), MongoDB, Cassandra, HDFS (50+ GB)
4. **ML models**: 2 trained models with documented performance
5. **Dashboards**: 6 dashboards across 3 platforms
6. **Tests**: 50+ automated tests
7. **Monitoring**: Prometheus + Grafana fully configured

---

## 🎤 ELEVATOR PITCH (for recruiters)

*"I built an end-to-end data engineering platform simulating a peer-to-peer energy trading marketplace. The system ingests data from 4 heterogeneous sources (APIs and large CSV files), processes 50+ GB through a Medallion architecture (Bronze/Silver/Gold layers) using Apache Spark, streams real-time events via Kafka with sub-10-second latency, and populates a dimensional data warehouse. The entire pipeline is orchestrated with Airflow (5 DAGs), includes ML models for production and consumption forecasting (R² > 0.90), and features comprehensive data quality checks and monitoring. All infrastructure runs on Docker, the code is tested (70%+ coverage), and results are visualized through Grafana, Superset, and Streamlit dashboards. This project demonstrates my ability to design, implement, and operate production-grade data platforms."*

---

**END OF PROJECT BRIEF**

This document serves as your comprehensive guide for implementing the Energy P2P Data Engineering project. Reference specific sections when working with Claude AI on implementation tasks, and use it as a portfolio artifact to demonstrate project scope and planning skills to recruiters.
