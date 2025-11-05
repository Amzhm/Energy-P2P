// MongoDB Initialization Script
// This script creates the database, collections, and indexes

db = db.getSiblingDB('energy_p2p');

// Create collections
db.createCollection('user_profiles');
db.createCollection('energy_transactions');
db.createCollection('anomalies');
db.createCollection('alerts');
db.createCollection('system_logs');

// Create indexes for user_profiles
db.user_profiles.createIndex({ "user_id": 1 }, { unique: true });
db.user_profiles.createIndex({ "location.coordinates": "2dsphere" });
db.user_profiles.createIndex({ "created_at": 1 });
db.user_profiles.createIndex({ "user_type": 1 });

// Create indexes for energy_transactions
db.energy_transactions.createIndex({ "transaction_id": 1 }, { unique: true });
db.energy_transactions.createIndex({ "seller_id": 1 });
db.energy_transactions.createIndex({ "buyer_id": 1 });
db.energy_transactions.createIndex({ "timestamp": -1 });
db.energy_transactions.createIndex({ "status": 1 });

// Create indexes for anomalies
db.anomalies.createIndex({ "household_id": 1 });
db.anomalies.createIndex({ "timestamp": -1 });
db.anomalies.createIndex({ "anomaly_type": 1 });
db.anomalies.createIndex({ "severity": 1 });

// Create indexes for alerts
db.alerts.createIndex({ "alert_id": 1 }, { unique: true });
db.alerts.createIndex({ "user_id": 1 });
db.alerts.createIndex({ "timestamp": -1 });
db.alerts.createIndex({ "alert_type": 1 });
db.alerts.createIndex({ "is_read": 1 });

// Create indexes for system_logs
db.system_logs.createIndex({ "timestamp": -1 });
db.system_logs.createIndex({ "service": 1 });
db.system_logs.createIndex({ "level": 1 });
db.system_logs.createIndex({ "timestamp": 1 }, { expireAfterSeconds: 2592000 }); // TTL: 30 days

// Insert sample user profile
db.user_profiles.insertOne({
    user_id: "user_demo_001",
    name: "Demo Solar Producer",
    user_type: "producer",
    location: {
        type: "Point",
        coordinates: [-0.1276, 51.5074] // London coordinates
    },
    panel_size_kwp: 5.5,
    created_at: new Date(),
    updated_at: new Date(),
    metadata: {
        installation_date: new Date("2020-01-01"),
        panel_manufacturer: "SolarTech",
        inverter_model: "InverterPro 5000"
    }
});

print("MongoDB initialization completed successfully!");
print("Collections created: user_profiles, energy_transactions, anomalies, alerts, system_logs");
print("Indexes created and sample data inserted.");