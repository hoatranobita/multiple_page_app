import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors

counts_url = "https://www.dropbox.com/s/pivx6ktd4zfj4jn/counts.csv?dl=1"
metadata_url = "https://www.dropbox.com/s/k5x3x4gtw0h12d0/seurat_metadata.csv?dl=1"
seurat_counts = pd.read_table(counts_url,sep=',', header=(0))
seurat_metadata = pd.read_table(metadata_url,sep=',', header=(0))
clusters = seurat_metadata.seurat_clusters

seurat_metadata = seurat_metadata[['Unnamed: 0','seurat_clusters']]
seurat_metadata= seurat_metadata.set_index(['Unnamed: 0'])

cols = seurat_counts.columns
seurat_counts_f = seurat_counts
seurat_counts_f = seurat_counts_f[(seurat_counts > 5).any(axis=1)]

template = 'plotly_white'
seurat_counts1 = seurat_counts.T
seurat_counts2 = pd.merge(seurat_counts1,seurat_metadata,left_index=True,right_index=True,how='left')

from sklearn.decomposition import PCA
pca_all = PCA(n_components = 100).fit(seurat_counts1)
#prepare a scatterplot of genes based on PC1 and PC2
X_pca = pca_all.transform(seurat_counts1)
selected = seurat_counts.columns[1]

TSNEdf = pd.read_csv('https://raw.githubusercontent.com/hoatranobita/app_to_cloud_3/main/TSNEdf.csv')
TSNEdf['clusters'] = TSNEdf['clusters'].astype(str)
UMAPdf = pd.read_csv('https://raw.githubusercontent.com/hoatranobita/app_to_cloud_3/main/UMAPdf.csv')
UMAPdf['clusters'] = UMAPdf['clusters'].astype(str)

UMAPdf_2 = UMAPdf.copy()

cluster_annotation = pd.read_table("https://www.dropbox.com/s/uv1j0rtxze639t1/annotated_clusters.csv?dl=1", sep=',', index_col=1)
cluster_annotation = cluster_annotation.rename(columns={"cluster": "clusters"}, errors="raise")
cluster_annotation.clusters = cluster_annotation.clusters.astype('str')

selected_gene = list(seurat_counts1.columns)
sel_len = len(selected_gene)
#sel_len = int(sel_len)

for i in range(sel_len):
  UMAPdf_2[selected_gene[i]] = seurat_counts1[selected_gene[i]].values

annotate_df = pd.merge(UMAPdf_2, cluster_annotation, on='clusters')

TSNEdf_2 = TSNEdf.copy()
selected_gene = list(seurat_counts1.columns)
sel_len = len(selected_gene)
#sel_len = int(sel_len)

for i in range(sel_len):
  TSNEdf_2[selected_gene[i]] = seurat_counts1[selected_gene[i]].values

annotate_df_2 = pd.merge(TSNEdf_2, cluster_annotation, on='clusters')

