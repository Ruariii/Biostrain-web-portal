import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import PBI_python_module as pb


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
    dataList=['Peak force', 'Force @ 0ms', 'Force @ 50ms', 'Force @ 100ms',
              'Force @ 150ms', 'Force @ 200ms', 'Force @ 250ms', 'Force @ 300ms']
    proList.append('Any')
    orgList.append('All')

    inputs = dbc.Row([

        # search_params
        html.Br(), html.Br(), html.Br(),
        dbc.Col([dbc.Label("Select Squad/Group", html_for="org-id"),
                dcc.Dropdown(orgList, value='Lucid', id="org-id", style={"color": "black"})], className="d-grid gap-2 mx-auto"),


        dbc.Col([dbc.Label("Select Protocol", html_for="pro-id"),
                dcc.Dropdown(proList, value='Easy', id="pro-id", style={"color": "black"})], className="d-grid gap-2 mx-auto")
    ])
    # search + clear buttons
    searchclear = dbc.Row([
        dbc.Col([dbc.Button("Update figures", id="search", color="secondary", size='md')],className="d-grid gap-2 mx-auto"),
        dbc.Col([dbc.Button("Reset", id='clear', color="light", size='md')],className="d-grid gap-2 mx-auto")
    ],
    )

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
            dbc.Card([
                dbc.CardBody([
                    html.H5("Peak force overview:", className="card-title"),
                    dbc.Row([dbc.Col([dcc.Graph(
                        id="main-scatter",
                        )]),
                            dbc.Col([
                                dcc.Graph(
                                    id="main-bar",
                                )
                            ])])

                ])
            ], color = '#f4f4f4'),
            html.Br(),
            dbc.Card([
                dbc.CardBody([
                    html.H5("Force @ 150ms overview:", className="card-title"),
                    dbc.Row([dbc.Col([dcc.Graph(
                        id="rfd-scatter",
                    )]),
                        dbc.Col([
                            dcc.Graph(
                                id="rfd-bar",
                            )
                        ])])

                ])
            ], color='#f4f4f4')
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
        Output('main-scatter', 'figure'),
        Output('main-bar', 'figure'),
        Output('rfd-scatter', 'figure'),
        Output('rfd-bar', 'figure'),
        Input('search', 'n_clicks'),
        State('org-id', 'value'),
        State('pro-id', 'value'))
    def create_df(n_click, org, pro):
        if n_click == None or (org == 'All' and pro == 'Any'):
            displayData=df.reset_index()
        else:
            if org == 'All':
                orgFilteredData = df
            else:
                orgFilteredData = df.query(f"Org == '{org}'")
            if pro == 'Any':
                proFilteredData = orgFilteredData
            else:
                proFilteredData = orgFilteredData.query(f"Protocol == '{pro}'")

            displayData= proFilteredData.reset_index()

            sortDict = pb.create_dict(displayData)

            plotDict1temp = {}
            plotDict2temp=  {}
            for user in sortDict:
                for protocol in sortDict[user]:
                    for tz in sortDict[user][protocol]:
                        for leg in sortDict[user][protocol][tz]:
                            for data in sortDict[user][protocol][tz][leg]:
                                if 'peak force' in data:
                                    plotDict1temp[f"{user}, {tz}, {leg}, {data}"] = sortDict[user][protocol][tz][leg][data]
                                elif '@ 150' in data:
                                    plotDict2temp[f"{user}, {tz}, {leg}, {data}"] = sortDict[user][protocol][tz][leg][data]
            plotDict1 = {k: v for k, v in plotDict1temp.items() if v}
            plotDict2 = {k: v for k, v in plotDict2temp.items() if v}

            keys1,keys2 = [],[]
            for key in plotDict1:
                keys1.append(key)
            for key in plotDict2:
                keys2.append(key)

            blAsymy = [0, 300]
            blAsymx = []
            for i in range(len(blAsymy)):
                blAsymx.append(blAsymy[i] * 1.3)



            fig1 = go.Figure()
            for user in plotDict1:
                name = ''.join(user.split(',')[0:3])
                fig1.add_trace(go.Bar(
                    name=''.join(user.split(',')[0:3]),
                    y=plotDict1[user],
                    hovertemplate=
                    f"<b> {name} </b><br><br>" +
                    "Peak force: %{y}kg<br>" +
                    "<extra></extra>"
                ))
            fig1.update_layout(yaxis_title="Peak force (kg)", xaxis_title="",
                              title_text=f"Data: Peak force, Squad: {org}, Protocol: {pro}", height=850)

            fig2 = go.Figure()
            xPlot, yPlot = {}, {}
            for user in plotDict1:
                if 'LHTZ, F' in user:
                    xPlot[user] = plotDict1[user]
                elif 'LHTZ, B' in user:
                    yPlot[user] = plotDict1[user]
                elif 'RHTZ, F' in user:
                    xPlot[user] = plotDict1[user]
                elif 'RHTZ, B' in user:
                    yPlot[user] = plotDict1[user]
            x = 0
            while x <= len(plotDict1) - 1:
                name = ''.join(keys1[x].split(',')[0:2])
                fig2.add_trace(go.Scatter(
                    x=xPlot[keys1[x]],
                    y=yPlot[keys1[x + 1]],
                    mode='markers',
                    name=keys1[x],
                    hovertemplate=
                    f"<b> {name} </b><br><br>" +
                    "Front leg peak force: %{x}kg<br>" +
                    "Back leg peak force: %{y}kg<br>" +
                    "<extra></extra>", )
                )
                x += 2
            fig2.add_trace(go.Scatter(
                x=blAsymx,
                y=blAsymy,
                name='30% asymmetry FL/BL',
                line={
                    'color': 'black',
                    'dash': 'dash'
                }))
            fig2.add_trace(go.Scatter(
                y=blAsymx,
                x=blAsymy,
                name='30% asymmetry BL/FL',
                line={
                    'color': 'black',
                    'dash': 'dash'
                }))
            fig2.update_layout(yaxis_title="Back leg peak force (kg)", xaxis_title="Front leg peak force (kg)",
                               title_text=f"Data: Peak force, Squad: {org}, Protocol: {pro}", height=850,
                               yaxis_range=[-5,120], xaxis_range=[-5,120])

            fig3 = go.Figure()
            for user in plotDict2:
                name = ''.join(user.split(',')[0:3])
                fig3.add_trace(go.Bar(
                    name=''.join(user.split(',')[0:3]),
                    y=plotDict2[user],
                    hovertemplate=
                    f"<b> {name} </b><br><br>" +
                    "Force @ 150ms: %{y}kg<br>" +
                    "<extra></extra>"
                ))
            fig3.update_layout(yaxis_title="Force @ 150ms (kg)", xaxis_title="",
                               title_text=f"Data: Peak force, Squad: {org}, Protocol: {pro}", height=850)

            fig4 = go.Figure()
            xPlot, yPlot = {}, {}
            for user in plotDict2:
                if 'LHTZ, F' in user:
                    xPlot[user] = plotDict2[user]
                elif 'LHTZ, B' in user:
                    yPlot[user] = plotDict2[user]
                elif 'RHTZ, F' in user:
                    xPlot[user] = plotDict2[user]
                elif 'RHTZ, B' in user:
                    yPlot[user] = plotDict2[user]
            x = 0
            while x <= len(plotDict2) - 1:
                name = ''.join(keys2[x].split(',')[0:2])
                fig4.add_trace(go.Scatter(
                    x=xPlot[keys2[x]],
                    y=yPlot[keys2[x + 1]],
                    mode='markers',
                    name=keys2[x],
                    hovertemplate=
                    f"<b> {name} </b><br><br>" +
                    "Front leg peak force: %{x}kg<br>" +
                    "Back leg peak force: %{y}kg<br>" +
                    "<extra></extra>", )
                )
                x += 2
            fig4.add_trace(go.Scatter(
                x=blAsymx,
                y=blAsymy,
                name='30% asymmetry FL/BL',
                line={
                    'color': 'black',
                    'dash': 'dash'
                }))
            fig4.add_trace(go.Scatter(
                y=blAsymx,
                x=blAsymy,
                name='30% asymmetry BL/FL',
                line={
                    'color': 'black',
                    'dash': 'dash'
                }))
            fig4.update_layout(yaxis_title="Back leg peak force (kg)", xaxis_title="Front leg peak force (kg)",
                               title_text=f"Data: Peak force, Squad: {org}, Protocol: {pro}", height=850,
                               yaxis_range=[-5,120], xaxis_range=[-5,120])

        return fig2, fig1, fig4, fig3




    @callback(
        Output('org-id', 'value'),
        Output('pro-id', 'value'),
        Input('clear', 'n_clicks')
        )
    def clearInps(clear_click):
        if clear_click > 0:

            return "All", "Any"