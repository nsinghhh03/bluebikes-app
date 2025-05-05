import dash
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

# Load data
multimodal_df = pd.read_csv("data/traveltimes.csv")

# --- Efficiency Map: Classify travel modes ---
def classify_mode(mode_str):
    mode_str = mode_str.upper()
    if mode_str == "BICYCLE":
        return "Bike Only"
    elif any(x in mode_str for x in ["SUBWAY", "BUS", "TRAM", "RAIL"]):
        return "Multimodal"
    elif "WALK" in mode_str:
        return "Bike + Walk"
    else:
        return "Other"

multimodal_df = multimodal_df.dropna(subset=["origin_lat", "origin_lon", "modes_used_multimodal"])
multimodal_df["mode_category"] = multimodal_df["modes_used_multimodal"].apply(classify_mode)
multimodal_df = multimodal_df[multimodal_df["mode_category"] != "Other"]

color_map = {
    "Bike Only": "#2E86DE",
    "Bike + Walk": "#A569BD",
    "Multimodal": "#FF0000"
}

# Create Efficiency Map figure
efficiency_fig = go.Figure()
for mode in multimodal_df["mode_category"].unique():
    subset = multimodal_df[multimodal_df["mode_category"] == mode]
    efficiency_fig.add_trace(go.Scattermapbox(
        lat=subset["origin_lat"],
        lon=subset["origin_lon"],
        mode="markers",
        marker=dict(size=6, color=color_map[mode], opacity=0.7),
        name=mode,
        text=subset["mode_category"],
        hoverinfo="text"
    ))

efficiency_fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        zoom=10.5,
        center=dict(lat=42.3601, lon=-71.0589)
    ),
    title=dict(
        text="Bike vs Multimodal Efficiency",
        x=0.5,
        xanchor="center",
        font=dict(size=22)
    ),
    legend=dict(
        title=dict(text="Mode Category", font=dict(size=16)),
        font=dict(size=14),
        x=0.01, y=0.01,
        xanchor="left", yanchor="bottom"
    ),
    margin=dict(r=0, l=0, b=0, t=50),
    template=None
)

# --- Longest Trips Map: Top 30% by mode ---
modes = {
    "Bike Only": "bike_duration",
    "Walk + Transit": "walktransit_duration",
    "Multimodal": "multimodal_duration"
}

mode_traces = []
visibility = [True, False, False]

for i, (label, duration_col) in enumerate(modes.items()):
    df = multimodal_df.dropna(subset=[duration_col])
    threshold = df[duration_col].quantile(0.7)
    df_top = df[df[duration_col] >= threshold]

    trace = go.Scattermapbox(
        lat=df_top["origin_lat"],
        lon=df_top["origin_lon"],
        mode="markers",
        marker=dict(
            size=10,
            color=df_top[duration_col],
            colorscale="Blues",
            colorbar=dict(title="Duration (min)"),
            opacity=0.85,
            cmin=df_top[duration_col].min(),
            cmax=df_top[duration_col].max()
        ),
        name=label,
        text=[f"{label}: {d:.1f} min" for d in df_top[duration_col]],
        hoverinfo="text",
        visible=visibility[i]
    )
    mode_traces.append(trace)

dropdown_buttons = [
    dict(label=label, method="update", args=[
        {"visible": [j == i for j in range(len(modes))]},
        {"title": f"Origins of Top 30% Longest {label} Trips"}
    ]) for i, label in enumerate(modes)
]

longest_trips_fig = go.Figure(data=mode_traces)
longest_trips_fig.update_layout(
    mapbox_style="carto-positron",
    mapbox=dict(zoom=10.5, center=dict(lat=42.36, lon=-71.06)),
    updatemenus=[dict(
        buttons=dropdown_buttons,
        direction="down",
        showactive=True,
        x=0.01, xanchor="left",
        y=0.98, yanchor="top"
    )],
    title=dict(
        text="Origins of the Top 30% Longest Trips by Mode",
        x=0.5, xanchor="center"
    ),
    margin=dict(r=0, t=60, l=0, b=0),
    height=600,
    template=None
)

# --- Dash Layout ---
layout = html.Div([
    html.H2("Multimodal Travel Comparison", style={"textAlign": "center", "marginBottom": "10px"}),

    html.P(
        "This dashboard explores how different travel modes perform across Metro Boston, "
        "highlighting areas where multimodal integration may fall short.",
        style={"textAlign": "center", "fontSize": "16px", "marginBottom": "4px"}
    ),
    html.P("\ud83d\udc4b Hover over the map to view trip durations and labels.",
           style={"textAlign": "center", "fontSize": "15px", "fontStyle": "italic", "marginBottom": "30px"}),

    html.Div([
        html.Div([
            html.H5("Mode Efficiency by Area", style={"marginBottom": "6px"}),
            dcc.Markdown("""
            **Takeaways:**  
            - Trips farther from downtown are more often more efficient on **Bike** than multimodal travel, 
              showing limited public transit access in outer areas.  
            - **Bike + Transit** routes dominate the city core, signaling strong Bluebike and MBTA integration in 
              dense, high-service neighborhoods like Downtown and Cambridge.
            """, style={"padding": "8px 12px"}),
            dcc.Graph(figure=efficiency_fig),
        ], style={
            "width": "48%",
            "display": "inline-block",
            "verticalAlign": "top",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            "padding": "8px",
            "borderRadius": "10px",
            "marginRight": "2%"
        }),

        html.Div([
            html.H5("Top 30% Longest Trips by Mode", style={"marginBottom": "6px"}),
            dcc.Markdown("""
            **Directions:** Use the dropdown to choose a mode and explore where it takes the longest to complete — 
            the map shows the top 30% longest trips for each mode.

            **Insights:**  
            - **Bike Only** has longer trips even in downtown zones, with more dark blue markers.  
            - **Walk + Transit** is slowest around Somerville and outlying neighborhoods.  
            - **Multimodal** trips are particularly inefficient along the Green Line near BU and Allston.
            """, style={"padding": "8px 12px"}),
            dcc.Graph(figure=longest_trips_fig),
        ], style={
            "width": "48%",
            "display": "inline-block",
            "verticalAlign": "top",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            "padding": "8px",
            "borderRadius": "10px"
        }),
    ])
])