ann1 = annotate_df[annotate_df['FTL'] > 10]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server
app.layout = html.Div([
    dbc.Tabs(
        [dbc.Tab(label="UMAP/tSNE", tab_id="umap"),
         dbc.Tab(label="Clustering", tab_id="clustering"),
         dbc.Tab(label="Gene Search", tab_id="gene_search"),
         dbc.Tab(label="Annotation", tab_id="annotation"),
         dbc.Tab(label="Table and Code", tab_id="table")],
        id="tabs",
        active_tab="umap",
    ),
    html.Div(id="tab-content", className="p-4"),
])


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")])
def render_tab_content(active_tab):
    if active_tab == "umap":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.RadioItems(
                        options=[
                            {"label": "UMAP", "value": 'UMAP'},
                            {"label": "tSNE", "value": 'tSNE'}],
                        value='UMAP',
                        id="radioitems-input_1",
                        inline=True
                    ),
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                # ,style={'padding-top' : 10}
                dbc.Col([
                    dbc.RadioItems(
                        options=[
                            {"label": "2D", "value": '2D'},
                            {"label": "3D", "value": '3D'}],
                        value='2D',
                        id="radioitems-input_2",
                        inline=True
                    ),
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                # ,style={'padding-top' : 10}
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('X_AXIS', style={'padding-top': 10, 'padding-right': 2})
                        ], width={'size': 4, "offset": 0, 'order': 1}),
                        dbc.Col([
                            dcc.Dropdown(id="x_axis",
                                         options=[],
                                         value=[],
                                         multi=False,
                                         disabled=False,
                                         clearable=False,
                                         searchable=True)
                        ], width={'size': 8, "offset": 0, 'order': 1}, style={'text-align': 'center'})
                    ])
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('Y_AXIS', style={'padding-top': 10, 'padding-right': 2})
                        ], width={'size': 4, "offset": 0, 'order': 1}),
                        dbc.Col([
                            dcc.Dropdown(id="y_axis",
                                         options=[],
                                         value=[],
                                         multi=False,
                                         disabled=False,
                                         clearable=False,
                                         searchable=True)
                        ], width={'size': 8, "offset": 0, 'order': 1}, style={'text-align': 'center'})
                    ])
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('Z_AXIS', style={'padding-top': 10, 'padding-right': 2})
                        ], width={'size': 4, "offset": 0, 'order': 1}),
                        dbc.Col([
                            dcc.Dropdown(id="z_axis",
                                         options=[],
                                         value=[],
                                         multi=False,
                                         disabled=False,
                                         clearable=False,
                                         searchable=True)
                        ], width={'size': 8, "offset": 0, 'order': 1}, style={'text-align': 'center'})
                    ])
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
            ], className='p-2 align-items-stretch'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_1', color="secondary"),
                                    dcc.Download(id='download_1'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_2', color="secondary"),
                                    dcc.Download(id='download_2'),
                                    dbc.Button("csv", size="sm", className="me-1", id='btn_3', color="secondary"),
                                    dcc.Download(id='download_3')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),

                            dbc.Row([
                                dbc.Col([
                                    html.Div(id='chart_title'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Loading(children=[
                                        dcc.Graph(id='scatter_chart', figure={}, style={'height': '450px'},
                                                  selectedData={'points': [{'hovertext': 'X24_CTGACACAATGC'}]})],
                                                color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=6),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button("SVG", size="sm", className="me-1", id='btn_4',
                                                       color="secondary"),
                                            dcc.Download(id='download_4'),
                                            dbc.Button("HTML", size="sm", className="me-1", id='btn_5',
                                                       color="secondary"),
                                            dcc.Download(id='download_5')
                                        ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Span(f"Sample Violin Plot for Samples",
                                                      style={'text-align': 'center'}),
                                            dcc.Loading(children=[
                                                dcc.Graph(id='violin_chart', figure={}, style={'height': '200px'})],
                                                        color='#119DFF', type='dot')
                                        ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                                    ]),
                                ])
                            ], className='h-100 text-left')
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button("SVG", size="sm", className="me-1", id='btn_6',
                                                       color="secondary"),
                                            dcc.Download(id='download_6'),
                                            dbc.Button("HTML", size="sm", className="me-1", id='btn_7',
                                                       color="secondary"),
                                            dcc.Download(id='download_7')
                                        ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div(id='chart_title_2'),
                                        ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.H6(f'Gene', style={'padding-top': 10, 'padding-right': 2}),
                                        ], width={'size': 3, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                                        dbc.Col([
                                            dcc.Dropdown(id="gene_2",
                                                         options=[{'label': i, 'value': i} for i in
                                                                  seurat_counts1.columns.unique()],
                                                         value=seurat_counts1.columns[1],
                                                         multi=False,
                                                         disabled=False,
                                                         clearable=False,
                                                         searchable=True)
                                        ], width={'size': 6, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                                    ]),

                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Loading(children=[
                                                dcc.Graph(id='violin_chart_2', figure={}, style={'height': '200px'})],
                                                        color='#119DFF', type='dot'),
                                        ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                                    ]),

                                ])
                            ], className='h-100 text-left')
                        ])
                    ])
                ], xs=6),
            ], className='p-2 align-items-stretch'),
        ])

    elif active_tab == "clustering":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('Cluster', style={'padding-top': 10, 'padding-right': 2}),
                            dcc.Input(type="number", id="num_of_cluster", value=4, min=0,
                                      style={'width': '100%', 'text-align': 'center'})
                        ], width={'size': 3, "offset": 0, 'order': 1},
                            style={'text-align': 'center', 'display': 'flex'}),  # ,style={'padding-top' : 10}
                        dbc.Col([
                            html.H6('ID Numbers', style={'padding-top': 10, 'padding-right': 2}),
                        ], width={'size': 3, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                        dbc.Col([
                            dcc.Input(type="number", id="num_of_id", value=0, min=0,
                                      style={'width': '40%', 'text-align': 'center'}),
                            dcc.Input(type="number", id="num_of_id_2", value=15, min=0,
                                      style={'width': '40%', 'text-align': 'center'})
                        ], width={'size': 3, "offset": 0, 'order': 1},
                            style={'text-align': 'center', 'display': 'flex'}),  # ,style={'padding-top' : 10}
                        dbc.Col([
                            dbc.Button("Submit", size="sm", className="me-1", id='submit', color="primary")
                        ], width={'size': 3, "offset": 0, 'order': 1}, style={'text-align': 'right'}),
                        # ,style={'padding-top' : 10}
                    ])
                ], width={'size': 6, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('GENE:', style={'padding-top': 10, 'padding-right': 2})
                        ], width={'size': 3, "offset": 0, 'order': 1}),
                        dbc.Col([
                            dcc.Dropdown(id="gene",
                                         options=[{'label': i, 'value': i} for i in seurat_counts1.columns.unique()],
                                         value=seurat_counts1.columns[1],
                                         multi=False,
                                         disabled=False,
                                         clearable=False,
                                         searchable=True)
                        ], width={'size': 9, "offset": 0, 'order': 1}, style={'text-align': 'center'})
                    ])
                ], width={'size': 6, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
            ], className='p-2 align-items-stretch'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_8', color="secondary"),
                                    dcc.Download(id='download_8'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_9', color="secondary"),
                                    dcc.Download(id='download_9'),
                                    dbc.Button("csv", size="sm", className="me-1", id='btn_10', color="secondary"),
                                    dcc.Download(id='download_10')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Span(f"Sample Violin Plot for Samples", style={'text-align': 'center'}),
                                    dcc.Loading(
                                        children=[dcc.Graph(id='violin_chart_3', figure={}, style={'height': '350px'})],
                                        color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_11', color="secondary"),
                                    dcc.Download(id='download_11'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_12', color="secondary"),
                                    dcc.Download(id='download_12')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id='chart_title_3'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Loading(
                                        children=[dcc.Graph(id='violin_chart_4', figure={}, style={'height': '350px'})],
                                        color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=6),
            ], className='p-2 align-items-stretch'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_13', color="secondary"),
                                    dcc.Download(id='download_13'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_14', color="secondary"),
                                    dcc.Download(id='download_14')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Span(f"Number of Cells in Each Cluster", style={'text-align': 'center'}),
                                    dcc.Loading(
                                        children=[dcc.Graph(id='bar_chart', figure={}, style={'height': '300px'})],
                                        color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=12),
            ], className='p-2 align-items-stretch'),

        ])

    elif active_tab == "gene_search":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('GENE:', style={'padding-top': 10, 'padding-right': 2})
                        ], width={'size': 3, "offset": 0, 'order': 1}),
                        dbc.Col([
                            dcc.Dropdown(id="selected_4",
                                         options=[{'label': i, 'value': i} for i in seurat_counts1.columns.unique()],
                                         value=seurat_counts1.columns[1],
                                         multi=False,
                                         disabled=False,
                                         clearable=False,
                                         searchable=True)
                        ], width={'size': 9, "offset": 0, 'order': 1}, style={'text-align': 'center'})
                    ])
                ], width={'size': 6, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                dbc.Col([
                    dbc.RadioItems(
                        options=[
                            {"label": "UMAP", "value": 'UMAP'},
                            {"label": "tSNE", "value": 'tSNE'}],
                        value='UMAP',
                        id="radioitems-input_3",
                        inline=True
                    ),
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                # ,style={'padding-top' : 10}
                dbc.Col([
                    dbc.RadioItems(
                        options=[
                            {"label": "2D", "value": '2D'},
                            {"label": "3D", "value": '3D'}],
                        value='2D',
                        id="radioitems-input_4",
                        inline=True
                    ),
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
            ], className='p-2 align-items-stretch'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_15', color="secondary"),
                                    dcc.Download(id='download_15'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_16', color="secondary"),
                                    dcc.Download(id='download_16')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id='chart_title_4'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Loading(
                                        children=[dcc.Graph(id='violin_chart_5', figure={}, style={'height': '400px'})],
                                        color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_17', color="secondary"),
                                    dcc.Download(id='download_17'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_18', color="secondary"),
                                    dcc.Download(id='download_18')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id='chart_title_5'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Loading(
                                        children=[dcc.Graph(id='violin_chart_6', figure={}, style={'height': '400px'})],
                                        color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=6),
            ], className='p-2 align-items-stretch'),

        ])

    elif active_tab == "annotation":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('GENE 1:', style={'padding-top': 10, 'padding-right': 2})
                        ], width={'size': 5, "offset": 0, 'order': 1}),
                        dbc.Col([
                            dcc.Dropdown(id="selected_gene_1",
                                         options=[{'label': i, 'value': i} for i in seurat_counts1.columns.unique()],
                                         value=seurat_counts1.columns[1],
                                         multi=False,
                                         disabled=False,
                                         clearable=False,
                                         searchable=True)
                        ], width={'size': 7, "offset": 0, 'order': 1}, style={'text-align': 'center'})
                    ])
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('GENE 2:', style={'padding-top': 10, 'padding-right': 2})
                        ], width={'size': 5, "offset": 0, 'order': 1}),
                        dbc.Col([
                            dcc.Dropdown(id="selected_gene_2",
                                         options=[{'label': i, 'value': i} for i in seurat_counts1.columns.unique()],
                                         value=seurat_counts1.columns[2],
                                         multi=False,
                                         disabled=False,
                                         clearable=False,
                                         searchable=True)
                        ], width={'size': 7, "offset": 0, 'order': 1}, style={'text-align': 'center'})
                    ])
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('GENE 3:', style={'padding-top': 10, 'padding-right': 2})
                        ], width={'size': 5, "offset": 0, 'order': 1}),
                        dbc.Col([
                            dcc.Dropdown(id="selected_gene_3",
                                         options=[{'label': i, 'value': i} for i in seurat_counts1.columns.unique()],
                                         value=seurat_counts1.columns[3],
                                         multi=False,
                                         disabled=False,
                                         clearable=False,
                                         searchable=True)
                        ], width={'size': 7, "offset": 0, 'order': 1}, style={'text-align': 'center'})
                    ])
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('GENE 4:', style={'padding-top': 10, 'padding-right': 2})
                        ], width={'size': 5, "offset": 0, 'order': 1}),
                        dbc.Col([
                            dcc.Dropdown(id="selected_gene_4",
                                         options=[{'label': i, 'value': i} for i in seurat_counts1.columns.unique()],
                                         value=seurat_counts1.columns[4],
                                         multi=False,
                                         disabled=False,
                                         clearable=False,
                                         searchable=True)
                        ], width={'size': 7, "offset": 0, 'order': 1}, style={'text-align': 'center'})
                    ])
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
            ], className='p-2 align-items-stretch'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_19', color="secondary"),
                                    dcc.Download(id='download_19'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_20', color="secondary"),
                                    dcc.Download(id='download_20')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Span(f"Ridgeline Plot for Selected Genes", style={'text-align': 'center'}),
                                    dcc.Loading(
                                        children=[dcc.Graph(id='violin_chart_7', figure={}, style={'height': '400px'})],
                                        color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_21', color="secondary"),
                                    dcc.Download(id='download_21'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_22', color="secondary"),
                                    dcc.Download(id='download_22')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Span(f"UMAP 3D", style={'text-align': 'center'}),
                                    dcc.Loading(
                                        children=[dcc.Graph(id='violin_chart_8', figure={}, style={'height': '400px'})],
                                        color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=6),
            ], className='p-2 align-items-stretch'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_23', color="secondary"),
                                    dcc.Download(id='download_23'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_24', color="secondary"),
                                    dcc.Download(id='download_24')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Span(f"Marker Gene Expression", style={'text-align': 'center'}),
                                    dcc.Loading(
                                        children=[dcc.Graph(id='violin_chart_9', figure={}, style={'height': '500px'})],
                                        color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("SVG", size="sm", className="me-1", id='btn_25', color="secondary"),
                                    dcc.Download(id='download_25'),
                                    dbc.Button("HTML", size="sm", className="me-1", id='btn_26', color="secondary"),
                                    dcc.Download(id='download_26')
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'right'}),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Span(f"Number of cells in Each Cell Type", style={'text-align': 'center'}),
                                    dcc.Loading(children=[
                                        dcc.Graph(id='violin_chart_10', figure={}, style={'height': '500px'})],
                                                color='#119DFF', type='dot'),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                        ])
                    ], className='h-100 text-left')
                ], xs=6),
            ], className='p-2 align-items-stretch'),

        ])
    elif active_tab == "table":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.RadioItems(
                        options=[
                            {"label": "UMAP", "value": 'UMAP'},
                            {"label": "tSNE", "value": 'tSNE'}],
                        value='UMAP',
                        id="radioitems-input_5",
                        inline=True
                    ),
                ], width={'size': 2, "offset": 0, 'order': 1}, style={'text-align': 'center'}),
                # ,style={'padding-top' : 10}
            ], className='p-2 align-items-stretch'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Span(f"Table", style={'text-align': 'center'}),
                                ], width={'size': 12, 'offset': 0, 'order': 1}, style={'text-align': 'center'}),
                            ]),
                            dbc.Row([
                                html.Div(
                                    id='tableDiv',
                                    className='tableDiv'),
                            ], className='p-2 align-items-stretch'),
                        ])
                    ], className='h-100 text-left')
                ], xs=12),
            ], className='p-2 align-items-stretch'),
        ])


