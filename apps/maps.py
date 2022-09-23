from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
import numpy as np
import dash_bootstrap_components as dbc
from app import app
from data_process import df

# get relative data folder
df2 = pd.pivot_table(df,('sale_dollars'),index=['store_name',"lat","lon"],aggfunc=np.sum).reset_index()
df2=df2[df2['lat'] != 0]

cities = df2.to_dict(orient='records')
dd_options = [dict(value=c["store_name"], label=c["store_name"]) for c in cities]
dd_defaults = [o["value"] for o in dd_options]
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['store_name'])} for c in cities])
geojson_filter = assign("function(feature, context){return context.props.hideout.includes(feature.properties.store_name);}")

layout = html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Markdown('''This is a tool that helps you search for stores by latitude and longitude extracted from the original data. 
                    However, the latitude and longitude data of many stores is missing or inaccurate, so we decided to remove stores that missing lattitude and longtitude.
                    This tool is executed referring the [dash-leaflet](http://dash-leaflet.herokuapp.com/)''')
                ])
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H6('Store Name')
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'padding-top': 10}),
                dbc.Col([
                    dcc.Dropdown(id="dd",
                                 value=df2['store_name'].iloc[0],
                                 options=dd_options,
                                 clearable=False,
                                 multi=True)
                ], width={'size': 10, "offset": 0, 'order': 1})
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dl.Map(children=[
                                dl.TileLayer(),
                                dl.GeoJSON(data=geojson,
                                           options=dict(filter=geojson_filter),
                                           hideout=dd_defaults,
                                           id="geojson",
                                           zoomToBounds=True),
                            ], style={'width': '100%', 'height': '70vh', 'margin': "auto", "display": "block"}, id="map"),
                        ])
                    ])
                ],xs=12)
            ],className='p-2 align-items-stretch'),
        ])

app.clientside_callback("function(x){return x;}", Output("geojson", "hideout"), Input("dd", "value"))