from dash import dcc
from dash import html,callback
import numpy as np
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from urllib.request import urlopen
import json
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from data_process import df, df2
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import dash_mantine_components as dmc
import dash_extensions as de

options = dict(loop=True, autoplay=True) #rendererSettings=dict(preserveAspectRatio='xMidYmid slice'

# Load json to create choropleth maps
with urlopen('https://gist.githubusercontent.com/mcwhittemore/96aaa132af24d3114643/raw/9cea5ced7476cc419621acf0505554e4b45ca459/iowa-counties.geojson') as response:
    counties = json.load(response)

# Data for first graph
df3 = df.pivot_table(values='sale_dollars',
                     index=['Season','category_name'],
                     aggfunc=np.sum).reset_index()
df3 = df3.sort_values(['Season', 'sale_dollars'], ascending=[True, False]).groupby('Season').head(10)
autumn = df3['sale_dollars'].iloc[0]
autumn = f'{autumn:,.2f}'
spring = df3['sale_dollars'].iloc[10]
spring = f'{spring:,.2f}'
summer = df3['sale_dollars'].iloc[20]
summer = f'{summer:,.2f}'
winter = df3['sale_dollars'].iloc[30]
winter = f'{winter:,.2f}'

autumn_2 = df3['category_name'].iloc[0]
spring_2 = df3['category_name'].iloc[10]
summer_2 = df3['category_name'].iloc[20]
winter_2 = df3['category_name'].iloc[30]

# First graph

# Second graph


layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.SLATE})
                ],style={'text-align':'right'})
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4("Analysys by category")
                ], width={'size': 12}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.H5("I. Seasonal Analysis")
                ], width={'size':12}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    dcc.Markdown("""In Iowa, Spring usually lasts from March to May, Summer from June to September, Autumn from October to December, Winter from January to March.""")
                ], width={'size': 12}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Top 10 Wines category sales each season'),
                            dcc.Graph(id='season_chart_1',figure={}),
                        ])
                    ])
                ],xs=9,style={'text-align':'center'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Sales percentage by season'),
                            dcc.Graph(id='season_chart_2',figure={})
                        ])
                    ])
                ], xs=3,style={'text-align':'center'})
            ],className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.Span(f'- The most sold wines category in Spring is {spring_2} with amount {spring}',
                            style={"white-space": "pre-line"}),
                ], width={'size': 12}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.Span(f'- The most sold wines category in Summer is {summer_2} with amount {summer}',
                            style={"white-space": "pre-line"}),
                ], width={'size': 12}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.Span(f'- The most sold wines category in Autumn is {autumn_2} with amount {autumn}',
                            style={"white-space": "pre-line"}),
                ], width={'size': 12}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.Span(f'- The most sold wines category in Winter is {winter_2} with amount {winter}',
                            style={"white-space": "pre-line"}),
                ], width={'size': 12}),
            ], className='p-2 align-items-center'),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H6('Date Picker',className='text-left'),
                ],width={'size':1,"offset":0,'order':1}),
                dbc.Col([
                    dcc.DatePickerRange(
                        id='my-date-picker-range',  # ID to be used for callback
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
                        initial_visible_month=dt.date(df['date'].max()),  # the month initially presented when the user opens the calendar
                        start_date=dt.date(df['date'].min()),
                        end_date=dt.date(df['date'].max()),
                        display_format='DDMMYYYY',  # how selected dates are displayed in the DatePickerRange component.
                        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                        minimum_nights=1,  # minimum number of days between start and end date
                        persistence=True,
                        persisted_props=['start_date'],
                        persistence_type='session',  # session, local, or memory. Default is 'local'
                        updatemode='singledate')
                ],width={'size':4,"offset":0,'order':1}),
                dbc.Col([
                    dbc.Button("Submit",id="btn",color="dark",className="ms-2",size='sm')
                ],width={'size':2,'offset':5,'order':1},style={'text-align':'right'})
            ],className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Sales Amount', className="card-title"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    de.Lottie(options=options, width="100%", height="100%",
                                              url="https://assets9.lottiefiles.com/packages/lf20_jev2s9zm.json")
                                ], width={'size': 4}, style={'text-align': 'right'}),
                                dbc.Col([
                                    html.Div(id='sales_indicator',style={'padding-top':20})
                                ], width={'size': 8},style={'text-align':'right'})
                            ])
                        ])
                    ], style={'height':'20vh'})
                ], width={'size': 3},style={'text-align':'right'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Revenues Amount', className="card-title"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    de.Lottie(options=options, width="100%", height="100%",
                                              url="https://assets8.lottiefiles.com/private_files/lf30_wypj5bum.json")
                                ], width={'size': 4}, style={'text-align': 'right'}),
                                dbc.Col([
                                    html.Div(id='revenues_indicator', style={'padding-top': 20})
                                ], width={'size': 8}, style={'text-align': 'right'})
                            ])
                        ])
                    ], style={'height':'20vh'})
                ], width={'size': 3}, style={'text-align': 'right'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Bottles Amount', className="card-title"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    de.Lottie(options=options, width="100%", height="100%",
                                              url="https://assets4.lottiefiles.com/packages/lf20_8uH7dH.json")
                                ], width={'size': 4}, style={'text-align': 'right'}),
                                dbc.Col([
                                    html.Div(id='bottle_indicator', style={'padding-top': 20})
                                ], width={'size': 8}, style={'text-align': 'right'})
                            ])
                        ])
                    ], style={'height':'20vh'})
                ], width={'size': 3}, style={'text-align': 'right'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Liters Amount', className="card-title"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    de.Lottie(options=options, width="100%", height="100%",
                                              url="https://assets1.lottiefiles.com/private_files/lf30_lem2zbj4.json")
                                ], width={'size': 4}, style={'text-align': 'right'}),
                                dbc.Col([
                                    html.Div(id='liters_indicator', style={'padding-top': 20})
                                ], width={'size': 8}, style={'text-align': 'right'})
                            ])
                        ])
                   ], style={'height':'20vh'})
                ], width={'size': 3}, style={'text-align': 'right'}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.H5("II. Top 10 sold wines category by elements")
                ], width={'size': 12}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.H6("1. Top 10 sold wines category by sales amount")
                ], width={'size': 6}),
                dbc.Col([
                    html.H6("2. Top 10 sold wines category by bottles amount")
                ], width={'size': 6}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.Div(id='top10_1_title')
                ], width={'size': 6}),
                dbc.Col([
                    html.Div(id='top10_2_title')
                ], width={'size': 6}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='top10_1',style={'height':350})],color='rgba(50, 171, 96, 0.6)',type='dot')
                        ])
                    ])
                ],xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='top10_2',style={'height':350})],color='rgba(50, 171, 96, 0.6)',type='dot')
                            ])
                        ])
                ],xs=6)
            ],className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.H6("3. Top 10 sold wines category by liters amount")
                ], width={'size': 6}),
                dbc.Col([
                    html.H6("4. Top 10 sold wines by category revenues amount")
                ], width={'size': 6}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.Div(id='top10_3_title')
                ], width={'size': 6}),
                dbc.Col([
                    html.Div(id='top10_4_title')
                ], width={'size': 6}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='top10_3',style={'height':350})],color='rgba(50, 171, 96, 0.6)',type='dot')
                            ])
                        ])
                    ], xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='top10_4',style={'height':350})],color='rgba(50, 171, 96, 0.6)',type='dot')
                            ])
                        ])
                    ], xs=6)
                ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.H5("III. Analysis by counties")
                ], width={'size': 12}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.H6("1. Choropleth map by sales amount")
                ], width={'size': 6}),
                dbc.Col([
                    html.H6("2. Choropleth map by sales liters")
                ], width={'size': 6}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.Div(id='map_1_title')
                ], width={'size': 6}),
                dbc.Col([
                    html.Div(id='map_2_title')
                ], width={'size': 6}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='map_1',style={'height':350})],
                                        color='rgba(50, 171, 96, 0.6)',type='dot')
                        ])
                    ])
                ], xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='map_2',style={'height':350})],
                                        color='rgba(50, 171, 96, 0.6)',type='dot')
                        ])
                    ])
                ], xs=6)
            ], className='p-2 align-items-center'),
            dmc.Text("Note: You can click on map to see charts for each county", size="sm",underline=True),
            html.Div(id='div_1'),
            dbc.Row([
                dbc.Col([
                    html.H5("IV. Time Series")
                ], width={'size': 12}),
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    html.H6('Date', className='text-left'),
                ], width={'size': 1, "offset": 0, 'order': 1}),
                dbc.Col([
                    dcc.DatePickerRange(
                        id='my-date-picker-range_2',  # ID to be used for callback
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
                    html.H6('Category', style={'text-align': 'left'})
                ], width={'size': 1, "offset": 0, 'order': 1}),
                dbc.Col([
                    dcc.Dropdown(id='category',
                                placeholder="Please select category",
                                options=[],
                                value=[],
                                multi=True,
                                disabled=False,
                                clearable=True,
                                searchable=True)
                ], width={'size': 5, 'offset': 0, 'order': 1}),
                dbc.Col([
                    dbc.Button("Submit", id="btn_2", color="dark", className="ms-2", size='sm')
                ], width={'size': 1, 'offset': 0, 'order': 1}, style={'text-align': 'right'})
            ], className='p-2 align-items-center'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(id='time_series_1', figure={}, style={'height': 350})],color='rgba(50, 171, 96, 0.6)',type='dot'),
                        ])
                    ])
                ], xs=12, style={'text-align': 'center'}),
            ], className='p-2 align-items-center'),
            dcc.Store(id='store_data',data=[],storage_type='memory')
        ],
    fluid=True,
    className="dbc")