@app.callback([Output('x_axis', 'options'),
               Output('x_axis', 'value'),
               Output('y_axis', 'options'),
               Output('y_axis', 'value'),
               Output('z_axis', 'options'),
               Output('z_axis', 'value')],
              [Input('radioitems-input_1', 'value')])
def update_axis(radioitems_input_1):
    if radioitems_input_1 == 'UMAP':
        value = [{'label': 'UMAP1', 'value': 'UMAP1'},
                 {'label': 'UMAP2', 'value': 'UMAP2'},
                 {'label': 'UMAP3', 'value': 'UMAP3'}]
        x = 'UMAP1'
        y = 'UMAP2'
        z = 'UMAP3'
        return value, x, value, y, value, z
    elif radioitems_input_1 == 'tSNE':
        value = [{'label': 'TSNE1', 'value': 'TSNE1'},
                 {'label': 'TSNE2', 'value': 'TSNE2'},
                 {'label': 'TSNE3', 'value': 'TSNE3'}]
        x = 'TSNE1'
        y = 'TSNE2'
        z = 'TSNE3'
        return value, x, value, y, value, z


@app.callback([Output('scatter_chart', 'figure'),
               Output('chart_title', 'children')],
              [Input('radioitems-input_1', 'value'),
               Input('radioitems-input_2', 'value'),
               Input('x_axis', 'value'),
               Input('y_axis', 'value'),
               Input('z_axis', 'value')
               ])
