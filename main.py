import streamlit as st
import pandas as pd
import numpy as np



calendar = st.sidebar.date_input('Pick a date')
date = st.sidebar.time_input('pick a time')
lat = st.sidebar.text_input('Latitude')
lon = st.sidebar.text_input('Longitude')



side1, side2 = st.beta_columns(2)
header = st.beta_container()

with header:
    st.title('Advanced bestest Weather Forecast')

with side1:
    st.header('Advanced bestest Weather Forecast')

with side2:
    st.header('Advanced bestest Weather Forecast2')

