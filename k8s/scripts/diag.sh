#!/bin/bash

echo "🔍 Finding correct Spark image tag..."
echo ""

echo "❌ bitnami/spark:3.4.1 does NOT exist"
echo ""
echo "✅ Let's try available tags:"
echo ""

# Try common Spark 3.4.x tags
TAGS=("3.4" "3.4.0" "3.5" "3.5.0" "latest")

for tag in "${TAGS[@]}"; do
    echo "Trying: bitnami/spark:$tag"
    docker pull bitnami/spark:$tag 2>&1 | grep -q "Downloaded newer image\|Image is up to date" 
    if [ $? -eq 0 ]; then
        echo "✅ SUCCESS! Tag $tag exists and is downloaded"
        WORKING_TAG=$tag
        break
    else
        echo "❌ Tag $tag not found"
    fi
    echo ""
done

if [ -z "$WORKING_TAG" ]; then
    echo "❌ No working tag found. Check Docker Hub manually:"
    echo "   https://hub.docker.com/r/bitnami/spark/tags"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ FOUND WORKING TAG: bitnami/spark:$WORKING_TAG"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "Now loading into KIND..."
kind load docker-image bitnami/spark:$WORKING_TAG --name energy-p2p

echo ""
echo "Updating spark.yaml to use tag: $WORKING_TAG"
echo ""

echo "Next steps:"
echo "1. Edit spark-fixed.yaml and change image to: bitnami/spark:$WORKING_TAG"
echo "2. Apply: kubectl apply -f spark-fixed.yaml"
echo "3. Check: kubectl get pods -n energy-p2p"