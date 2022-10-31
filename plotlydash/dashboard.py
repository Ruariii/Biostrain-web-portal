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
    proList=df['Protocol'].unique()

    inputs = dbc.Row([

        # search_params
        html.Br(), html.Br(), html.Br(),
        dbc.Col([dbc.Label("Select squad", html_for="org-id"),
                dcc.Dropdown(df['Org'].unique(), placeholder='Any', id="org-id", style={"color": "black"})]),


        dbc.Col([dbc.Label("Select Protocol", html_for="pro-id"),
                dcc.Dropdown(df['Protocol'].unique(), placeholder='Any', id="pro-id", style={"color": "black"})]),


        dbc.Col([dbc.Label("Select Transformational Zone", html_for="tz-id"),
                 dcc.Dropdown(['LHTZ', 'RHTZ', 'Both'],
                              placeholder='Both', id="tz-id", style={"color": "black"})]),

        dbc.Col([dbc.Label("Select Leg", html_for="leg-id"),
                 dcc.Dropdown(['Front leg', 'Back leg', 'Both'],
                              placeholder='Both', id="leg-id", style={"color": "black"})]),


        dbc.Col([dbc.Label("Select Data to View", html_for="data-id"),
                dcc.Dropdown(['Crush factor', 'Peak force', 'Force @ 0ms', 'Force @ 50ms', 'Force @ 100ms',
                      'Force @ 150ms', 'Force @ 200ms', 'Force @ 250ms', 'Force @ 300ms'],
                     placeholder='Crush factor', id="data-id", style={"color": "black"})]),
        html.Br(),
        html.Br()
    ])
    # search + clear buttons
    searchclear = dbc.Row([
        dbc.Col([dbc.Button("Update figures", id="search", color="secondary", size='md')],className="d-grid gap-2 mx-auto"),
        dbc.Col([dbc.Button("Clear", id='clear', color="light", size='md')],className="d-grid gap-2 mx-auto")
    ],
    )



    fig1 = px.scatter(df2, x=df2['Timestamp'], y=(df2["Right peak force"] + df2["Left peak force"]),
                     color=df2['User'], hover_data=['Org', 'Protocol', 'TZ'], symbol=df2['Org'])
    fig1.update_layout(yaxis_title="Crush factor (kg)", yaxis_range=[0,300], xaxis_nticks=5,
                      title_text="Peak force crush factor - all users:", height=750)


    dash_app.layout = dbc.Form(
        children = [
            html.H3("Lucid Dashboard: Squad view", style={'textAlign':'center'}),
            html.Br(),
            inputs,
            html.Br(),
            searchclear,
            html.Br(),
            dcc.Graph(
                id="main-scatter",
                figure=fig1
            ),

        ],
        id="dashboard-container", style={'width':'80%', 'x-align':'center'}, className="d-grid gap-2 mx-auto"
    )
    return dash_app.server

