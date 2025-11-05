#!/bin/bash

# Script to deploy the Energy P2P Data Platform on Kubernetes (KIND)
# This script deploys all services in the correct order

set -e

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║          ENERGY P2P DATA PLATFORM - Kubernetes Deployment            ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED} kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

# Check if KIND cluster is running
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED} Kubernetes cluster not accessible. Make sure KIND cluster is running.${NC}"
    echo -e "${YELLOW} Start KIND with: kind create cluster --name energy-p2p${NC}"
    exit 1
fi

echo -e "${GREEN} Kubernetes cluster detected${NC}"
echo ""

# Function to wait for pods to be ready
wait_for_pods() {
    local namespace=$1
    local app=$2
    local max_wait=300  # 5 minutes
    local elapsed=0
    
    echo -e "${BLUE} Waiting for $app pods to be ready...${NC}"
    
    while [ $elapsed -lt $max_wait ]; do
        if kubectl get pods -n $namespace -l app=$app --field-selector=status.phase=Running 2>/dev/null | grep -q Running; then
            echo -e "${GREEN} $app is ready${NC}"
            return 0
        fi
        sleep 5
        elapsed=$((elapsed + 5))
    done
    
    echo -e "${YELLOW}  $app taking longer than expected (but continuing...)${NC}"
    return 0
}

# Step 1: Create namespace
echo -e "${BLUE} Step 1: Creating namespace...${NC}"
kubectl apply -f ../base/namespace.yaml
echo ""

# Step 2: Create ConfigMaps and Secrets
echo -e "${BLUE}  Step 2: Creating ConfigMaps and Secrets...${NC}"
kubectl apply -f ../base/configmap.yaml
#kubectl apply -f ../base/hdfs_config.yaml
kubectl apply -f ../base/secrets.yaml
echo ""

# Step 3: Create PersistentVolumeClaims
echo -e "${BLUE} Step 3: Creating PersistentVolumeClaims...${NC}"
kubectl apply -f ../base/pvcs.yaml
echo -e "${YELLOW} Waiting for PVCs to be bound (this may take a moment)...${NC}"
sleep 10
kubectl get pvc -n energy-p2p
echo ""

# Step 4: Deploy Storage Layer (HDFS)
echo -e "${BLUE}  Step 4: Deploying HDFS (Hadoop)...${NC}"
kubectl apply -f ../base/hdfs.yaml
wait_for_pods energy-p2p hdfs-namenode
echo ""

# Step 5: Deploy Databases
echo -e "${BLUE}  Step 5: Deploying Databases (PostgreSQL, MongoDB, Cassandra, Redis)...${NC}"
kubectl apply -f ../base/databases.yaml
wait_for_pods energy-p2p postgresql
wait_for_pods energy-p2p mongodb
wait_for_pods energy-p2p redis
echo -e "${YELLOW}Cassandra may take 2-3 minutes to start (StatefulSet)...${NC}"
echo ""

# Step 6: Deploy Streaming (Kafka & Zookeeper)
echo -e "${BLUE} Step 6: Deploying Kafka & Zookeeper...${NC}"
kubectl apply -f ../base/kafka.yaml
wait_for_pods energy-p2p zookeeper
wait_for_pods energy-p2p kafka
echo ""

# Step 7: Deploy Spark
#echo -e "${BLUE} Step 7: Deploying Apache Spark...${NC}"
#kubectl apply -f ../base/spark.yaml
#wait_for_pods energy-p2p spark-master
#echo ""

# Step 8: Initialize Airflow Database
echo -e "${BLUE}  Step 8: Initializing Airflow...${NC}"
echo -e "${YELLOW} Creating Airflow database in PostgreSQL...${NC}"
kubectl exec -n energy-p2p deployment/postgresql -- psql -U energy_user -d postgres -c "CREATE DATABASE airflow_db;" 2>/dev/null || echo "Database may already exist"
echo ""

# Step 9: Deploy Airflow
echo -e "${BLUE}  Step 9: Deploying Apache Airflow...${NC}"
kubectl apply -f ../base/airflow.yaml
echo -e "${YELLOW} Waiting for Airflow init job to complete...${NC}"
kubectl wait --for=condition=complete --timeout=300s job/airflow-init -n energy-p2p 2>/dev/null || echo "Init job completed or timed out"
wait_for_pods energy-p2p airflow-webserver
echo ""

# Step 11: Deploy Visualization
echo -e "${BLUE} Step 11: Deploying Visualization (Superset, Jupyter)...${NC}"
kubectl apply -f ../base/visualization.yaml
echo ""

# Summary
echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║                       DEPLOYMENT COMPLETE!                           ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${GREEN} All services have been deployed to Kubernetes!${NC}"
echo ""

# Get NodePort IPs
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')

echo -e "${BLUE} Service Status:${NC}"
kubectl get pods -n energy-p2p
echo ""

echo -e "${BLUE} Access Your Services:${NC}"
echo ""
echo -e "  ${GREEN}HDFS Namenode:${NC}       http://${NODE_IP}:30870"

echo ""
echo -e "  ${GREEN}PostgreSQL:${NC}          ${NODE_IP}:30432 (energy_user/energy_pass)"
echo -e "  ${GREEN}MongoDB:${NC}             ${NODE_IP}:30017 (energy_user/energy_pass)"
echo -e "  ${GREEN}Cassandra:${NC}           ${NODE_IP}:30042"
echo -e "  ${GREEN}Spark Master:${NC}        http://${NODE_IP}:30080"
echo -e "  ${GREEN}Airflow:${NC}             http://${NODE_IP}:30081 (admin/admin)"
echo -e "  ${GREEN}Kafka UI:${NC}            http://${NODE_IP}:30088"
echo -e "  ${GREEN}Superset:${NC}            http://${NODE_IP}:30082 (admin/admin)"
echo -e "  ${GREEN}Jupyter:${NC}             http://${NODE_IP}:30888 (token: energy-p2p-token)"
echo -e "  ${GREEN}Kafka:${NC}               ${NODE_IP}:30092"
echo ""

echo -e "${YELLOW} Useful Commands:${NC}"
echo -e "  kubectl get pods -n energy-p2p                    # View all pods"
echo -e "  kubectl logs -f <pod-name> -n energy-p2p          # View logs"
echo -e "  kubectl exec -it <pod-name> -n energy-p2p -- bash # Shell into pod"
echo -e "  kubectl get svc -n energy-p2p                     # View services"
echo ""


echo -e "${GREEN} Your Data Platform is ready on Kubernetes! ✨${NC}"