#!/bin/bash

# Function to check if command succeeded
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

echo "Starting setup process..."

# # Remove existing environment
# conda deactivate 2>/dev/null
# conda env remove -n geo -y

# Create fresh environment with specific versions
conda create -n spark python=3.10.12 -y
check_status "Failed to create environment"

# Source conda
source $(conda info --base)/etc/profile.d/conda.sh
conda activate spark
check_status "Failed to activate environment"

# Install packages in specific order
conda install -c conda-forge geopandas==1.0.1
check_status "Failed to install geopandas==1.0.1"

conda install anaconda::streamlit
check_status "Failed to install streamlit"

conda install conda-forge::rasterio
check_status "Failed to install rasterio"

echo "Installation complete! Please test the environment."