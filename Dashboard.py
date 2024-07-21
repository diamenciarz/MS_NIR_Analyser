from dash import dash_table, Dash, dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import webbrowser
import pandas as pd
import numpy as np
import base64
import io
import json

# Create a special class that would save and load DataFrames into a json file


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = dbc.Container([
    dbc.Row([
        html.Div('Data, Graph, and Controls', className="text-primary text-center fs-3")
    ]),
    dbc.Row([
        dcc.Upload(
        id='upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
        ),
    ]),
    dbc.Row(dcc.Dropdown(["Empty"], "Empty", id="dropdown"), id="dropdown-div"),
    dbc.Row(id="graph-div"),
    dcc.Store(id='data-store')
], fluid=True)

def read_df(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if ".csv" in filename:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif ".xlsx" in filename:
        df = pd.read_excel(io.BytesIO(decoded))
    elif ".xls" in filename:
        df = pd.read_excel(io.BytesIO(decoded))
    
    df = df.set_index(df.columns[0])
    return df

@callback(Output('data-store', 'data'),
            Input('upload', 'contents'),
            State('upload', 'filename'),
            prevent_initial_call=True)
def save_data(list_of_contents, list_of_names):
        if list_of_contents is not None:
            data_frames = [read_df(c, n) for c, n in
                zip(list_of_contents, list_of_names)]
            df_dict = {name:df.to_json(date_format='iso', orient='split') for df, name in zip(data_frames, list_of_names)}
            
            return json.dumps(df_dict)

@callback(Output('dropdown-div', 'children'),
            Input('data-store', 'data'),
            prevent_initial_call=True)
def update_dropdown(json_data):
    df_dict = json.loads(json_data)
    list_of_names = list(df_dict.keys())
    children = dcc.Dropdown(list_of_names, list_of_names[0], id="dropdown")
    
    return children

def calculate_counts(df):
    # names, counts = df.index.value_counts()
    counts = df.index.value_counts()
    df_counts = pd.DataFrame(counts.sort_values()).reset_index()
    return df_counts

@callback(Output('graph-div', 'children'),
          Input('dropdown', 'value'),
          Input('data-store', 'data'),
          prevent_initial_call=True)
def update_table(filename, json_data):
    print("Dropdown", filename)
    df_dict = json.loads(json_data)
    if filename in df_dict.keys():
        json_df = df_dict[filename]
        df = pd.DataFrame(**json.loads(json_df))
        df_counts = calculate_counts(df)
        
        table = dash_table.DataTable(data=df_counts.to_dict('records'), columns=[{"name": i, "id": i} for i in df_counts.columns], id="tbl")
        return html.Div([html.H3(filename), table])

if __name__ == '__main__':
    port = 5081
    webbrowser.open(f'http://127.0.0.1:{port}/', new=0)
    app.run(debug=True, port=port)
