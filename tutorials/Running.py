from dash import Dash, dcc, html, Input, Output, State, callback
import time

app = Dash(__name__)

# There is input, button and text
app.layout = html.Div([
    html.Div(dcc.Input(id='input-on-submit-text', type='text')),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='container-output-text',
             children='Enter a value and press submit')
])


@callback(
    # Change the text message
    Output('container-output-text', 'children'),
    # When button clicked
    Input('submit-button', 'n_clicks'),
    # using the value from the Input field to the function
    State('input-on-submit-text', 'value'),
    prevent_initial_call=True,
    # Set the parameter "disabled" from "submit-button" to True for 5 seconds and False - afterwards
    running=[(Output("submit-button", "disabled"), True, False)]
)
def update_output(n_clicks, value):
    time.sleep(5)
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks 
    )


if __name__ == '__main__':
    app.run(debug=True)
