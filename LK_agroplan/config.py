import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of config.py

# ---------------------------------------------------------------------------------------------------------------------
# Solar data (if needed, add paths here)

geotiff_file_base_dir_path = os.path.join(BASE_DIR, "data", "solar", "solargis" )

LK_AvgDailyTotals_geotiff_base_dir_path = os.path.join(geotiff_file_base_dir_path, "Sri-Lanka_GISdata_LTAy_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF")
LK_AvgDailyTotals_geotiff_files_paths_dict = {
# TODO: Complete this dictionary with the correct paths to the geotiff files
}

LK_DailySum_total_geotiff_base_dir_path = os.path.join(geotiff_file_base_dir_path,"Sri-Lanka_GISdata_LTAy_DailySum_GlobalSolarAtlas-v2_GEOTIFF")
LK_DailySum_geotiff_files_paths_dict = {
    "opta": os.path.join(LK_DailySum_total_geotiff_base_dir_path, "OPTA.tif"),
    "dif" : os.path.join(LK_DailySum_total_geotiff_base_dir_path, "DIF.tif"),
    "dni" : os.path.join(LK_DailySum_total_geotiff_base_dir_path, "DNI.tif"),
    "pvout" : os.path.join(LK_DailySum_total_geotiff_base_dir_path, "PVOUT.tif"),
    "gti" : os.path.join(LK_DailySum_total_geotiff_base_dir_path, "GTI.tif"),
    "ghi" : os.path.join(LK_DailySum_total_geotiff_base_dir_path, "GHI.tif"),
    "metadata" : os.path.join(LK_DailySum_total_geotiff_base_dir_path, "LK_DailySum_geo_tiff_metadata.json"),
}


LK_YearlyMonthlyTotals_geotiff_base_dir_path = os.path.join(geotiff_file_base_dir_path, "Sri-Lanka_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF")
LK_YearlyMonthlyTotals_geotiff_files_paths_dict = {
# TODO: Complete this dictionary with the correct paths to the geotiff files
}

LK_YearlyMonthlyTotals_geotiff_base_dir_path = os.path.join(geotiff_file_base_dir_path, "Sri-Lanka_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF")
LK_YearlyMonthlyTotals_geotiff_files_paths_dict = {
# TODO: Complete this dictionary with the correct paths to the geotiff files
}

LK_YearlySum_geotiff_base_dir_path = os.path.join(geotiff_file_base_dir_path, "Sri-Lanka_GISdata_LTAy_YearlySum_GlobalSolarAtlas-v2_GEOTIFF")
LK_YearlySum_geotiff_files_paths_dict = {
# TODO: Complete this dictionary with the correct paths to the geotiff files
}















#-----------------------------------------------------------------------------------------------------------------------

# Agri data
RAINFALL_DATA_CSV_PATH = os.path.join(BASE_DIR, "data", "agri", "rainfall_lk.csv")

# LK shape directory
lk_shape_dir_path = os.path.join(BASE_DIR, "data", "lk_shp")

# Load the shapefiles
lk_adm0_shp_path = os.path.join(lk_shape_dir_path, "lka_admbnda_adm0_slsd_20220816.shp")  # Country
lk_adm1_shp_path = os.path.join(lk_shape_dir_path, "lka_admbnda_adm1_slsd_20220816.shp")  # Province
lk_adm2_shp_path = os.path.join(lk_shape_dir_path, "lka_admbnda_adm2_slsd_20220816.shp")  # District
lk_adm3_shp_path = os.path.join(lk_shape_dir_path, "lka_admbnda_adm3_slsd_20220816.shp")  # Subdistrict
lk_adm4_shp_path = os.path.join(lk_shape_dir_path, "lka_admbnda_adm4_slsd_20220816.shp")  # Division
lk_admALL_shp_itos_1_path = os.path.join(lk_shape_dir_path, "lka_admbndl_admALL_slsd_itos_20220816.shp")  # ITOS 1
lk_admALL_shp_itos_2_path = os.path.join(lk_shape_dir_path, "lka_admbndp_admALL_slsd_itos_20220816.shp")  # ITOS 2

# ------------------------------------------------------------
# Colormaps
cmaps_list = ["viridis", "plasma", "inferno", "magma", "cividis"]