#!/bin/bash

# Script to create Kafka topics on Kubernetes
# Run this after Kafka pod is running

set -e

echo "Initializing Kafka topics on Kubernetes..."
echo ""

# Wait for Kafka to be ready
echo " Waiting for Kafka to be ready..."
kubectl wait --for=condition=ready pod -l app=kafka -n energy-p2p --timeout=300s

# Get the kafka pod name
KAFKA_POD=$(kubectl get pods -n energy-p2p -l app=kafka -o jsonpath='{.items[0].metadata.name}')

if [ -z "$KAFKA_POD" ]; then
    echo " Error: Could not find Kafka pod"
    exit 1
fi

echo "Found Kafka pod: $KAFKA_POD"
echo ""

# Topic configuration
PARTITIONS=3
REPLICATION_FACTOR=1

# Create topic: energy-meters (high throughput)
echo " Creating topic: energy-meters"
kubectl exec -n energy-p2p $KAFKA_POD -- kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --topic energy-meters \
  --partitions 6 \
  --replication-factor $REPLICATION_FACTOR \
  --config retention.ms=604800000 \
  --config compression.type=snappy \
  --if-not-exists

# Create topic: spot-prices
echo " Creating topic: spot-prices"
kubectl exec -n energy-p2p $KAFKA_POD -- kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --topic spot-prices \
  --partitions $PARTITIONS \
  --replication-factor $REPLICATION_FACTOR \
  --config retention.ms=2592000000 \
  --if-not-exists

# Create topic: weather-alerts
echo " Creating topic: weather-alerts"
kubectl exec -n energy-p2p $KAFKA_POD -- kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --topic weather-alerts \
  --partitions $PARTITIONS \
  --replication-factor $REPLICATION_FACTOR \
  --config retention.ms=604800000 \
  --if-not-exists

# Create topic: dashboard-updates
echo " Creating topic: dashboard-updates"
kubectl exec -n energy-p2p $KAFKA_POD -- kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --topic dashboard-updates \
  --partitions $PARTITIONS \
  --replication-factor $REPLICATION_FACTOR \
  --config retention.ms=86400000 \
  --config cleanup.policy=delete \
  --if-not-exists

# Create topic: anomalies
echo " Creating topic: anomalies"
kubectl exec -n energy-p2p $KAFKA_POD -- kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --topic anomalies \
  --partitions $PARTITIONS \
  --replication-factor $REPLICATION_FACTOR \
  --config retention.ms=2592000000 \
  --if-not-exists

# List all topics
echo ""
echo " Kafka topics created successfully!"
echo ""
echo " Listing all topics:"
kubectl exec -n energy-p2p $KAFKA_POD -- kafka-topics --list --bootstrap-server localhost:9092

# Describe topics
echo ""
echo " Topic details:"
for topic in energy-meters spot-prices weather-alerts dashboard-updates anomalies; do
  echo ""
  echo " Topic: $topic"
  kubectl exec -n energy-p2p $KAFKA_POD -- kafka-topics --describe \
    --bootstrap-server localhost:9092 \
    --topic $topic
done

echo ""
echo "Kafka initialization complete!"
echo ""

# Get node IP for Kafka UI access
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
echo " Access Kafka UI at: http://${NODE_IP}:30088"