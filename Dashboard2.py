from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import webbrowser
import pandas as pd
import base64
import io


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
        id='upload-table',
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
    # dbc.Row([
    #     dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
    #                    value='lifeExp',
    #                    inline=True,
    #                    id='radio-buttons-final')
    # ]),
    dbc.Row(id="graph-div"),
], fluid=True)

def parse_contents(contents, filename):
    print(filename)
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if ".csv" in filename:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif ".xlsx" in filename:
        df = pd.read_excel(io.BytesIO(decoded))
    elif ".xls" in filename:
        df = pd.read_excel(io.BytesIO(decoded))
    
    df = df.set_index(df.columns[0])
    df.index.name = "Y"
    fig = go.Figure()
    for i in range(df.shape[0]):
        fig.add_trace(go.Scatter(x=df.columns, y=df.iloc[i], name=str(df.index[i])))

    fig.update_layout(clickmode='event+select', title=filename)
    fig.update_xaxes(title_text="mz")
    fig.update_yaxes(title_text="Intensity")
    fig.update_traces(marker_size=20)
    return dcc.Graph(figure=fig, id='data-plot')
    

@callback(Output('graph-div', 'children'),
            Input('upload-table', 'contents'),
            State('upload-table', 'filename'),
            prevent_initial_call=True
            )
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

if __name__ == '__main__':
    port = 5081
    webbrowser.open(f'http://127.0.0.1:{port}/', new=1)
    app.run(debug=True, port=port)
