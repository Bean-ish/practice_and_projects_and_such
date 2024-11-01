# packages
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt


# import data
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year


# create app
app = dash.Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# layout
app.layout = html.Div(children = [
    
    html.H1(['Australia Wildfire Dashboard'], 
        style = {'textAlign': 'center', 'color': '#503D36','font-size': 26}),
        

    html.Div([

        html.Div([

            html.H2('Select Region:', style={'margin-right': '2em'}),
            
            dcc.RadioItems(
                id = 'region',
                options = [{"label":"New South Wales","value": "NSW"},
                            {"label":"Northern Territory","value": "NT"},
                            {"label":"Queensland","value": "QL"},
                            {"label":"South Australia","value": "SA"},
                            {"label":"Tasmania","value": "TA"},
                            {"label":"Victoria","value": "VI"},
                            {"label":"Western Australia","value": "WA"}],
                inline=True,
                value = 'NSW')
        ]),

        html.Div([

            html.H2('Select Year:', style={'margin-right': '2em'}),
            
            dcc.Dropdown(
                id = 'year',
                options = df.Year.unique(),
                value = 2005)
        ]),

        html.Div([
            dcc.Graph(id = 'plot1'),
            dcc.Graph(id = 'plot2')
        ], style={'display': 'flex'})
    ]),

])

# callback decorator and function
@app.callback(
    [Output(component_id = 'plot1', component_property = 'figure'),
    Output(component_id = 'plot2', component_property = 'figure')],
    [Input(component_id = 'region', component_property = 'value'),
    Input(component_id = 'year', component_property = 'value')]
    )

def update_figures(input_region, input_year):

    region_filter = df[df['Region'] == input_region]
    year_filter = region_filter[region_filter['Year'] == input_year]
    
    data1 = year_filter.groupby(['Month'])['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(
        data1, 
        names = 'Month', 
        values = 'Estimated_fire_area',
        title = "{} : Monthly Average Estimated Fire Area in year {}".format(input_region,input_year)
    )

    data2 =  year_filter.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(
        data2,
        x = 'Month',
        y = 'Count',
        title = '{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region,input_year)
    )

    return(fig1, fig2)


# start the server
if __name__ == '__main__':
    app.run_server()