@callback([Output('season_chart_1', 'figure'),
           Output('season_chart_2', 'figure')],
          Input(ThemeChangerAIO.ids.radio("theme"), "value"))
def update_graph(theme):
    df3 = df.pivot_table(values='sale_dollars',
                         index=['Season', 'category_name'],
                         aggfunc=np.sum).reset_index()
    df3 = df3.sort_values(['Season', 'sale_dollars'], ascending=[True, False]).groupby('Season').head(10)
    fig_1 = go.Figure(data=[
        go.Bar(name='Type', x=[tuple(df3['Season']), tuple(df3['category_name'])],
               y=list(df3['sale_dollars'])),
    ])
    fig_1.update_traces(marker_color='lightseagreen')
    fig_1.update_layout(template=template_from_url(theme), margin=dict(l=0, r=0, t=0, b=0))
    df4 = df.pivot_table(values='sale_dollars',
                         index=['Season'],
                         aggfunc=np.sum).reset_index()
    fig_2 = px.pie(df4,
                   values='sale_dollars',
                   names='Season',
                   color_discrete_sequence=px.colors.qualitative.Prism,
                   hole=0.7)
    fig_2.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h"),template=template_from_url(theme))
    return fig_1,fig_2

@callback([Output('sales_indicator', 'children'),
           Output('revenues_indicator', 'children'),
           Output('bottle_indicator', 'children'),
           Output('liters_indicator', 'children')],
          [Input('btn','n_clicks'),
           Input(ThemeChangerAIO.ids.radio("theme"), "value")],
          [State('my-date-picker-range', 'start_date'),
           State('my-date-picker-range', 'end_date')])
def update_indicator(n_clicks,theme,start_date,end_date):
    dff = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    dff = dff[['sale_dollars','revenues','bottles_sold','volume_sold_liters']]
    dff.loc['Sum'] = dff.sum()
    value_1 = dff['sale_dollars'].iloc[-1]
    value_2 = dff['revenues'].iloc[-1]
    value_3 = dff['bottles_sold'].iloc[-1]
    value_4 = dff['volume_sold_liters'].iloc[-1]
    value_1 = f'{value_1:,.0f}'
    value_2 = f'{value_2:,.0f}'
    value_3 = f'{value_3:,.0f}'
    value_4 = f'{value_4:,.0f}'
    return html.H3(f'$ {value_1}'),html.H3(f'$ {value_2}'),html.H3(f'{value_3}'),html.H3(f'{value_4}')

@callback([Output('top10_1', 'figure'),
           Output('top10_2', 'figure'),
           Output('top10_3', 'figure'),
           Output('top10_4', 'figure'),
           Output('top10_1_title', 'children'),
           Output('top10_2_title', 'children'),
           Output('top10_3_title', 'children'),
           Output('top10_4_title', 'children')],
          [Input('btn','n_clicks'),
           Input(ThemeChangerAIO.ids.radio("theme"), "value")],
          [State('my-date-picker-range', 'start_date'),
           State('my-date-picker-range', 'end_date')])

