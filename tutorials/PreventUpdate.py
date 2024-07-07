from dash import Dash, html, Input, Output, callback
from dash.exceptions import PreventUpdate
import webbrowser

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Button('Click here to see the content', id='show-secret'),
    html.Div(id='body-div')
])

@callback(
    Output('body-div', 'children'),
    Input('show-secret', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return "Elephants are the only animal that can't jump"

if __name__ == '__main__':
    port = 5081
    webbrowser.open(f'http://127.0.0.1:{port}/', new=0)
    app.run(debug=True, port=port)
