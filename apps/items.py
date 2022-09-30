from dash import dcc
from dash import html
import numpy as np
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from app import app
from data_process import df

# Data for first graph
df3_1 = df.pivot_table(values='sale_dollars',
                     index=['Season','item_description'],
                     aggfunc=np.sum).reset_index()
df3_1 = df3_1.sort_values(['Season', 'sale_dollars'], ascending=[True, False]).groupby('Season').head(10)
autumn_1 = df3_1['sale_dollars'].iloc[0]
autumn_1 = f'{autumn_1:,.2f}'
spring_1 = df3_1['sale_dollars'].iloc[10]
spring_1 = f'{spring_1:,.2f}'
summer_1 = df3_1['sale_dollars'].iloc[20]
summer_1 = f'{summer_1:,.2f}'
winter_1 = df3_1['sale_dollars'].iloc[30]
winter_1 = f'{winter_1:,.2f}'

autumn_2_1 = df3_1['item_description'].iloc[0]
spring_2_1 = df3_1['item_description'].iloc[10]
summer_2_1 = df3_1['item_description'].iloc[20]
winter_2_1 = df3_1['item_description'].iloc[30]

fig_1_1 = go.Figure(data=[
        go.Bar(name='Type', x=[tuple(df3_1['Season']), tuple(df3_1['item_description'])],
               y=list(df3_1['sale_dollars'])),
    ])
fig_1_1.update_traces(marker_color='lightseagreen')
fig_1_1.update_layout(template='plotly_white',margin=dict(l=0,r=0,t=0,b=0))

layout = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H4("Analysys by items")
                ], width={'size': 12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H5("I. Seasonal Analysis")
                ], width={'size':12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    dcc.Markdown("""In Iowa, Spring usually lasts from March to May, Summer from June to September, Autumn from October to December, Winter from January to March.""")
                ], width={'size': 12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Top 10 Wines items sales each season'),
                            dcc.Graph(figure=fig_1_1),
                        ])
                    ])
                ],xs=12,style={'text-align':'center'}),
            ],className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.Span(f'- The most sold wines items in Spring is {spring_2_1} with amount {spring_1}',
                            style={"white-space": "pre-line"}),
                ], width={'size': 12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.Span(f'- The most sold wines items in Summer is {summer_2_1} with amount {summer_1}',
                            style={"white-space": "pre-line"}),
                ], width={'size': 12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.Span(f'- The most sold wines items in Autumn is {autumn_2_1} with amount {autumn_1}',
                            style={"white-space": "pre-line"}),
                ], width={'size': 12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.Span(f'- The most sold wines items in Winter is {winter_2_1} with amount {winter_1}',
                            style={"white-space": "pre-line"}),
                ], width={'size': 12}),
            ], className='p-2 align-items-stretch'),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H6('Date Picker',className='text-center'),
                ],width={'size':2,"offset":0,'order':1},style={'padding-top':10}),
                dbc.Col([
                    dcc.DatePickerRange(
                        id='my-date-picker-range_3',  # ID to be used for callback
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
                    dbc.Button("Submit",id="btn_3",color="dark",className="ms-2",size='sm')
                ],width={'size':2,'offset':4,'order':1},style={'text-align':'right'})
            ],className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H5("II. Top 10 sold wines items by elements")
                ], width={'size': 12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H6("1. Top 10 sold wines items by sales amount")
                ], width={'size': 6}),
                dbc.Col([
                    html.H6("2. Top 10 sold wines items by bottles amount")
                ], width={'size': 6}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.Div(id='top10_items_1')
                ], width={'size': 6}),
                dbc.Col([
                    html.Div(id='top10_items_2')
                ], width={'size': 6}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='top10_1_1',style={'height':350})],color='rgba(50, 171, 96, 0.6)',type='dot')
                        ])
                    ])
                ],xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='top10_2_1',style={'height':350})],color='rgba(50, 171, 96, 0.6)',type='dot')
                            ])
                        ])
                ],xs=6)
            ],className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H6("3. Top 10 sold wines items by liters amount")
                ], width={'size': 6}),
                dbc.Col([
                    html.H6("4. Top 10 sold wines items by revenues amount")
                ], width={'size': 6}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.Div(id='top10_items_3')
                ], width={'size': 6}),
                dbc.Col([
                    html.Div(id='top10_items_4')
                ], width={'size': 6}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='top10_3_1',style={'height':350})],color='rgba(50, 171, 96, 0.6)',type='dot')
                            ])
                        ])
                    ], xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(children=[dcc.Graph(figure={},id='top10_4_1',style={'height':350})],color='rgba(50, 171, 96, 0.6)',type='dot')
                            ])
                        ])
                    ], xs=6)
                ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H5("III. Time Series")
                ], width={'size': 12}),
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H6('Date', className='text-left'),
                ], width={'size': 1, "offset": 0, 'order': 1}, style={'padding-top': 10}),
                dbc.Col([
                    dcc.DatePickerRange(
                        id='my-date-picker-range_4',  # ID to be used for callback
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
                    html.H6('Items', style={'text-align': 'left'})
                    ], width={'size': 1, "offset": 0, 'order': 1}, style={'padding-top': 10}),
                dbc.Col([
                    dcc.Dropdown(id='items',
                                placeholder="Please select category",
                                options=[],
                                value=[],
                                multi=True,
                                disabled=False,
                                clearable=True,
                                searchable=True)
                ], width={'size': 5, 'offset': 0, 'order': 1}),
                dbc.Col([
                    dbc.Button("Submit", id="btn_4", color="dark", className="ms-2", size='sm')
                ], width={'size': 1, 'offset': 0, 'order': 1}, style={'text-align': 'right'})
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='time_series_2', figure={}, style={'height': 350}),
                        ])
                    ])
                ], xs=12, style={'text-align': 'center'}),
            ], className='p-2 align-items-stretch'),
        ])

