#!/bin/bash

set -euo pipefail

# Create a Kind cluster
kind create cluster --name lanchonete-k8s --config infra/config/kind-config.yaml

# Set KUBECONFIG environment variable
export KUBECONFIG="$(kind get kubeconfig-path --name=lanchonete-k8s)"