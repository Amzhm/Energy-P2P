-- Cassandra Initialization Script
-- This script creates the keyspace and tables for time-series data

-- Create keyspace
CREATE KEYSPACE IF NOT EXISTS energy_timeseries
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE energy_timeseries;

-- Table for real-time energy metrics (streaming data)
CREATE TABLE IF NOT EXISTS energy_metrics_realtime (
    household_id text,
    timestamp timestamp,
    production_kwh double,
    consumption_kwh double,
    self_consumption_kwh double,
    grid_import_kwh double,
    grid_export_kwh double,
    battery_charge_kwh double,
    battery_level_percent double,
    PRIMARY KEY (household_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND default_time_to_live = 604800  -- 7 days retention
  AND compaction = {
    'class': 'TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': 1
};

-- Table for aggregated metrics (5-minute windows)
CREATE TABLE IF NOT EXISTS energy_metrics_5min (
    household_id text,
    window_start timestamp,
    window_end timestamp,
    avg_production_kwh double,
    avg_consumption_kwh double,
    max_production_kwh double,
    max_consumption_kwh double,
    min_production_kwh double,
    min_consumption_kwh double,
    total_production_kwh double,
    total_consumption_kwh double,
    record_count int,
    PRIMARY KEY (household_id, window_start)
) WITH CLUSTERING ORDER BY (window_start DESC)
  AND default_time_to_live = 2592000  -- 30 days retention
  AND compaction = {
    'class': 'TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': 7
};

-- Table for hourly aggregations
CREATE TABLE IF NOT EXISTS energy_metrics_hourly (
    household_id text,
    date text,  -- Format: YYYY-MM-DD
    hour int,
    avg_production_kwh double,
    avg_consumption_kwh double,
    max_production_kwh double,
    max_consumption_kwh double,
    total_production_kwh double,
    total_consumption_kwh double,
    energy_balance_kwh double,  -- production - consumption
    self_sufficiency_percent double,
    record_count int,
    PRIMARY KEY ((household_id, date), hour)
) WITH CLUSTERING ORDER BY (hour ASC)
  AND default_time_to_live = 7776000  -- 90 days retention
  AND compaction = {
    'class': 'TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': 7
};

-- Table for anomaly detection results
CREATE TABLE IF NOT EXISTS detected_anomalies (
    anomaly_id uuid,
    household_id text,
    timestamp timestamp,
    anomaly_type text,
    severity text,
    metric_name text,
    metric_value double,
    expected_value double,
    deviation_percent double,
    description text,
    is_resolved boolean,
    PRIMARY KEY (household_id, timestamp, anomaly_id)
) WITH CLUSTERING ORDER BY (timestamp DESC, anomaly_id ASC)
  AND default_time_to_live = 7776000;  -- 90 days retention

-- Table for spot prices (streaming from API)
CREATE TABLE IF NOT EXISTS spot_prices (
    region text,
    timestamp timestamp,
    price_eur_per_kwh double,
    currency text,
    source text,
    PRIMARY KEY (region, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND default_time_to_live = 2592000;  -- 30 days retention

-- Create materialized view for latest metrics per household
CREATE MATERIALIZED VIEW IF NOT EXISTS latest_energy_metrics AS
    SELECT household_id, timestamp, production_kwh, consumption_kwh, 
           self_consumption_kwh, grid_import_kwh, grid_export_kwh
    FROM energy_metrics_realtime
    WHERE household_id IS NOT NULL 
      AND timestamp IS NOT NULL
    PRIMARY KEY (household_id, timestamp)
    WITH CLUSTERING ORDER BY (timestamp DESC);

-- Insert sample data for testing
INSERT INTO energy_metrics_realtime (
    household_id, timestamp, production_kwh, consumption_kwh,
    self_consumption_kwh, grid_import_kwh, grid_export_kwh,
    battery_charge_kwh, battery_level_percent
) VALUES (
    'household_demo_001',
    toTimestamp(now()),
    2.5,
    1.8,
    1.5,
    0.3,
    1.0,
    0.0,
    65.0
);

-- Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_anomaly_type ON detected_anomalies (anomaly_type);
CREATE INDEX IF NOT EXISTS idx_severity ON detected_anomalies (severity);
CREATE INDEX IF NOT EXISTS idx_spot_prices_time ON spot_prices (timestamp);
