from dash import html

def render_header():
    return html.Div([
        html.H1("🚲 Understanding Bluebikes + MBTA Use", style={
            'textAlign': 'center',
            'marginTop': '20px'
        }),
        html.Hr()
    ])
