import streamlit as st
import os

st.set_page_config(page_title="Multi-Page Streamlit App", layout="wide")

st.sidebar.title("Navigation")
pages = {
    "Home": "app.py",
    "Page 1": "pages/page1.py",
    "Page 2": "pages/page2.py"
}

st.success("Download this shapefiles form this url and unzip it and rename it to 'lk_shp' and place that in LK_agroplan/data/ ")
st.warn("wget https://data.humdata.org/dataset/0bedcaf3-88cd-4591-b9d5-5d3220e26abf/resource/51a81e72-583c-407f-bce6-6f7b42431c93/download/lka_adm_20220816_shp.zip -O lk_shp.zip")

page = st.sidebar.radio("Go to", list(pages.keys()))

if page == "Home":
    st.title("Welcome to the Multi-Page Streamlit App")
    st.write("Select a page from the sidebar.")
else:
    os.system(f"streamlit run {pages[page]}")