def update_graph(n_clicks,theme,start_date,end_date):
    dff = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    df5 = dff.pivot_table(values='sale_dollars',
                         index=['category_name'],
                         aggfunc=np.sum).reset_index()

    df5 = df5.sort_values(['sale_dollars'], ascending=[False]).head(10)
    df5 = df5.sort_values(['sale_dollars'], ascending=[True])
    top10_1_title_1 = df5['category_name'].iloc[9]
    top10_1_title_2 = df5['sale_dollars'].iloc[9]
    top10_1_title_2 = f'{top10_1_title_2:,.2f}'
    top10_1_title_3 = df5['sale_dollars'].iloc[9]

    fig_3 = px.bar(df5, x='sale_dollars', y='category_name', orientation='h', text='sale_dollars')
    fig_3.update_traces(marker_color='rgba(50, 171, 96, 0.6)', marker_line_color='rgba(50, 171, 96, 1.0)',
                      marker_line_width=1,texttemplate='%{text:,.2f}', textposition='outside')
    fig_3.update_layout(template=template_from_url(theme), margin=dict(l=0, r=0, t=0, b=0))
    fig_3.update_layout({'xaxis': {'range': [0, top10_1_title_3 * 1.3]}})

    df6 = dff.pivot_table(values='bottles_sold',
                              index=['category_name'],
                              aggfunc=np.sum).reset_index()

    df6 = df6.sort_values(['bottles_sold'], ascending=[False]).head(10)
    df6 = df6.sort_values(['bottles_sold'], ascending=[True])
    top10_2_title_1 = df6['category_name'].iloc[9]
    top10_2_title_2 = df6['bottles_sold'].iloc[9]
    top10_2_title_2 = f'{top10_2_title_2:,.2f}'
    top10_2_title_3 = df6['bottles_sold'].iloc[9]

    fig_4 = px.bar(df6, x='bottles_sold', y='category_name', orientation='h', text='bottles_sold')
    fig_4.update_traces(marker_color='rgba(50, 171, 96, 0.6)', marker_line_color='rgba(50, 171, 96, 1.0)',
                      marker_line_width=1,texttemplate='%{text:,.2f}', textposition='outside')
    fig_4.update_layout(template=template_from_url(theme), margin=dict(l=0, r=0, t=0, b=0))
    fig_4.update_layout({'xaxis': {'range': [0, top10_2_title_3 * 1.3]}})

    df7 = dff.pivot_table(values='volume_sold_liters',
                         index=['category_name'],
                         aggfunc=np.sum).reset_index()

    df7 = df7.sort_values(['volume_sold_liters'], ascending=[False]).head(10)
    df7 = df7.sort_values(['volume_sold_liters'], ascending=[True])
    top10_3_title_1 = df7['category_name'].iloc[9]
    top10_3_title_2 = df7['volume_sold_liters'].iloc[9]
    top10_3_title_2 = f'{top10_3_title_2:,.2f}'
    top10_3_title_3 = df7['volume_sold_liters'].iloc[9]

    fig_5 = px.bar(df7, x='volume_sold_liters', y='category_name', orientation='h', text='volume_sold_liters')
    fig_5.update_traces(marker_color='rgba(50, 171, 96, 0.6)', marker_line_color='rgba(50, 171, 96, 1.0)',
                      marker_line_width=1,texttemplate='%{text:,.2f}', textposition='outside')
    fig_5.update_layout(template=template_from_url(theme), margin=dict(l=0, r=0, t=0, b=0))
    fig_5.update_layout({'xaxis': {'range': [0, top10_3_title_3 * 1.3]}})

    df8 = dff.pivot_table(values='revenues',
                              index=['category_name'],
                              aggfunc=np.sum).reset_index()
    df8 = df8.sort_values(['revenues'], ascending=[False]).head(10)
    df8 = df8.sort_values(['revenues'], ascending=[True])
    top10_4_title_1 = df8['category_name'].iloc[9]
    top10_4_title_2 = df8['revenues'].iloc[9]
    top10_4_title_2 = f'{top10_4_title_2:,.2f}'
    top10_4_title_3 = df8['revenues'].iloc[9]
    fig_6 = px.bar(df8, x='revenues', y='category_name', orientation='h', text='revenues')
    fig_6.update_traces(marker_color='rgba(50, 171, 96, 0.6)', marker_line_color='rgba(50, 171, 96, 1.0)',
                      marker_line_width=1,texttemplate='%{text:,.2f}', textposition='outside')
    fig_6.update_layout(template=template_from_url(theme), margin=dict(l=0, r=0, t=0, b=0))
    fig_6.update_layout({'xaxis':{'range':[0, top10_4_title_3*1.3]}})
    return fig_3,\
           fig_4,\
           fig_5,\
           fig_6,\
           html.Span(f'The most sold wines category by sales amount from {start_date} to {end_date} is {top10_1_title_1} with amount {top10_1_title_2}'),\
           html.Span(f'The most sold wines category by bottles from {start_date} to {end_date} is {top10_2_title_1} with amount {top10_2_title_2}'),\
           html.Span(f'The most sold wines category by liters from {start_date} to {end_date} is {top10_3_title_1} with amount {top10_3_title_2}'),\
           html.Span(f'The most sold wines category by revenues from {start_date} to {end_date} is {top10_4_title_1} with amount {top10_4_title_2}')

