import streamlit as st
import os

st.set_page_config(page_title="Multi-Page Streamlit App", layout="wide")

st.sidebar.title("Navigation")
pages = {
    "Home": "app.py",
    "Page 1": "pages/page1.py",
    "Page 2": "pages/page2.py"
}

page = st.sidebar.radio("Go to", list(pages.keys()))

if page == "Home":
    st.title("Welcome to the Multi-Page Streamlit App")
    st.write("Select a page from the sidebar.")
else:
    os.system(f"streamlit run {pages[page]}")
