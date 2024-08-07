from dash import Dash, Input, Output, ctx, html, dcc, callback
import plotly.express as px
import plotly.graph_objects as go
import webbrowser

app = Dash(__name__)

app.layout = html.Div([
    html.Button('Draw Graph', id='draw'),
    html.Button('Reset Graph', id='reset'),
    dcc.Graph(id='graph')
])

@callback(
    Output('graph', 'figure'),
    Input('reset', 'n_clicks'),
    Input('draw', 'n_clicks'),
    prevent_initial_call=True
)
def update_graph(b1, b2):
    # We know how many times a button has been clicked but 
    print(b1, b2)
    triggered_id = ctx.triggered_id
    print(ctx.args_grouping)
    print(ctx.triggered_prop_ids)
    if triggered_id == 'reset':
         return reset_graph()
    elif triggered_id == 'draw':
         return draw_graph()

def draw_graph():
    df = px.data.iris()
    return px.scatter(df, x=df.columns[0], y=df.columns[1])

def reset_graph():
    return go.Figure()

if __name__ == '__main__':
    port = 5081
    webbrowser.open(f'http://127.0.0.1:{port}/', new=0)
    app.run(debug=True, port=port)
