import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import folium
import urllib.parse
import requests

from utils import * 

datasets = ["era5_wind_100m_u-hourly", "era5_wind_100m_v-hourly", "era5_land_precip-hourly", 
            "era5_volumetric_soil_water_layer_1-hourly", "cpcc_temp_min-daily", "cpcc_temp_max-daily"]


header = st.beta_container()
with header:
    st.title('Weather App')
    st.text('Pick time & location to begin')

side1, side2, side3, side4 = st.beta_columns(4)


calendar = st.sidebar.date_input('Pick a date')
date = st.sidebar.time_input('pick a time')
lat = st.sidebar.text_input('Latitude')
lon = st.sidebar.text_input('Longitude')


if st.sidebar.button("Use Lat & Lon"):
    set_latlon(lat, lon, header)

st.sidebar.text('OR')

address = st.sidebar.text_input('Address')

if st.sidebar.button("Use address"):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()
    lat, lon = response[0]["lat"], response[0]["lon"]
    set_latlon(lat, lon, header)


with side1:
    st.header('Temperature')
    st.text('Max Temperature')
    st.text('Min Temperature')


with side2:
    st.header('Precipitation')
    st.text('Chance of Rain %')


with side3:
    st.header('Soil Water Layer')
    st.text('Chance of Flood %')


with side4:
    st.header('Wind')
    st.text('Wind Speed')
    st.text('Wind Direction')
