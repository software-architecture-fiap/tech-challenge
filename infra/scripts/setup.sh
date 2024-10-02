#!/bin/bash
set -euo pipefail

CLUSTER_NAME="lanchonete-k8s"
kind create cluster --name ${CLUSTER_NAME} --config infra/config/kind-config.yaml

# Set KUBECONFIG environment variable
export KUBECONFIG="$(kind get kubeconfig --name=${CLUSTER_NAME})"