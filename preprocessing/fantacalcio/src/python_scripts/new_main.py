from pathlib import Path
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd


# Dash and CSS Definition
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Retreive df
parent_folder = Path.cwd().parent
season = 2019
data_url = "data/stats" + str(season) + ".csv"
filename = parent_folder / data_url
original_df = pd.read_csv(filename)
team_df = original_df.sort_values(by=["Squadra"], ascending=True)

# Important global variables
roles = {"All": "Players",
         "P": "GoalKeepers",
         "D": "Defenders",
         "C": "Midfielders",
         "A": "Forwarders"}

color_by_role = {"P": "#A569BD",
                 "D": "#3498DB",
                 "C": "#16A085",
                 "A": "#E74C3C"}

numbers_of_players = [5, 10, 15, 20, 25]

stats_to_show = ["Media voto + Media Fantavoto",
                 "Goal fatti + Rigori segnati", "Ammonizioni + Espulsioni"]

app.layout = html.Div([

    html.H1(children='Welcome to FantaStats!'),

    html.H4(children='In this dashboard you can plot some interesting stats about last Serie A season.'),

    html.Br(),

    html.H6(children='''The following graph shows the statistics about the number of goals
                        scored or conceded, rispectevely for players or GoalKeepers.'''),

    html.Br(),

    html.Div([
        html.Div([
            html.Div([
                html.Div(children='Filter by role:', className='four columns', style={
                         "textAlign": "right", "paddingTop": "5px"}),
                html.Div([
                    dcc.Dropdown(
                        clearable=False,
                        searchable=False,
                        id='players_role_goals',
                        options=[{'label': value, 'value': key}
                                 for key, value in roles.items()],
                        value='All'
                    )], className='eight columns')
            ], className='row'), ], className='five columns'),
        html.Div("", className='two columns'),
        html.Div([
            html.Div([
                html.Div(children='Show only top:', className='four columns', style={
                         "textAlign": "right", "paddingTop": "5px"}),
                html.Div([
                    dcc.Dropdown(
                        clearable=False,
                        searchable=False,
                        id='players_number_goals',
                        options=[{'label': str(i), 'value': i}
                                 for i in numbers_of_players],
                        value=20
                    )], className='eight columns')
            ], className='row'), ], className='five columns')
    ], className='row'),

    dcc.Graph(id='goals_graph'),

    html.Br(),
    html.Br(),
    html.Br(),

    html.H6(children='''The following graph shows the statistics about the grade
                        point average.'''),

    html.Br(),

    html.Div([
        html.Div([
            html.Div([
                html.Div(children='Filter by role:', className='four columns', style={
                         "textAlign": "right", "paddingTop": "5px"}),
                html.Div([
                    dcc.Dropdown(
                        clearable=False,
                        searchable=False,
                        id='players_role_mv',
                        options=[{'label': value, 'value': key}
                                 for key, value in roles.items()],
                        value='All'
                    )], className='eight columns')
            ], className='row'), ], className='five columns'),
        html.Div("", className='two columns'),
        html.Div([
            html.Div([
                html.Div(children='Show only top:', className='four columns', style={
                         "textAlign": "right", "paddingTop": "5px"}),
                html.Div([
                    dcc.Dropdown(
                        clearable=False,
                        searchable=False,
                        id='players_number_mv',
                        options=[{'label': str(i), 'value': i}
                                 for i in numbers_of_players],
                        value=20
                    )], className='eight columns')
            ], className='row'), ], className='five columns')
    ], className='row'),

    dcc.Graph(id='mv_graph'),

    html.Br(),
    html.Br(),
    html.Br(),

    html.H6(children='''The following graph shows the stats players filtered by their team.'''),

    html.Br(),

    html.Div([
        html.Div([
            html.Div([
                html.Div(children='Filter by team:', className='four columns', style={
                         "textAlign": "right", "paddingTop": "5px"}),
                html.Div([
                    dcc.Dropdown(
                        clearable=False,
                        id='team_value',
                        options=[{'label': team, 'value': team}
                                 for team in team_df["Squadra"].unique()],
                        value='Atalanta'
                    )], className='eight columns')
            ], className='row'), ], className='five columns'),
        html.Div("", className='two columns'),
        html.Div([
            html.Div([
                html.Div(children='Stats to show', className='four columns', style={
                         "textAlign": "right", "paddingTop": "5px"}),
                html.Div([
                    dcc.Dropdown(
                        clearable=False,
                        searchable=False,
                        id='stats_value',
                        options=[{'label': i, 'value': i}
                                 for i in stats_to_show],
                        value="Media voto + Media Fantavoto"
                    )], className='eight columns')
            ], className='row'), ], className='five columns')
    ], className='row'),

    dcc.Graph(id='team_graph'),

], className='container', style={'maxWidth': '100vw'})


@app.callback(
    Output('goals_graph', 'figure'),
    [Input('players_role_goals', 'value'),
     Input('players_number_goals', 'value')])
