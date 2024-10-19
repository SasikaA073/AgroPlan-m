import streamlit as st
import pandas as pd
import geopandas as gpd

# Load the shapefiles
lk_adm0_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm0_slsd_20220816.shp")
lk_adm1_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm1_slsd_20220816.shp")
lk_adm2_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm2_slsd_20220816.shp")
lk_adm3_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm3_slsd_20220816.shp")
lk_adm4_shp = gpd.read_file("datasets/lk_shp/lka_admbnda_adm4_slsd_20220816.shp")
lk_admALL_shp_itos_1 = gpd.read_file("datasets/lk_shp/lka_admbndl_admALL_slsd_itos_20220816.shp")
lk_admALL_shp_itos_2 = gpd.read_file("datasets/lk_shp/lka_admbndp_admALL_slsd_itos_20220816.shp")

# Load the rainfall data
rainfall_df = pd.read_csv('datasets/rainfall_lk.csv')
rainfall_df = rainfall_df.drop(rainfall_df.index[0])

# Import page functions
from pages.1_rainfall_distribution import display_rainfall_distribution
from pages.2_solar_irradiance_distribution import display_solar_irradiance_distribution
from pages.0_admin_divisions import display_admin_divisions  # Update based on your script names

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Rainfall Distribution", "Solar Irradiance Distribution", "Administrative Divisions"])

    if page == "Rainfall Distribution":
        display_rainfall_distribution(lk_adm2_shp, rainfall_df)
    elif page == "Solar Irradiance Distribution":
        display_solar_irradiance_distribution()
    elif page == "Administrative Divisions":
        display_admin_divisions(lk_adm0_shp, lk_adm1_shp, lk_adm2_shp, lk_adm3_shp, lk_adm4_shp, lk_admALL_shp_itos_1, lk_admALL_shp_itos_2)

if __name__ == "__main__":
    main()
