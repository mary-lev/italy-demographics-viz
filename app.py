import numpy as np
import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import pydeck as pdk


def determine_color(row):
    # Apply a non-linear scaling - logarithmic in this case
    # Adding 1 to avoid log(0) which is undefined
    male_count = np.log(row['Males'] + 1)
    max_log_males = np.log(max_males + 1)
    red_intensity = int(male_count / max_log_males * 255)
    return [red_intensity, 0, 0, 255]

@st.cache_data
def load_data():
    csv_data = pd.read_csv('data/STRASA_2021_en_Municipalities.csv', skiprows=1)
    with open("combined_geojson.geojson", 'r') as f:
        data = json.load(f)

    return csv_data, data

csv_data, geojson_data = load_data()

gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])

csv_data = csv_data[csv_data['Age'] == 999]
csv_data["All"] = csv_data["Males"] + csv_data["Females"]

csv_data['Municipality code'] = csv_data['Municipality code'].astype(str)
csv_data['Municipality code'] = csv_data['Municipality code'].apply(lambda x: str(x).zfill(6))

gdf['com_istat_code'] = gdf['com_istat_code'].str.strip()

gdf.set_crs('epsg:4326', inplace=True)

gdf_projected = gdf.to_crs('epsg:32632')
gdf_projected['centroid'] = gdf_projected.geometry.centroid
centroids = gdf_projected['centroid'].to_crs('epsg:4326')

merged_data = gdf.merge(csv_data, left_on='com_istat_code', right_on='Municipality code')
max_males = merged_data['Males'].max()
default_color = [255, 255, 255, 100]  # White color

merged_data['color'] = merged_data.apply(determine_color, axis=1)
# Assuming 'color' is the column with the assigned colors
merged_data['color'] = merged_data['color'].apply(lambda x: x if x is not None else default_color)

st.title('Municipality Data Visualization')

merged_data['latitude'] = centroids.y
merged_data['longitude'] = centroids.x

def convert_geom(geom):
    if geom.geom_type == 'Polygon':
        # For a single Polygon, return its exterior coordinates
        return [list(geom.exterior.coords)]
    elif geom.geom_type == 'MultiPolygon':
        # For MultiPolygon, extract each polygon part
        all_coords = []
        for part in geom.geoms:
            all_coords.append(list(part.exterior.coords))
        return all_coords
    return []


# Apply conversion to each geometry
merged_data['polygon'] = merged_data.geometry.apply(convert_geom)
#merged_data["polygon"] = merged_data.geometry

tooltip = {
    "html": "<b>{name} ({com_istat_code}): </b> {All}",  # Adjust according to your DataFrame columns
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

layer = pdk.Layer(
    'PolygonLayer',
    merged_data,  # or json_data if you converted it to JSON
    get_polygon='polygon',
    get_fill_color='color',
    get_line_color=[255, 255, 255, 255],
    get_line_width=1,
    pickable=True,
    auto_highlight=True,
)


view_state = pdk.ViewState(
    latitude=merged_data['latitude'].mean(),
    longitude=merged_data['longitude'].mean(),
    zoom=10
)

r = pdk.Deck(
    layers=layer,
    initial_view_state=view_state,
    tooltip=tooltip  # Define the tooltip as per your requirement
)


st.pydeck_chart(r)