@callback([Output('map_1', 'figure'),
           Output('map_2', 'figure'),
           Output('map_1_title', 'children'),
           Output('map_2_title', 'children'),
           Output('store_data', 'data')],
          [Input('btn','n_clicks'),
           Input(ThemeChangerAIO.ids.radio("theme"), "value")],
          [State('my-date-picker-range', 'start_date'),
           State('my-date-picker-range', 'end_date')])

def update_graph(n_clicks,theme,start_date,end_date):
    global dff
    dff = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    df9 = dff.pivot_table(values='sale_dollars',
                         index=['county',"county_fips"],
                         aggfunc=np.sum).reset_index()
    #df9 = pd.merge(df9, df2[['county', 'county_fips']], on='county', how='left')
    df9 = df9.sort_values(['sale_dollars'], ascending=[False])
    map_1_title_1 = df9['county'].iloc[0]
    map_1_title_2 = df9['sale_dollars'].iloc[0]
    map_1_title_2 = f'{map_1_title_2:,.2f}'
    fig_7 = px.choropleth_mapbox(df9,
                                 locations=df9["county_fips"],
                                 geojson=counties,
                                 featureidkey="properties.geoid",
                                 color=df9['sale_dollars'],
                                 hover_name="county",
                                 range_color=(0, df9['sale_dollars'].iloc[0]),
                                 zoom=5,
                                 center={"lat": 42.01604, "lon": -92.91157},
                                 color_continuous_scale="Viridis")
    fig_7.update_layout(template=template_from_url(theme),
                        margin=dict(l=0, r=0, t=0, b=0),
                        clickmode='event+select')

    df10 = dff.pivot_table(values='volume_sold_liters',
                          index=['county',"county_fips"],
                          aggfunc=np.sum).reset_index()
    #df10 = pd.merge(df10, df2[['county', 'county_fips']], on='county', how='left')
    df10 = df10.sort_values(['volume_sold_liters'], ascending=[False])
    map_2_title_1 = df10['county'].iloc[0]
    map_2_title_2 = df10['volume_sold_liters'].iloc[0]
    map_2_title_2 = f'{map_2_title_2:,.2f}'
    fig_8 = px.choropleth_mapbox(df10,
                                 locations=df10["county_fips"],
                                 geojson=counties,
                                 featureidkey="properties.geoid",
                                 color=df10['volume_sold_liters'],
                                 hover_name="county",
                                 range_color=(0, df10['volume_sold_liters'].iloc[0]),
                                 zoom=5,
                                 center={"lat": 42.01604, "lon": -92.91157},
                                 color_continuous_scale="Viridis")
    fig_8.update_layout(template=template_from_url(theme),
                        margin=dict(l=0, r=0, t=0, b=0),
                        clickmode='event+select')

    return fig_7,\
           fig_8,\
           html.Span(f'The most sold wines county by sales amount from {start_date} to {end_date} is {map_1_title_1} with amount {map_1_title_2}'),\
           html.Span(f'The most sold wines county by liters from {start_date} to {end_date} is {map_2_title_1} with amount {map_2_title_2}'),\
           dff.to_dict(orient='records')

@callback(Output('div_1', 'children'),
          [Input('map_1', 'clickData'),
           Input('store_data', 'data'),
           Input(ThemeChangerAIO.ids.radio("theme"), "value")])

