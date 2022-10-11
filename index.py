from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from apps import general, maps, items, store, about, table
from app import app, server

app.layout = html.Div(children=html.Div(
    [dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                align_end=True,
                children=[
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Analysis by Items", href='/page-2'),
                    dbc.DropdownMenuItem("Analysis by Stores", href='/page-3'),
                    dbc.DropdownMenuItem("Find Store", href='/page-4'),
                    dbc.DropdownMenuItem("Table", href='/page-5'),
                    dbc.DropdownMenuItem("About", href='/page-6')
                ],
        )
            ],
            brand="Iowa Liquor Sales Dashboard",
            color="primary",
            dark=True,
        ),
        dbc.Container(id="page-content", className="pt-4")
    ])
)

app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]

@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:  # if pathname in ["/", "/page-1"]:
        return general.layout
    elif pathname == "/page-2":
        return items.layout
    elif pathname == "/page-3":
        return store.layout
    elif pathname == "/page-4":
        return maps.layout
    elif pathname == "/page-5":
        return table.layout
    elif pathname == "/page-6":
        return about.layout
if __name__ == '__main__':
    app.run_server(debug=False,port='8053')