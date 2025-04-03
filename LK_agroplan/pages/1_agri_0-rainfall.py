import pandas as pd
import streamlit as st
import config
import os

st.title("Page 2")
st.write("This is the second page.")

# Debugging: Print the absolute path to verify
csv_path = os.path.abspath(config.RAINFALL_DATA_CSV_PATH)
st.write(f"Loading file from: {csv_path}")

# Extract file metadata
try:
    file_stats = os.stat(csv_path)

    metadata = {
        "File Name": os.path.basename(csv_path),
        "File Size (KB)": round(file_stats.st_size / 1024, 2),
        "Last Modified": pd.to_datetime(file_stats.st_mtime, unit="s"),
        "Created On": pd.to_datetime(file_stats.st_ctime, unit="s"),
    }

    # Display metadata
    st.write("### File Metadata:")
    st.json(metadata)

    # Read CSV and display sample data
    rainfall_df = pd.read_csv(config.RAINFALL_DATA_CSV_PATH)
    st.table(rainfall_df.head())

except FileNotFoundError:
    st.error("Error: CSV file not found. Check the file path in config.py.")
except Exception as e:
    st.error(f"An error occurred: {e}")
