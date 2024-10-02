#!/bin/bash

# Function to delete manifests in a given directory
delete_manifests() {
    local dir=$1
    if [ -d "$dir" ]; then
        echo "Deleting manifests in $dir"
        kubectl delete -f "$dir"
    else
        echo "Directory $dir does not exist"
    fi
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <production_manifests_dir> <development_manifests_dir>"
    exit 1
fi

# Get the directories from the arguments
PROD_MANIFESTS_DIR=$1
DEV_MANIFESTS_DIR=$2

# Delete production manifests
delete_manifests "$PROD_MANIFESTS_DIR"

# Delete development manifests
delete_manifests "$DEV_MANIFESTS_DIR"

echo "Manifests deletion completed."