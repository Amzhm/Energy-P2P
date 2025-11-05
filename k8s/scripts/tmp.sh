
# Step 6: Deploy Streaming (Kafka & Zookeeper)
echo -e "${BLUE}📨 Step 6: Deploying Kafka & Zookeeper...${NC}"
kubectl apply -f k8s/base/12-kafka.yaml
wait_for_pods energy-p2p zookeeper
wait_for_pods energy-p2p kafka
echo ""

# Step 7: Deploy Spark
echo -e "${BLUE}⚡ Step 7: Deploying Apache Spark...${NC}"
kubectl apply -f k8s/base/13-spark.yaml
wait_for_pods energy-p2p spark-master
echo ""

# Step 8: Initialize Airflow Database
echo -e "${BLUE}✈️  Step 8: Initializing Airflow...${NC}"
echo -e "${YELLOW}⏳ Creating Airflow database in PostgreSQL...${NC}"
kubectl exec -n energy-p2p deployment/postgresql -- psql -U energy_user -d postgres -c "CREATE DATABASE airflow_db;" 2>/dev/null || echo "Database may already exist"
echo ""

# Step 9: Deploy Airflow
echo -e "${BLUE}✈️  Step 9: Deploying Apache Airflow...${NC}"
kubectl apply -f k8s/base/14-airflow.yaml
echo -e "${YELLOW}⏳ Waiting for Airflow init job to complete (this may take 2-3 minutes)...${NC}"
kubectl wait --for=condition=complete --timeout=300s job/airflow-init -n energy-p2p 2>/dev/null || echo "Init job completed or timed out"
wait_for_pods energy-p2p airflow-webserver
echo ""

# Step 10: Deploy Monitoring
echo -e "${BLUE}📊 Step 10: Deploying Monitoring (Prometheus, Grafana)...${NC}"
kubectl apply -f k8s/base/15-monitoring.yaml
wait_for_pods energy-p2p prometheus
wait_for_pods energy-p2p grafana
echo ""

# Step 11: Deploy Visualization
echo -e "${BLUE}📈 Step 11: Deploying Visualization (Superset, Jupyter)...${NC}"
kubectl apply -f k8s/base/16-visualization.yaml
echo ""



echo -e "  ${GREEN}Spark Master:${NC}        http://${NODE_IP}:30080"
echo -e "  ${GREEN}Airflow:${NC}             http://${NODE_IP}:30081 (admin/admin)"
echo -e "  ${GREEN}Kafka UI:${NC}            http://${NODE_IP}:30088"
echo -e "  ${GREEN}Prometheus:${NC}          http://${NODE_IP}:30090"
echo -e "  ${GREEN}Grafana:${NC}             http://${NODE_IP}:30000 (admin/admin)"
echo -e "  ${GREEN}Superset:${NC}            http://${NODE_IP}:30082 (admin/admin)"
echo -e "  ${GREEN}Jupyter:${NC}             http://${NODE_IP}:30888 (token: energy-p2p-token)"

echo -e "  ${GREEN}Kafka:${NC}               ${NODE_IP}:30092"

echo -e "${YELLOW} Next Steps:${NC}"
echo -e "  1. Initialize HDFS directories: ./k8s/scripts/init-hdfs.sh"
echo -e "  2. Create Kafka topics: ./k8s/scripts/init-kafka.sh"
echo -e "  3. Initialize databases: ./k8s/scripts/init-databases.sh"
echo -e "  4. Access Airflow UI and start exploring!"
echo ""