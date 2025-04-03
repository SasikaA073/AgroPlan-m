import rasterio
import matplotlib.pyplot as plt
import geopandas as gpd
from rasterio.plot import show
import json
import config 
from config_lk_shape_files import lk_adm3_shp
import streamlit as st

# TODO: Change cmap from dropdown list from Streamlit
cmap = config.cmaps_list[0]

# Jaffna & Colombo Coordinates
jaffna_lon, jaffna_lat = 80.0167, 9.6647
colombo_lon, colombo_lat = 79.8612, 6.9271

# TODO: Change to Streamlit dropdown list for other variations
geotiff_files_dict = config.LK_DailySum_geotiff_files_paths_dict

# Load metadata safely
with open(geotiff_files_dict["metadata"], "r") as f:
    geotiff_metrics_dict = json.load(f)
    
# st.write(geotiff_metrics_dict)
metric = "ghi"

# Show the options in the left handside using streamlit 
showGrid = st.sidebar.checkbox("Show Grid", value=True)
cmap = st.sidebar.selectbox("Select Colormap", config.cmaps_list, index=0)

# Get the selected TIFF file and its metadata
tiff_file_path = geotiff_files_dict[metric]
metric_details = geotiff_metrics_dict[metric]

st.title(metric_details['title'])


# Check CRS of GeoTIFF and shapefile
with rasterio.open(tiff_file_path) as src:
    raster_crs = src.crs
    # print(f"Raster CRS: {raster_crs}")

shapefile_crs = lk_adm3_shp.crs
# print(f"Shapefile CRS: {shapefile_crs}")

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
    # cbar issue: fix 2
    # img = ax.imshow(data, cmap=cmap, extent=[bounds.left, bounds.right, bounds.bottom, bounds.top])

    
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
        # cbar = plt.colorbar(img, ax=ax)
        # cbar issue : fix 1
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

# plt.show()  # Comment this out when using Streamlit
st.pyplot(fig)  # This displays the figure in Streamlit

st.markdown("---")
st.subheader("Abstract")
st.write(metric_details['abstract'])
st.subheader("Purpose")
st.write(metric_details['purpose'])