from urllib.request import urlopen
import requests
import json
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

df = pd.read_csv("covid19-th-acc.csv")
df.replace("กทม","กรุงเทพมหานคร", inplace=True)

province_eng = pd.read_csv("Thailand_Province_Boundaries_2019.csv")
province_eng = province_eng[["PROV_NAMT","PROV_NAME"]]

df = df.set_index('Province')

province_eng = province_eng.set_index('PROV_NAMT')

data = pd.concat([df,province_eng], axis=1, sort=False)
data["Count_of_no"] = data["Count_of_no"].fillna(0)
data["Count_of_no"] = data["Count_of_no"].astype('int')
data["PROV_NAME"] = data["PROV_NAME"].str.lower().str.title()

data_no_outlier = data[data["PROV_NAME"] != "Bangkok"]


# Preparing map for ploting

# with urlopen('https://raw.githubusercontent.com/apisit/thailand.json/master/thailandWithName.json') as response:
#     thailand_map_data = json.load(response)

# for index, v in enumerate(thailand_map_data["features"]):
#     if v["properties"]["name"] == "Bangkok Metropolis":
#         thailand_map_data["features"][index]["properties"]["name"] = "Bangkok"

# data_max = data_no_outlier["Count_of_no"].max()


# # Create the graph

# fig = px.choropleth(data, geojson=thailand_map_data, color="Count_of_no",
#                     locations="PROV_NAME", featureidkey="properties.name",
#                     projection="mercator",
#                     color_continuous_scale="Reds",
#                     range_color = [0, data_max]
#                    )

# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

df = px.data.gapminder()
fig = px.choropleth(df, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year", range_color=[20,80])

# Create take the graph to the app

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)