@app.callback([Output('top10_1_1', 'figure'),
               Output('top10_2_1', 'figure'),
               Output('top10_3_1', 'figure'),
               Output('top10_4_1', 'figure'),
               Output('top10_items_1', 'children'),
               Output('top10_items_2', 'children'),
               Output('top10_items_3', 'children'),
               Output('top10_items_4', 'children')],
              [Input('btn_3','n_clicks')],
             [State('my-date-picker-range_3', 'start_date'),
              State('my-date-picker-range_3', 'end_date')])
def update_graph(n_clicks_1,start_date_3,end_date_3):
    dff_1 = df[(df['date'] >= start_date_3) & (df['date'] <= end_date_3)]
    df4_1 = dff_1.pivot_table(values='sale_dollars',
                         index=['item_description'],
                         aggfunc=np.sum).reset_index()

    df4_1 = df4_1.sort_values(['sale_dollars'], ascending=[False]).head(10)
    df4_1 = df4_1.sort_values(['sale_dollars'], ascending=[True])
    top10_items_1_1 = df4_1['item_description'].iloc[9]
    top10_items_1_2 = df4_1['sale_dollars'].iloc[9]
    top10_items_1_2= f'{top10_items_1_2:,.2f}'
    top10_items_1_3 = df4_1['sale_dollars'].iloc[9]
    fig_2_1 = px.bar(df4_1, x='sale_dollars', y='item_description', orientation='h', text='sale_dollars')
    fig_2_1.update_traces(marker_color='rgba(50, 171, 96, 0.6)', marker_line_color='rgba(50, 171, 96, 1.0)',
                      marker_line_width=1,texttemplate='%{text:,.2f}', textposition='outside')
    fig_2_1.update_layout(template='plotly_white', margin=dict(l=0, r=0, t=0, b=0))
    fig_2_1.update_layout({'xaxis': {'range': [0, top10_items_1_3 * 1.4]}})

    df5_1 = dff_1.pivot_table(values='bottles_sold',
                              index=['item_description'],
                              aggfunc=np.sum).reset_index()

    df5_1 = df5_1.sort_values(['bottles_sold'],ascending=[False]).head(10)
    df5_1 = df5_1.sort_values(['bottles_sold'], ascending=[True])
    top10_items_2_1 = df5_1['item_description'].iloc[9]
    top10_items_2_2 = df5_1['bottles_sold'].iloc[9]
    top10_items_2_2 = f'{top10_items_2_2:,.2f}'
    top10_items_2_3 = df5_1['bottles_sold'].iloc[9]

    fig_3_1 = px.bar(df5_1, x='bottles_sold', y='item_description', orientation='h', text='bottles_sold')
    fig_3_1.update_traces(marker_color='rgba(50, 171, 96, 0.6)', marker_line_color='rgba(50, 171, 96, 1.0)',
                      marker_line_width=1,texttemplate='%{text:,.2f}', textposition='outside')
    fig_3_1.update_layout(template='plotly_white', margin=dict(l=0, r=0, t=0, b=0))
    fig_3_1.update_layout({'xaxis': {'range': [0, top10_items_2_3 * 1.4]}})

    df6_1 = dff_1.pivot_table(values='volume_sold_liters',
                         index=['item_description'],
                         aggfunc=np.sum).reset_index()

    df6_1 = df6_1.sort_values(['volume_sold_liters'], ascending=[False]).head(10)
    df6_1 = df6_1.sort_values(['volume_sold_liters'], ascending=[True])
    top10_items_3_1 = df6_1['item_description'].iloc[9]
    top10_items_3_2 = df6_1['volume_sold_liters'].iloc[9]
    top10_items_3_2 = f'{top10_items_3_2:,.2f}'
    top10_items_3_3 = df6_1['volume_sold_liters'].iloc[9]

    fig_4_1 = px.bar(df6_1, x='volume_sold_liters', y='item_description', orientation='h', text='volume_sold_liters')
    fig_4_1.update_traces(marker_color='rgba(50, 171, 96, 0.6)', marker_line_color='rgba(50, 171, 96, 1.0)',
                      marker_line_width=1,texttemplate='%{text:,.2f}', textposition='outside')
    fig_4_1.update_layout(template='plotly_white', margin=dict(l=0, r=0, t=0, b=0))
    fig_4_1.update_layout({'xaxis': {'range': [0, top10_items_3_3 * 1.4]}})

    df7_1 = dff_1.pivot_table(values='revenues',
                         index=['item_description'],
                         aggfunc=np.sum).reset_index()

    df7_1 = df7_1.sort_values(['revenues'], ascending=[False]).head(10)
    df7_1 = df7_1.sort_values(['revenues'], ascending=[True])
    top10_items_4_1 = df7_1['item_description'].iloc[9]
    top10_items_4_2 = df7_1['revenues'].iloc[9]
    top10_items_4_2 = f'{top10_items_4_2:,.2f}'
    top10_items_4_3 = df7_1['revenues'].iloc[9]

    fig_5_1 = px.bar(df7_1, x='revenues', y='item_description', orientation='h', text='revenues')
    fig_5_1.update_traces(marker_color='rgba(50, 171, 96, 0.6)', marker_line_color='rgba(50, 171, 96, 1.0)',
                      marker_line_width=1,texttemplate='%{text:,.2f}', textposition='outside')
    fig_5_1.update_layout(template='plotly_white', margin=dict(l=0, r=0, t=0, b=0))
    fig_5_1.update_layout({'xaxis': {'range': [0, top10_items_4_3 * 1.4]}})
    return fig_2_1,\
           fig_3_1,\
           fig_4_1,\
           fig_5_1,\
           html.Span(f'The most sold wines items by sales amount from {start_date_3} to {end_date_3} is {top10_items_1_1} with amount {top10_items_1_2}'), \
           html.Span(f'The most sold wines items by bottles amount from {start_date_3} to {end_date_3} is {top10_items_2_1} with amount {top10_items_2_2}'), \
           html.Span(f'The most sold wines items by liters amount from {start_date_3} to {end_date_3} is {top10_items_3_1} with amount {top10_items_3_2}'), \
           html.Span(f'The most sold wines items by liters amount from {start_date_3} to {end_date_3} is {top10_items_4_1} with amount {top10_items_4_2}')

