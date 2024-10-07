#!/bin/bash
set -euo pipefail

IMAGE_BASE_NAME="web"
CLUSTER_NAME="lanchonete-k8s"

# Check if the arguments is correct
if [ -z "$1" ]; then
    echo "Usage: $0 <image_version>"
    exit 1
fi

IMAGE_VERSION="$1"
IMAGE_NAME="${IMAGE_BASE_NAME}:${IMAGE_VERSION}"

echo "Building container image..."
echo "Image version: $IMAGE_VERSION"
docker build -t $IMAGE_NAME .

echo "Loading image $IMAGE_NAME into Kind, it may take a few minutes..."
kind load docker-image $IMAGE_NAME --name $CLUSTER_NAME

echo "Build and publish of $IMAGE_NAME completed!"