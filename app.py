import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(page_title="🌳 Tree Dashboard", layout="wide")

# Load data
tree_df = load_data("tree_survival_summary.csv")
site_df = load_data("inventory_site_codes.csv")
greenbush_df = load_data("greenbush_trees.csv")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🌿 Survival Analysis",
    "🗺️ Geographic View",
    "🔍 Data Explorer"
])

# --- Overview ---
with tab1:
    st.header("📊 Overview: Tree Data Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌳 Total Survival Summary Entries", len(tree_df))
    col2.metric("📍 Total Site Codes", len(site_df))
    col3.metric("🌿 Greenbush Trees", len(greenbush_df))

    st.markdown("---")
    st.subheader("Quick Preview of Data")

    st.write("### Tree Survival Summary Sample")
    st.dataframe(tree_df.head())

    st.write("### Inventory Site Codes Sample")
    st.dataframe(site_df.head())

    st.write("### Greenbush Trees Sample")
    st.dataframe(greenbush_df.head())

# --- Survival Analysis ---
with tab2:
    st.header("🌿 Survival Analysis")
    st.write("Add charts and filters here later.")

    if "Survival %" in tree_df.columns:
        st.subheader("Survival % Distribution")
        st.bar_chart(tree_df["Survival %"])
    else:
        st.warning("No 'Survival %' column found in survival summary data.")

# --- Geographic View ---
with tab3:
    st.header("🗺️ Geographic View")
    st.info("Map feature placeholder. Add coordinates to display trees geographically.")
    st.map()  # placeholder map

# --- Data Explorer ---
with tab4:
    st.header("🔍 Explore the Data")
    dataset = st.selectbox("Choose a dataset", [
        "Tree Survival Summary",
        "Site Codes",
        "Greenbush Trees"
    ])

    if dataset == "Tree Survival Summary":
        st.dataframe(tree_df)
    elif dataset == "Site Codes":
        st.dataframe(site_df)
    else:
        st.dataframe(greenbush_df)

