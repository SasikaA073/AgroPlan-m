import geopandas as gpd
import config

# Define a dictionary of shapefiles and titles for each plot
shapefiles_dict = {
    "Sri Lanka: ADM0 (Country)": gpd.read_file(config.lk_adm0_shp_path),
    "Sri Lanka: ADM1 (Province)": gpd.read_file(config.lk_adm1_shp_path),
    "Sri Lanka: ADM2 (District)": gpd.read_file(config.lk_adm2_shp_path),
    "Sri Lanka: ADM3 (Subdistrict)": gpd.read_file(config.lk_adm3_shp_path),
    "Sri Lanka: ADM4 (Division)": gpd.read_file(config.lk_adm4_shp_path),
    "Sri Lanka: ADM ALL ITOS 1": gpd.read_file(config.lk_admALL_shp_itos_1_path),
    "Sri Lanka: ADM ALL ITOS 2": gpd.read_file(config.lk_admALL_shp_itos_2_path)
}

lk_adm0_shp = shapefiles_dict["Sri Lanka: ADM0 (Country)"]
lk_adm1_shp = shapefiles_dict["Sri Lanka: ADM1 (Province)"]
lk_adm2_shp = shapefiles_dict["Sri Lanka: ADM2 (District)"]
lk_adm3_shp = shapefiles_dict["Sri Lanka: ADM3 (Subdistrict)"]
lk_adm4_shp = shapefiles_dict["Sri Lanka: ADM4 (Division)"]
lk_admALL_shp_itos_1 = shapefiles_dict["Sri Lanka: ADM ALL ITOS 1"]
lk_admALL_shp_itos_2 = shapefiles_dict["Sri Lanka: ADM ALL ITOS 2"]

