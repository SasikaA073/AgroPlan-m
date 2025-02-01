import folium
import pandas as pd
import requests
import json
import random

# Fetch Sri Lanka districts GeoJSON
geojson_url = "https://raw.githubusercontent.com/CodeForAfrica/DataViz/master/GeoJSON/SriLankaDistricts.geojson"
response = requests.get(geojson_url)
sri_lanka_geo = response.json()

# Generate sample data for demonstration
districts = [feature['properties']['NAME_2'] for feature in sri_lanka_geo['features']]
rain_data = {'District': districts, 
             'Rainfall': [random.randint(800, 3000) for _ in districts]}
solar_data = {'District': districts,
              'SolarIrradiance': [random.uniform(4.0, 6.5) for _ in districts]}

rain_df = pd.DataFrame(rain_data)
solar_df = pd.DataFrame(solar_data)

# Create base map centered on Sri Lanka
sri_lanka_map = folium.Map(location=[7.8731, 80.7718], zoom_start=7)

# Add Rainfall Distribution layer
folium.Choropleth(
    geo_data=sri_lanka_geo,
    name='Rainfall Distribution',
    data=rain_df,
    columns=['District', 'Rainfall'],
    key_on='feature.properties.NAME_2',
    fill_color='Blues',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Annual Rainfall (mm)'
).add_to(sri_lanka_map)

# Add Solar Irradiance layer
folium.Choropleth(
    geo_data=sri_lanka_geo,
    name='Solar Irradiance',
    data=solar_df,
    columns=['District', 'SolarIrradiance'],
    key_on='feature.properties.NAME_2',
    fill_color='Oranges',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Solar Irradiance (kWh/m²/day)'
).add_to(sri_lanka_map)

# Add layer control and title
folium.LayerControl().add_to(sri_lanka_map)
title_html = '''
             <h3 align="center" style="font-size:16px"><b>Sri Lanka - Climate Resources</b></h3>
             '''
sri_lanka_map.get_root().html.add_child(folium.Element(title_html))

# Save the map
sri_lanka_map.save('sri_lanka_climate_map.html')