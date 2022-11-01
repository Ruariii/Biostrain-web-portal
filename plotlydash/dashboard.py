import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def init_dashboard(server):

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"],
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ]
    )

    df = pd.read_csv('database.csv')
    df2 = df.sort_values('Timestamp')
    proList=list(df['Protocol'].unique())
    orgList=list(df['Org'].unique())
    tzList=['LHTZ', 'RHTZ', 'Both']
    legList=['Front leg', 'Back leg', 'Both']
    dataList=['Crush factor', 'Peak force', 'Force @ 0ms', 'Force @ 50ms', 'Force @ 100ms',
              'Force @ 150ms', 'Force @ 200ms', 'Force @ 250ms', 'Force @ 300ms']
    proList.append('Any')
    orgList.append('All')

    inputs = dbc.Row([

        # search_params
        html.Br(), html.Br(), html.Br(),
        dbc.Col([dbc.Label("Select Squad/Group", html_for="org-id"),
                dcc.Dropdown(orgList, value='All', id="org-id", style={"color": "black"})], className="d-grid gap-2 mx-auto"),


        dbc.Col([dbc.Label("Select Protocol", html_for="pro-id"),
                dcc.Dropdown(proList, value='Any', id="pro-id", style={"color": "black"})], className="d-grid gap-2 mx-auto")
    ])
    # search + clear buttons
    searchclear = dbc.Row([
        dbc.Col([dbc.Button("Update figures", id="search", color="secondary", size='md')],className="d-grid gap-2 mx-auto"),
        dbc.Col([dbc.Button("Reset", id='clear', color="light", size='md')],className="d-grid gap-2 mx-auto")
    ],
    )



    fig = px.scatter(df2, x=df2['Timestamp'], y=(df2["Right peak force"] + df2["Left peak force"]),
                     color=df2['User'], hover_data=['Org', 'Protocol', 'TZ'], symbol=df2['Org'])
    fig.update_layout(yaxis_title="Crush factor (kg)", yaxis_range=[0,300], xaxis_nticks=5,
                      title_text="Peak force crush factor - all users:", height=750)


    dash_app.layout = dbc.Form(
        children = [
            html.Br(),
            html.H3("Lucid Dashboard: Squad view", style={'textAlign':'center'}),
            html.Hr(),
            html.Br(),
            dbc.Card([dbc.CardBody([inputs,
            html.Br(),
            searchclear])], color='#f4f4f4'),
            dcc.Store(id='displayData'),
            html.Br(),
            dbc.Card([dbc.CardBody([dbc.Row([
                dbc.Col(md=2, children=[
                    html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
                    dbc.Card(
                        dbc.CardBody([dbc.Label("Select Transition Zone", html_for="tz-fig1"),
                        dcc.Dropdown(tzList, value='Both', id="tz-fig1", style={"color": "black"}),
                        html.Br(),
                        dbc.Label("Select Leg", html_for="leg-fig1"),
                        dcc.Dropdown(legList, value='Both', id="leg-fig1", style={"color": "black"}),
                        html.Br(),
                        dbc.Label("Select Data", html_for="data-fig1"),
                        dcc.Dropdown(dataList, value='Crush factor', id="data-fig1", style={"color": "black"})]),
                        color='light'
                        )
                ]),
                dbc.Col(md=10, children=[dcc.Graph(
                        id="main-scatter",
                        figure=fig)], className="d-grid gap-2 mx-auto")])])], color='#f4f4f4')

        ],
        id="dashboard-container", style={'width':'90%', 'x-align':'center'}, className="d-grid gap-2 mx-auto"
    )
    return dash_app.server

def init_callbacks(dash_app):

    df = pd.read_csv('database.csv')
    df2 = df.sort_values('Timestamp')

    @callback(
        Output('pro-id', 'options'),
        Input('org-id', 'value'))
    def set_pro_options(selected_org):
        proList = list(df['Protocol'].unique())
        proList.append('Any')
        if selected_org == 'All':
            pro_options = proList
        else:
            pro_options = []
            for i in range(len(df['Org'])):
                if df['Org'][i] == selected_org:
                    pro_options.append(df['Protocol'][i])
            pro_options=list(set(pro_options))
            pro_options.append('Any')
        return pro_options

    @callback(
        Output('leg-fig1', 'options'),
        Input('data-fig1', 'value')
    )
    def update_leg_1(dataVal):
        if dataVal == 'Crush factor':
            legOptions=['Both']
        else:
            legOptions=['Front leg', 'Back leg', 'Both']
        return legOptions


    @callback(
        Output('displayData', 'data'),
        Input('search', 'n_clicks'),
        State('org-id', 'value'),
        State('pro-id', 'value'))
    def create_df(n_click, org, pro):
        if n_click == None or (org == 'All' and pro == 'Any'):
            displayData=df
        else:
            if org == 'All':
                displayData = df.query(f"Protocol=='{pro}'")
            elif pro == 'Any':
                displayData=df.query(f"Org=='{org}'")
            else:
                displayData=df.query(f"Org=='{org}' & Protocol=='{pro}'")

        return displayData.to_json()

    @callback(
        Output('main-scatter', 'figure'),
        Input('search', 'n_clicks'),
        State('displayData', 'data')
    )
    def update_figs(n_click, data):

        filteredDf = pd.read_json(data)
        fig = px.scatter(filteredDf, x=filteredDf['Timestamp'], y=(filteredDf["Right peak force"] + filteredDf["Left peak force"]),
                          color=filteredDf['User'], hover_data=['Org', 'Protocol', 'TZ'], symbol=filteredDf['Org'])
        fig.update_layout(yaxis_title="Crush factor (kg)", yaxis_range=[0, 300], xaxis_nticks=5,
                           title_text="Peak force crush factor - all users:", height=750)

        return fig




    @callback(
        Output('org-id', 'value'),
        Output('pro-id', 'value'),
        Input('clear', 'n_clicks')
        )
    def clearInps(clear_click):
        return "All", "Any"

