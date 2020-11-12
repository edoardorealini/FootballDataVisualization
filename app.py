import plotly.graph_objects as go

import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import numpy as np
import base64
import random
import math

from scipy import stats
from dash.dependencies import Input, Output
from utils import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"]
data_path = "./data/"


# -------Important variables for FANTACALCIO purposes-------

# Retreive df
season = 2019
data_url = "./data/fantacalcio/stats" + str(season) + ".csv"
img_url = './data/fantacalcio/no_img' + str(season) + '.csv'
original_df = pd.read_csv(data_url)
team_df = original_df.sort_values(by=["Squadra"], ascending=True)
no_images = pd.read_csv(img_url)["Nome"].to_list()

all_names = original_df["Nome"]
all_names_at_least_one_match_df = original_df[original_df["Partite giocate"] > 0].sort_values(by=["Nome"], ascending=True)
all_names_at_least_one_match = all_names_at_least_one_match_df["Nome"]
campioncini = {}

for player_name in all_names:
    modified_name = player_name
    if " " in modified_name:
        modified_name = modified_name.replace(" ", "-")
    if "\'" in modified_name:
        modified_name = modified_name.replace("\'", "-")
    if "." in modified_name:
        modified_name = modified_name.replace(".", "")

    url_img = "./data/fantacalcio/campioncini/"

    if modified_name not in no_images:
        # campioncini[player_name] = img_name
        campioncini[player_name] = url_img + modified_name + ".png"
    else:
        # campioncini[player_name] = "./data/fantacalcio/campioncini/noimg.png"
        campioncini[player_name] = url_img + "noimg.png"

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


# ----------------------------- APP ----------------------------------------

# Initialise the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server

