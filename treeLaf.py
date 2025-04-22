st.set_page_config(page_title="Tree Lafayette Dashboard", layout="wide")

st.title("🌳 Tree Lafayette Growth & Survival Dashboard")

# Upload file (optional)
uploaded_file = st.file_uploader("Upload a tree survival data file (.csv or .xlsx)", type=["csv", "xlsx"])

# Load data
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.success("✅ Uploaded file loaded.")
else:
    df = pd.read_csv("tree_survival_summary.csv")
    st.info("ℹ️ Using default dataset.")

# Optional: Show data preview
with st.expander("🔍 Preview Data"):
    st.dataframe(df.head(15))

# Filter by species
species_list = df["Species"].dropna().unique()
selected_species = st.selectbox("Filter by species", options=species_list)
filtered_df = df[df["Species"] == selected_species]

# Plotting example
st.subheader(f"📊 Trees Planted Over Time for {selected_species}")
fig, ax = plt.subplots()
sns.barplot(data=filtered_df, x="Yr planted", y="Number planted", ax=ax)
plt.xticks(rotation=45ddddst.pyplot(fig)
