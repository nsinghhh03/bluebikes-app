import pandas as pd
import plotly.express as px
import plotly.io as pio

# Load dataset
print("Loading Bluebike trip data...")
df = pd.read_csv("data/classifiedbluebike_trips.csv")
print(f"Loaded data with {len(df)} rows")

# Filter settings
selected_seasons = ['spring_fall', 'summer']
selected_weekday_types = ['Weekday', 'Saturday', 'Sunday']

# Apply filters
filtered_df = df[
    df['season'].isin(selected_seasons) &
    df['weekday_type'].isin(selected_weekday_types)
].copy()

# Shorten label
filtered_df['Short_Label'] = filtered_df['Trip_Classification'].replace(
    {'Complementary/Supplemental': 'Comp/Supp'}
)

# --- Donut Chart: Trip Classification Breakdown ---
classification_counts = (
    filtered_df['Short_Label']
    .value_counts()
    .reset_index(name='Count')
    .rename(columns={'index': 'Short_Label'})
)

donut_colors = ['#3B8EA5', '#6A5ACD', '#87CEFA', '#4B0082']

donut_fig = px.pie(
    classification_counts,
    names='Short_Label',
    values='Count',
    hole=0.5,
    color_discrete_sequence=donut_colors
)

donut_fig.update_traces(textposition='inside', textinfo='label+percent')
donut_fig.update_layout(
    title={'text': 'Trip Classification Breakdown', 'x': 0.5, 'xanchor': 'center'},
    title_font_size=20,
    legend_title_text='Classification Type'
)

pio.write_json(donut_fig, "data/bluebike_donut.json")
print("Saved donut chart to data/bluebike_donut.json")

# --- Heatmap: Trip Frequency by Hour and Weekday ---
if 'start_hour' in df.columns and 'weekday' in df.columns:
    heatmap_fig = px.density_heatmap(
        df,
        x='start_hour',
        y='weekday',
        title='Trip Frequency by Hour and Weekday',
        nbinsx=24,
        nbinsy=7,
        color_continuous_scale='Blues'
    )

    heatmap_fig.update_layout(
        title={
            'text': 'Trip Frequency by Hour and Weekday',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    pio.write_json(heatmap_fig, "data/bluebike_heatmap.json")
    print("Saved heatmap to data/bluebike_heatmap.json")
else:
    print("start_hour or weekday column not found. Heatmap not created.")

print("Precomputation complete.")
