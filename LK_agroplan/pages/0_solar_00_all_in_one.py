import rasterio
import matplotlib.pyplot as plt
import geopandas as gpd
from rasterio.plot import show
import json
import config
from config_lk_shape_files import lk_adm3_shp
import streamlit as st

# Write a function to get the distribution value when the location (longitude and latitude) is given
def get_distribution_value(lon, lat, geotiff_file_path: str):
    with rasterio.open(geotiff_file_path) as src:
        row, col = src.index(lon, lat)
       
        # Check if the point is within the raster bounds
        if 0 <= row < src.height and 0 <= col < src.width:
            # Read the value at the specified location
            value = src.read(1)[row, col]
           
            # Check for nodata/masked values
            if value == src.nodata:
                return None
            return value
        else:
            return None

# Jaffna & Colombo Coordinates
jaffna_lon, jaffna_lat = 80.0167, 9.6647
colombo_lon, colombo_lat = 79.8612, 6.9271

# Load metadata
geotiff_files_dict = config.LK_DailySum_geotiff_files_paths_dict

with open(geotiff_files_dict["metadata"], "r") as f:
    geotiff_metrics_dict = json.load(f)

# Sidebar controls
st.sidebar.header("Map Controls")
showGrid = st.sidebar.checkbox("Show Grid", value=True)
cmap = st.sidebar.selectbox("Select Colormap", config.cmaps_list, index=0)

# Create a dropdown for selecting the metric
metric = st.sidebar.selectbox("Select Metric", list(geotiff_files_dict.keys())[:-1])  # Exclude metadata

# Get the selected TIFF file and its metadata
tiff_file_path = geotiff_files_dict[metric]
metric_details = geotiff_metrics_dict[metric]

st.title(metric_details['title'])

# Check CRS of GeoTIFF and shapefile
with rasterio.open(tiff_file_path) as src:
    raster_crs = src.crs

shapefile_crs = lk_adm3_shp.crs
assert raster_crs == shapefile_crs, "CRS of raster and shapefile do not match!"

# Open and plot the raster
with rasterio.open(tiff_file_path) as src:
    data = src.read(1)  # Read the first band
    
    # Get raster bounds and transform
    bounds = src.bounds
    transform = src.transform
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot the raster
    img = show(src, ax=ax, cmap=cmap)
    
    # Plot the shapefile on top
    lk_adm3_shp.plot(ax=ax, color='none', edgecolor='black', linewidth=0.3)
    
    # Add city markers
    ax.scatter(jaffna_lon, jaffna_lat, color="red", marker='x', s=50, label="Jaffna")
    ax.scatter(colombo_lon, colombo_lat, color="red", marker='o', s=50, label="Colombo")
    
    # Add labels near markers
    ax.text(jaffna_lon, jaffna_lat, "  Jaffna", color="red", fontsize=12,
            verticalalignment='bottom', fontweight='bold')
    ax.text(colombo_lon, colombo_lat, "  Colombo", color="red", fontsize=12,
            verticalalignment='bottom', fontweight='bold')
    
    # Add colorbar only if an image is plotted
    if img is not None:
        cbar = plt.colorbar(img.get_images()[0], ax=ax)
        cbar.set_label(metric_details['unit'])
    
    # Set labels and title
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(metric_details.get('title', 'Solar Data Visualization'))
    
    # Set axis limits to fit Sri Lanka
    ax.set_xlim(bounds.left, bounds.right)
    ax.set_ylim(bounds.bottom, bounds.top)
    
    ax.grid(showGrid)
    ax.legend()

st.pyplot(fig)  # This displays the figure in Streamlit

# Add coordinate input section
st.markdown("---")
st.subheader("Check Value at Specific Location")

# Create two columns for latitude and longitude inputs
col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input("Latitude (°N)", value=6.5219, min_value=-90.0, max_value=90.0, format="%.6f")

with col2:
    longitude = st.number_input("Longitude (°E)", value=80.1137, min_value=-180.0, max_value=180.0, format="%.6f")

# Add a button to get the value
if st.button("Get Value"):
    # Call the function to get the distribution value
    result = get_distribution_value(longitude, latitude, tiff_file_path)
    
    # Display the result
    if result is not None:
        st.success(f"Value at {latitude}° N, {longitude}° E: **{result:.4f}** {metric_details['unit']}")
        
        # Add a marker for this point on the map
        with rasterio.open(tiff_file_path) as src:
            fig, ax = plt.subplots(figsize=(10, 10))
            img = show(src, ax=ax, cmap=cmap)
            lk_adm3_shp.plot(ax=ax, color='none', edgecolor='black', linewidth=0.3)
            
            # Plot existing markers
            ax.scatter(jaffna_lon, jaffna_lat, color="red", marker='x', s=50, label="Jaffna")
            ax.scatter(colombo_lon, colombo_lat, color="red", marker='o', s=50, label="Colombo")
            
            # Add the new location marker
            ax.scatter(longitude, latitude, color="green", marker='^', s=100, label="Selected Location")
            
            # Add labels
            ax.text(jaffna_lon, jaffna_lat, "  Jaffna", color="red", fontsize=12,
                    verticalalignment='bottom', fontweight='bold')
            ax.text(colombo_lon, colombo_lat, "  Colombo", color="red", fontsize=12,
                    verticalalignment='bottom', fontweight='bold')
            ax.text(longitude, latitude, f"  Selected ({latitude:.4f}°N, {longitude:.4f}°E)", 
                   color="green", fontsize=12, verticalalignment='bottom', fontweight='bold')
            
            if img is not None:
                cbar = plt.colorbar(img.get_images()[0], ax=ax)
                cbar.set_label(metric_details['unit'])
            
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.set_title(f"{metric_details.get('title', 'Solar Data Visualization')} - Selected Location")
            
            ax.set_xlim(bounds.left, bounds.right)
            ax.set_ylim(bounds.bottom, bounds.top)
            
            ax.grid(showGrid)
            ax.legend()
            
            st.pyplot(fig)
    else:
        st.error(f"No data available at {latitude}° N, {longitude}° E. The location might be outside the raster bounds.")

# Display metadata
st.markdown("---")
st.subheader("Abstract")
st.write(metric_details['abstract'])
st.subheader("Purpose")
st.write(metric_details['purpose'])