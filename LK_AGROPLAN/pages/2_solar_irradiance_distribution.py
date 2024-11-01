import rasterio
import matplotlib.pyplot as plt
import geopandas as gpd
from rasterio.plot import show
import pandas as pd
import streamlit as st

# Set the title of the page
st.title("Solar Irradiance Distribution in Sri Lanka")

# Load the shapefiles (replace with actual file path if different)
lk_adm2_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm2_slsd_20220816.shp")

# Load the solar irradiance data
# Replace 'datasets/solar_irradiance_lk.csv' with your actual solar irradiance dataset path
solar_df = pd.read_csv('datasets/solar_irradiance_lk.csv')

tiff_file_path = "LK_AGROPLAN/datasets/LK_Solar_Dataset/Sri-Lanka_GISdata_LTAy_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF/GTI.tif"

lk_adm2_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm2_slsd_20220816.shp")

# Load the rainfall data
rainfall_df = pd.read_csv('datasets/rainfall_lk.csv')
rainfall_df = rainfall_df.drop(rainfall_df.index[0])

# Get unique dates for the dropdown
unique_dates = rainfall_df['date'].unique()

# Dropdown to select date
selected_date = st.selectbox("Select Date", unique_dates)

# Filter the rainfall data based on the selected date
filtered_df = rainfall_df[rainfall_df['date'] == selected_date]

# Merge the rainfall data with the geographic data
merged = lk_adm2_shp.merge(filtered_df, on='ADM2_PCODE')

rainfall_gdf = merged

# Open the GeoTIFF file
with rasterio.open(tiff_file_path) as src:
    # Read the data
    data = src.read(1)  # Read the first band

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10))  # Adjust size as needed

    # Plot the GeoTIFF data using imshow instead of show
    raster_plot = ax.imshow(data,
                           extent=[src.bounds.left, src.bounds.right,
                                 src.bounds.bottom, src.bounds.top],
                           cmap='viridis')

    # Overlay the rainfall data
    rainfall_plot = rainfall_gdf.plot(
        ax=ax,
        column='rfh',  # Column for color-coding in the rainfall dataset
        cmap='coolwarm',  # Colormap for values in the column
        edgecolor='black',  # Border color of geometries
        linewidth=0.3,  # Border thickness
        alpha=0.4,  # Transparency
    )

    # Set the title and labels
    plt.title("Rainfall + Solar Irradiance")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Add colorbars for both plots
    plt.colorbar(raster_plot, label='GeoTIFF Values', ax=ax, orientation='vertical', pad=0.02)
    plt.colorbar(mappable=rainfall_plot.get_children()[0], label='Rainfall Values', ax=ax, orientation='vertical', pad=0.04)

    # plt.show()
    # Show the plot in the Streamlit app
    st.pyplot(fig)