def update_scatter_chart(radioitems_input_1, radioitems_input_2, x_axis, y_axis, z_axis):
    if radioitems_input_1 == 'tSNE' and radioitems_input_2 == '2D':
        figTSNE = px.scatter(TSNEdf, x=TSNEdf[x_axis], y=TSNEdf[y_axis], color='clusters',
                             labels='Id',
                             hover_name='Id')
        figTSNE.update_layout(template=template,
                              margin=dict(l=0, r=0, t=0, b=0),
                              clickmode='event+select',
                              # dragmode='select',
                              hovermode='closest')
        # figTSNE.update_traces(marker_size = 3)
        return figTSNE, html.Span(f'2D TSNE', style={'text-align': 'center'})

    elif radioitems_input_1 == 'tSNE' and radioitems_input_2 == '3D':
        figTSNE3D = px.scatter_3d(TSNEdf, x=TSNEdf[x_axis], y=TSNEdf[y_axis], z=TSNEdf[z_axis],
                                  color='clusters',
                                  hover_name='Id')
        figTSNE3D.update_layout(template=template,
                                legend_traceorder="normal",
                                margin=dict(l=0, r=0, t=0, b=0),
                                clickmode='event+select',
                                # dragmode='select',
                                hovermode='closest')
        figTSNE3D.update_traces(marker_size=2)
        return figTSNE3D, html.Span(f'3D TSNE', style={'text-align': 'center'})

    elif radioitems_input_1 == 'UMAP' and radioitems_input_2 == '2D':
        figUMAP = px.scatter(UMAPdf, x=UMAPdf[x_axis], y=UMAPdf[y_axis], color='clusters',
                             labels='Id',
                             hover_name='Id')
        figUMAP.update_layout(template=template,
                              margin=dict(l=0, r=0, t=0, b=0),
                              clickmode='event+select',
                              # dragmode='select',
                              hovermode='closest')
        # figUMAP.update_traces(marker_size = 3)
        return figUMAP, html.Span(f'2D UMAP', style={'text-align': 'center'})

    elif radioitems_input_1 == 'UMAP' and radioitems_input_2 == '3D':
        figUMAP3D = px.scatter_3d(UMAPdf, x=UMAPdf[x_axis], y=UMAPdf[y_axis], z=UMAPdf[z_axis],
                                  color='clusters',
                                  hover_name='Id')
        figUMAP3D.update_layout(template=template,
                                legend_traceorder="normal",
                                margin=dict(l=0, r=0, t=0, b=0),
                                clickmode='event+select',
                                # dragmode='select',
                                hovermode='closest')
        figUMAP3D.update_traces(marker_size=2)
        return figUMAP3D, html.Span(f'3D UMAP', style={'text-align': 'center'})