def init_callbacks(dash_app):

    df = pd.read_csv('database.csv')
    df2 = df.sort_values('Timestamp')

    @callback(
        Output('user-id', 'options'),
        Input('pro-id', 'value'))
    def set_pro_options(selected_org):
        if selected_org == 'Any':
            pro_options = df['Protocol'].unique()
        else:
            pro_options = []
            for i in range(len(df['Org'])):
                if df['Org'][i] == selected_org:
                    pro_options.append(df['Protocol'][i])
                    pro_options = list(np.unique(pro_options))
        return pro_options

    @callback(
        output=[Output('main-scatter', 'figure')],
        inputs=[Input('search', 'n_clicks')],
        state=[State("org-id", "value"), State("user-id", "value"),
               State("pro-id", "value"), State("tz-id", "value"),
               State("leg-id", "value"), State("data-id", "value")])
    def plotData(search_click, org_val, pro_val, tz_val, leg_val, data_val):
        if search_click == None:


            fig1 = px.scatter(df2, x=df2['Timestamp'], y=(df2["Right peak force"] + df2["Left peak force"]),
                              color=df2['User'], hover_data=['Org', 'Protocol', 'TZ'], symbol=df2['Org'])
            fig1.update_layout(yaxis_title="Crush factor (kg)", yaxis_range=[0, 300], xaxis_nticks=5,
                               title_text="Peak force crush factor - all users:", height=750)

            return fig1

        else:
            Lprefix, Rprefix = 'Left ', 'Right '
            FprefixL, BprefixL = 'LHTZ: Front leg ', 'LHTZ: Back leg '
            FprefixR, BprefixR = 'RHTZ: Front leg ', 'RHTZ: Back leg '
            if tz_val == 'Both':
                searchParams = {'Org': org_val, 'Protocol': pro_val}

            else:
                searchParams = {'Org': org_val, 'Protocol': pro_val, 'TZ': tz_val}
            index = []
            toDrop = []
            for i in range(len(df)):
                test = 0
                for param in searchParams:
                    if searchParams[param] == df[param][i]:
                        test += 1
                if test == len(searchParams):
                    index.append(i)
                else:
                    toDrop.append(i)

            displayData = df.drop(['Org', 'User', 'Protocol'], axis=1)
            displayData = displayData.drop(toDrop, axis=0)
            displayData = displayData.reset_index(drop=True)  # return displayData for table

            # split data into LHTZ/RHTZ
            Ltests, Rtests = [], []
            count = 0
            for tz in displayData['TZ']:
                if tz == 'LHTZ':
                    Rtests.append(count)
                else:
                    Ltests.append(count)
                count += 1

            lData = displayData.drop(Ltests, axis=0)
            rData = displayData.drop(Rtests, axis=0)

            # filter out front/back leg depending on leg_val
            plotDict = {}
            if leg_val == 'Front leg' and tz_val == 'LHTZ':
                for data in data_val:
                    plotDict[FprefixL + data.lower()] = lData[Lprefix + data.lower()]
            if leg_val == 'Back leg' and tz_val == 'LHTZ':
                for data in data_val:
                    plotDict[BprefixL + data.lower()] = lData[Rprefix + data.lower()]
            if leg_val == 'Both' and tz_val == 'LHTZ':
                for data in data_val:
                    plotDict[FprefixL + data.lower()] = lData[Lprefix + data.lower()]
                    plotDict[BprefixL + data.lower()] = lData[Rprefix + data.lower()]

            if leg_val == 'Front leg' and tz_val == 'RHTZ':
                for data in data_val:
                    plotDict[FprefixR + data.lower()] = rData[Rprefix + data.lower()]
            if leg_val == 'Back leg' and tz_val == 'RHTZ':
                for data in data_val:
                    plotDict[BprefixR + data.lower()] = rData[Lprefix + data.lower()]
            if leg_val == 'Both' and tz_val == 'RHTZ':
                for data in data_val:
                    plotDict[FprefixR + data.lower()] = rData[Rprefix + data.lower()]
                    plotDict[BprefixR + data.lower()] = rData[Lprefix + data.lower()]

            if leg_val == 'Front leg' and tz_val == 'Both':
                for data in data_val:
                    plotDict[FprefixL + data.lower()] = lData[Lprefix + data.lower()]
                    plotDict[FprefixR + data.lower()] = rData[Rprefix + data.lower()]
            if leg_val == 'Back leg' and tz_val == 'Both':
                for data in data_val:
                    plotDict[BprefixL + data.lower()] = lData[Rprefix + data.lower()]
                    plotDict[BprefixR + data.lower()] = rData[Lprefix + data.lower()]
            if leg_val == 'Both' and tz_val == 'Both':
                for data in data_val:
                    plotDict[FprefixL + data.lower()] = lData[Lprefix + data.lower()]
                    plotDict[BprefixL + data.lower()] = lData[Rprefix + data.lower()]
                    plotDict[FprefixR + data.lower()] = rData[Rprefix + data.lower()]
                    plotDict[BprefixR + data.lower()] = rData[Lprefix + data.lower()]

            xplot = displayData['Timestamp']

            ptitle = 'Data: '+str(displayData)+' Squad: '+str(org_val)+' Protocol: '+str(pro_val)

            fig = go.Figure()
            fig.update_layout(title_text=ptitle)

            for plot in plotDict:
                fig.add_trace(go.Scatter(
                    x=xplot,
                    y=plotDict[plot],
                    name=plot))

            return fig

    @callback(
        Output('org-id', 'value'),
        Output('pro-id', 'value'),
        Output('tz-id', 'value'),
        Output('leg-id', 'value'),
        Output('data-id', 'value'),
        Input('clear', 'n_clicks'))
    def clearInps(clear_click):
        return "Any", "Any", "Any","Any", "Crush Factor"

