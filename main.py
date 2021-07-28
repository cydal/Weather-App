import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import folium
import urllib.parse
import requests

from utils import * 


header = st.beta_container()
with header:
    st.title('Weather App')
    st.text('Enter Location to begin')

side1, side2, side3, side4 = st.beta_columns(4)


calendar = st.sidebar.date_input('Pick a date')
date = st.sidebar.time_input('pick a time')
lat = st.sidebar.text_input('Latitude')
lon = st.sidebar.text_input('Longitude')


if st.sidebar.button("Use Lat & Lon"):
    set_latlon(lat, lon, side1)

st.sidebar.text('OR')

address = st.sidebar.text_input('Address')

if st.sidebar.button("Use address"):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()
    lat, lon = response[0]["lat"], response[0]["lon"]
    set_latlon(lat, lon, side1)


with side2:
    st.text(calendar)


with side3:
    st.header(date)

