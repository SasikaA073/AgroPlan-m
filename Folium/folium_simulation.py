import folium
import geopandas as gpd
import pandas as pd
import numpy as np
import branca.colormap as cm
import matplotlib.colors as mcolors
import matplotlib.cm as mcm

# --- 1. Configuration ---
# Path to your downloaded Sri Lanka administrative boundaries file
BOUNDARY_FILE = 'sri_lanka_adm.geojson' # ADJUST THIS PATH

# Approximate map center and zoom
map_center = [7.8731, 80.7718] # Center of Sri Lanka
map_zoom = 7

# Simulation parameters (adjust grid density as needed)
lat_min, lat_max = 5.8, 9.9
lon_min, lon_max = 79.5, 82.0
grid_density = 0.05 # Smaller value = denser grid (more points, slower)

# PVOut range from the original image's color bar
pv_min, pv_max = 3.2, 4.5

# --- 2. Load Administrative Boundaries ---
try:
    sri_lanka_gdf = gpd.read_file(BOUNDARY_FILE)
    # Ensure it's using WGS84 (lat/lon)
    sri_lanka_gdf = sri_lanka_gdf.to_crs(epsg=4326)
    print(f"Successfully loaded boundaries from {BOUNDARY_FILE}")
    # Use 'NAME_1' for provinces or 'NAME_2' for districts (check your file)
    # Adjust 'NAME_?' based on the actual column name in your GeoJSON/Shapefile
    boundary_name_col = 'NAME_2' if 'NAME_2' in sri_lanka_gdf.columns else 'NAME_1'
    if boundary_name_col not in sri_lanka_gdf.columns:
        print(f"Warning: Could not find expected boundary name column ('NAME_1' or 'NAME_2'). Using index.")
        boundary_name_col = sri_lanka_gdf.index # Fallback

except Exception as e:
    print(f"Error loading boundary file '{BOUNDARY_FILE}': {e}")
    print("Please ensure the file exists and is a valid GeoJSON or Shapefile.")
    print("You can download boundaries from sources like https://gadm.org/download_country.html")
    exit() # Exit if boundaries can't be loaded

# --- 3. Simulate PV Potential Data ---
lons = np.arange(lon_min, lon_max, grid_density)
lats = np.arange(lat_min, lat_max, grid_density)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# Simple simulation function (higher latitude = slightly higher PV)
# Add a dip in the central region to mimic highlands
def simulate_pvout(lat, lon):
    base_value = 3.2 + (lat - lat_min) * (4.5 - 3.2) / (lat_max - lat_min)
    # Add a dip around central highlands (approx coords)
    center_lat, center_lon = 7.0, 80.7
    distance_sq = (lat - center_lat)**2 + (lon - center_lon)**2
    dip = 0.5 * np.exp(-distance_sq / 0.5) # Adjust width (0.5) and depth (0.5)
    pv = base_value - dip
    # Add some noise
    noise = np.random.normal(0, 0.05)
    # Clamp values to the observed range
    return np.clip(pv + noise, pv_min, pv_max)

pvout_values = simulate_pvout(lat_grid, lon_grid)

# Create a DataFrame
sim_data = pd.DataFrame({
    'latitude': lat_grid.ravel(),
    'longitude': lon_grid.ravel(),
    'PVOut_kWh_kWp': pvout_values.ravel()
})

# Convert to GeoDataFrame
sim_gdf = gpd.GeoDataFrame(
    sim_data,
    geometry=gpd.points_from_xy(sim_data.longitude, sim_data.latitude),
    crs="EPSG:4326" # WGS84
)

# --- 4. Filter Simulated Points within Sri Lanka Boundaries ---
# This is important to only show points actually on land
# Use spatial join: keep only points that intersect with the boundary polygons
points_within_sl = gpd.sjoin(sim_gdf, sri_lanka_gdf, how='inner', predicate='intersects') # Use 'intersects' or 'within'
print(f"Generated {len(sim_data)} grid points, kept {len(points_within_sl)} points within boundaries.")

# --- 5. Create the Folium Map ---
m = folium.Map(location=map_center, zoom_start=map_zoom, tiles='CartoDB positron')

# --- 6. Add Simulated PV Data as Circle Markers ---

# Create a colormap (using 'viridis' like the original image)
# We use branca for the colormap object that folium can use as a legend
colormap = cm.LinearColormap(
    colors=mcm.viridis.colors, # Get colors from matplotlib's viridis
    vmin=pv_min,
    vmax=pv_max,
    caption='Longterm yearly average of daily totals (kWh/kWp)' # Legend caption
)

# Create a feature group for the PV data points
pv_layer = folium.FeatureGroup(name='PV Potential (Simulated)')

# Add points to the feature group
for idx, row in points_within_sl.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    pv_value = row['PVOut_kWh_kWp']
    color = mcolors.to_hex(mcm.viridis((pv_value - pv_min) / (pv_max - pv_min))) # Normalize and get hex

    folium.CircleMarker(
        location=[lat, lon],
        radius=3, # Adjust size as needed
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        stroke=False, # No border for circles
        tooltip=f"PV Potential: {pv_value:.2f} kWh/kWp<br>Lat: {lat:.4f}<br>Lon: {lon:.4f}"
    ).add_to(pv_layer)

# Add the feature group to the map
pv_layer.add_to(m)

# --- 7. Add Administrative Boundaries Layer ---
style_function = lambda x: {
    'fillColor': 'none', # No fill
    'color': 'black',    # Black border
    'weight': 0.5,       # Thin border
    'fillOpacity': 0,
}

hover_style = lambda x: {
    'fillColor': 'grey',
    'color': 'black',
    'weight': 1,
    'fillOpacity': 0.3,
}

folium.GeoJson(
    sri_lanka_gdf,
    name='Administrative Boundaries',
    style_function=style_function,
    highlight_function=hover_style, # Style on hover
    tooltip=folium.features.GeoJsonTooltip(
        fields=[boundary_name_col], # Show the district/province name on hover
        aliases=['Region:'],          # Alias for the field name
        sticky=True # Tooltip follows mouse
    )
).add_to(m)

# --- 8. Add City Markers ---
folium.Marker(
    location=[9.6615, 80.0255], # Jaffna coordinates
    popup='Jaffna',
    tooltip='Jaffna',
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

folium.Marker(
    location=[6.9271, 79.8612], # Colombo coordinates
    popup='Colombo',
    tooltip='Colombo',
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)


# --- 9. Add Colormap Legend and Layer Control ---
m.add_child(colormap) # Add the legend to the map
folium.LayerControl().add_to(m) # Add layer control to toggle layers

# --- 10. Save the Map ---
output_file = 'sri_lanka_pv_potential_interactive_map.html'
m.save(output_file)

print(f"\nInteractive map saved to: {output_file}")
print("Open this file in your web browser.")