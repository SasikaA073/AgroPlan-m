import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st

# Set the title of the page
st.title("Solar Irradiance Distribution in Sri Lanka")

# Load the shapefiles (replace with actual file path if different)
lk_adm2_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm2_slsd_20220816.shp")

# Load the solar irradiance data
# Replace 'datasets/solar_irradiance_lk.csv' with your actual solar irradiance dataset path
solar_df = pd.read_csv('datasets/solar_irradiance_lk.csv')

# Get unique dates for the dropdown (assuming your data has a 'date' column)
unique_dates = solar_df['date'].unique()

# Dropdown to select date
selected_date = st.selectbox("Select Date", unique_dates)

# Filter the solar irradiance data based on the selected date
filtered_solar_df = solar_df[solar_df['date'] == selected_date]

# Merge the solar data with the geographic data
merged_solar = lk_adm2_shp.merge(filtered_solar_df, on='ADM2_PCODE')

# Create the plot
fig, ax = plt.subplots(figsize=(10, 10))
merged_solar.plot(
    ax=ax,
    column='solar_irradiance',  # Column for color-coding, replace with your actual column name
    cmap='viridis',  # Choose an appropriate colormap
    edgecolor='black',
    linewidth=0.3,
    alpha=0.7,
)

plt.title(f"Solar Irradiance Data on {selected_date}")
plt.axis('off')  # Turn off the axis

# Show the plot in the Streamlit app
st.pyplot(fig)