@app.callback(Output('violin_chart', 'figure'),
              [Input('scatter_chart', 'selectedData')])
def update_violin_chart(selectedData):
    if selectedData != []:
        id_name = [p['hovertext'] for p in selectedData['points']]
        fig = px.violin(seurat_counts, y=id_name)
        fig.update_layout(template=template, margin=dict(l=0, r=0, t=0, b=0))

    if selectedData == []:
        fig = px.violin(seurat_counts, y='X24_CTGACACAATGC')
        fig.update_layout(template=template, margin=dict(l=0, r=0, t=0, b=0))
    return fig


@app.callback([Output('violin_chart_2', 'figure'),
               Output('chart_title_2', 'children')],
              [Input('gene_2', 'value')])
def update_violin_chart(gene):
    violin_chart_2 = px.violin(seurat_counts1,
                               y=gene,
                               x=UMAPdf.clusters,
                               color=UMAPdf.clusters)
    violin_chart_2.update_xaxes(categoryorder="total descending")
    violin_chart_2.update_layout(legend_traceorder="normal", template=template, margin=dict(l=0, r=0, t=0, b=0))
    return violin_chart_2, html.Span(f'Gene %s Expression Across Clusters' % gene)


@app.callback(Output('violin_chart_3', 'figure'),
              [Input('submit', 'n_clicks')],
              [State('num_of_cluster', 'value'),
               State('num_of_id', 'value'),
               State('num_of_id_2', 'value')])
