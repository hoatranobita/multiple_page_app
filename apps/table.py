from dash import dash_table
from data_process import df
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from app import app

df_table = df[['invoice_and_item_number','date','store_name','address','county',
               'category_name','item_description','bottles_sold',
               'sale_dollars','volume_sold_liters','revenues','lat','lon','Season']]
layout = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H6('Date',className='text-left', style={'padding-top': 10})
                ], width={'size': 1, "offset": 0, 'order': 1}),
                dbc.Col([
                    dcc.DatePickerRange(
                        id='my-date-picker-range_6',  # ID to be used for callback
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
                    html.H6('Store', style={'text-align': 'left'})
                ], width={'size': 1, "offset": 0, 'order': 1}, style={'padding-top': 10}),
                dbc.Col([
                    dcc.Dropdown(id='stores_2',
                                 placeholder="Please select stores",
                                 options=[{'label':x,'value':x} for x in df_table.sort_values('store_name')['store_name'].unique()],
                                 value=[],
                                 multi=True,
                                 disabled=False,
                                 clearable=True,
                                 searchable=True)
                ], width={'size': 4, 'offset': 0, 'order': 1}),
                dbc.Col([
                    dbc.Button("Submit", id="btn_6", color="dark", className="ms-2", size='sm')
                ], width={'size': 1, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                dbc.Col([
                    dbc.Button("Download", id="btn_7", color="dark", className="ms-2", size='sm'),
                    dcc.Download(id='download_1')
                ], width={'size': 1, 'offset': 0, 'order': 1}, style={'text-align': 'right'})
            ], className='p-2 align-items-stretch'),
            dbc.Row([
                dbc.Col([
                    html.H6('Category', style={'text-align': 'left'})
                ], width={'size': 1, "offset": 0, 'order': 1}, style={'padding-top': 10}),
                dbc.Col([
                    dcc.Dropdown(id='category_2',
                                placeholder="Please select category",
                                options=[{'label':x,'value':x} for x in df_table.sort_values('category_name')['category_name'].unique()],
                                value=[],
                                multi=True,
                                disabled=False,
                                clearable=True,
                                searchable=True)
                ], width={'size': 5, "offset": 0, 'order': 1}),
                dbc.Col([
                    html.H6('Items', style={'text-align': 'left'})
                ], width={'size': 1, "offset": 0, 'order': 1}, style={'padding-top': 10}),
                dbc.Col([
                    dcc.Dropdown(id='items_2',
                                placeholder="Please select items",
                                options=[{'label':x,'value':x} for x in df_table.sort_values('item_description')['item_description'].unique()],
                                value=[],
                                multi=True,
                                disabled=False,
                                clearable=True,
                                searchable=True)
                ], width={'size': 5, "offset": 0, 'order': 1})
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H5('Data Table',className='text-center', style={'padding-top': 20}),
                    dash_table.DataTable(id='table',
                    columns=[{"name":i,"id":i} for i in df_table.columns],
                    data=[],
                    style_table={'overflow':'scroll','height':550},
                    style_header={'backgroundColor':'orange','padding':'10px','color':'#000000'},
                    style_cell={'textAlign':'center','font_size': '12px',
                                'whiteSpace':'normal','height':'auto'},
                    editable=True,              # allow editing of data inside all cells
                    filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                    sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                    sort_mode="single",         # sort across 'multi' or 'single' columns
                    column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                    row_selectable="multi",     # allow users to select 'multi' or 'single' rows
                    row_deletable=True,         # choose if user can delete a row (True) or not (False)
                    selected_columns=[],        # ids of columns that user selects
                    selected_rows=[],           # indices of rows that user selects
                    page_action="native")
                ])
            ]),
            dcc.Store(id='store_date',data=[],storage_type='memory')
        ])

@app.callback([Output('table','data'),
               Output('store_date','data')],
              [Input('btn_6','n_clicks')],
              [State('my-date-picker-range_6','start_date'),
               State('my-date-picker-range_6','end_date'),
               State('stores_2','value'),
               State('category_2','value'),
               State('items_2','value')])
def update_table(n_clicks,start_date_6,end_date_6,store,category,items):
    global df_table_2
    df_table_2 = df_table[(df_table['date'] >= start_date_6) & (df_table['date'] <= end_date_6)]
    if store != []:
        df_table_2 = df_table_2[df_table_2['store_name'].isin(store)]
    if category != []:
        df_table_2 = df_table_2[df_table_2['category_name'].isin(category)]
    if items != []:
        df_table_2 = df_table_2[df_table_2['item_description'].isin(items)]
    return df_table_2.to_dict(orient='records'),df_table_2.to_dict(orient='records')


@app.callback(Output('download_1','data'),
              [Input('btn_7','n_clicks')],
              [State('store_date','data')],
              prevent_initial_call=True)
def generate_excel(n_clicks,n):
    df_table_3 = df_table_2.copy()
    if n_clicks > 0:
        return dcc.send_data_frame(df_table_3.to_excel,filename='Data_table' + ".xlsx",index=False)