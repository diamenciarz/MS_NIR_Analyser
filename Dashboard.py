from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

app = Dash(__name__)


app.layout = html.Div(
    [
        html.H1("Interactive color selection with simple Dash example"),
        html.P("Select color:"),
        dcc.Dropdown(
            id="dropdown",
            options=["Gold", "MediumTurquoise", "LightGreen"],
            value="Gold",
            clearable=False,
        ),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"),
)
def display_color(color):
    fig = go.Figure(go.Bar(x=["a", "b", "c"], y=[2, 3, 1], marker_color=color))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)