def update_violin_chart(n_clicks, num_of_cluster, num_of_id, num_of_id_2):
    global seurat_counts3
    seurat_counts3 = seurat_counts2[seurat_counts2['seurat_clusters'] == num_of_cluster]
    seurat_counts3.drop(['seurat_clusters'], axis=1, inplace=True)
    seurat_counts3 = seurat_counts3.T
    selected_id = list(seurat_counts3.columns[num_of_id:num_of_id_2])  # .columns[1:50]

    violin_chart_3 = px.violin(seurat_counts, y=selected_id)
    violin_chart_3.update_layout(template=template, margin=dict(l=0, r=0, t=0, b=0))
    return violin_chart_3


@app.callback([Output('violin_chart_4', 'figure'),
               Output('chart_title_3', 'children')],
              [Input('gene', 'value')])
def update_violin_chart(gene):
    violin_chart_4 = px.violin(seurat_counts1,
                               y=gene,
                               x=UMAPdf.clusters,
                               color=UMAPdf.clusters)
    violin_chart_4.update_xaxes(categoryorder="total descending")
    violin_chart_4.update_layout(legend_traceorder="normal", template=template, margin=dict(l=0, r=0, t=0, b=0))
    return violin_chart_4, html.Span(f'Gene %s Expression Across Clusters' % gene)


@app.callback(Output('bar_chart', 'figure'),
              [Input('gene', 'value')])
def update_violin_chart(gene):
    Cell_count_clus = UMAPdf[['Id', 'clusters']].groupby(['clusters'], as_index=False).count()
    bar_chart = px.bar(Cell_count_clus, x='clusters', y='Id').update_xaxes(categoryorder="total descending")
    bar_chart.update_layout(template=template, margin=dict(l=0, r=0, t=0, b=0))
    return bar_chart


@app.callback([Output('violin_chart_5', 'figure'),
               Output('chart_title_4', 'children')],
              [Input('selected_4', 'value')])
def update_violin_chart(gene):
    ann1 = annotate_df[annotate_df[gene] > 10]
    fig = px.violin(ann1, y=gene, x='Cell Type',
                    color='Cell Type',
                    hover_name='Id')
    fig.update_layout(legend_traceorder="normal", template=template).update_xaxes(categoryorder="total descending")
    return fig, html.Span(f'%s Expression Across Cell Types' % gene)


@app.callback([Output('violin_chart_6', 'figure'),
               Output('chart_title_5', 'children')],
              [Input('selected_4', 'value'),
               Input('radioitems-input_3', 'value'),
               Input('radioitems-input_4', 'value')])
def update_violin_chart(gene, radioitems_input_3, radioitems_input_4):
    colorscales = ['tempo', 'PuBu']  # https://plotly.com/python/builtin-colorscales/
    if radioitems_input_3 == 'UMAP' and radioitems_input_4 == '2D':
        # x and y given as array_like objects
        figUMAP = px.scatter(annotate_df, x='UMAP1', y='UMAP2', color=annotate_df[gene],
                             labels='Id',
                             hover_name='Id',
                             color_continuous_scale=colorscales[1])
        figUMAP.update_layout(template=template, margin=dict(l=0, r=0, t=0, b=0))
        figUMAP.update_traces(marker_size=4)
        return figUMAP, html.Span('2D UMAP')

    elif radioitems_input_3 == 'UMAP' and radioitems_input_4 == '3D':
        # x and y given as array_like objects
        figUMAP = px.scatter_3d(annotate_df, x='UMAP1', y='UMAP2', z='UMAP3', color=annotate_df[gene],
                                labels='Id',
                                hover_name='Id',
                                color_continuous_scale=colorscales[1])
        figUMAP.update_layout(template=template, margin=dict(l=0, r=0, t=0, b=0))
        figUMAP.update_traces(marker_size=4)
        return figUMAP, html.Span('3D UMAP')

    elif radioitems_input_3 == 'tSNE' and radioitems_input_4 == '2D':
        # x and y given as array_like objects
        figUMAP = px.scatter(annotate_df_2, x='TSNE1', y='TSNE2', color=annotate_df_2[gene],
                             labels='Id',
                             hover_name='Id',
                             color_continuous_scale=colorscales[1])
        figUMAP.update_layout(template=template, margin=dict(l=0, r=0, t=0, b=0))
        figUMAP.update_traces(marker_size=4)
        return figUMAP, html.Span('2D TSNE')

    elif radioitems_input_3 == 'tSNE' and radioitems_input_4 == '3D':
        # x and y given as array_like objects
        figUMAP = px.scatter_3d(annotate_df_2, x='TSNE1', y='TSNE2', z='TSNE3', color=annotate_df_2[gene],
                                labels='Id',
                                hover_name='Id',
                                color_continuous_scale=colorscales[1])
        figUMAP.update_layout(template=template, margin=dict(l=0, r=0, t=0, b=0))
        figUMAP.update_traces(marker_size=4)
        return figUMAP, html.Span('3D TSNE')


