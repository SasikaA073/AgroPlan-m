# %%
# https://www.fao.org/faolex/opendata/en/

# %%
# TODO: Download the shape file of sri lanka

# %%
!wget https://data.humdata.org/dataset/0bedcaf3-88cd-4591-b9d5-5d3220e26abf/resource/51a81e72-583c-407f-bce6-6f7b42431c93/download/lka_adm_20220816_shp.zip -O lk_shp.zip

# %%
# prompt: !unzip lk_shp.zip  to lk_shp

!unzip lk_shp.zip -d lk_shp

# %%


# %%
# TODO: Download the rainfall dataset sri lanka
!wget https://data.humdata.org/dataset/4302257e-5fa6-4c88-b8f7-f78730d8c48b/resource/e8139c32-d073-4eea-935c-7de4415b7877/download/lka-rainfall-adm2-full.csv -O rainfall_lk.csv


# %%
import os

lk_shp_file_paths = []
# Corrected code
for f in os.listdir("/content/lk_shp"):
    if f.endswith(".shp"):
        lk_shp_file_paths.append("/content/lk_shp/" + f)
        print(lk_shp_file_paths[-1])


# %%
import pandas as pd
import geopandas as gpd

# Load the shapefiles
lk_adm0_shp = gpd.read_file("/content/lk_shp/lka_admbnda_adm0_slsd_20220816.shp") # country
lk_adm1_shp = gpd.read_file("/content/lk_shp/lka_admbnda_adm1_slsd_20220816.shp") # province
lk_adm2_shp = gpd.read_file("/content/lk_shp/lka_admbnda_adm2_slsd_20220816.shp") # district
lk_adm3_shp = gpd.read_file("/content/lk_shp/lka_admbnda_adm3_slsd_20220816.shp") # subdistrict
lk_adm4_shp = gpd.read_file("/content/lk_shp/lka_admbnda_adm4_slsd_20220816.shp") # division
lk_admALL_shp_itos_1 = gpd.read_file("/content/lk_shp/lka_admbndl_admALL_slsd_itos_20220816.shp") # itos 1
lk_admALL_shp_itos_2 = gpd.read_file("/content/lk_shp/lka_admbndp_admALL_slsd_itos_20220816.shp") # itos 2

# %%
# import geopandas as gpd
# import matplotlib.pyplot as plt

# # Load sample data (assuming you have a shapefile or GeoDataFrame)
# # For demonstration, let's use a built-in world dataset from geopandas
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# # Create a plot
# fig, ax = plt.subplots(figsize=(12, 8))

# # Plot using various parameters
# world.plot(
#     ax=ax,
#     column='gdp_md_est',  # Column for color-coding
#     cmap='coolwarm',       # Colormap for values in the column
#     legend=True,           # Display legend
#     edgecolor='black',     # Border color of geometries
#     linewidth=0.5,         # Border thickness
#     alpha=0.7,             # Transparency
#     missing_kwds={'color': 'lightgrey', 'label': 'No Data'},  # Handling missing values
#     vmin=1000, vmax=1e7,   # Range for color scaling
#     legend_kwds={
#         'label': "GDP Estimate (Millions USD)",
#         'orientation': "horizontal",  # Customizing legend
#     }
# )

# # Adding a title to the plot
# ax.set_title("World Map: GDP Estimate by Country", fontsize=15)

# # Show the plot
# plt.show()


# %%
lk_adm0_shp.head(2)

# %%
import matplotlib.pyplot as plt

# Create subplots (4 rows, 2 columns)
fig, axes = plt.subplots(4, 2, figsize=(14, 18))  # Adjust figure size to fit all plots

# Define a list of shapefiles and titles for each plot
shapefiles = [
    (lk_adm0_shp, "Sri Lanka: ADM0 (Country)"),
    (lk_adm1_shp, "Sri Lanka: ADM1 (Province)"),
    (lk_adm2_shp, "Sri Lanka: ADM2 (District)"),
    (lk_adm3_shp, "Sri Lanka: ADM3 (Subdistrict)"),
    (lk_adm4_shp, "Sri Lanka: ADM4 (Division)"),
    (lk_admALL_shp_itos_1, "Sri Lanka: ADM ALL ITOS 1"),
    (lk_admALL_shp_itos_2, "Sri Lanka: ADM ALL ITOS 2"),  # Uncomment for more layers
]

# Loop through shapefiles and plot them on each subplot
for i, (shapefile, title) in enumerate(shapefiles):
    ax = axes.flatten()[i]  # Get the current subplot
    shapefile.plot(ax=ax, color="beige", edgecolor='black', linewidth=0.3)  # Plot each shapefile
    ax.set_title(title)
    ax.set_axis_off()

# Adjust layout and show the plots
plt.tight_layout()
plt.show()

# %%
lk_adm4_shp.head(2)

# %%
lk_adm4_shp.columns

# %%
lk_adm4_shp.ADM3_PCODE.unique().shape

# %%
lk_adm4_shp.ADM4_PCODE.unique().shape

# %%
# Read the CSV file
rainfall_df = pd.read_csv('/content/rainfall_lk.csv')
rainfall_df = rainfall_df.drop(rainfall_df.index[0])
rainfall_df.head()

# %%
lk_adm4_shp.ADM3_PCODE.unique()

# %%
rainfall_df.date.unique().shape

# %%
# Assuming 'rainfall_df' is your DataFrame and 'date' is a column with date values
date_counts = rainfall_df['date'].value_counts()

# Optionally, sort the counts by date if needed
date_counts = date_counts.sort_index()
date_counts

# %%
rainfall_df.adm2_id.unique()

# %%
rainfall_df[:100]

# %%
print(rainfall_df.columns)

# %%
filtered_df = rainfall_df[rainfall_df['date'] == "2024-10-01"]
filtered_df.shape

# %%
# Merge the rainfall data with the geographic data
merged = lk_adm2_shp.merge(filtered_df, on='ADM2_PCODE')
merged

# %%
merged.head()

# %%
merged.rfh.min()

# %%
merged.rfh.max()

# %%
# Subset the data to a smaller sample (e.g., first 1000 rows)

# Create the plot
fig, ax = plt.subplots(figsize=(8, 8))  # Increase figure size to 10x10 inches

# subset_merged = merged.sample(1000)
merged.plot(
    ax=ax,
    column='rfh',  # Column for color-coding
    cmap='coolwarm',       # Colormap for values in the column
    # legend=True,           # Display legend
    edgecolor='black',     # Border color of geometries
    linewidth=0.3,         # Border thickness
    alpha=0.7,             # Transparency
    # vmin=merged.rfh.max(), vmax=merged.rfh.min(),   # Range for color scaling
)

plt.title("Rainfall data on 2024-10-11")
plt.show()


# %% [markdown]
# 


