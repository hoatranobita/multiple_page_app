import dash_bootstrap_components as dbc
import dash
FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"
FA2 = "https://use.fontawesome.com/releases/v6.0.0/css/all.css"
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.LUX,FA,FA2,dbc_css],
                title='Iowa Sales Report'
                )
server = app.server