@app.callback(Output('violin_chart_7', 'figure'),
              [Input('selected_gene_1', 'value'),
               Input('selected_gene_2', 'value'),
               Input('selected_gene_3', 'value'),
               Input('selected_gene_4', 'value')])
def update_violin_chart(selected_gene_1, selected_gene_2, selected_gene_3, selected_gene_4):
    selected_gene = [selected_gene_1, selected_gene_2, selected_gene_3, selected_gene_4]
    selected_gene.append('ANXA2')
    sel_len = len(selected_gene)
    sel_len = int(sel_len)

    for i in range(sel_len):
        UMAPdf_2[selected_gene[i]] = seurat_counts1[selected_gene[i]].values

    colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', sel_len, colortype='rgb')

    fig = go.Figure()
    for data_line, color, i in zip(UMAPdf_2, colors, selected_gene):
        fig.add_trace(go.Violin(x=UMAPdf_2[i], line_color=color, name=i))

    fig.update_traces(orientation='h', side='positive', width=2, points=False)
    fig.update_layout(xaxis_showgrid=True, xaxis_zeroline=False,
                      template=template)
    return fig


@app.callback(Output('violin_chart_8', 'figure'),
              [Input('selected_gene_1', 'value'),
               Input('selected_gene_2', 'value'),
               Input('selected_gene_3', 'value'),
               Input('selected_gene_4', 'value')])
def update_violin_chart(selected_gene_1, selected_gene_2, selected_gene_3, selected_gene_4):
    figUMAP3D = px.scatter_3d(annotate_df, x='UMAP1', y='UMAP2', z='UMAP3',
                              color='Cell Type',
                              hover_name='Id')
    figUMAP3D.update_layout(template=template, legend_traceorder="normal", margin=dict(l=0, r=0, t=0, b=0))
    figUMAP3D.update_traces(marker_size=2)
    return figUMAP3D


@app.callback(Output('violin_chart_9', 'figure'),
              [Input('selected_gene_1', 'value'),
               Input('selected_gene_2', 'value'),
               Input('selected_gene_3', 'value'),
               Input('selected_gene_4', 'value')])
def update_violin_chart(selected_gene_1, selected_gene_2, selected_gene_3, selected_gene_4):
    colorscales = ['tempo', 'PuBu']  # https://plotly.com/python/builtin-colorscales/
    fig = make_subplots(rows=2, cols=2,
                        vertical_spacing=0.1)

    fig.add_trace(go.Scatter(x=annotate_df.UMAP1, y=annotate_df.UMAP2, mode='markers',
                             name=selected_gene_1,
                             hovertext=annotate_df[selected_gene_1],
                             marker=dict(
                                 size=3,
                                 color=annotate_df[selected_gene_1],
                                 colorscale=colorscales[1],
                                 showscale=True, colorbar=dict(len=0.4, x=-0.15, y=0.8))
                             ), row=1, col=1)

    fig.add_trace(go.Scatter(x=annotate_df.UMAP1, y=annotate_df.UMAP2, mode='markers',
                             name=selected_gene_2,
                             hovertext=annotate_df[selected_gene_2],
                             marker=dict(
                                 size=3,
                                 color=annotate_df[selected_gene_2],
                                 colorscale=colorscales[1],
                                 showscale=True, colorbar=dict(len=0.4, x=1, y=0.8))
                             ), row=1, col=2)
    fig.add_trace(go.Scatter(x=annotate_df.UMAP1, y=annotate_df.UMAP2, mode='markers',
                             name=selected_gene_3,
                             hovertext=annotate_df[selected_gene_3],
                             marker=dict(
                                 size=3,
                                 color=annotate_df[selected_gene_3],
                                 colorscale=colorscales[1],
                                 showscale=True, colorbar=dict(len=0.4, x=-0.15, y=0.2))
                             ), row=2, col=1)
    fig.add_trace(go.Scatter(x=annotate_df.UMAP1, y=annotate_df.UMAP2, mode='markers',
                             name=selected_gene_4,
                             hovertext=annotate_df[selected_gene_4],
                             marker=dict(
                                 size=3,
                                 color=annotate_df[selected_gene_4],
                                 colorscale=colorscales[1],
                                 showscale=True, colorbar=dict(len=0.4, x=1, y=0.2))
                             ), row=2, col=2)
    fig.update_layout(template=template, showlegend=False)
    return fig


