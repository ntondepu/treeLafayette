#Tree Lafayette Survival Analysis
This repository contains a Streamlit dashboard for analyzing tree planting and survival data in Lafayette. The goal of the project is to help visualize trends in tree survival rates by location, year, and species, using data from local planting efforts.

Features
Survival rate analysis by site and year using summarized data

Survival rate analysis by species using planting data

Automatic column renaming and formatting for clarity

Graceful handling of missing or incomplete data

Interactive plots with Streamlit's built-in charting tools

How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/tree-lafayette.git
cd tree-lafayette
Install the required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Launch the Streamlit app:

bash
Copy
Edit
streamlit run app.py
Data Sources
The app expects two main dataframes:

summary_df
This dataframe should contain aggregated data by site and year. The app will automatically rename the following columns:


Original Column	Renamed To
Site code	Site
Year notes began	Year Planted
No. live trees	Number alive
No trees planted	Number planted
A "Survival Rate (%)" column will be calculated as:

javascript
Copy
Edit
(Number alive / Number planted) * 100
planting_df
This dataframe should include individual tree records with at least:

Species

Survival Rate (%)

Output
Line charts of survival rate trends by site and by year

Bar chart of survival rates by species

Warnings if required columns are missing

Potential Improvements
Add filters for specific years, species, or locations

Include raw counts in visualizations

Support CSV file uploads for custom data exploration

Integrate with GIS data for spatial analysis

License
This project is licensed under the MIT License.
