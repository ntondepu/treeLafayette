import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# --- Data Loading Function ---
def load_data(default_path: str, file_type: str = "csv"):
    """
    Loads default data from the repo, but allows user upload to override.
    
    Parameters:
        default_path (str): Path to the default CSV or Excel file.
        file_type (str): "csv" or "excel"
    
    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    uploaded_file = st.sidebar.file_uploader(f"Upload a new {file_type.upper()} file to override", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.sidebar.success("Uploaded file loaded successfully.")
            return df
        except Exception as e:
            st.sidebar.error(f"Failed to load uploaded file: {e}")
    
    # Fallback to default
    try:
        if file_type == "csv":
            df = pd.read_csv(default_path)
        else:
            df = pd.read_excel(default_path)
        st.sidebar.info("Using default dataset from repository.")
        return df
    except Exception as e:
        st.sidebar.error(f"Failed to load default file: {e}")
        return pd.DataFrame()

# --- Streamlit App Logic ---
# Default paths (replace with your actual repo paths)
default_planting_path = "tree_survival_summary.csv"
default_summary_path = "inventory_site_codes.csv"

# Load data (with the option to upload new files)
planting_df = load_data(default_planting_path, file_type="csv")
summary_df = load_data(default_summary_path, file_type="csv")

# --- Streamlit Tabs ---
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

    selected_sheet = st.selectbox("Choose a sheet to explore", ["planting_df", "summary_df"])
    
    if selected_sheet == "planting_df":
        st.dataframe(planting_df)
    else:
        st.dataframe(summary_df)
