import math
import json
import pandas as pd
import pydeck as pdk
import streamlit as st
import geopandas as gpd


st.title("Provincial Demographics: The Migrant Ratio")


def determine_color(row):
    if row['Popolazione fine periodo'] > 0:
        percentage = row['percentage']

        # Non-linear scaling: Use a square root function to increase contrast
        scaled_percentage = math.sqrt((percentage - 1.6) / (20.62 - 1.6))  # Square root scaling

        # Calculate blue intensity (lower percentages start at white, higher at dark blue)
        blue_intensity = int(scaled_percentage * 255)

        return [255 - blue_intensity, 255 - blue_intensity, 255, 255]  # From white to dark blue
    else:
        return [200, 200, 200, 255]


@st.cache_data
def load_data():
    csv_data = pd.read_csv('data/STRASA_2022_en_Provinces.csv', skiprows=1)
    with open("data/limits_IT_provinces.geojson", 'r') as f:
        data = json.load(f)

    return csv_data, data

@st.cache_data
def load_population():
    csv_data = pd.read_csv('data/Bilancio_demografico_mensile.csv')
    return csv_data

csv_data, geojson_data = load_data()
population = load_population()

filtered_population = population[
    (population['Sesso'] == "Totale") &
    (population['Provincia'].isin(csv_data['Province']))
]

gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])

csv_data = csv_data[csv_data['Age'] == 999]
csv_data["All"] = csv_data["Males"] + csv_data["Females"]

combined_values_df = filtered_population.reset_index()
new_df = combined_values_df[['Provincia', 'Popolazione fine periodo']]


csv_data = csv_data.merge(new_df, left_on='Province', right_on='Provincia')

csv_data['Province code'] = csv_data['Province code'].astype(str)
csv_data['Province code'] = csv_data['Province code'].apply(lambda x: str(x).zfill(3))

gdf['prov_istat_code'] = gdf['prov_istat_code'].str.strip()

gdf.set_crs('epsg:4326', inplace=True)
gdf_projected = gdf.to_crs('epsg:32632')
gdf_projected['centroid'] = gdf_projected.geometry.centroid
centroids = gdf_projected['centroid'].to_crs('epsg:4326')

merged_data = gdf.merge(csv_data, left_on='prov_istat_code', right_on='Province code')

default_color = [255, 255, 255, 100]  # White color

merged_data["percentage"] = round(merged_data["All"] / merged_data["Popolazione fine periodo"] * 100, 2)
merged_data['color'] = merged_data.apply(determine_color, axis=1)
merged_data['color'] = merged_data['color'].apply(lambda x: x if x is not None else default_color)

st.write(f"Migrants' percent to the total population: from {min(merged_data['percentage'])} to {max(merged_data['percentage'])}")

merged_data['latitude'] = centroids.y
merged_data['longitude'] = centroids.x

def convert_geom(geom):
    if geom.geom_type == 'Polygon':
        return [list(geom.exterior.coords)]
    elif geom.geom_type == 'MultiPolygon':
        coords = []
        for part in geom.geoms:
            coords.append(list(part.exterior.coords))
        return coords
    return []

merged_data['polygon'] = merged_data.geometry.apply(convert_geom)

layer = pdk.Layer(
    'PolygonLayer',
    merged_data,
    get_polygon='polygon',
    get_fill_color='color',
    get_line_color=[255, 255, 255, 255],
    get_line_width=1,
    pickable=True,
    auto_highlight=True,
)

tooltip = {
    "html": "<b>{prov_name} ({prov_istat_code}): </b> {percentage}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

view_state = pdk.ViewState(latitude=merged_data['latitude'].mean(), longitude=merged_data['longitude'].mean(), zoom=5)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
)

st.pydeck_chart(r)
