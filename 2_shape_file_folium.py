import folium
import pandas as pd
import geopandas as gpd

# Create a basic map centered on Sri Lanka
sri_lanka_map = folium.Map(location=[7.8731, 80.7718], zoom_start=7)

# Load the administrative boundaries GeoJSON
lk_adm0_shp = gpd.read_file("LK_AGROPLAN/datasets/lk_shp/lka_admbnda_adm0_slsd_20220816.shp") # country
lk_adm1_shp = gpd.read_file("LK_AGROPLAN/datasets/lk_shp/lka_admbnda_adm1_slsd_20220816.shp") # province
lk_adm2_shp = gpd.read_file("LK_AGROPLAN/datasets/lk_shp/lka_admbnda_adm2_slsd_20220816.shp") # district
lk_adm3_shp = gpd.read_file("LK_AGROPLAN/datasets/lk_shp/lka_admbnda_adm3_slsd_20220816.shp") # subdistrict
lk_adm4_shp = gpd.read_file("LK_AGROPLAN/datasets/lk_shp/lka_admbnda_adm4_slsd_20220816.shp") # division
lk_admALL_shp_itos_1 = gpd.read_file("LK_AGROPLAN/datasets/lk_shp/lka_admbndl_admALL_slsd_itos_20220816.shp") # itos 1
lk_admALL_shp_itos_2 = gpd.read_file("LK_AGROPLAN/datasets/lk_shp/lka_admbndp_admALL_slsd_itos_20220816.shp") # itos 2

# Add the GeoJSON to the map
folium.GeoJson(lk_adm0_shp).add_to(sri_lanka_map)
folium.GeoJson(lk_adm1_shp).add_to(sri_lanka_map)
folium.GeoJson(lk_adm2_shp).add_to(sri_lanka_map)






# Optionally, add any additional markers you already had
folium.Marker(
    [6.9271, 79.8612],
    popup="Colombo<br>Rain: 2500mm<br>Solar: 5.2 kWh/m²/day",
    icon=folium.Icon(color='blue')
).add_to(sri_lanka_map)

folium.Marker(
    [7.2964, 80.6350],
    popup="Kandy<br>Rain: 2000mm<br>Solar: 5.8 kWh/m²/day",
    icon=folium.Icon(color='orange')
).add_to(sri_lanka_map)

# Save the map to an HTML file
sri_lanka_map.save('simple_map.html')
