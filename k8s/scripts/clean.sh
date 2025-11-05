#!/bin/bash

# Script to delete all resources from the Energy P2P platform

set -e

echo "  WARNING This will delete ALL resources in the energy-p2p namespace!"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo " Deletion cancelled."
    exit 0
fi

echo ""
echo "  Deleting all resources..."

# Delete all resources in order
kubectl delete -f ../base/visualization.yaml --ignore-not-found=true
#kubectl delete -f k8s/base/15-monitoring.yaml --ignore-not-found=true
kubectl delete -f ../base/airflow.yaml --ignore-not-found=true
kubectl delete -f ../base/spark.yaml --ignore-not-found=true
kubectl delete -f ../base/kafka.yaml --ignore-not-found=true
kubectl delete -f ../base/databases.yaml --ignore-not-found=true
kubectl delete -f ../base/hdfs.yaml --ignore-not-found=true
kubectl delete -f ../base/pvcs.yaml --ignore-not-found=true
kubectl delete -f ../base/secrets.yaml --ignore-not-found=true
kubectl delete -f ../base/configmap.yaml --ignore-not-found=true

echo ""
echo " Waiting for pods to terminate..."
kubectl wait --for=delete pod --all -n energy-p2p --timeout=300s 2>/dev/null || true

echo ""
read -p "Do you want to delete the namespace too? (yes/no): " delete_ns

if [ "$delete_ns" = "yes" ]; then
    kubectl delete -f ../base/namespace.yaml --ignore-not-found=true
    echo " Namespace deleted"
else
    echo " Namespace preserved"
fi

echo ""
echo " Cleanup complete!"