# Define the app
app.layout = html.Div(children=[html.Div(style={'textAlign': 'center'},className="row", children=[html.H1("Data Results and Visualization - Politecnico di Milano")]),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='SERIE A', children=[

            html.Div(children=[

                html.Div(className="row", style={"padding": 20}),

                #row for dropdown selectors for WINS AND GOALS graphs
                html.Div(className="row", children=[

                    html.Div(className='six columns',
                        children=[
                            html.Div(style={"marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}, children=[html.P('Season')]),
                            html.Div(children=[html.Div(
                                className='row',
                                children =  [
                                                dcc.Dropdown(id='season_selector_wins', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                                            multi=False, value="2019",
                                                            className='season_selector_wins',
                                                            clearable=False,
                                                            searchable=False,
                                                            style={"width": "60%", "marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}
                                                            )
                                            ])
                            ])
                        ]),

                    html.Div(className='six columns',
                        children=[
                            html.Div(style={"marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}, children=[html.P('Season')]),

                            html.Div(style={'textAlign': 'center'},
                                children =  [
                                                dcc.Dropdown(id='season_selector_goals', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                                            multi=False, value="2019",
                                                            className='season_selector_goals',
                                                            clearable=False,
                                                            searchable=False,
                                                            style={"width": "60%", "marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}
                                                            )
                                            ])
                        ]
                    )
                ]),

                #row for the actual graphs wins and goals
                html.Div(className='row',
                    children=  [
                                    html.Div(className='six columns',
                                            children=[
                                                dcc.Graph(id='bar_wins', config={'displayModeBar': True})
                                            ]),

                                    html.Div(className='six columns',
                                            children=[
                                                dcc.Graph(id='bar_goals', config={'displayModeBar': True})
                                            ])
                                ]
                ),

                html.Div(className="row", style={"padding": 30}),

                #row for dropdown selectors for the 2 SCATTER graphs
                html.Div(className='row',
                    children=  [
                                    html.Div(className='six columns',
                                        children=[
                                            html.Div(style={"marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}, children=[html.P('Season')]),
                                            html.Div(children=[html.Div(
                                                className='row',
                                                children=[
                                                    dcc.Dropdown(id='season_selector_scatter', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                                                multi=False, value="2019",
                                                                className='season_selector_wins',
                                                                clearable=False,
                                                                searchable=False,
                                                                style={"width": "60%", "marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}
                                                                ),
                                                ])
                                            ])
                                        ]),

                                    html.Div(className='six columns',
                                            children=[
                                                html.Div(style={"marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}, children=[html.P('Season')]),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(id='season_select_bubble', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                                                    multi=False, value="2019",
                                                                    className='season_selector_goals',
                                                                    clearable=False,
                                                                    searchable=False,
                                                                    style={"width": "60%", "marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}
                                                                    ),
                                                    ])
                                                ] #, style={"display":"none"}
                                            )
                                ]),

                #row for dropdown selectors for the 2 scatter graphs
                html.Div(className='row',
                    children=  [
                                    html.Div(className='six columns',
                                            children=[
                                                dcc.Graph(id='scatter_season', config={'displayModeBar': True})
                                            ]),

                                    html.Div(className='six columns',
                                            children=[
                                                dcc.Graph(id='bubble', config={'displayModeBar': True})
                                            ])
                                ]
                ),

                html.Div(className="row", style={"padding": 30}),

                #teams viz selectors
                html.Div(className='row',
                    children=  [
                                    html.Div(className='four columns',
                                        children=[
                                            html.Div(style={"marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}, children=[html.P('Team')]),
                                            html.Div(children=[html.Div(
                                                className='row',
                                                children=[
                                                    dcc.Dropdown(id='team_selector_points', options=get_teams_dict_list(),
                                                                multi=False, value="Juventus",
                                                                className='season_selector_wins',
                                                                clearable=True,
                                                                searchable=True,
                                                                style={"width": "60%", "marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}
                                                                ),
                                                ])
                                            ])
                                        ]),

                                    html.Div(className='four columns',
                                            children=[
                                                html.Div(style={"marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}, children=[html.P('Team')]),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(id='team_selector_wins', options=get_teams_dict_list(),
                                                                    multi=False, value="Juventus",
                                                                    className='season_selector_goals',
                                                                    clearable=True,
                                                                    searchable=True,
                                                                    style={"width": "60%", "marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}
                                                                    ),
                                                    ])
                                                ] #, style={"display":"none"}
                                            ),

                                    html.Div(className='four columns',
                                            children=[
                                                html.Div(style={"marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}, children=[html.P('Team')]),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(id='team_selector_scoring', options=get_teams_dict_list(),
                                                                    multi=False, value="Juventus",
                                                                    className='season_selector_goals',
                                                                    clearable=True,
                                                                    searchable=True,
                                                                    style={"width": "60%", "marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}
                                                                    ),
                                                    ])
                                                ] #, style={"display":"none"}
                                            )
                                ]),

                #row for dropdown selectors for the 2 scatter graphs
                html.Div(className='row',
                    children=  [
                                    html.Div(className='four columns',
                                            children=[
                                                dcc.Graph(id='lines_team_points', config={'displayModeBar': True})
                                            ]),

                                    html.Div(className='four columns',
                                            children=[
                                                dcc.Graph(id='lines_team_wins', config={'displayModeBar': True})
                                            ]),

                                    html.Div(className='four columns',
                                            children=[
                                                dcc.Graph(id='lines_team_scoring', config={'displayModeBar': True})
                                            ]),
                                ]
                ),

                 html.Div(className="row", style={"padding": 30}),

                #row for dropdown selectors for the 2 SCATTER graphs
                html.Div(className='row',
                    children=[
                        html.Div(style={"marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}, children=[html.P('Season')]),
                        html.Div(children=[html.Div(
                            className='row',
                            children=[
                                dcc.Dropdown(id='season_selector_parallel', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                            multi=False, value="2019",
                                            className='season_selector_parallel',
                                            clearable=False,
                                            searchable=False,
                                            style={"width": "60%", "marginRight": "auto", "marginLeft": "auto", "textAlign": "center"}
                                            ),
                            ])
                        ])
                    ]),

                # row for dropdown selectors for the 2 scatter graphs
                html.Br(),
                html.Div(className='row',
                        children=[
                            dcc.Graph(id='parallel', config={'displayModeBar': True})
                        ])

            ], style={'maxWidth': '94vw', "marginRight": "auto", "marginLeft": "auto"})

            ]),    # closes serieA tab

            dcc.Tab(label='FANTACALCIO', children=[
                # TODO rick aggiungi HTML qui
                html.Div([

                    html.Div([
                        html.Br(),
                        html.Div([
                            html.H1([
                                html.I(className="fa fa-futbol-o"),
                                html.B(children='  Welcome to FantaStats!  '),
                                html.I(className="fa fa-futbol-o"),
                            ])
                        ], className="row"),

                        html.H4(children='In this dashboard you can plot some interesting stats about the players of last Serie A season.'),

                        html.Br(),
                    ], style={"textAlign": "center"}, id="introText"),

                    # first row
                    html.Div([
                        # second column first row
                        html.Div([
                            html.P(style={"fontSize": "1.15em"},children='''The following graph shows the statistics about the number of goals
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
                                html.Div(
                                    "", className='two columns'),
                                html.Div([
                                    html.Div([
                                        html.Div(children='Show top:', className='four columns', style={
                                            "textAlign": "right", "paddingTop": "5px"}),
                                        html.Div([
                                            dcc.Dropdown(
                                                clearable=False,
                                                searchable=False,
                                                id='players_number_goals',
                                                options=[{'label': str(i), 'value': i}
                                                         for i in numbers_of_players],
                                                value=15
                                            )], className='eight columns')
                                    ], className='row'), ], className='five columns')
                            ], className='row'),

                            dcc.Graph(id='goals_graph', config={'displayModeBar': False})
                        ], className="six columns"),

                        # second column first row
                        html.Div([
                            html.P(style={"fontSize": "1.15em"},children='''The following graph shows the statistics about the grade
                                             point average and the  so-called Fantagrade.'''),

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
                                html.Div(
                                    "", className='two columns'),
                                html.Div([
                                    html.Div([
                                        html.Div(children='Show top:', className='four columns', style={
                                            "textAlign": "right", "paddingTop": "5px"}),
                                        html.Div([
                                            dcc.Dropdown(
                                                clearable=False,
                                                searchable=False,
                                                id='players_number_mv',
                                                options=[{'label': str(i), 'value': i}
                                                         for i in numbers_of_players],
                                                value=15
                                            )], className='eight columns')
                                    ], className='row'), ], className='five columns')
                            ], className='row'),

                            dcc.Graph(id='mv_graph', config={'displayModeBar': False})
                        ], className="six columns")
                    ], className="row"),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    # second row
                    html.Div([
                        html.P(style={"fontSize": "1.15em", "textAlign": "center"},
                               children='In the next section you can compare two players by plotting their \
                               most significant stats.'),

                        html.Br(),

                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div(children='First player:', className='six columns', style={
                                        "textAlign": "right", "paddingTop": "5px"}),
                                    html.Div([
                                        dcc.Dropdown(
                                            clearable=False,
                                            id='player_to_show_name1',
                                            options=[{'label': name, 'value': name} for name in all_names_at_least_one_match],
                                            value='IMMOBILE'
                                        )], className='six columns')
                                ], className='row', style={"maxWidth": "50%", "marginRight": "auto", "marginLeft": "auto"}),
                            ], className='six columns'),
                            html.Div([
                                html.Div([
                                    html.Div(children='Second player:', className='six columns', style={
                                        "textAlign": "right", "paddingTop": "5px"}),
                                    html.Div([
                                        dcc.Dropdown(
                                            clearable=False,
                                            id='player_to_show_name2',
                                            options=[{'label': name, 'value': name} for name in all_names_at_least_one_match],
                                            value='LUKAKU'
                                        )], className='six columns')
                                ], className='row', style={"maxWidth": "50%", "marginLeft": "auto", "marginRight": "auto"}),
                            ], className='six columns')
                        ], className='row'),

                        html.Div(id="player_stats")
                    ], className="row"),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    # third row
                    html.Div([
                        html.P(style={"fontSize": "1.15em"},
                               children='''The following graph shows the stats players filtered by their team.'''),

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
                            html.Div(className='one columns'),
                            html.Div([
                                html.Div([
                                    html.Div(children='Stats to show:', className='four columns', style={
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
                                ], className='row'), ], className='six columns'),
                        ], className='row'),

                        dcc.Graph(id='team_graph', config={'displayModeBar': False})
                    ], className="row"),

                ], style={'maxWidth': '94vw', "marginRight": "auto", "marginLeft": "auto"})
            ]),

        ])
    ])
])


# ----------------------------- CALLBACKS ----------------------------------------

trx = {
    "duration": 500,
    "easing": "circle",
    "ordering": "traces first"
}

#bar wins callback function, triggered by its dropdown menu
@app.callback(Output('bar_wins', 'figure'),
              [Input('season_selector_wins', 'value')])
def update_bar_wins(selected_dropdown_value):

    #print(trace_title)

    df = pd.read_csv("./data/teams/" + str(selected_dropdown_value) + ".csv")
    df = df.sort_values(by='wins', ascending=False)

    teams = df["team_name"].to_list()
    wins = df["wins"].to_list()
    draws = df["draws"].to_list()
    loses = df["loses"].to_list()

    fig = go.Figure()

    fig.add_trace(go.Bar(x=teams, y=wins,
                    #base=0,
                    marker_color='rgb(73,138,93)',
                    marker_opacity=1,
                    name='Wins'))

    fig.add_trace(go.Bar(x=teams, y=draws,
                    #base=wins,
                    marker_color='rgb(248,208,20)',
                    name='Draws'))

    fig.add_trace(go.Bar(x=teams, y=loses,
                    #base=addition(wins,draws),
                    marker_color='rgb(209,68,72)',
                    marker_opacity=1,
                    name='Defeats'))

    trace_title = "Wins-Draws-Defeats comparison season " + str(selected_dropdown_value)

    fig.update_layout(
        title=str(trace_title),
        title_x=0.5,
        #xaxis_categoryorder='total descending',
        barmode='stack',
        xaxis_title="Teams",
        yaxis_title="Matches",
        legend_orientation="v",
        hovermode="x unified"
        #transition=trx
    )

    return fig


#bar goals callback function, triggered by its dropdown menu
@app.callback(Output('bar_goals', 'figure'),
              [Input('season_selector_goals', 'value')])
def update_bar_goals(selected_dropdown_value):

    trace_title = "Goals comparison for season " + str(selected_dropdown_value)

    df = pd.read_csv("./data/teams/" + str(selected_dropdown_value) + ".csv")
    df['goalsDifference'] = difference(df["goalsFor"].to_list(), df["goalsAgainst"].to_list())
    df = df.sort_values('goalsDifference', ascending=False)

    teams = df["team_name"].to_list()
    goalsFor = df["goalsFor"].to_list()
    goalsAgainst = df["goalsAgainst"].to_list()
    goalsDifference = df["goalsDifference"].to_list()

    goalsPositive, goalsNegative = difference_pos_neg(goalsDifference)

    fig = go.Figure()

    fig.add_trace(go.Bar(x=teams, y=convert(goalsAgainst),
                    base=0,
                    marker_color='rgb(237,183,149)',
                    name='Goals conceded'))

    fig.add_trace(go.Bar(x=teams, y=goalsFor,
                    base=0,
                    marker_color='rgb(23,76,140)',
                    name='Goals scored'))

    fig.add_trace(go.Bar(x=teams, y=convert(goalsNegative),
            base=0,
            marker_color='rgb(209,68,72)',
            name='Goals negative'))

    fig.add_trace(go.Bar(x=teams, y=goalsPositive,
            base=0,
            marker_color='rgb(73,138,93)',
            name='Goals positive'))

    fig.update_layout(
        title=trace_title,
        title_x = 0.5,
        xaxis_title="Teams",
        yaxis_title="Goals",
        barmode='stack',
        legend_orientation='v',
        hovermode="x unified"
        #transition=trx
    )

    return fig


#scatter season callback function, triggered by its dropdown menu
@app.callback(Output('scatter_season', 'figure'),
              [Input('season_selector_scatter', 'value')])
def update_scatter_season(selected_dropdown_value):

    trace_title = "Goals average scatter plot - season " + str(selected_dropdown_value)

    df = pd.read_csv("./data/teams/" + str(selected_dropdown_value) + ".csv")
    avg_for = df["avg_goalsFor"].to_list()
    avg_against = df["avg_goalsAgainst"].to_list()
    teams = df["team_name"].to_list()

    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(avg_for),np.array(avg_against))
    line = slope*np.array(avg_for)+intercept

    fig = go.Figure()

    avg_for_x, avg_against_y = [],[]
    color_list = np.divide(avg_against, avg_for)
    rgb_color_list = colorscale_to_rgb(list(color_list), 'gnuplot')

    for i in range(0,20):

        avg_for_x.append(avg_for[i])
        avg_against_y.append(avg_against[i])

        marker_text = "Team: " + teams[i] + "<br>" + "avg scored: " + str(avg_for[i]) + "<br>" + "avg conceded: " + str(avg_against[i])

        fig.add_trace(go.Scatter(x=avg_for_x, y=avg_against_y,
                                mode='markers',
                                name=teams[i],
                                marker=dict(
                                    size=16,
                                    color=rgb_color_list[i],
                                    line_width=1.5,
                                    opacity=0.85,
                                    showscale=False),
                                text=marker_text,
                                hoverinfo="text"))

        avg_for_x.clear()
        avg_against_y.clear()


    fig.add_trace(go.Scatter(x=np.array(avg_for),y=line,
                            mode='lines',
                            marker_color="black",
                            name='Line Fit'))

    #fig.update_traces(marker=dict(color=color_list, colorscale='Reds'))


    fig.update_layout(
        title=trace_title,
        title_x=0.5,
        xaxis_title="Average goals scored",
        yaxis_title="Average goals conceded",
        legend=dict(orientation="h"),
        showlegend=False,
        #hovermode="x unified"
        #transition=trx
        )

    return fig


@app.callback(Output('parallel', 'figure'),
              [Input('season_selector_parallel', 'value')])
def update_parallel(selected_dropdown_value):
    season = selected_dropdown_value

    trace_title = "Parallel Coordinates Shots on Season " + str(season)

    data = pd.read_csv("./data/shots/" + str(season) + ".csv", delimiter=";")
    goalkeeper_area = data['SixYardBox'].to_list()
    penalty_area = data['PenaltyArea'].to_list()
    out_area = data['OutOfBox'].to_list()
    total = data['total'].to_list()

    fig = go.Figure()

    #srgb_color_list = colorscale_to_rgb(total, 'Pastel1')

    fig.add_trace(go.Parcoords(
            line_color = total,
            line_colorscale = 'Spectral',
            line_colorbar_title = 'Total shots',
            dimensions = list([
                dict(range = [100,400],
                    label = 'Out Of Box', values = data['OutOfBox']),
                dict(range = [0,100],
                    label = 'Six Yard Box', values = data['SixYardBox']),
                dict(range = [100,500],
                    label = 'Penalty Area', values = data['PenaltyArea']),
                dict(range = [5,8],
                    label = 'Rating', values = data['Rating'])
            ])
        ))


    fig.update_layout(
        plot_bgcolor = 'rgb(230,236,245)',
        paper_bgcolor = 'rgb(230,236,245)',
        title=trace_title,
        title_x=0.5,
        title_y=0.96,
        )

    return fig


#teams lines points callback function, triggered by its dropdown menu
@app.callback(Output('lines_team_points', 'figure'),
              [Input('team_selector_points', 'value')])
def update_lines_points(selected_dropdown_value):

    points_list = []

    seasons = list(range(2010,2020))

    for season in seasons:
        try:
            df = pd.read_csv("./data/teams/" + str(season) + ".csv")
            df = df[df.team_name == selected_dropdown_value]
            wins = df["wins"].to_list()
            draws = df["draws"].to_list()
            points = (wins[0]*3) + draws[0]
            points_list.append(points)

        except:
            points_list.append(0)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=seasons, y=points_list,
                        mode='lines+markers',
                        name='points',
                        line_shape='spline',
                        line_width=3,
                        marker_size=10,
                        )

                )

    fig.update_layout(
        title= str(selected_dropdown_value) + " points by year",
        title_x=0.5,
        xaxis_title="Year",
        yaxis_title="Points",
        hovermode="x unified"
        #transition=trx
    )

    return fig


#teams lines wins callback function, triggered by its dropdown menu
@app.callback(Output('lines_team_wins', 'figure'),
              [Input('team_selector_wins', 'value')])
def update_lines_wins(selected_dropdown_value):

    wins_list = []
    draws_list = []
    loses_list = []

    seasons = list(range(2010,2020))

    for season in seasons:
        try:
            df = pd.read_csv("./data/teams/" + str(season) + ".csv")
            df = df[df.team_name == selected_dropdown_value]
            #df = df[['wins','draws','loses']]
            wins = df["wins"].to_list()
            draws = df["draws"].to_list()
            loses = df["loses"].to_list()
            wins_list.append(wins[0])
            draws_list.append(draws[0])
            loses_list.append(loses[0])

        except:
            wins_list.append(0)
            draws_list.append(0)
            loses_list.append(0)


    fig = go.Figure()

    fig.add_trace(go.Scatter(x=seasons, y=wins_list,
                        mode='lines+markers',
                        line_shape='spline',
                        line_width=3,
                        marker_size=10,
                        name='Wins'))
    fig.add_trace(go.Scatter(x=seasons, y=loses_list,
                        mode='lines+markers',
                        line_shape='spline',
                        line_width=3,
                        marker_size=10,
                        name='Defeats'))
    fig.add_trace(go.Scatter(x=seasons, y=draws_list,
                        mode='lines+markers',
                        line_shape='spline',
                        line_width=3,
                        marker_size=10,
                        name='Draws'))


    fig.update_layout(
        title= str(selected_dropdown_value) + " wins, losses and draws by year",
        title_x=0.5,
        xaxis_title="Year",
        yaxis_title="Wins",
        hovermode="x unified"
        #transition=trx
    )

    return fig


#teams lines scoring callback function, triggered by its dropdown menu
@app.callback(Output('lines_team_scoring', 'figure'),
              [Input('team_selector_scoring', 'value')])
def update_lines_scoring(selected_dropdown_value):

    goalsFor_list = []
    goalsAgainst_list = []

    seasons = list(range(2010,2020))

    for season in seasons:
        try:
            df = pd.read_csv("./data/teams/" + str(season) + ".csv")
            df = df[df.team_name == selected_dropdown_value]
            goalsfor = df["avg_goalsFor"].to_list()
            goalsagainst = df["avg_goalsAgainst"].to_list()
            goalsFor_list.append(goalsfor[0])
            goalsAgainst_list.append(goalsagainst[0])

        except:
            goalsFor_list.append(0)
            goalsAgainst_list.append(0)


    fig = go.Figure()

    fig.add_trace(go.Scatter(x=seasons, y=goalsFor_list,
                        mode='lines+markers',
                        name='Goals scored',
                        line_shape='spline',
                        line_width=3,
                        marker_size=10,
                        )

                    )
    fig.add_trace(go.Scatter(x=seasons, y=goalsAgainst_list,
                        mode='lines+markers',
                        name='Goals conceded',
                        line_shape='spline',
                        line_width=3,
                        marker_size=10,
                        )
                    )

    fig.update_layout(
        title= str(selected_dropdown_value) + " scoring rate by year",
        title_x=0.5,
        xaxis_title="Year",
        yaxis_title="Average",
        hovermode="x unified"
    )

    return fig


#teams lines scoring callback function, triggered by its dropdown menu
@app.callback(Output('bubble', 'figure'),
              [Input('season_select_bubble', 'value')])
def update_bubbles(selected_dropdown_value):

    goal_data = pd.read_csv("./data/teams/" + str(selected_dropdown_value) + ".csv")
    goal_data = goal_data.sort_values(by=["team_name"])
    goals = goal_data['goalsFor'].to_list()

    data = pd.read_csv("./data/shots/" + str(selected_dropdown_value) + ".csv", delimiter=";")
    data = data.sort_values(by=['team_name'])
    teams = data['team_name'].to_list()
    shots = data['total'].to_list()

    scoring_percentage = list(map(lambda x: x*100, division(goals, shots)))

    fig = go.Figure()

    shot_x, score_y = [], []
    rgb_color_list = colorscale_to_rgb(goals, 'Set2')

    for i in range(0,20):
        shot_x.append(shots[i])
        score_y.append(scoring_percentage[i])

        marker_text = "Teams: " + teams[i] + "<br>" + "Goals: " + str(goals[i])

        fig.add_trace(go.Scatter(x=shot_x, y=score_y, name=teams[i],
                        mode='markers',
                        text=marker_text,
                        marker=dict(
                            size=goals[i]/1.5,
                            opacity=0.9,
                            color=rgb_color_list[i],
                            line_width=1.7),
                        hoverinfo="text"))

        shot_x.clear()
        score_y.clear()

    fig.update_layout(
        title='Scoring rates for season ' + str(selected_dropdown_value),
        title_x=0.5,
        xaxis_title='Shots taken',
        yaxis_title='Scoring Rate % (Goals/Shots)',
        legend_orientation="h",
        showlegend=False,
        #transition=trx
    )

    return fig

# -----------------------FANTACALCIO CALLBACKS------------------


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

    fig.update_layout(hovermode="x unified")

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
        go.Scatter(name='Avg Fantagrade', x=filtered["Nome"],
                   y=filtered["Media Fantavoto"], marker_color='#0088E0', mode='lines+markers'))

    fig.add_trace(go.Bar(name='Avg grade', x=filtered["Nome"],
                         y=filtered["Media voto"], marker_color='#E53935'))

    fig.update_layout(xaxis=dict(title_text="Name of players"),
                      yaxis=dict(title_text=y_title), title_text=title)

    fig.update_layout(hovermode="x unified")

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
    filtered = filtered[filtered["Partite giocate"] > 3]
    filtered = filtered.sort_values(by=[stats[0]], ascending=False)
    filtered = filtered.head(25)

    colors = []

    for role in filtered["Ruolo"]:
        colors.append(color_by_role[role])

    fig = go.Figure()

    if (stats[0] == "Media voto"):
        fig.add_trace(go.Scatter(name='Avg Fantagrade', x=filtered["Nome"],
                                 y=filtered[stats[1]], marker_color='#0088E0', mode='lines+markers'))
        fig.add_trace(go.Bar(name='Avg grade', x=filtered["Nome"],
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

    fig.update_layout(hovermode="x unified")

    return fig


@app.callback(
    Output('player_stats', 'children'),
    [Input('player_to_show_name1', 'value'), Input('player_to_show_name2', 'value')])
def update_player_graph(player_name_1, player_name_2):

    bigDiv = []

    player_1 = original_df[original_df["Nome"] == player_name_1]
    grade_1 = np.array(player_1["Media Fantavoto"])[0]
    role_short = np.array(player_1["Ruolo"])[0]
    role_1 = roles[role_short]
    role_1 = "<b>The role of the player is: " + role_1[:-1] + "</b>"

    player_2 = original_df[original_df["Nome"] == player_name_2]
    grade_2 = np.array(player_2["Media Fantavoto"])[0]
    role_short = np.array(player_2["Ruolo"])[0]
    role_2 = roles[role_short]
    role_2 = "<b>The role of the player is: " + role_2[:-1] + "</b>"

    y_values_1 = ["Autogoal", "Espulsioni", "Ammonizioni", "Assists tot", "Goals tot", "Partite giocate"]
    x_values_1 = -1 * np.array(player_1[y_values_1])[0]

    y_values_2 = ["Autogoal", "Espulsioni", "Ammonizioni", "Assists tot", "Goals tot", "Partite giocate"]
    x_values_2 = np.array(player_2[y_values_2])[0]

    player_2 = original_df[original_df["Nome"] == player_name_2]
    grade_2 = np.array(player_2["Media Fantavoto"])[0]

    colors_bars = ["#AF7AC5", "#E74C3C", "#F1C40F", "#58D68D", "#229954", "#2980B9"]

    loser_color = "#707B7C"

    bigDiv.append(html.Br())
    # bigDiv.append(html.Br())
    bigDiv.append(
        html.Div([
            html.B(children="Stats of " + player_name_1, className="six columns", style={"fontSize": "18px"}),
            html.B(children="Stats of " + player_name_2, className="six columns", style={"fontSize": "18px", "textAlign": "right"})
        ], className="row")
    )

    y_values_bug_fix = ["Autogoal ", "Espulsioni ", "Ammonizioni ", "Assists tot ", "Goals tot ", "Partite giocate "]
    fig = go.Figure()

    # add the trace of the first player
    fig.add_trace(go.Bar(x=x_values_1, y=y_values_bug_fix, name=player_name_1, orientation='h',
                         text=(-1 * x_values_1), hoverinfo='text', marker_color=colors_bars))

    # add the trace of the second player
    fig.add_trace(go.Bar(x=x_values_2, y=y_values_bug_fix, name=player_name_2, orientation='h',
                         hoverinfo='x', marker_color=colors_bars))

    list = [-40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40]
    pos_list = [40, 35, 30, 25, 20, 15, 10, 5, 0, 5, 10, 15, 20, 25, 30, 35, 40]

    x_axis = {"range": [-40, 40], "tickvals": list, "ticktext": pos_list, "title": "Number"}

    fig.update_layout(title_text=role_1, xaxis=x_axis, barmode='overlay', bargap=0.1)

    # grade of first player
    voto_1 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=grade_1,
        title={'text': "<b>Fantagrade</b>"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [None, 12]},
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 6}}
    ))

    voto_1.update_layout(autosize=False, width=300, height=300, margin_t=0)

    # grade of second player
    voto_2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=grade_2,
        title={'text': "<b>Fantagrade</b>"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [None, 12]},
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 6}}
    ))

    voto_2.update_layout(autosize=False, width=300, height=300, margin_t=0)

    encoded_image_1 = base64.b64encode(open(campioncini[player_name_1], 'rb').read())
    encoded_image_2 = base64.b64encode(open(campioncini[player_name_2], 'rb').read())

    row = html.Div([
        # image of campioncino 1
        html.Div([
            html.Br(),
            html.Br(),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image_1.decode()), alt=player_name_1, style={"minWidth": "95px",
                     "display": "block", "marginRight": "auto", "marginLeft": "auto", "maxWidth": "120px"}),
            dcc.Graph(figure=voto_1, config={'displayModeBar': False})
        ], className="three columns"),

        # relevant stats: goals, assists, cards, avg grade
        html.Div([
            dcc.Graph(figure=fig, config={'displayModeBar': False})
        ], className="six columns"),

        # image of campioncino 2
        html.Div([
            html.Br(),
            html.Br(),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image_2.decode()), alt=player_name_2, style={"minWidth": "95px",
                     "display": "block", "marginRight": "auto", "marginLeft": "auto", "maxWidth": "120px"}),
            dcc.Graph(figure=voto_2, config={'displayModeBar': False})
        ], className="three columns"),

    ], className="row")

    bigDiv.append(row)

    return bigDiv


# ----------------------------- MAIN ----------------------------------------

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
