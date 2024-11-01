#!/bin/bash

# Function to check if command succeeded
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

echo "Starting setup process..."

# Remove existing environment (uncomment if needed)
# conda deactivate 2>/dev/null
echo "Removing existing 'spark' environment"
conda env remove -n spark -y
check_status "Failed to remove existing environment"

# Create fresh environment with specific versions
echo "Creating environment"
conda create -n spark python=3.10.12 -y
check_status "Failed to create environment"

# Source conda
echo "Activating environment"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate spark
check_status "Failed to activate environment"

# Install packages in specific order
echo "Installing geopandas"
conda install -c conda-forge geopandas==1.0.1 -y
check_status "Failed to install geopandas==1.0.1"

echo "Installing streamlit"
conda install anaconda::streamlit -y
check_status "Failed to install streamlit"

# Install rasterio (uncomment if needed)
# conda install -c conda-forge rasterio -y
# check_status "Failed to install rasterio"

echo "Installation complete! Please test the environment."