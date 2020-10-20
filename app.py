import plotly.graph_objects as go

import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import numpy as np 
import random
import math

from scipy import stats
from dash.dependencies import Input, Output
from utils import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data_path = "./data/"


# ----------------------------- APP ----------------------------------------

# Initialise the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server

# Define the app
app.layout = html.Div(children=[html.Center(className="row", children=[html.H2("Data Results and Visualization - Politecnico di Milano")]), 
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='SERIE A', children=[

                html.Div(className="row", style={"padding": 20}),

                #row for dropdown selectors for WINS AND GOALS graphs
                html.Div(className="row", children=[                

                    html.Div(className='six columns',
                        children=[
                            html.Center(children=[html.P('Season')]),
                            html.Center(children=[html.Div(
                                className='row',
                                children =  [
                                                dcc.Dropdown(id='season_selector_wins', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                                            multi=False, value="2019",
                                                            className='season_selector_wins',
                                                            clearable=False,
                                                            searchable=False,
                                                            style={"width": "60%",
                                                                    "verticalAlign": "middle"                                                            
                                                            }
                                                            )
                                            ])
                            ])
                        ]),

                    html.Div(className='six columns',
                        children=[
                            html.Center(children=[html.P('Season')]),

                            html.Center(
                                className='div-for-dropdown',
                                children =  [
                                                dcc.Dropdown(id='season_selector_goals', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                                            multi=False, value="2019",
                                                            className='season_selector_goals',
                                                            clearable=False,
                                                            searchable=False,
                                                            style={"width": "60%"}
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
                                            html.Center(children=[html.P('Season')]),
                                            html.Center(children=[html.Div(
                                                className='row',
                                                children=[
                                                    dcc.Dropdown(id='season_selector_scatter', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                                                multi=False, value="2019",
                                                                className='season_selector_wins',
                                                                clearable=False,
                                                                searchable=False,
                                                                style={"width": "60%"}
                                                                ),
                                                ])
                                            ])
                                        ]),

                                    html.Div(className='six columns',
                                            children=[
                                                html.Center(children=[html.P('Season')]),
                                                html.Center(
                                                    className='div-for-dropdown',
                                                    children=[
                                                        dcc.Dropdown(id='season_select_bubble', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                                                    multi=False, value="2019",
                                                                    className='season_selector_goals',
                                                                    clearable=False,
                                                                    searchable=False,
                                                                    style={"width": "60%"}
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
                                            html.Center(children=[html.P('Team')]),
                                            html.Center(children=[html.Div(
                                                className='row',
                                                children=[
                                                    dcc.Dropdown(id='team_selector_points', options=get_teams_dict_list(),
                                                                multi=False, value="Juventus",
                                                                className='season_selector_wins',
                                                                clearable=True,
                                                                searchable=True,
                                                                style={"width": "60%"}
                                                                ),
                                                ])
                                            ])
                                        ]),

                                    html.Div(className='four columns',
                                            children=[
                                                html.Center(children=[html.P('Team')]),
                                                html.Center(
                                                    className='div-for-dropdown',
                                                    children=[
                                                        dcc.Dropdown(id='team_selector_wins', options=get_teams_dict_list(),
                                                                    multi=False, value="Juventus",
                                                                    className='season_selector_goals',
                                                                    clearable=True,
                                                                    searchable=True,
                                                                    style={"width": "60%"}
                                                                    ),
                                                    ])
                                                ] #, style={"display":"none"}
                                            ),

                                    html.Div(className='four columns',
                                            children=[
                                                html.Center(children=[html.P('Team')]),
                                                html.Center(
                                                    className='div-for-dropdown',
                                                    children=[
                                                        dcc.Dropdown(id='team_selector_scoring', options=get_teams_dict_list(),
                                                                    multi=False, value="Juventus",
                                                                    className='season_selector_goals',
                                                                    clearable=True,
                                                                    searchable=True,
                                                                    style={"width": "60%"}
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
                        html.Center(children=[html.P('Season')]),
                        html.Center(children=[html.Div(
                            className='row',
                            children=[
                                dcc.Dropdown(id='season_selector_parallel', options=[{'label': str(i), 'value': str(i)} for i in range(2010, 2020)],
                                            multi=False, value="2019",
                                            className='season_selector_parallel',
                                            clearable=False,
                                            searchable=False,
                                            style={"width": "60%"}
                                            ),
                            ])
                        ])
                    ]),
            
                #row for dropdown selectors for the 2 scatter graphs
                                
                html.Div(className='row',
                        children=[
                            dcc.Graph(id='parallel', config={'displayModeBar': True})
                        ])
                                
                

            ]), #closes serieA tab

            dcc.Tab(label='FANTACALCIO', children=[
                #TODO rick aggiungi HTML qui
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [1, 4, 1],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [1, 2, 3],
                            'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                )
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
        #transition=trx
    )

    return fig


#scatter season callback function, triggered by its dropdown menu
@app.callback(Output('scatter_season', 'figure'),
              [Input('season_selector_scatter', 'value')])
def update_scatter_season(selected_dropdown_value):

    trace_title = "Goals average scatter plot - season " + str(selected_dropdown_value)    

    df = pd.read_csv("./data/teams/" + str(selected_dropdown_value) + ".csv")
    teams = df["team_name"].to_list()
    avg_for = df["avg_goalsFor"].to_list()
    avg_against = df["avg_goalsAgainst"].to_list()

    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(avg_for),np.array(avg_against))
    line = slope*np.array(avg_for)+intercept

    fig = go.Figure()

    avg_for_x, avg_against_y = [],[]
    color_list = np.divide(avg_for, avg_against)
    rgb_color_list = colorscale_to_rgb(list(color_list), 'Blues')

    for i in range(0,20):
        
        avg_for_x.append(avg_for[i])
        avg_against_y.append(avg_against[i])

        fig.add_trace(go.Scatter(x=avg_for_x, y=avg_against_y, 
                                mode='markers',
                                name=teams[i],
                                marker=dict(
                                    size=16,
                                    color=rgb_color_list[i],
                                    line_width=1.5,
                                    opacity=0.85,
                                    showscale=False)))
        
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
            line_colorscale = 'Reds',
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
        title_y=0.96)

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
        
        marker_text = "Goals:" + str(goals[i])
        
        fig.add_trace(go.Scatter(x=shot_x, y=score_y, name=teams[i], 
                        mode='markers',
                        text=marker_text,
                        marker=dict(
                            size=goals[i],
                            opacity=0.9,
                            color=rgb_color_list[i],
                            line_width=1.7
                    )))
        
        shot_x.clear()
        score_y.clear()
        
    fig.update_layout(
        title='Scoring rates for season ' + str(selected_dropdown_value),
        title_x=0.5,
        xaxis_title='Shots taken',
        yaxis_title='Scoring Rate % (Goals/Shots)',
        legend_orientation="h",
        showlegend=False
        #transition=trx
    )

    return fig


# ----------------------------- MAIN ----------------------------------------

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)