import os
import pandas as pd
import geopandas as gpd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.cm import ScalarMappable

import config
from config_lk_shape_files import lk_adm2_shp

st.title("Page 2")
st.write("This is the second page.")

# Debugging: Print the absolute path to verify
csv_path = os.path.abspath(config.RAINFALL_DATA_CSV_PATH)
st.write(f"Loading file from: {csv_path}")

try:
    file_stats = os.stat(csv_path)

    metadata = {
        "File Name": os.path.basename(csv_path),
        "File Size (KB)": round(file_stats.st_size / 1024, 2),
        "Last Modified": pd.to_datetime(file_stats.st_mtime, unit="s"),
        "Created On": pd.to_datetime(file_stats.st_ctime, unit="s"),
    }

    # st.write("### File Metadata:")
    # st.json(metadata)

    rainfall_df = pd.read_csv(config.RAINFALL_DATA_CSV_PATH)
    selected_date = st.selectbox("Select a date", rainfall_df['date'].unique()[-5:])
    filtered_df = rainfall_df[rainfall_df['date'] == selected_date]

    merged = lk_adm2_shp.merge(filtered_df, on='ADM2_PCODE')

    fig, ax = plt.subplots(figsize=(8, 8))
    merged.plot(
        ax=ax,
        column='rfh',
        cmap='viridis',
        legend=False,
        edgecolor='black',
        linewidth=0.3,
        alpha=0.7,
    )

    norm = mpl.colors.Normalize(vmin=merged['rfh'].min(), vmax=merged['rfh'].max())
    sm = ScalarMappable(cmap='viridis', norm=norm)
    sm._A = []
    cbar = plt.colorbar(sm, ax=ax, shrink=0.7)
    cbar.set_label("Rainfall (rfh)")

    plt.title(f"Rainfall data on {selected_date}", fontsize=10)

    st.pyplot(fig)  # <- Use st.pyplot to render inside Streamlit

except FileNotFoundError:
    st.error("Error: CSV file not found. Check the file path in config.py.")
except Exception as e:
    st.error(f"An error occurred: {e}")
