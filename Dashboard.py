from urllib.request import urlopen
import requests
import json
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

# Setup the app
app = dash.Dash(__name__)
server = app.server


# Preparing Data

# Extract Data from API
url = "https://covid19.th-stat.com/api/open/cases/sum"
with requests.get(url) as response:
    data = json.loads(response.text)
    
data_covid19_sum = pd.DataFrame.from_dict(data)
data_covid19_sum.reset_index(inplace=True)
data_covid19_sum = data_covid19_sum[["index", "Province"]]

col_name = {'Province': 'PUI_sum', 'index': 'Province'}

data_covid19_sum.rename(columns=col_name, inplace=True)

# Read province for merge with API Data
th_province = pd.read_csv("Province_Name.csv")

# Merge data and this is real used data
data = pd.merge(th_province,data_covid19_sum, on='Province', how='left')
data["PUI_sum"] = data["PUI_sum"].fillna(0).astype('int')


# Remove Bangkok from data since it is the outlier
data_no_outlier = data[data["Province"] != "Bangkok"]


# Preparing map for ploting
with open('thailand_map_data.json') as file:
    thailand_map_data = json.load(file)


# Set maximum data equal quatile 95
data_max = data_no_outlier["PUI_sum"].quantile(.95)

# Create the graph
fig = px.choropleth_mapbox(data, geojson=thailand_map_data, color="PUI_sum",
                    locations="Province", featureidkey="properties.name",
                    color_continuous_scale="Reds",
                    mapbox_style="carto-positron",
                    zoom=5, center = {"lat": 13.7367, "lon": 100.5231},
                    opacity=0.8,
                    range_color = (1, data_max)
                   )

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# Create take the graph to the app

app.layout = html.Div([
    dcc.Graph(figure=fig,style={'height': '95vh', 'margin': '20px'})
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
