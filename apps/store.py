from dash import dcc
from dash import html
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from app import app
from data_process import df


px.set_mapbox_access_token('pk.eyJ1IjoiY292aWRwcm9qZWN0IiwiYSI6ImNsMW95Y2Z6MTE2NW0zZG8ybTZjbWlha3YifQ.xaeH7tKRNdRnevWw2uZ70Q')

layout = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H4("Analysys by stores")
                ], width={'size': 12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H5("I. Time series")
                ], width={'size':12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H6('Date', className='text-left'),
                ], width={'size': 1, "offset": 0, 'order': 1}, style={'padding-top': 10}),
                dbc.Col([
                    dcc.DatePickerRange(
                        id='my-date-picker-range_5',  # ID to be used for callback
                        calendar_orientation='horizontal',  # vertical or horizontal
                        day_size=39,  # size of calendar image. Default is 39
                        end_date_placeholder_text="Return",  # text that appears when no end date chosen
                        with_portal=False,  # if True calendar will open in a full screen overlay portal
                        first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                        reopen_calendar_on_clear=True,
                        is_RTL=False,  # True or False for direction of calendar
                        clearable=True,  # whether or not the user can clear the dropdown
                        number_of_months_shown=1,  # number of months shown when calendar is open
                        min_date_allowed=dt.date(df['date'].min()),  # minimum date allowed on the DatePickerRange component
                        max_date_allowed=dt.date(df['date'].max()),  # maximum date allowed on the DatePickerRange component
                        initial_visible_month=dt.date(df['date'].max()),
                        # the month initially presented when the user opens the calendar
                        start_date=dt.date(df['date'].min()),
                        end_date=dt.date(df['date'].max()),
                        display_format='DDMMYYYY',  # how selected dates are displayed in the DatePickerRange component.
                        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                        minimum_nights=1,  # minimum number of days between start and end date
                        persistence=True,
                        persisted_props=['start_date'],
                        persistence_type='session',  # session, local, or memory. Default is 'local'
                        updatemode='singledate')
                ], width={'size': 4, "offset": 0, 'order': 1}),
                dbc.Col([
                    html.H6('Stores', style={'text-align': 'left'})
                ], width={'size': 1, "offset": 0, 'order': 1}, style={'padding-top': 10}),
                dbc.Col([
                    dcc.Dropdown(id='stores',
                                placeholder="Please select stores",
                                options=[],
                                value=[],
                                multi=True,
                                disabled=False,
                                clearable=True,
                                searchable=True)
                ], width={'size': 5, 'offset': 0, 'order': 1}),
                dbc.Col([
                    dbc.Button("Submit", id="btn_5", color="dark", className="ms-2", size='sm')
                ], width={'size': 1, 'offset': 0, 'order': 1}, style={'text-align': 'right'})
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H5('I. Time series by stores')
                ], width={'size': 12, "offset": 0, 'order': 1},),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='time_series_3',figure={},style={'height':350}),
                        ])
                    ])
                ],xs=12,style={'text-align':'center'}),
            ],className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H5('II. Bubble maps')
                ], width={'size': 12, "offset": 0, 'order': 1}, ),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H6('1. Bubble maps by sale amounts')
                ], width={'size': 6, "offset": 0, 'order': 1}),
                dbc.Col([
                    html.H6('2. Bubble maps by bottles')
                ], width={'size': 6, "offset": 0, 'order': 1}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='bubble_map_1',figure={})
                        ])
                    ])
                ], xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='bubble_map_2',figure={})
                        ])
                    ])
                ], xs=6)
            ], className='p-2 align-items-stretch'),
        ])
@app.callback(Output('stores','options'),
              [Input('my-date-picker-range_5','start_date'),
               Input('my-date-picker-range_5','end_date')])

def update_options(start_date_5,end_date_5):
    global dff_2
    dff_2 = df[(df['date'] >= start_date_5) & (df['date'] <= end_date_5)]
    return [{'label':x,'value':x} for x in dff_2.sort_values('store_name')['store_name'].unique()]

@app.callback(Output('time_series_3','figure'),
              [Input('btn_5','n_clicks')],
              [State('stores','value'),
               State('my-date-picker-range_5','start_date'),
               State('my-date-picker-range_5','end_date')])

def update_graph(n_clicks,stores,start_date_5,end_date_5):
    dff_6 = df[(df['date'] >= start_date_5) & (df['date'] <= end_date_5)]
    if stores != [] :
        dff_6 = dff_6[dff_6['store_name'].isin(stores)]
        dff_6_1 = dff_6.pivot_table(values='sale_dollars',
                                    index=['date','store_name'],
                                    aggfunc=np.sum).reset_index()
        fig = px.line(dff_6_1,
                      x='date',
                      y='sale_dollars',
                      color='store_name')
        #fig.update_traces(mode='lines+markers')  # line_shape='spline'
        fig.update_layout(template='plotly_white',margin=dict(l=0,r=0,t=0,b=0),yaxis_title=None, xaxis_title=None)
        fig.update_yaxes(showline=True, showgrid=True, separatethousands=True)
        fig.update_xaxes(showline=True, showgrid=True, separatethousands=True,rangeslider_visible=True)
        return fig
    else:
        dff_6_1 = dff_6.pivot_table(values='sale_dollars',
                                    index=['date'],
                                    aggfunc=np.sum).reset_index()
        fig = px.line(dff_6_1,
                         x='date',
                         y='sale_dollars')
        #fig.update_traces(mode='lines+markers')  # line_shape='spline'
        fig.update_layout(template='plotly_white',margin=dict(l=0,r=0,t=0,b=0),yaxis_title=None, xaxis_title=None)
        fig.update_yaxes(showline=True, showgrid=True, separatethousands=True)
        fig.update_xaxes(showline=True, showgrid=True, separatethousands=True,rangeslider_visible=True)
        return fig

@app.callback([Output('bubble_map_1','figure'),Output('bubble_map_2','figure')],
              [Input('btn_5','n_clicks')],
              [State('my-date-picker-range_5', 'start_date'),
              State('my-date-picker-range_5', 'end_date')]
              )

def update_graph(n_clicks,start_date_5, end_date_5):
    dff_9 = df[(df['date'] >= start_date_5) & (df['date'] <= end_date_5)]
    dff_9_1 = pd.pivot_table(dff_9, ('sale_dollars'), index=['store_name', "lat", "lon"], aggfunc=np.sum).reset_index()

    fig_5 = px.scatter_mapbox(dff_9_1,
                          lat=dff_9_1["lat"],
                          lon=dff_9_1["lon"],
                          size="sale_dollars",
                          color='sale_dollars',
                          color_continuous_scale=px.colors.sequential.Plasma,
                          zoom=5,
                          center={"lat": 42.01604, "lon": -92.91157},
                          hover_name="store_name")
    fig_5.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    dff_9_2 = pd.pivot_table(df,('bottles_sold'),index=['store_name',"lat","lon"],aggfunc=np.sum).reset_index()
    fig_6 = px.scatter_mapbox(dff_9_2,
                          lat=dff_9_2["lat"],
                          lon=dff_9_2["lon"],
                          size="bottles_sold",
                          color='bottles_sold',
                          color_continuous_scale=px.colors.sequential.Viridis,
                          zoom=5,
                          center={"lat": 42.01604, "lon": -92.91157},
                          hover_name="store_name")
    fig_6.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig_5, fig_6
