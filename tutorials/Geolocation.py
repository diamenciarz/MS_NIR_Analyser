from dash import Dash, dcc, html, Input, Output, callback
import webbrowser

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Button("Update Position", id="update_btn"),
        dcc.Geolocation(id="geolocation"),
        html.Div(id="text_position"),
    ]
)

# When the button is pressed, update the geolocation meter
@callback(Output("geolocation", "update_now"), Input("update_btn", "n_clicks"))
def update_now(click):
    return True if click and click > 0 else False

# When the locaton is updated, update the text
@callback(
    Output("text_position", "children"),
    Input("geolocation", "local_date"),
    Input("geolocation", "position"),
)
def display_output(date, pos):
    if pos:
        return html.P(
            f"As of {date} your location was: lat {pos['lat']},lon {pos['lon']}, accuracy {pos['accuracy']} meters",
        )
    return "No position data available"


if __name__ == "__main__":
    port = 5081
    webbrowser.open(f'http://127.0.0.1:{port}/', new=0)
    app.run(debug=True, port=port)
