# importing libraries
import dash
from dash import dcc   # contains Dash Core components to create elements such as graphs, dropdowns, sliders
from dash import html  # contains Dash HTML components to create and style HTML content
from dash.dependencies import Output, Input
import plotly.express as px  # used for creating graphs

# importing dataset from plotly
df = px.data.gapminder()
gapminder = df
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']  # CSS file used to format the webpage

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

gapminder2007 = gapminder.query('year == 2007')
# to describe layout of dashboard
app.layout = html.Div(children=[
    html.H1(
        "DashBoard for Country Statistics from 1952-2007"
        ,   # Main Heading),
    ),
    
    html.Div([
        # Placeholder to generate plotly figures
        
        dcc.Graph(id='earth Graph',figure=px.line_geo(df[df['year'] == 2007], locations='iso_alpha', color='continent', projection='orthographic')),
        dcc.Graph(id='bubble_graph',figure=px.scatter(gapminder2007, x='gdpPercap', y='lifeExp', color='continent', size='pop', size_max=60,hover_name='country')),
        dcc.Graph(id='voilen Graph',figure= px.scatter(gapminder, x='gdpPercap', y='lifeExp', color='continent', size='pop', size_max=60,hover_name='country', facet_col='continent')),
        dcc.Graph(id='voilen Graph2',figure= px.scatter(gapminder2007, x='pop', y='lifeExp', color='continent', size='pop', size_max=60,hover_name='country', facet_col='continent')),
        dcc.Graph(id='animated-graph',figure=px.scatter(gapminder, x='gdpPercap', y='lifeExp', color='continent', size='pop', size_max=40,hover_name='country', log_x=True, animation_frame='year',animation_group='country', range_x=[25, 10000], range_y=[25,90])),
        dcc.Graph(id='geo-graph',figure=px.choropleth(gapminder, locations='iso_alpha', color='lifeExp', hover_name='country',animation_frame='year', color_continuous_scale=px.colors.sequential.Plasma, projection='natural earth')),
        dcc.Graph(id='pie-plot america',figure=px.pie(df[(df['continent']=="Americas") & (df['year'] == 2007)].head(20), values='pop', names='country',title='Population of American continent',hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'}),className='five columns'),
        dcc.Graph(id='pie-plot europe',figure=px.pie(df[(df['continent']=="Europe") & (df['year'] == 2007)].head(20), values='pop', names='country',title='Population of European continent',hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'}),className='five columns'),
        dcc.Graph(id='pie-plot asia',figure=px.pie(df[(df['continent']=="Asia") & (df['year'] == 2007)].head(20), values='pop', names='country',title='Population of Asian continent',hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'}),className='five columns'),
        dcc.Graph(id='pie-plot africa',figure=px.pie(df[(df['continent']=="Africa") & (df['year'] == 2007)].head(20), values='pop', names='country',title='Population of African continent',hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'}),className='five columns'),

    html.Div(children=[
    html.Label("Country"),
        dcc.Dropdown(id='dpdn2', value=['India','China'], multi=True,options=[{'label': x, 'value': x} for x in df.country.unique()]),
        dcc.Graph(id='pie-graph', figure={}, className='five columns'),]),
        dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None,
                    config={
                        'staticPlot': False,
                        'scrollZoom': True,
                        'doubleClick': 'reset',
                        'showTips': False,
                        'displayModeBar': True,
                        'watermark': True,
                        },
                    className='five columns'
                    ),
        dcc.Graph(id='pie-chart-pop-continent',figure={},className='five columns'),
        dcc.Graph(id='my-graph2', figure={}, clickData=None, hoverData=None, 
                    config={
                        'staticPlot': False,     # True, False
                        'scrollZoom': True,      # True, False
                        'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                        'showTips': False,       # True, False
                        'displayModeBar': True,  # True, False, 'hover'
                        'watermark': True,
                        # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                            },
                    className='five columns',
                    ),

    ]),
])

# Here Callback function is automatically called by Dash whenever there is change in input component and output component is updated accordingly
@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
# Function for plotting gdp per capita vs year graph
def update_graph(country_chosen):
    dff = df[df.country.isin(country_chosen)]
    fig = px.line(data_frame=dff, x='year', y='gdpPercap', color='country',                                  # Plot Line graph
                  custom_data=['country', 'continent', 'lifeExp', 'pop'],title='Gdp per Capita(1952-2007)')
    fig.update_traces(mode='lines+markers')   # Update the figure
    return fig

@app.callback(
    Output(component_id='my-graph2', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph2(country_chosen):
    dff = df[df.country.isin(country_chosen)]
    fig = px.line(data_frame=dff, x='year', y='lifeExp', color='country',custom_data=['country', 'continent', 'gdpPercap', 'pop'],title="Life Expectancy Vs Year Graph")
    fig.update_traces(mode='lines+markers')
    return fig

# Callback Function for pie graph
@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='dpdn2', component_property='value')
)

# Function to plot pie chart
def update_side_graph(hov_data,country_chosen):
    if hov_data is None:
        dff2 = df[df.country.isin(country_chosen)]
        dff2 = dff2[dff2.year == 1952]
        fig2 = px.pie(data_frame=dff2, values='pop', names='country',title='Population for 1952')
        return fig2
    else:
        dff2 = df[df.country.isin(country_chosen)]
        hov_year = hov_data['points'][0]['x']
        dff2 = dff2[dff2.year == hov_year]
        fig2 = px.pie(data_frame=dff2, values='pop', names='country', title=f'Population for: {hov_year}')   # Plot pie chart
        return fig2

# Callback to plot second pir chart
@app.callback(
    Output(component_id='pie-chart-pop-continent', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph2', component_property='hoverData'),
    # Input(component_id='dpdn2', component_property='value'),
)
def update_pop_graph(hov_data,click_data):
    if hov_data is None:
        x = 2007
        df_cont_pop = df[df['year']==x].groupby(by='continent').sum().reset_index()
        fig3 = px.pie(data_frame=df_cont_pop,values='pop', names='continent',title='Continent Wise Population for 2007')
        return fig3

    else:
        hov_year = hov_data['points'][0]['x']
        df_cont_pop = df[df['year']==hov_year].groupby(by='continent').sum().reset_index()
        fig3 = px.pie(data_frame=df_cont_pop,values='pop', names='continent',title=f'Continent Wise Population for {hov_year}')

        return fig3
# Creating Server to run the dashboard
if __name__ == '__main__':
    app.run_server(debug=True)
