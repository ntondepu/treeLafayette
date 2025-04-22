import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tree Lafayette Dashboard", layout="wide")

st.title("🌳 Tree Lafayette Dashboard")

# --- Upload Section ---
st.sidebar.header("📁 Upload Tree Data")
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    # Load all sheets from Excel
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    st.sidebar.success(f"Loaded sheets: {', '.join(sheet_names)}")

    # Assume sheet names for now (change based on actual Excel structure)
    planting_df = xls.parse(sheet_names[0])
    summary_df = xls.parse(sheet_names[1])

else:
    st.warning("Please upload an Excel file with multiple sheets (e.g., planting data + summary).")
    st.stop()

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["🌲 Overview", "📈 Health & Growth", "📋 Species Summary", "🧪 Raw Data"])

# --- Overview Tab ---
with tab1:
    st.header("🌲 Overview: Tree Planting Projects")
    st.write(f"Total records: {len(planting_df)}")

    if 'Year Planted' in planting_df.columns:
        fig1, ax1 = plt.subplots()
        sns.countplot(data=planting_df, x="Year Planted", ax=ax1)
        plt.xticks(rotation=45)
        st.pyplot(fig1)

# --- Health & Growth Tab ---
with tab2:
    st.header("📈 Tree Health & Growth Over Time")
    if "Trunk Diameter (in.)" in planting_df.columns and "Year Planted" in planting_df.columns:
        fig2, ax2 = plt.subplots()
        sns.boxplot(data=planting_df, x="Year Planted", y="Trunk Diameter (in.)", ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

# --- Species Summary Tab ---
with tab3:
    st.header("📋 Summary by Species / Genus")
    if "Species" in summary_df.columns and "Avg Growth Rate" in summary_df.columns:
        top_species = summary_df.sort_values(by="Avg Growth Rate", ascending=False).head(10)
        st.bar_chart(top_species.set_index("Species")["Avg Growth Rate"])

# --- Data Explorer Tab ---
with tab4:
    st.header("🧪 Explore Raw Data")
    selected_sheet = st.selectbox("Select sheet to view", sheet_names)
    df_selected = xls.parse(selected_sheet)
    st.dataframe(df_selected)

