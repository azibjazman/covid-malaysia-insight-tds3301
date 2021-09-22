import streamlit as st 
import numpy as np
import pandas as pd
import altair as alt 
from streamlit_folium import folium_static
import folium
import geopandas as gp

st.set_page_config(layout="wide") #Force Streamlit to go wide mode

df_map = gp.read_file('msia-states.json') #Geo-JSON file, a layer of Malaysia map with states taking boundaries
m = folium.Map([4.602973124617278, 108.64564992244625], zoom_start=5.5) #Interactive map. Map[centre code]


df_map['Cases'] = [1322,3456,2332,3432,2321,2223,6567,6762,5569,3870,9807,3498,5489,9870,10709,7790]
bins = list(df_map["Cases"].quantile([0, 0.5, 0.75, 0.95, 1]))

states = folium.Choropleth(
    geo_data=df_map, 
    data=df_map,
    key_on="feature.properties.name_1",
    columns=['name_1',"Cases"],
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="Cases",
    bins=bins,
    reset=True,
    ).add_to(m)


states.geojson.add_child(
    folium.features.GeoJsonTooltip(fields=['name_1', 'Cases'
                                           ],
                                    aliases=['State: ','Cases: '
                                             ])
)

folium.TileLayer('Stamen Terrain').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)
folium.TileLayer('Stamen Water Color').add_to(m)
folium.TileLayer('cartodbpositron').add_to(m)
folium.TileLayer('cartodbdark_matter').add_to(m)
folium.LayerControl().add_to(m)

folium_static(m)

make_map_responsive= """
 <style>
 [title~="st.iframe"] { width: 100%}
 </style>
"""
st.markdown(make_map_responsive, unsafe_allow_html=True)


