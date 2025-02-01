import folium
import pandas as pd
import geopandas as gpd

# 1. Load the CSV data
df = pd.read_csv("rain_data.csv")

# 2. Load the administrative boundaries GeoJSON
#    Ensure that the GeoJSON file has a property that can be joined with 'adm2_id'
geo_data = gpd.read_file("lk_shp/lka_admbnda_adm2_slsd_20220816.shp")

# 3. (Optional) If needed, inspect your GeoDataFrame to check the matching column name:
#print(geo_data.columns)

# 4. Merge the CSV data with the GeoDataFrame
#    Change 'adm2_id' below if the column name is different in your geo file.
merged = geo_data.merge(df, on='adm2_id')

# 5. Create a Folium map; adjust the starting location and zoom to suit your area
m = folium.Map(location=[7.8731, 80.7718], zoom_start=7)  # Example: Centered on Sri Lanka

# 6. Create a Choropleth layer. Here we are mapping the 'rfh' column, which you can change.
folium.Choropleth(
    geo_data=merged,
    data=merged,
    columns=['adm2_id', 'rfh'],  # Change 'rfh' to the column you want to visualize
    key_on='feature.properties.adm2_id',  # Adjust if your GeoJSON uses a different property name
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Rainfall (rfh)'
).add_to(m)

# 7. Save the map to an HTML file
m.save("rainfall_choropleth.html")
