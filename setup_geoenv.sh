#!/bin/bash

# Function to check if command succeeded
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

echo "Starting setup process..."

# Remove existing environment
conda deactivate 2>/dev/null
conda env remove -n geo -y

# Create fresh environment with specific versions
conda create -n geo python=3.10 -y
check_status "Failed to create environment"

# Source conda
source $(conda info --base)/etc/profile.d/conda.sh
conda activate geo
check_status "Failed to activate environment"

# Install packages in specific order
conda install -c conda-forge gdal=3.4.3 -y
check_status "Failed to install GDAL"

conda install -c conda-forge fiona=1.8.21 -y
check_status "Failed to install Fiona"

conda install -c conda-forge pyogrio -y
check_status "Failed to install pyogrio"

conda install -c conda-forge geopandas=0.12.2 -y
check_status "Failed to install GeoPandas"

conda install -c conda-forge streamlit pandas matplotlib -y
check_status "Failed to install additional packages"

echo "Installation complete! Please test the environment."