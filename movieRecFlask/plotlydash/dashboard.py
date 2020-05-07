"""Create a Dash app within a Flask app."""
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import dash_bootstrap_components as dbc
# pip install dash-bootstrap-components

from movieRecFlask.plotlydash import dashdata



# https://pypi.org/project/dash-bootstrap-components/
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/

# Connecting to PostgreSQL database
from sqlalchemy import create_engine
# Local Settings
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/recommender_db'
# user = 'postgres'
# password = 'password'
# host ='localhost'
# port ='5432'
# db = 'recommender_db'
# url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

# Webhost Setting (Heroku)
import os
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

url = os.environ['DATABASE_URL']


def create_dashboard(server):



    """Create a Dash app."""
    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/dashapp/',
                         external_stylesheets=[dbc.themes.SLATE]
                         )

    # total users over time dataframe from postgres server
    query = 'SELECT id, registration_date FROM users;'
    con = create_engine(url)
    df_users = pd.read_sql(query, con)

    # get-recs-clicks dataframe
    df = pd.read_csv('movieRecFlask/plotlydash/dashdata/recs-clicked.csv', parse_dates=['date'])
    total_get_recs_rows = df.groupby([df.date.index, df.userId]).size()

    # logins dataframe
    df_logins = pd.read_csv('movieRecFlask/plotlydash/dashdata/logins.csv', parse_dates=['date'])
    total_get_logins_rows = df_logins.groupby([df_logins.date.index, df_logins.userId]).size()

    nav = dbc.NavbarSimple(
        children=[
            # These Navlinks need to be coded with 'external_link=True'
            # Otherwise, Dash will not link out of itself back to the Flask app/website
            dbc.NavItem(dbc.NavLink("Home", external_link=True, href="/home")),
            dbc.NavItem(dbc.NavLink("Dashboard", href="/dashapp/")),
            dbc.NavItem(dbc.NavLink("About", external_link=True, href="/about")),
            dbc.NavItem(dbc.NavLink("Data", external_link=True, href="/data")),
            # Not using this, saving for reference
            # dbc.DropdownMenu(
            #     children=[
            #         dbc.DropdownMenuItem("More pages", header=True),
            #         dbc.DropdownMenuItem("Page 2", href="#"),
            #         dbc.DropdownMenuItem("Page 3", href="#"),
            #      ],
            #     nav=True,
            #     in_navbar=True,
            #     label="More",
            # ),
        ],
        brand="Movie Recommender: Dashboard",
        brand_href="/dashapp/",
        color="primary",
        dark=True,

    )

    dash_app.layout = html.Div([nav,


        # first scatter plot object
                                dcc.Graph(
                                    id='rec-clicks-per-day',
                                    figure={
                                        'data': [
                                            go.Bar(
                                                x=df['date'],
                                                #y=df['userId'],
                                                y=total_get_recs_rows,
                                                marker_color = 'salmon'
                                                # marker=dict(
                                                #     line=dict(
                                                #         width=35)),

                                            )

                                        ],
                                        'layout': go.Layout(
                                            title='Number of "Get Recs!" clicks per day',
                                            xaxis={'title': 'Date'},
                                            yaxis={'title': 'Number of Recommendations'},

                                            hovermode='closest'
                                        )}),

                                dcc.Graph(
                                    id='total-users-over-time',
                                    figure={
                                        'data': [
                                            go.Scatter(
                                                x=df_users['registration_date'],
                                                y=df_users['id'],
                                                marker=dict(
                                                    line=dict(
                                                        color='mediumspringgreen',
                                                        width=10))

                                            )

                                        ],
                                        'layout': go.Layout(
                                            title='Total Users over Time',
                                            xaxis={'title': 'Date'},
                                            yaxis={'title': 'Total Users'},
                                            hovermode='closest'
                                        )}),

                                dcc.Graph(
                                    id='user-logins-per-day',
                                    figure={
                                        'data': [
                                            go.Bar(
                                                x=df_logins['date'],
                                                #y=df['userId'],
                                                y=total_get_logins_rows,
                                                marker_color='indianred'
                                                # marker=dict(
                                                #     line=dict(
                                                #         color='deeppink',
                                                #         width=30)),

                                            )

                                        ],
                                        'layout': go.Layout(
                                            title='Number of User Logins per day',
                                            xaxis={'title': 'Date'},
                                            yaxis={'title': 'Number of Logins'},
                                            hovermode='closest'

                                        )})

                                ]

                               )

    return dash_app.server
