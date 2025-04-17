import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(page_title="🌳 Tree Dashboard", layout="wide")
st.title("🌱 Urban Tree Data Dashboard")

tree_df = load_data("data/tree_survival_summary.csv")
site_df = load_data("data/inventory_site_codes.csv")
greenbush_df = load_data("data/greenbush_trees.csv")


tab1, tab2, tab3 = st.tabs(["Tree Survival Summary", "Site Inventory", "Greenbush Trees"])

with tab1:
    st.subheader("🌳 Tree Survival Summary")
    st.dataframe(tree_df)
    st.bar_chart(tree_df["Survival %"] if "Survival %" in tree_df else tree_df.select_dtypes(include='number'))

with tab2:
    st.subheader("📍 Site Codes")
    st.dataframe(site_df)

with tab3:
    st.subheader("🌿 Greenbush Tree Inventory")
    st.dataframe(greenbush_df)

