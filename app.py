from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import os
from pages.overview_tab import layout as overview_layout
from pages.multimodal_tab import layout as multimodal_layout

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # For Render deployment

# Define layout
app.layout = html.Div([
    html.H1("🚲 Understanding Bluebikes + MBTA Use", style={"textAlign": "center", "padding": "20px"}),
    
    dcc.Tabs(id="tabs", value="overview", children=[
        dcc.Tab(label="Bluebike Overview", value="overview"),
        dcc.Tab(label="Multimodal Comparison", value="multimodal")
    ]),

    html.Div(id="tab-content")
])

# Callback to switch tab content
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_content(tab):
    if tab == "overview":
        return overview_layout
    elif tab == "multimodal":
        return multimodal_layout
    return html.Div("404: Tab not found")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)