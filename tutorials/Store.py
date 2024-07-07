from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import webbrowser
import pandas as pd
import time

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Div(id="table"),
    dcc.Dropdown([3, 10, 5], 3, id='dropdown'),

    # dcc.Store stores the intermediate value
    dcc.Store(id='intermediate-value')
])

@callback(Output('intermediate-value', 'data'), Input('dropdown', 'value'))
def clean_data(value):
     # some expensive data processing step
     time.sleep(3)
     cleaned_df = pd.DataFrame([[value,value+1], [value-2, value*2]], index=["A", "B"], columns=["Sad", "Happy"])
     # more generally, this line would be
     return cleaned_df.to_json(date_format='iso', orient='split')

@callback(Output('graph', 'figure'), Input('intermediate-value', 'data'))
def update_graph(jsonified_cleaned_data):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    dff = pd.read_json(jsonified_cleaned_data, orient='split')

    figure = px.scatter(dff, x=dff.columns[0], y=dff.columns[1])
    return figure

@callback(Output('table', 'children'), Input('intermediate-value', 'data'))
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    return [dash_table.DataTable(data=dff.to_dict("records"), page_size=12, style_table={'overflowX': 'auto'})]

# Run the app
if __name__ == '__main__':
    port = 5080
    webbrowser.open(f'http://127.0.0.1:{port}/', new=0)
    app.run(debug=True, port=port)
    