def update_bar_chart(clickdata,store_data,theme):
    #if clickdata == []:
        #dff_z = dff[dff['county'] == 'Polk']
    if clickdata:
        points = clickdata['points'][0]['location']
        dff_z = dff[dff['county_fips'] == points]

        dff_z_1 = dff_z.pivot_table(values='sale_dollars',
                          index=['store_name'],
                          aggfunc=np.sum).reset_index()
        dff_z_1 = dff_z_1.sort_values(['sale_dollars'], ascending=[False]).head(30)
        fig = px.bar(dff_z_1,x='sale_dollars',y='store_name',orientation='h')
        fig.update_traces(marker_color='rgba(50, 171, 96, 0.6)',
                      marker_line_color='rgba(50, 171, 96, 1.0)',
                      marker_line_width=0.5)
        fig.update_layout(template=template_from_url(theme), margin=dict(l=0, r=0, t=0, b=0),yaxis_title=None, xaxis_title=None)

        dff_z_2 = dff_z.pivot_table(values='sale_dollars',
                                index=['category_name'],
                                aggfunc=np.sum).reset_index()
        dff_z_2 = dff_z_2.sort_values(['sale_dollars'], ascending=[False]).head(30)
        fig_2 = px.bar(dff_z_2, x='sale_dollars', y='category_name',orientation='h')
        fig_2.update_traces(marker_color='rgba(50, 171, 96, 0.6)',
                        marker_line_color='rgba(50, 171, 96, 1.0)',
                        marker_line_width=0.5)
        fig_2.update_layout(template=template_from_url(theme),
                        margin=dict(l=0, r=0, t=0, b=0),
                        yaxis_title=None,
                        xaxis_title=None)
        dff_z_3 = dff_z.pivot_table(values='sale_dollars',
                                index=['item_description'],
                                aggfunc=np.sum).reset_index()
        dff_z_3 = dff_z_3 .sort_values(['sale_dollars'], ascending=[False]).head(30)
        fig_3 = px.bar(dff_z_3, x='sale_dollars', y='item_description',orientation='h')
        fig_3.update_traces(marker_color='rgba(50, 171, 96, 0.6)',
                        marker_line_color='rgba(50, 171, 96, 1.0)',
                        marker_line_width=0.5)
        fig_3.update_layout(template=template_from_url(theme),
                        margin=dict(l=0, r=0, t=0, b=0),
                        yaxis_title=None,
                        xaxis_title=None)

        #dff_z_4 = dff_z.pivot_table(values='sale_dollars',
                                    #index=['date', 'store_name'],
                                    #aggfunc=np.sum).reset_index()
        #fig_4 = px.line(dff_z_4,
                      #x='date',
                      #y='sale_dollars',
                      #color='store_name')
        # fig.update_traces(mode='lines+markers')  # line_shape='spline'
        #fig_4.update_layout(template=template_from_url(theme), margin=dict(l=0, r=0, t=0, b=0), yaxis_title=None,
                          #xaxis_title=None)
        #fig_4.update_yaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True)
        #fig_4.update_xaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True,
                         #rangeslider_visible=True)

        #dff_z_5 = dff_z.pivot_table(values='sale_dollars',
                                    #index=['date', 'category_name'],
                                    #aggfunc=np.sum).reset_index()
        #fig_5 = px.line(dff_z_5,
                      #x='date',
                      #y='sale_dollars',
                      #color='category_name')
        # fig.update_traces(mode='lines+markers')  # line_shape='spline'
        #fig_5.update_layout(template=template_from_url(theme), margin=dict(l=0, r=0, t=0, b=0), yaxis_title=None,
                          #xaxis_title=None)
        #fig_5.update_yaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True)
        #fig_5.update_xaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True,
                         #rangeslider_visible=True)

        #dff_z_6 = dff_z.pivot_table(values='sale_dollars',
                                    #index=['date', 'item_description'],
                                    #aggfunc=np.sum).reset_index()
        #fig_6 = px.line(dff_z_6,
                      #x='date',
                      #y='sale_dollars',
                      #color='item_description')
        # fig.update_traces(mode='lines+markers')  # line_shape='spline'
        #fig_6.update_layout(template=template_from_url(theme), margin=dict(l=0, r=0, t=0, b=0), yaxis_title=None,
                          #xaxis_title=None)
        #fig_6.update_yaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True)
        #fig_6.update_xaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True,
                         #rangeslider_visible=True)

        return html.Div(dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Span(f'1. Top sold store by each county'),
                                    dcc.Loading(children=[dcc.Graph(figure=fig,
                                                                    id='bar_1',
                                                                    style={'height': 350})],
                                                color='rgba(50, 171, 96, 0.6)', type='dot')
                                ], width={'size': 4}),
                                dbc.Col([
                                    html.Span(f'2. Top sold category by each county'),
                                    dcc.Loading(children=[dcc.Graph(figure=fig_2,
                                                                    id='bar_2',
                                                                    style={'height': 350})],
                                                color='rgba(50, 171, 96, 0.6)', type='dot')
                                ], width={'size': 4}),
                                dbc.Col([
                                    html.Span(f'3. Top sold items by each county'),
                                    dcc.Loading(children=[dcc.Graph(figure=fig_3,
                                                                    id='bar_3',
                                                                    style={'height': 350})],
                                                color='rgba(50, 171, 96, 0.6)', type='dot')
                                ], width={'size': 4})
                            ]),
                            #dbc.Row([
                                #dbc.Col([
                                    #dcc.Loading(children=[dcc.Graph(figure=fig_4, id='bar_4', style={'height': 350})],
                                                #color='rgba(50, 171, 96, 0.6)', type='dot')
                                #], width={'size': 12}),
                                #dbc.Col([
                                    #dcc.Loading(children=[dcc.Graph(figure=fig_5, id='bar_5', style={'height': 350})],
                                                #color='rgba(50, 171, 96, 0.6)', type='dot')
                                #], width={'size': 6}),
                                #dbc.Col([
                                    #dcc.Loading(children=[dcc.Graph(figure=fig_6, id='bar_6', style={'height': 350})],
                                                #color='rgba(50, 171, 96, 0.6)', type='dot')
                                #], width={'size': 4})
                            #])
                        ])
                    ])
                ], xs=12),
            ], className='p-2 align-items-center')
        )

