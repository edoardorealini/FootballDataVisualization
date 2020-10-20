from pathlib import Path
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


# Definition of useful functions

def getDataByRole(role, num):
    global original_df
    global title

    words = title.split(" ")
    words[2] = roles[role]
    title = " ".join(words)

    # filter df by role of the player
    filtered = original_df[original_df["Ruolo"] == role]

    # return different stats for GoalKeepers
    if role == "P":
        filtered = filtered[filtered["Partite giocate"] > 5]
        # filtered = filtered[filtered["Goals subiti"] > 0]
        filtered = filtered.sort_values(by=["Goal subiti"], ascending=True)
        filtered = filtered.head(num)
        p_title = title + "<b> for number of goals conceded</b>"
        y_axis = dict(title="Goals conceded")
        return [{'name': ["Goal conceded", "Penalty blocked"], 'x': [filtered["Nome"], filtered["Nome"]],
                 'y': [filtered["Goal subiti"], filtered["Rigori parati"]],
                 }, {'title': p_title, 'yaxis': y_axis}]
    # return arg list to set x, y and chart title
    else:
        filtered = filtered[filtered["Goals tot"] > 0]
        filtered = filtered.sort_values(by=["Goals tot"], ascending=False)
        filtered = filtered.head(num)
        o_title = title + "<b> for number of goals scored</b>"
        y_axis = dict(title="Goals scored")
        return [{'name': ["Goal scored", "Penalty scored"], 'x': [filtered["Nome"], filtered["Nome"]],
                 'y': [filtered["Goal fatti"], filtered["Rigori segnati"]],
                 }, {'title': o_title, 'yaxis': y_axis}]


def update_number(num):
    global title
    global num_players_to_show
    global original_df

    words = title.split(" ")
    role = words[2]
    role_short = ""
    num_players_to_show = num

    for key, value in roles.items():
        if value == role:
            role_short = key

    # filter df by role of the player
    filtered = original_df[original_df["Ruolo"] == role_short]

    # return different stats for GoalKeepers
    if role_short == "P":
        filtered = filtered[filtered["Partite giocate"] > 5]
        # filtered = filtered[filtered["Goals subiti"] > 0]
        filtered = filtered.sort_values(by=["Goal subiti"], ascending=True)
        filtered = filtered.head(num)
        p_title = title + "<b> for number of goals conceded</b>"
        y_axis = dict(title="Goals conceded")
        return [{'name': ["Goal conceded", "Penalty blocked"], 'x': [filtered["Nome"], filtered["Nome"]],
                 'y': [filtered["Goal subiti"], filtered["Rigori parati"]],
                 }, {'title': p_title, 'yaxis': y_axis}]
    # return arg list to set x, y and chart title
    else:
        filtered = filtered[filtered["Goals tot"] > 0]
        filtered = filtered.sort_values(by=["Goals tot"], ascending=False)
        filtered = filtered.head(num)
        o_title = title + "<b> for number of goals scored</b>"
        y_axis = dict(title="Goals scored")
        return [{'name': ["Goal scored", "Penalty scored"], 'x': [filtered["Nome"], filtered["Nome"]],
                 'y': [filtered["Goal fatti"], filtered["Rigori segnati"]],
                 }, {'title': o_title, 'yaxis': y_axis}]


# FROM HERE ON, MAIN

parent_folder = Path.cwd().parent

season = 2019

data_url = "data/stats" + str(season) + ".csv"

filename = parent_folder / data_url

original_df = pd.read_csv(filename)

num_players_to_show = 20

title = "<b>Top " + str(num_players_to_show) + \
    " scorers of season " + str(season) + "-" + str(season + 1) + "</b>"
y_title = "Goals scored"

roles = {"P": "GoalKeepers",
         "D": "Defenders",
         "C": "Midfielders",
         "A": "Forwarders"}

initial_df = original_df[original_df["Goals tot"] > 0]
initial_df = initial_df.sort_values(by=["Goals tot"], ascending=False)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = go.Figure(data=[
    go.Bar(name='Goal scored', x=initial_df["Nome"].head(num_players_to_show),
           y=initial_df["Goal fatti"], marker_color='#0088E0'),
    go.Bar(name='Penalty scored', x=initial_df["Nome"].head(num_players_to_show),
           y=initial_df["Rigori segnati"], marker_color='#03B157')
])

fig.update_layout(barmode='stack', xaxis=dict(title_text="Name of players"),
                  yaxis=dict(title_text=y_title), title_text=title)

role_buttons = dict(
    buttons=list([
        dict(
            args=getDataByRole(role="P", num=num_players_to_show),
            label=roles["P"],
            method="update"
        ),
        dict(
            args=getDataByRole(role="D", num=num_players_to_show),
            label=roles["D"],
            method="update"
        ),
        dict(
            args=getDataByRole(role="C", num=num_players_to_show),
            label=roles["C"],
            method="update"
        ),
        dict(
            args=getDataByRole(role="A", num=num_players_to_show),
            label=roles["A"],
            method="update"
        )
    ]),
    active=-1,
    direction="down",
    showactive=True,
    x=0.05,
    xanchor="left",
    y=1.15,
    yanchor="top"
)

num_players_buttons = dict(
    buttons=list([
        dict(
            args=update_number(num=5),
            label="5",
            method="update"
        ),
        dict(
            args=update_number(num=10),
            label="10",
            method="update"
        ),
        dict(
            args=update_number(num=15),
            label="15",
            method="update"
        ),
        dict(
            args=update_number(num=20),
            label="20",
            method="update"
        )
    ]),
    active=3,
    direction="down",
    showactive=True,
    x=1,
    xanchor="right",
    y=1.15,
    yanchor="top"
)

fig.update_layout(
    updatemenus=[role_buttons, num_players_buttons]
)

fig.update_layout(annotations=[
    dict(text="Role:", x=0.005, xref="paper", y=1.13, yref="paper",
         align="left", showarrow=False),
    dict(text="  Number of players to show:", x=0.9, xref="paper", y=1.13,
         yref="paper", showarrow=False)
])


app.layout = html.Div(children=[
    html.H1(children='Welcome to our dashboard!'),

    html.Div(children='''
        Here, you can plot some stats about last Serie A season.
    '''),

    dcc.Graph(
        id='goals-graph',
        figure=fig
    )
])

# if __name__ == '__main__':
#    app.run_server(debug=True)
