import json
import plotly.io as pio
from dash import html, dcc
import dash_bootstrap_components as dbc

# Load precomputed figures
with open("data/bluebike_donut.json", "r") as f:
    donut_fig = pio.from_json(json.dumps(json.load(f)))

with open("data/bluebike_heatmap.json", "r") as f:
    heatmap_fig = pio.from_json(json.dumps(json.load(f)))

with open("data/station_density_map_cleaned.json", "r") as f:
    density_map_fig = pio.from_json(json.dumps(json.load(f)))

with open("data/classification_by_density_cleaned.json", "r") as f:
    density_bar_fig = pio.from_json(json.dumps(json.load(f)))

with open("data/classification_by_hour_weekday2.json", "r") as f:
    hour_weekday_fig = pio.from_json(json.dumps(json.load(f)))

# Load KPI metrics
with open("data/kpi_summary.json", "r") as f:
    kpis = json.load(f)

# Styling for KPI cards
tile_color = "#e6f2ff"
tile_style = {
    "backgroundColor": tile_color,
    "height": "100%",
    "textAlign": "center",
    "padding": "15px"
}

tile_keys = [
    "Median Trip Duration (min)",
    "Most Popular Start Hour",
    "Most Popular Month",
    "Trips Near MBTA (%)",
    "Unique Stations"
]

kpi_cards = dbc.Row([
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H6(key, className="card-title"),
                html.H4(
                    f"{kpis[key] if not isinstance(kpis[key], float) else round(kpis[key], 2)}",
                    className="card-text"
                )
            ]),
            className="shadow-sm",
            style=tile_style
        ),
        width=2
    ) for key in tile_keys
], className="mb-4 justify-content-center")

# Layout
layout = html.Div([
    html.H3("Bluebike Trip Overview", style={"textAlign": "center", "paddingTop": "30px"}),

    html.P(
        "This section explores patterns in Bluebike trips, including how trip purposes vary by transit proximity, "
        "time of day, and weekday type. Trip classification refers to whether Bluebikes are used to connect to the MBTA (as a first or last mile solution), to supplement or complement transit routes, or independently of transit altogether.",
        style={"textAlign": "center", "maxWidth": "800px", "margin": "0 auto", "paddingBottom": "20px"}
    ),

    kpi_cards,

    # First row: Donut + Heatmap
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Graph(figure=donut_fig, config={"displayModeBar": True}, style={"height": "400px"}),
                html.Div([
                    html.Strong("Key Takeaway:"),
                    html.P(
                        "Most trips are complementary or supplemental to transit. Smaller shares serve as first or last mile connections, "
                        "highlighting how Bluebikes often replace full transit routes or support partial ones.",
                        style={"marginBottom": "0"}
                    )
                ], style={"padding": "10px 20px"})
            ], body=True, style={"boxShadow": "0 4px 8px rgba(0,0,0,0.05)"})
        ], width=6),

        dbc.Col([
            dbc.Card([
                dcc.Graph(figure=heatmap_fig, config={"displayModeBar": True}, style={"height": "400px"}),
                html.Div([
                    html.Strong("Key Takeaway:"),
                    html.P(
                        "Bluebike usage peaks during early morning and evening commute hours on weekdays, indicating integration with work-based travel.",
                        style={"marginBottom": "0"}
                    )
                ], style={"padding": "10px 20px"})
            ], body=True, style={"boxShadow": "0 4px 8px rgba(0,0,0,0.05)"})
        ], width=6)
    ], className="mb-4", justify="center"),

    # Second row: Station Density Map + Classification by Density Tier
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Graph(figure=density_map_fig, config={"displayModeBar": True}, style={"height": "500px"}),
                html.Div([
                    html.Strong("Key Takeaway:"),
                    html.P(
                        "Start station density is highest in Cambridge, indicating that more trips originate from these central nodes. "
                        "These stations act as key mobility anchors in the Bluebikes network.",
                    ),
                    html.Br(),
                    html.P(
                        "High-density clusters correspond with areas near universities, major employers, and MBTA hubs, where cycling is already normalized. "
                        "Their frequent use reinforces the centrality of Bluebikes in high-mobility zones."
                    ),
                    html.P(
                        "Peripheral stations with sparse usage, particularly in residential neighborhoods, could benefit from infrastructure investments "
                        "to expand accessibility in areas with less transit access as well."
                    )
                ], style={"padding": "10px 20px"})
            ], body=True, style={"boxShadow": "0 4px 8px rgba(0,0,0,0.05)"})
        ], width=6),

        dbc.Col([
            dbc.Card([
                dcc.Graph(figure=density_bar_fig, config={"displayModeBar": True}, style={"height": "500px"}),
                html.Div([
                    html.Strong("How we defined density:"),
                    html.P("Stations were binned into 'Low', 'Medium', and 'High' density tiers based on trip count quantiles (q=3)."),
                    html.Br(),
                    html.Strong("Key Insights:"),
                    html.Ul([
                        html.Li("Complementary/Supplemental trips dominate across all station density tiers."),
                        html.Li("First Mile usage is more common in low-density areas, where Bluebikes help bridge the gap to distant transit stops."),
                        html.Li("Last Mile usage rises in higher density stations, reflecting end-of-trip convenience.")
                    ])
                ], style={"padding": "10px 20px"})
            ], body=True, style={"boxShadow": "0 4px 8px rgba(0,0,0,0.05)"})
        ], width=6)
    ], justify="center", align="start", className="mb-4"),

    # Third row: Hourly Trip Distribution by Weekday
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Div([
                    dcc.Graph(figure=hour_weekday_fig, config={"displayModeBar": True}, style={"height": "550px"}),
                    html.Div([
                        html.Strong("What you're seeing:"),
                        html.P(
                            "Use the weekday slider to examine how trip types shift across each day. "
                            "The play button animates hourly patterns through the week, offering insight into temporal demand."
                        ),
                        html.P(
                            "Focus on when each trip type (e.g., First Mile, Last Mile) is most prevalent across weekdays versus weekends."
                        ),
                        html.Br(),
                        html.Strong("Key Insights:"),
                        html.Ul([
                            html.Li("On weekdays like Tuesday, First and Last Mile trips peak sharply at 8 AM and 5 PM—clearly aligned with commuting hours."),
                            html.Li("First Mile usage is especially dominant in the early morning, whereas Last Mile usage rises in the evening."),
                            html.Li("Saturday reveals a slower, extended midday peak from 11 AM to 5 PM, reflecting more flexible, non-work travel."),
                            html.Li("Transit Agnostic and Last Mile trips grow in both volume and share on weekends, suggesting use for leisure, errands, and varied destinations.")
                        ])
                    ], style={"padding": "10px 20px"})
                ])
            ], body=True, style={"boxShadow": "0 4px 8px rgba(0,0,0,0.05)", "marginBottom": "40px"})
        ], width=12)
    ], justify="center")
])