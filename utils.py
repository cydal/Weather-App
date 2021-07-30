import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import folium
import urllib.parse
import requests



def set_latlon(lat, lon, layout):
    with layout:
        lat, lon = float(lat), float(lon)

        m = folium.Map(location=[lat, lon], zoom_start=16)
        tooltip = "Liberty Bell"
        folium.Marker(
        [lat, lon], popup="Liberty Bell", 
        tooltip=tooltip).add_to(m)
        folium_static(m)


def calc_wind(u, v):
  ws = np.sqrt(u**2 + v*82)
  wd = np.mod(180+ np.rad2deg(np.arctan2(u, v)), 360)
  return([ws, wd])


def get_data(dataset, lat, lon):
  query = f"https://api.dclimate.net/apiv2/grid-history/{dataset}/{lat}_{lon}?also_return_metadata=false&use_imperial_units=true&also_return_snapped_coordinates=true&convert_to_local_time=true"
  response = requests.get(query)

  print(response.status_code)
  if response.status_code != 200:
    return("Error: Check location & dataset")

  data = response.json()
  first = list(data['data'].keys())[0]
  last = list(data['data'].keys())[-1]

  key, value = [], []
  for k in data['data']:
    key.append(k)
    # remove text 
    if data['data'][k]:
      value.append(data['data'][k].split(" ")[0])
    else:
      value.append(data['data'][k])

  df = pd.DataFrame({
                    "date_time": key,
                    "value": value
  })
  df["date_time"] = pd.to_datetime(df["date_time"])


  return(df)


def get_all_data(datasets, lat, lon):
  all_data = []

  for dataset in datasets:
    all_data.append(get_data(dataset, lat, lon))
  return(all_data)



def rain_classifier(value):

  if value == 0:
    return("No rain in the last hour")

  elif value > 0 and value<=0.05:
    return("It's drizzling a, an umbrella won't be a bad idea")

  elif value > 0.5 and value<=0.1:
    return("A light rain, you should go out with an umbrella")

  elif value > 0.1 and value<=0.3:
    return("Rain's quite heavy")

  else:
    return("Very heavy downpour, hope you are indoors")


def chance_of_flood(value):
  if value>0.1:
    return("There's a chance of flood")
  else:
    return("Little chance of flood")


def get_specific(query, all_data):

  for i, df_name in enumerate(datasets):
    df = all_data[i]
    if i == 4 or i == 5:
      query_d = pd.to_datetime(query).replace(second=0, microsecond=0, minute=0, hour=0)
      return_value = df["value"][df["date_time"] == query_d]
      if return_value.empty:
        return_value = "Data Not available"
      else:
        return_value = return_value.item()
    else:
      query_d = pd.to_datetime(query).replace(second=0, microsecond=0, minute=0)
      return_value = df["value"][df["date_time"].dt.tz_convert(None) == query_d]
      if return_value.empty:
        return_value = "Data Not available"
      else:
        return_value = return_value.item()

    returns[df_name] = return_value