@app.callback(Output('violin_chart_10', 'figure'),
              [Input('selected_gene_1', 'value'),
               Input('selected_gene_2', 'value'),
               Input('selected_gene_3', 'value'),
               Input('selected_gene_4', 'value')])
def update_violin_chart(selected_gene_1, selected_gene_2, selected_gene_3, selected_gene_4):
    df1 = annotate_df[['Id', 'Cell Type']].groupby(['Cell Type'], as_index=False).count()

    fig = px.bar(df1, x='Cell Type', y='Id', color='Cell Type')
    return fig


@app.callback(Output('tableDiv', 'children'),
              [Input('radioitems-input_5', 'value')])
def update_data_2(radioitems_input_5):
    if radioitems_input_5 == 'UMAP':
        UMAPdf_3 = UMAPdf.copy()
        try:
            selected_gene = cluster_annotation.index
            sel_len = len(selected_gene)
            for i in range(sel_len):
                UMAPdf_3[selected_gene[i]] = seurat_counts1[selected_gene[i]].values
        except KeyError:  # IndexError as an example
            pass
        UMAPdf_3.clusters = UMAPdf_3.clusters.astype('str')
        annotate_df_3 = pd.merge(UMAPdf_3, cluster_annotation, on='clusters')
        mycolumns = [{'name': i, 'id': i} for i in annotate_df_3.columns]

        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=mycolumns,
                data=annotate_df_3.to_dict("rows"),
                style_table={'overflow': 'scroll', 'height': 550},
                style_header={'backgroundColor': 'orange', 'padding': '10px', 'color': '#000000'},
                style_cell={'textAlign': 'center',
                            'font_size': '12px',
                            'whiteSpace': 'normal',
                            'height': 'auto'},
                editable=True,  # allow editing of data inside all cells
                filter_action="native",  # allow filtering of data by user ('native') or not ('none')
                sort_action="native",  # enables data to be sorted per-column by user or not ('none')
                sort_mode="single",  # sort across 'multi' or 'single' columns
                column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                row_selectable="multi",  # allow users to select 'multi' or 'single' rows
                row_deletable=True,  # choose if user can delete a row (True) or not (False)
                selected_columns=[],  # ids of columns that user selects
                selected_rows=[],  # indices of rows that user selects
                page_action="native")
        ])

    elif radioitems_input_5 == 'tSNE':
        TSNEdf_3 = TSNEdf.copy()
        try:
            selected_gene = cluster_annotation.index
            sel_len = len(selected_gene)
            for i in range(sel_len):
                TSNEdf_3[selected_gene[i]] = seurat_counts1[selected_gene[i]].values
        except KeyError:  # IndexError as an example
            pass

        TSNEdf_3.clusters = TSNEdf_3.clusters.astype('str')
        annotate_df_3 = pd.merge(TSNEdf_3, cluster_annotation, on='clusters')
        mycolumns = [{'name': i, 'id': i} for i in annotate_df_3.columns]

        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=mycolumns,
                data=annotate_df_3.to_dict("rows"),
                style_table={'overflow': 'scroll', 'height': 550},
                style_header={'backgroundColor': 'orange', 'padding': '10px', 'color': '#000000'},
                style_cell={'textAlign': 'center',
                            'font_size': '12px',
                            'whiteSpace': 'normal',
                            'height': 'auto'},
                editable=True,  # allow editing of data inside all cells
                filter_action="native",  # allow filtering of data by user ('native') or not ('none')
                sort_action="native",  # enables data to be sorted per-column by user or not ('none')
                sort_mode="single",  # sort across 'multi' or 'single' columns
                column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                row_selectable="multi",  # allow users to select 'multi' or 'single' rows
                row_deletable=True,  # choose if user can delete a row (True) or not (False)
                selected_columns=[],  # ids of columns that user selects
                selected_rows=[],  # indices of rows that user selects
                page_action="native")
        ])



if __name__ == '__main__':
    app.run_server(debug=False)