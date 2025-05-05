from dash import dcc

def render_tabs():
    return dcc.Tabs(id="tabs", value="overview", children=[
        dcc.Tab(label="Bluebike Overview", value="overview"),
        dcc.Tab(label="Multimodal Comparison", value="multimodal"),
    ])
