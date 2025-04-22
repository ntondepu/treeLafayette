import pandas as pd
import plotly.express as px
import statsmodels.api as sm

# define file path to xlsx files 
workbook_greenbush = 'Files/greenbush.xlsx'
workbook_inventory = 'Files/inventory.xlsx'
workbook_survival = 'Files/survival.xlsx'

# read data into variable
survival_sheet = pd.read_excel(workbook_survival, sheet_name='Data')
inventory_sheet = pd.read_excel(workbook_inventory, sheet_name='Site Codes')
greenbush_data = pd.read_excel(workbook_greenbush, sheet_name='Data')
greenbush_survival = pd.read_excel(workbook_greenbush, sheet_name='Survival', header=None)
greenbush_growth = pd.read_excel(workbook_greenbush, sheet_name='Growth - Average trunk diamter ', header=None)
greenbush_summary = pd.read_excel(workbook_greenbush, sheet_name='Summary statistics')

# remove duplicate values & ensure proper header formatting
s_survival = survival_sheet.drop_duplicates()
s_inventory = inventory_sheet.drop_duplicates()
g_data = greenbush_data.drop_duplicates()
g_survival = greenbush_survival.drop_duplicates().drop([0, 1])
g_growth = greenbush_growth.drop_duplicates().drop([0])
g_summary = greenbush_summary.drop_duplicates()

# standardize headers for g_growth data
new_header = g_growth.iloc[0] 
g_growth = g_growth[1:] 
g_growth.columns = new_header 

# concat data set 
df = {'s_survival': s_survival, 's_inventory': s_inventory, 'g_data': g_data, 'g_survival': g_survival, 'g_growth': g_growth, 'g_summary': g_summary}
merged_df = pd.concat(df)

# basic pie chart for frequency by genus
fig = px.pie(g_summary[0:-1], values='Current freq (%)', names='Genus', title='Frequency by Genus')
fig.show()

# function to show loss % by location, filtered by year
s_i = df['s_inventory']
def loss_by_year(year):
    subset = s_i[s_i['Year notes began'] == year]
    fig = px.bar(subset, x= "Location", y= "Loss (%)", title= "Loss (%) per Location by Year")
    fig.show()

# linear regression prediction of loss % based on columns (might remove due to insignificance/lack of correlation)
# create column for native ratio %
native_ratio = []
s_i = s_i.dropna()

for x in range(0, 1 + len(s_i)):
    if (x != 15):
        n = s_i['Native'][x]
        e = s_i['Exotic'][x]
        n_e = n/(n + e)
        native_ratio.append(n_e)
    else:
        continue

# add native ratio column to dataset
s_i['Native Plant Ratio'] = native_ratio
print(s_i)

# add columns as options for x axis (for easier implementation into streamlight)
col = list(s_i.columns)
def reg_plot(z):
    if (z <= len(col)):
        fig = px.scatter(
            s_i, x=col[z], y='Loss (%)', opacity=0.65,
            trendline='ols', trendline_color_override='darkblue'
        )
        fig.show()

# visual for number of trees planted and alive by species (wip)
s_s = df['s_survival']
fig = px.bar(s_s, x="Species", y="Number planted",
             color='Number alive')
fig.show()



