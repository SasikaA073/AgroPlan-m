import streamlit as st
import matplotlib.pyplot as plt
from config_lk_shape_files import shapefiles_dict

st.title("Sri Lanka Shapefile Visualization")

# Create subplots (4 rows, 2 columns)
fig, axes = plt.subplots(4, 2, figsize=(14, 18))  # Adjust figure size to fit all plots
axes = axes.flatten()  # Flatten the 2D array to a 1D list

# Loop through shapefiles and plot them on each subplot
for i, (title, shapefile) in enumerate(shapefiles_dict.items()):  
    ax = axes[i]  # Get the current subplot
    shapefile.plot(ax=ax, color="beige", edgecolor='black', linewidth=0.3)  # Plot each shapefile
    ax.set_title(title, fontsize=10)
    ax.set_axis_off()

# Hide unused subplots (if there are fewer shapefiles than subplots)
for j in range(len(shapefiles_dict), len(axes)):
    axes[j].set_visible(False)

# Adjust layout and show the plots in Streamlit
plt.tight_layout()
st.pyplot(fig)  # Display figure in Streamlit
