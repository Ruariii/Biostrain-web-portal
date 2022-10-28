import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def init_dashboard(server):

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ]
    )
    df = pd.read_csv('database.csv')
    dash_app.layout = html.Div(
        children = [
            dcc.Graph(
                id="main-scatter",
                figure={
                    "data":[
                        {
                            "x":df["Timestamp"],
                            "y":(df["Right peak force"]+df["Left peak force"]),
                            "color":df["User"],
                            "name":"Crush factor",
                            "type":"scatter"
                        }
                    ],
                    "layout":{
                        "title":"Crush factor - all users",
                        "height": 500,
                        "padding": 100
                    }
                }
            )
        ],
        id="dashboard-container"
    )
    return dash_app.server