def update_goals_graph(players_role_goals, players_number_goals):

    if players_role_goals == "All":
        filtered = original_df
    else:
        filtered = original_df[original_df["Ruolo"] == players_role_goals]

    title = "<b>Top " + str(players_number_goals) + " " + \
        roles[players_role_goals] + " of season " + \
            str(season) + "-" + str(season + 1) + "</b>"

    # return different stats for GoalKeepers
    if players_role_goals == "P":
        filtered = filtered[filtered["Partite giocate"] > 5]
        # filtered = filtered[filtered["Goals subiti"] > 0]
        filtered = filtered.sort_values(by=["Goal subiti"], ascending=True)
        filtered = filtered.head(players_number_goals)
        y_title = "Goals conceded"
        fig = go.Figure(data=[
            go.Bar(name='Goal conceded', x=filtered["Nome"].head(players_number_goals),
                   y=filtered["Goal subiti"], marker_color='#F1C40F'),
            go.Bar(name='Penalty blocked', x=filtered["Nome"].head(players_number_goals),
                   y=filtered["Rigori parati"], marker_color='#03B157')
        ])
    else:
        filtered = filtered[filtered["Goals tot"] > 0]
        filtered = filtered.sort_values(by=["Goals tot"], ascending=False)
        filtered = filtered.head(players_number_goals)
        y_title = "Goals scored"
        fig = go.Figure(data=[
            go.Bar(name='Goal scored', x=filtered["Nome"],
                   y=filtered["Goal fatti"], marker_color='#0088E0'),
            go.Bar(name='Penalty scored', x=filtered["Nome"],
                   y=filtered["Rigori segnati"], marker_color='#03B157')
        ])

    fig.update_layout(barmode='stack', xaxis=dict(title_text="Name of players"),
                      yaxis=dict(title_text=y_title), title_text=title)

    return fig


@app.callback(
    Output('mv_graph', 'figure'),
    [Input('players_role_mv', 'value'),
     Input('players_number_mv', 'value')])
def update_mv_graph(players_role_mv, players_number_mv):

    if players_role_mv == "All":
        filtered = original_df
    else:
        filtered = original_df[original_df["Ruolo"] == players_role_mv]

    title = "<b>Top " + str(players_number_mv) + " " + \
        roles[players_role_mv] + " of season " + \
            str(season) + "-" + str(season + 1) + "</b>"

    filtered = filtered[filtered["Partite giocate"] > 5]
    filtered = filtered.sort_values(by=["Media Fantavoto"], ascending=False)
    filtered = filtered.head(players_number_mv)
    y_title = "Grade"
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(name='Average Fantagrade', x=filtered["Nome"],
                   y=filtered["Media Fantavoto"], marker_color='#0088E0', mode='lines+markers'))

    fig.add_trace(go.Bar(name='Average grade', x=filtered["Nome"],
                         y=filtered["Media voto"], marker_color='#E53935'))

    fig.update_layout(xaxis=dict(title_text="Name of players"),
                      yaxis=dict(title_text=y_title), title_text=title)

    return fig


@app.callback(
    Output('team_graph', 'figure'),
    [Input('team_value', 'value'),
     Input('stats_value', 'value')])
def update_team_graph(team_value, stats_value):

    filtered = original_df[original_df["Squadra"] == team_value]

    title = "<b>Players of " + team_value + " of season " + \
            str(season) + "-" + str(season + 1) + \
        " ordered by " + stats_value + "</b>"

    stats = stats_value.split(" + ")
    print(stats)
    filtered = filtered[filtered["Partite giocate"] > 3]
    filtered = filtered.sort_values(by=[stats[0]], ascending=False)
    filtered = filtered.head(25)

    colors = []

    for role in filtered["Ruolo"]:
        colors.append(color_by_role[role])

    fig = go.Figure()

    if (stats[0] == "Media voto"):
        fig.add_trace(go.Scatter(name='Average Fantagrade', x=filtered["Nome"],
                                 y=filtered[stats[1]], marker_color='#0088E0', mode='lines+markers'))
        fig.add_trace(go.Bar(name='Average grade', x=filtered["Nome"],
                             y=filtered[stats[0]], marker_color=colors)),
        y_title = "Grade"

    if (stats[0] == "Goal fatti"):
        fig.add_trace(go.Bar(name='Goal scored', x=filtered["Nome"],
                             y=filtered[stats[0]], marker_color='#0088E0'))
        fig.add_trace(go.Bar(name='Penalty scored', x=filtered["Nome"],
                             y=filtered[stats[1]], marker_color='#03B157'))
        y_title = "Goals scored"

    if (stats[0] == "Ammonizioni"):
        fig.add_trace(go.Bar(name='Yellow cards', x=filtered["Nome"],
                             y=filtered[stats[0]], marker_color='#F1C40F'))
        fig.add_trace(go.Bar(name='Red cards', x=filtered["Nome"],
                             y=filtered[stats[1]], marker_color='#E53935'))
        y_title = "Cards"

    fig.update_layout(barmode='stack', xaxis=dict(title_text="Name of players"),
                      yaxis=dict(title_text=y_title), title_text=title)

    return fig


# TODO: radar
# TODO: ruolo su giocatore hover / cambia colore
# TODO: mettere campioncini
# TODO: ordinare html
# TODO: only 5 giornate for statistical purposes

if __name__ == '__main__':
    app.run_server(debug=True)

'''
# first row
html.Div([
    html.Div([], className="six columns"),
    html.Div([], className="six columns"),
], className="row"),
'''
