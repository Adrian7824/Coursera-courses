# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("c:/Users/52932/Downloads/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload]
    ),
    dcc.Graph(id='success-payload-scatter-chart'),
    dcc.Graph(id='success-pie-chart')
])

@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Mostrar un gráfico circular con el porcentaje de éxito para cada sitio de lanzamiento
        site_success_counts = spacex_df.groupby('Launch Site')['class'].mean()
        site_names = site_success_counts.index
        site_success_percent = site_success_counts * 100

        fig = px.pie(
            names=site_names,
            values=site_success_percent,
            title='Success Percentage by Launch Site',
        )
    else:
        # Filtrar el DataFrame para el sitio de lanzamiento seleccionado
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        total_success = len(site_data[site_data['class'] == 1])
        total_failed = len(site_data[site_data['class'] == 0])

        fig = px.pie(
            names=['Success', 'Failure'],
            values=[total_success, total_failed],
            title=f'Success/Failure for {selected_site}',
        )

    return fig
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, selected_payload_range):
    if selected_site == 'ALL':
        # Mostrar un gráfico de dispersión con Payload Mass (kg) vs. class (éxito/fracaso)
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                  (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Payload vs. Launch Outcome')
    else:
        # Filtrar el DataFrame para el sitio de lanzamiento seleccionado
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        filtered_data = site_data[(site_data['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                 (site_data['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f'Payload vs. Launch Outcome for {selected_site}')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)