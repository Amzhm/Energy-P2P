#!/bin/bash
set -e

# ================================
# UNIFIED POSTGRESQL INITIALIZATION
# Creates all databases in a single PostgreSQL instance
# ================================

echo " Starting PostgreSQL initialization..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    
    -- ================================
    -- CREATE DATABASES
    -- ================================
    
    -- Airflow database
    CREATE DATABASE airflow_db;
    GRANT ALL PRIVILEGES ON DATABASE airflow_db TO $POSTGRES_USER;
    
    -- Superset database
    CREATE DATABASE superset_db;
    GRANT ALL PRIVILEGES ON DATABASE superset_db TO $POSTGRES_USER;
    
    COMMENT ON DATABASE airflow_db IS 'Airflow metadata database';
    COMMENT ON DATABASE superset_db IS 'Apache Superset metadata database';
    
    
    -- ================================
    -- CONFIGURE MAIN DATA WAREHOUSE
    -- ================================
    
    \c $POSTGRES_DB;
    
    -- Install extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
    CREATE EXTENSION IF NOT EXISTS "btree_gin";
    CREATE EXTENSION IF NOT EXISTS "btree_gist";
    
    -- Create schemas for Medallion architecture
    CREATE SCHEMA IF NOT EXISTS bronze;
    CREATE SCHEMA IF NOT EXISTS silver;
    CREATE SCHEMA IF NOT EXISTS gold;
    CREATE SCHEMA IF NOT EXISTS staging;
    
    -- Add comments
    COMMENT ON SCHEMA bronze IS 'Raw data layer - unprocessed data from sources';
    COMMENT ON SCHEMA silver IS 'Cleaned and validated data layer';
    COMMENT ON SCHEMA gold IS 'Business-ready aggregated data layer';
    COMMENT ON SCHEMA staging IS 'Temporary staging area for ETL processes';
    
    -- Grant permissions
    GRANT ALL ON SCHEMA bronze TO $POSTGRES_USER;
    GRANT ALL ON SCHEMA silver TO $POSTGRES_USER;
    GRANT ALL ON SCHEMA gold TO $POSTGRES_USER;
    GRANT ALL ON SCHEMA staging TO $POSTGRES_USER;
    
    -- Set default privileges for future objects
    ALTER DEFAULT PRIVILEGES IN SCHEMA bronze GRANT ALL ON TABLES TO $POSTGRES_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA silver GRANT ALL ON TABLES TO $POSTGRES_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA gold GRANT ALL ON TABLES TO $POSTGRES_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA staging GRANT ALL ON TABLES TO $POSTGRES_USER;
    
    
    -- ================================
    -- CREATE METADATA TABLES
    -- ================================
    
    -- Table to track data pipeline runs
    CREATE TABLE IF NOT EXISTS staging.pipeline_runs (
        run_id SERIAL PRIMARY KEY,
        pipeline_name VARCHAR(100) NOT NULL,
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_time TIMESTAMP,
        status VARCHAR(20) CHECK (status IN ('running', 'success', 'failed')),
        records_processed INTEGER,
        error_message TEXT,
        metadata JSONB
    );
    
    CREATE INDEX idx_pipeline_runs_name ON staging.pipeline_runs(pipeline_name);
    CREATE INDEX idx_pipeline_runs_status ON staging.pipeline_runs(status);
    CREATE INDEX idx_pipeline_runs_start_time ON staging.pipeline_runs(start_time DESC);
    
    COMMENT ON TABLE staging.pipeline_runs IS 'Tracks all ETL/ELT pipeline executions';
    
    
    -- ================================
    -- CONFIGURE AIRFLOW DATABASE
    -- ================================
    
    \c airflow_db;
    
    -- No additional setup needed - Airflow will create its schema
    -- Just ensure the database exists
    
    
    -- ================================
    -- CONFIGURE SUPERSET DATABASE
    -- ================================
    
    \c superset_db;
    
    -- No additional setup needed - Superset will create its schema
    -- Just ensure the database exists

EOSQL

echo ""
echo " PostgreSQL initialization completed successfully!"
echo ""
echo " Created databases:"
echo "   • energy_dwh    (Main data warehouse with bronze/silver/gold schemas)"
echo "   • airflow_db    (Airflow metadata)"
echo "   • superset_db   (Superset metadata)"
echo ""
echo "🔧 Installed extensions:"
echo "   • uuid-ossp"
echo "   • pg_stat_statements"
echo "   • btree_gin"
echo "   • btree_gist"
echo ""