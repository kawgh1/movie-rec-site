# movieRecFlask/plotlydash/dashboard1.py
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
from dash.dependencies import Input, Output


# Reference Documentation for Dash
# https://pypi.org/project/dash-bootstrap-components/
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/

# Connecting to PostgreSQL database
from sqlalchemy import create_engine


def create_dashboard(server):
    ##################################################################
    # - DEFAULT LOCAL HOST SETTINGS - check settings in run.py as well
    ##################################################################
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/recommender_db'
    ###################################################################
    # user = 'postgres'
    # password = 'password'
    # host = 'localhost'
    # port = '5432'
    # db = 'recommender_db'
    # url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)


    ##########################################################
    # - WEB HOST SETTINGS - check settings in run.py as well
    ##########################################################
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    ##########################################################
    import os
    url = os.environ['DATABASE_URL']

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

    """Create a Dash app."""
    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/dashapp/',
                         external_stylesheets=[dbc.themes.SLATE]
                         )

    # create postgres connection from Dash App
    con = create_engine(url)

    # Filling Dash Graph x and y values with method calls to get data from postgres

    # return the 'just_date' column
    def total_get_recs_rows_x():
        # # get-recs-clicks dataframe
        query1 = 'SELECT date, user_id FROM recsclicks;'
        df_total_get_recs_rows = pd.read_sql(query1, con)

        df_total_get_recs_rows['just_date'] = df_total_get_recs_rows['date'].dt.date

        return df_total_get_recs_rows['just_date']

    # return total_get_recs_rows which is # of rows in the table
    def total_get_recs_rows_y():
        # # get-recs-clicks dataframe
        query1 = 'SELECT date, user_id FROM recsclicks;'
        df_total_get_recs_rows = pd.read_sql(query1, con)

        df_total_get_recs_rows['just_date'] = df_total_get_recs_rows['date'].dt.date

        total_get_recs_rows = df_total_get_recs_rows.groupby([df_total_get_recs_rows.just_date.index,
                                                              df_total_get_recs_rows.user_id]).size()
        return total_get_recs_rows

    # Recommender Average Compatibility Score of Top Recommendation Graph
    # return the 'data' column

    def total_get_comp_rows_x():
        # # get-recs-clicks dataframe
        query3 = 'SELECT date, comp_score FROM recsclicks;'
        df_total_get_comps_rows = pd.read_sql(query3, con)

        # df_total_get_comps_rows['just_date'] = df_total_get_comps_rows['date'].dt.date

        return df_total_get_comps_rows['date']

        # return the current average compatibility score all top 1 recommendations

    def total_get_comp_rows_y():
        # # get-recs-clicks dataframe
        query1 = 'SELECT date, comp_score FROM recsclicks;'
        df_total_get_comps_rows = pd.read_sql(query1, con)

        x = df_total_get_comps_rows.expanding(min_periods=1)['comp_score'].mean()

        return x

    # Logins per day graph
    # return the 'just_date' column
    def total_get_logins_rows_x():
        query2 = 'SELECT date, userid FROM logins;'
        df_total_get_logins_rows = pd.read_sql(query2, con)

        df_total_get_logins_rows['just_date'] = df_total_get_logins_rows['date'].dt.date

        return df_total_get_logins_rows['just_date']

    # return total_get_logins_rows which is # of rows in the table
    def total_get_logins_rows_y():
        # total users over time dataframe from postgres server
        query2 = 'SELECT date, userid FROM logins;'
        df_total_get_logins_rows = pd.read_sql(query2, con)

        df_total_get_logins_rows['just_date'] = df_total_get_logins_rows['date'].dt.date

        total_get_logins_rows = df_total_get_logins_rows.groupby([df_total_get_logins_rows.just_date.index,
                                                                  df_total_get_logins_rows.userid]).size()
        return total_get_logins_rows

    # total users graph
    def total_users_over_time_x():
        query = 'SELECT id, registration_date FROM users;'
        df_users = pd.read_sql(query, con)

        return df_users['registration_date']

    def total_users_over_time_y():
        query = 'SELECT id, registration_date FROM users;'
        df_users = pd.read_sql(query, con)

        return df_users['id']



    # ----------------------------------------------------------------------------------------------------



# Begin Dash Layout

    navbar = dbc.NavbarSimple(
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

    # Dash app layout

    dash_app.layout = html.Div([navbar,

                                    html.Div([
                                            # graphs
                                            dcc.Graph(id='rec-clicks-per-day', relayoutData=False, style={'width': '95%', 'margin': '0 auto'}),
                                            dcc.Graph(id='average-comp-score-over-time', relayoutData=False, style={'width': '95%', 'margin': '0 auto'}),

                                            dcc.Graph(id='user-logins-per-day', relayoutData=False, style={'width': '95%','margin': '0 auto'}),
                                            dcc.Graph(id='total-users-over-time', relayoutData=False, style={'width': '95%', 'margin': '0 auto'}),

                                            dcc.Interval(id='interval-component',
                                                         # update graphs every interval = 1 hour = 3600000 milliseconds
                                                         interval=3600000,
                                                         n_intervals=0),

                                    ])

                                ])

    # The four callbacks below continuously update the graphs above
    # and define their layout, by using the methods at beginning of this file
    # to make data calls to the postgres server as data is updated from the
    # main site routes
    # Update rec-clicks-per-day graph
    @dash_app.callback(Output('rec-clicks-per-day', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def update_graph(n):


        fig = {
            'data': [
                go.Bar(
                    x=total_get_recs_rows_x(),
                    # y=df['userId'],
                    y=total_get_recs_rows_y(),
                    marker_color='salmon'
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
            )}

        return fig

    # Update average-comp-score-over-time graph
    @dash_app.callback(Output('average-comp-score-over-time', 'figure'),
                       [Input('interval-component', 'n_intervals')])
    def update_graph2(n):
        fig = {
            'data': [
                go.Scatter(
                    x=total_get_comp_rows_x(),
                    y=total_get_comp_rows_y(),
                    marker=dict(
                        line=dict(
                            color='blue',
                            width=10)))

            ],
            'layout': go.Layout(
                title='Average Compatibility Score Over Time',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Avg Comp Score of Top Recommendation'},
                hovermode='closest'

            )}
        return fig

    # Update user-logins-per-day graph
    @dash_app.callback(Output('user-logins-per-day', 'figure'),
                       [Input('interval-component', 'n_intervals')])
    def update_graph2(n):
        fig = {
            'data': [
                go.Bar(
                    x=total_get_logins_rows_x(),
                    # y=df['userId'],
                    y=total_get_logins_rows_y(),
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

            )}
        return fig

    # Update total-users-over-time graph
    @dash_app.callback(Output('total-users-over-time', 'figure'),
                       [Input('interval-component', 'n_intervals')])
    def update_graph1(n):
        fig = {
            'data': [
                go.Scatter(
                    x=total_users_over_time_x(),
                    y=total_users_over_time_y(),
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
            )}
        return fig

    return dash_app.server
