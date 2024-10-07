#!/bin/bash
set -euo pipefail

# Check if the arguments is correct
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <development|production> <image_version>"
    exit 1
fi

# Params
ENVIRONMENT=$1      # development or production
IMAGE_VERSION=$2    # image version (i.e: v1.0.0)
CLUSTER_NAME="lanchonete-k8s"

# Get path to the Kustomize manifests
case "$ENVIRONMENT" in
    development)
        KUSTOMIZE_DIR="/kubernetes/development"
        ;;
    production)
        KUSTOMIZE_DIR="/kubernetes/production"
        ;;
    *)
        echo "Invalid environment. Choose between 'development' or 'production'."
        exit 1
        ;;
esac

IMAGE_NAME="web:$IMAGE_VERSION"
echo "Updating Kustomize with the image version $IMAGE_VERSION..."

# Navigate to the Kustomize directory
KUSTOMIZE_DIR="$(pwd)/infra/kubernetes/$ENVIRONMENT"
cd $KUSTOMIZE_DIR

if [ ! -f kustomization.yaml ]; then
    echo "Error: Missing kustomization file 'kustomization.yaml' in $KUSTOMIZE_DIR."
    exit 1
fi

# Create namespace for environment
kubectl get namespace $ENVIRONMENT || kubectl create namespace $ENVIRONMENT

# Update the image version using kustomize
kustomize edit set image web=$IMAGE_NAME

echo "Applying Kubernetes manifests for $ENVIRONMENT environment..."
kubectl apply -k $KUSTOMIZE_DIR -n $ENVIRONMENT

if [ $? -ne 0 ]; then
    echo "Deployment failed!"
    exit 1
else
    echo "Deployment complete!"
fi
