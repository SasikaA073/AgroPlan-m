import os
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st

# Set the title of the page
st.title("Administrative Divisions of Sri Lanka")

# Load the shapefiles
lk_adm0_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm0_slsd_20220816.shp")
lk_adm1_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm1_slsd_20220816.shp")
lk_adm2_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm2_slsd_20220816.shp")
lk_adm3_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm3_slsd_20220816.shp")
lk_adm4_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm4_slsd_20220816.shp")

# Define the shapefiles to plot
shapefiles = [
    (lk_adm0_shp, "Sri Lanka: ADM0 (Country)"),
    (lk_adm1_shp, "Sri Lanka: ADM1 (Province)"),
    (lk_adm2_shp, "Sri Lanka: ADM2 (District)"),
    (lk_adm3_shp, "Sri Lanka: ADM3 (Subdistrict)"),
    (lk_adm4_shp, "Sri Lanka: ADM4 (Division)"),
]

# Create subplots for each administrative division
fig, axes = plt.subplots(len(shapefiles), 1, figsize=(10, 15))

for ax, (shapefile, title) in zip(axes, shapefiles):
    shapefile.plot(ax=ax, color="beige", edgecolor='black', linewidth=0.3)
    ax.set_title(title)
    ax.axis('off')

# Display the plots
st.pyplot(fig)
