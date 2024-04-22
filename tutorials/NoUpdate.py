from dash import Dash, dcc, html, Input, Output, callback, no_update
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.P('Enter a composite number to see its prime factors'),
    # Debounce makes it that the script only runs once we un-click the input window
    dcc.Input(id='num', type='number', debounce=True, min=2, step=1),
    html.P(id='err', style={'color': 'red'}),
    html.P(id='out')
])

@callback(
    Output('err', 'children'),
    Output('out', 'children'),
    Input('num', 'value')
)
def show_factors(num):
    if num is None:
        # PreventUpdate prevents ALL outputs updating
        raise PreventUpdate

    factors = prime_factors(num)
    if len(factors) == 1:
        # dash.no_update prevents any single output updating
        # (note: it's OK to use for a single-output callback too)
        return '{} is prime!'.format(num), no_update

    return '', '{} is {}'.format(num, ' * '.join(str(n) for n in factors))

def prime_factors(num):
    n, i, out = num, 2, []
    while i * i <= n:
        if n % i == 0:
            n = int(n / i)
            out.append(i)
        else:
            # Increase i by 1 if i is 2 and n was not divisible by i.
            # Increase i by 2 if divisibility by 2 was already checked
            i += 1 if i == 2 else 2
    out.append(n)
    return out

if __name__ == '__main__':
    app.run(debug=True)