@callback(Output('category','options'),
          [Input('my-date-picker-range_2','start_date'),
           Input('my-date-picker-range_2','end_date')])

def update_options(start_date_2,end_date_2):
    dff_2 = df[(df['date'] >= start_date_2) & (df['date'] <= end_date_2)]
    return [{'label':x,'value':x} for x in dff_2.sort_values('category_name')['category_name'].unique()]

@callback(Output('time_series_1','figure'),
              [Input('btn_2','n_clicks'),
               Input(ThemeChangerAIO.ids.radio("theme"), "value")],
              [State('category','value'),
               State('my-date-picker-range_2','start_date'),
               State('my-date-picker-range_2','end_date')])

def update_graph(n_clicks,theme,category,start_date_2,end_date_2):
    dff_3 = df[(df['date'] >= start_date_2) & (df['date'] <= end_date_2)]
    if category != [] :
        dff_3 = dff_3[dff_3['category_name'].isin(category)]
        dff_3_1 = dff_3.pivot_table(values='sale_dollars',
                                    index=['date','category_name'],
                                    aggfunc=np.sum).reset_index()
        fig = px.line(dff_3_1,
                      x='date',
                      y='sale_dollars',
                      color='category_name')
        #fig.update_traces(mode='lines+markers')  # line_shape='spline'
        fig.update_layout(hovermode='x unified',template=template_from_url(theme),margin=dict(l=0,r=0,t=0,b=0),
                          yaxis_title=None, xaxis_title=None)
        fig.update_yaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True,
                         spikemode='across',spikesnap='cursor')
        fig.update_xaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True,rangeslider_visible=True,
                         spikemode='across',spikesnap='cursor')
        return fig
    else:
        dff_3_1 = dff_3.pivot_table(values='sale_dollars',
                                    index=['date'],
                                    aggfunc=np.sum).reset_index()
        fig = px.line(dff_3_1,
                         x='date',
                         y='sale_dollars')
        #fig.update_traces(mode='lines+markers')  # line_shape='spline'
        fig.update_layout(hovermode='x unified',template=template_from_url(theme),margin=dict(l=0,r=0,t=0,b=0),yaxis_title=None, xaxis_title=None)
        fig.update_yaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True,
                         showspikes=True,spikemode='across',spikesnap='cursor')
        fig.update_xaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True,rangeslider_visible=True,showspikes=True,
                         spikemode='across',spikesnap='cursor')
        return fig