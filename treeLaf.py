import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Tree Lafayette Dashboard", layout="wide")

st.title("Tree Lafayette Growth & Survival Dashboard")

# --- File Upload ---
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    st.sidebar.success(f"Loaded sheets: {', '.join(sheet_names)}")

    # Attempt to load relevant sheets
    try:
        planting_df = xls.parse(sheet_names[0])
        summary_df = xls.parse(sheet_names[1])
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        st.stop()

else:
    st.warning("Please upload an Excel file with tree data.")
    st.stop()

# --- Tabs ---
overview_tab, survival_tab, map_tab, explorer_tab = st.tabs([
    "Overview", "Survival Analysis", "Geographic View", "Data Explorer"
])

# --- 1. Overview Tab ---
with overview_tab:
    st.header("Overview")
    
    if "Species" in planting_df.columns:
        st.metric("Total Trees Planted", len(planting_df))

    if "Survival Rate (%)" in summary_df.columns:
        avg_survival = summary_df["Survival Rate (%)"].mean()
        st.metric("Average Survival Rate", f"{avg_survival:.1f}%")

    if "Species" in planting_df.columns:
        species_counts = planting_df["Species"].value_counts().reset_index()
        species_counts.columns = ["Species", "Count"]
        fig = px.bar(species_counts, x="Species", y="Count", title="Tree Count by Species")
        st.plotly_chart(fig)

    if "Year Planted" in planting_df.columns:
        year_counts = planting_df["Year Planted"].value_counts().sort_index()
        st.bar_chart(year_counts)

# --- 2. Survival Analysis ---
with survival_tab:
    st.header("Survival Analysis")

    if {"Species", "Site", "Year Planted", "Survival Rate (%)"}.issubset(summary_df.columns):
        st.subheader("Survival by Species")
        species_survival = summary_df.groupby("Species")["Survival Rate (%)"].mean().sort_values(ascending=False)
        st.bar_chart(species_survival)

        st.subheader("Survival by Site")
        site_survival = summary_df.groupby("Site")["Survival Rate (%)"].mean().sort_values()
        st.line_chart(site_survival)

        st.subheader("Survival by Year")
        if "Year" in summary_df.columns:
            year_survival = summary_df.groupby("Year")["Survival Rate (%)"].mean()
            st.line_chart(year_survival)

# --- 3. Geographic View ---
with map_tab:
    st.header("Geographic View")

    if {"Latitude", "Longitude", "Species", "Survival Rate (%)", "Year Planted"}.issubset(planting_df.columns):
        selected_species = st.selectbox("Filter by species", planting_df["Species"].unique())
        filtered_map_df = planting_df[planting_df["Species"] == selected_species]

        fig_map = px.scatter_mapbox(
            filtered_map_df,
            lat="Latitude",
            lon="Longitude",
            color="Survival Rate (%)",
            size_max=15,
            zoom=11,
            mapbox_style="open-street-map",
            hover_name="Species",
            hover_data=["Site", "Year Planted"]
        )
        st.plotly_chart(fig_map)
    else:
        st.info("Map requires 'Latitude', 'Longitude', 'Species', 'Survival Rate (%)', and 'Year Planted' columns.")

# --- 4. Data Explorer ---
with explorer_tab:
    st.header("Data Explorer")

    selected_sheet = st.selectbox("Choose a sheet to explore", sheet_names)
    df = xls.parse(selected_sheet)

    st.dataframe(df)

    st.markdown("Search and filter using the sidebar or browser tools.")