@app.callback(Output('items','options'),
              [Input('my-date-picker-range_4','start_date'),
               Input('my-date-picker-range_4','end_date')])

def update_options(start_date_4,end_date_4):
    global dff_7
    dff_7 = df[(df['date'] >= start_date_4) & (df['date'] <= end_date_4)]
    return [{'label':x,'value':x} for x in dff_7.sort_values('item_description')['item_description'].unique()]

@app.callback(Output('time_series_2','figure'),
              [Input('btn_4','n_clicks')],
              [State('items','value'),
               State('my-date-picker-range_4','start_date'),
               State('my-date-picker-range_4','end_date')])

def update_graph(n_clicks,items,start_date_4,end_date_4):
    dff_8 = df[(df['date'] >= start_date_4) & (df['date'] <= end_date_4)]
    if items != [] :
        dff_8 = dff_8[dff_8['item_description'].isin(items)]
        dff_8_1 = dff_8.pivot_table(values='sale_dollars',
                                    index=['date','item_description'],
                                    aggfunc=np.sum).reset_index()
        fig = px.line(dff_8_1,
                      x='date',
                      y='sale_dollars',
                      color='item_description')
        #fig.update_traces(mode='lines+markers')  # line_shape='spline'
        fig.update_layout(template='plotly_white',margin=dict(l=0,r=0,t=0,b=0),yaxis_title=None, xaxis_title=None)
        fig.update_yaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True)
        fig.update_xaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True,rangeslider_visible=True)
        return fig
    else:
        dff_8_1 = dff_8.pivot_table(values='sale_dollars',
                                    index=['date'],
                                    aggfunc=np.sum).reset_index()
        fig = px.line(dff_8_1,
                         x='date',
                         y='sale_dollars')
        #fig.update_traces(mode='lines+markers')  # line_shape='spline'
        fig.update_layout(template='plotly_white',margin=dict(l=0,r=0,t=0,b=0),yaxis_title=None, xaxis_title=None)
        fig.update_yaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True)
        fig.update_xaxes(showline=True, showgrid=True, exponentformat="none", separatethousands=True,rangeslider_visible=True)
        return fig