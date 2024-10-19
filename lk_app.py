import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st

# Set the title of the app
st.title("Rainfall Distribution in Sri Lanka")

# Load the shapefiles
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

# Create the plot
fig, ax = plt.subplots(figsize=(10, 10))
merged.plot(
    ax=ax,
    column='rfh',  # Column for color-coding
    cmap='coolwarm',
    edgecolor='black',
    linewidth=0.3,
    alpha=0.7,
)

plt.title(f"Rainfall Data on {selected_date}")
plt.axis('off')  # Turn off the axis

# Show the plot in the Streamlit app
st.pyplot(fig, clear_figure=True)
