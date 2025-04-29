import streamlit as st
import pandas as pd
import plotly.express as px


# --- Page Config ---
st.set_page_config(
    page_title="Tree Planting & Survival Dashboard 🌳",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Dark Green Theme ---
st.markdown(
    """
    <style>
    body {
        background-color: #228B22; /* Forest Green background */
        color: white;
    }
    .stApp {
        background-color: #228B22; /* Forest Green background */
    }
    .css-18e3th9 {
        background-color: #228B22; /* Forest Green for main container */
    }
    .stButton>button {
        background-color: #0b3d0b;
        color: white;
    }
    .stTabs [role="tab"] {
        background-color: #2e8b57;
        padding: 10px;
        margin-right: 10px;
        border-radius: 10px;
        color: white;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #006400;
        color: white;
    }
    .css-1v3fvcr, .css-1d391kg {
        background-color: transparent; /* Make sidebar transparent */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Dashboard Header ---
st.title("🌳 Tree Planting & Survival Dashboard")
st.caption("This Streamlit application provides an interactive dashboard for exploring tree planting and survival data in Lafayette, Indiana.")

# --- Data Loading Function ---
def load_data(default_path: str, file_type: str = "csv", key: str = "data_file_uploader"):
    uploaded_file = st.sidebar.file_uploader(
        f"Upload a new {file_type.upper()} file to override", 
        type=["csv", "xlsx"], 
        key=key
    )
    
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
default_planting_path = "tree_survival_summary.csv"
default_summary_path = "inventory_site_codes.csv"
default_greenbush_path = "greenbush_trees.csv"

planting_df = load_data(default_planting_path, "csv", "planting_file_uploader")
summary_df = load_data(default_summary_path, "csv", "summary_file_uploader")
greenbush_df = load_data(default_greenbush_path, "csv", "greenbush_file_uploader")

# --- Streamlit Tabs ---
overview_tab, survival_tab, map_tab, explorer_tab, correlation_tab = st.tabs([
    "Overview", "Survival Analysis", "Geographic View", "Data Explorer", "Correlation Explorer"
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

    # Strip any leading/trailing whitespace from columns
    summary_df.columns = summary_df.columns.str.strip()

    # Rename summary_df columns
    column_renames = {
        "Site code": "Site",
        "Year notes began": "Year Planted",
        "No. live trees": "Number alive",
        "No trees planted": "Number planted"
    }
    summary_df.rename(columns=column_renames, inplace=True)

    # Compute Survival Rate (%) if possible (for summary_df)
    if "Number alive" in summary_df.columns and "Number planted" in summary_df.columns:
        summary_df["Survival Rate (%)"] = (summary_df["Number alive"] / summary_df["Number planted"]) * 100
    else:
        st.warning("Missing columns: 'Number alive' or 'Number planted' to compute survival rate.")

    # Compute Survival Rate (%) if possible (for planting_df)
    if "Number alive" in planting_df.columns and "Number planted" in planting_df.columns:
        planting_df["Survival Rate (%)"] = (planting_df["Number alive"] / planting_df["Number planted"]) * 100
    else:
        st.warning("Missing columns: 'Number alive' or 'Number planted' to compute survival rate.")

    # Show column names for debugging
    st.write("Summary Data Columns:", summary_df.columns.tolist())

    # Survival by Site and Year (from summary_df)
    required_summary_cols = {"Site", "Year Planted", "Survival Rate (%)"}
    if required_summary_cols.issubset(summary_df.columns):
        st.subheader("Survival by Site")
        site_survival = summary_df.groupby("Site")["Survival Rate (%)"].mean().sort_values()
        st.line_chart(site_survival)

        st.subheader("Survival by Year")
        year_survival = summary_df.groupby("Year Planted")["Survival Rate (%)"].mean()
        st.line_chart(year_survival)
    else:
        st.warning("Missing required columns in summary_df for site/year survival analysis.")

    # Survival by Species (from planting_df)
    st.subheader("Survival by Species (from planting data)")
    if {"Species", "Survival Rate (%)"}.issubset(planting_df.columns):
        species_survival = planting_df.groupby("Species")["Survival Rate (%)"].mean().sort_values(ascending=False)
        st.bar_chart(species_survival)
    else:
        st.warning("Missing 'Species' or 'Survival Rate (%)' in planting_df to plot species survival.")
        
# --- 3. Geographic View ---
with map_tab:
    st.header("Geographic View (Planting Data)")

    # append lafayette to each street address (assume location in lafayette)
    if "Site" in planting_df.columns:
        planting_df['Full Address'] = planting_df['Site'] + ", Lafayette, IN"

    # show tree count per site
    if "Site" in planting_df.columns:
        site_counts = planting_df["Site"].value_counts().reset_index()
        site_counts.columns = ["Site", "Count"]
        fig = px.bar(site_counts, x="Site", y="Count", title="Tree Count by Site")
        st.plotly_chart(fig)

    # use heatmap to illustrate most common survival rate/site planting combo
    heat_fig = px.density_heatmap(planting_df, title="Survival Rates at Planting Sites", x="Site", y="Survival Rate (%)", color_continuous_scale="Viridis")
    st.plotly_chart(heat_fig)

# --- 4. Data Explorer ---
with explorer_tab:
    st.header("Data Explorer")

    selected_sheet = st.selectbox("Choose a sheet to explore", ["planting_df", "summary_df", "greenbush_df"])
    
    if selected_sheet == "planting_df":
        st.dataframe(planting_df)
    elif selected_sheet == "summary_df":
        st.dataframe(summary_df)
    else:
        st.dataframe(greenbush_df)

# --- 5. Correlation Explorer ---
with correlation_tab:
    st.header("Correlation Explorer")

    # Compute Survival Rate (%) if possible
    if "Number alive" in summary_df.columns and "Number planted" in summary_df.columns:
        summary_df["Survival Rate (%)"] = (summary_df["Number alive"] / summary_df["Number planted"]) * 100
    else:
        st.warning("Missing columns: 'Number alive' or 'Number planted' to compute survival rate.")
    
    # Compute Survival Rate (%) if possible (for summary_df)
    if "Number alive" in summary_df.columns and "Number planted" in summary_df.columns:
        summary_df["Survival Rate (%)"] = (summary_df["Number alive"] / summary_df["Number planted"]) * 100
    else:
        st.warning("Missing columns: 'Number alive' or 'Number planted' to compute survival rate.")

    # Compute Survival Rate (%) if possible (for planting_df)
    if "Number alive" in summary_df.columns and "Number planted" in summary_df.columns:
        planting_df["Survival Rate (%)"] = (planting_df["Number alive"] / planting_df["Number planted"]) * 100
    else:
        st.warning("Missing columns: 'Number alive' or 'Number planted' to compute survival rate.")

    # Compute native (%) if possible
    if "Native" in summary_df.columns and "Exotic" in summary_df.columns:
        summary_df["Native (%)"] = 100 * (summary_df["Native"] / ((summary_df["Native"]) + summary_df["Exotic"]))
    else:
        st.warning("Missing columns: 'Exotic' or 'Native' to compute survival rate.")

    # Compute Good/Exc (%) if possible
    if "No. Exc, Good" in summary_df.columns and "No. Fair, Poor" in summary_df.columns:
        summary_df["Good/Exc (%)"] = 100 * (summary_df["No. Exc, Good"] / (summary_df["No. Exc, Good"] + summary_df["No. Fair, Poor"]))
    else:
        st.warning("Missing columns: 'No. Exc, Good' or 'No. Fair, Poor.")

    st.write("Pick a field to correlate with year planted")
    selected_col = st.selectbox("Choose a field", ["Trk diam (in.)", "Growth rate (in./y)"])
    if selected_col == "Trk diam (in.)":
        fig = px.scatter(
            planting_df, x='Yr planted', y='Trk diam (in.)', opacity=0.65,
            trendline='ols', trendline_color_override='darkblue'
        )
    else:
        fig = px.scatter(
            planting_df, x='Yr planted', y='Growth rate (in./y)', opacity=0.65,
            trendline='ols', trendline_color_override='darkblue'
        )
    st.plotly_chart(fig)

    st.write("Pick a field to correlate with survival rate (%)")
    selected_col2 = st.selectbox("Choose a field", ["Native (%)", "Growth rate (in./y)", "Good/Exc (%)"])
    if selected_col2 == "Native (%)":
        fig2 = px.scatter(
            summary_df, x='Native (%)', y='Survival Rate (%)', opacity=0.65,
            trendline='ols', trendline_color_override='darkblue'
        )
    elif selected_col2 == "Good/Exc (%)":
        fig2 = px.scatter(
            summary_df, x='Good/Exc (%)', y='Survival Rate (%)', opacity=0.65,
            trendline='ols', trendline_color_override='darkblue'
        )
    else: 
        fig2 = px.scatter(
            planting_df, x='Growth rate (in./y)', y='Survival Rate (%)', opacity=0.65,
            trendline='ols', trendline_color_override='darkblue'
        )
    st.plotly_chart(fig2)






