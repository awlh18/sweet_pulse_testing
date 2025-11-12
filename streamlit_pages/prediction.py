import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import datetime
from sklearn.metrics import mean_absolute_error
from src.feature_functions import *


today = datetime.datetime.now() - datetime.timedelta(hours=8)
day_of_week = today.strftime('%A')

#st.set_page_config(layout="wide")

# title 
#st.title('Sales Monitor')

st.markdown(f'### Today\'s date: {day_of_week}, {today.year}-{today.month}-{today.day}')

# define function to make API call for weather data 
def fetch_forecast():
    url = "https://api.weather.gc.ca/collections/citypageweather-realtime/items/bc-74"
    response = requests.get(url)
    data = response.json()

    forecasts = data['properties']['forecastGroup']['forecasts']

    # get forecast period 
    period = [forecasts[i]['period']['value']['en'] for i in range(len(forecasts))]

    # get forcast temperature 
    temps = [forecasts[i]['temperatures']['temperature'][0]['value']['en'] for i in range(len(forecasts))]

    # get accumulated rainfall at the beginning of the period 
    precip_start = [
    forecasts[i]
    .get('precipitation', {})
    .get('precipPeriods', [{}])[0]
    .get('start', {})
    .get('en', 0)
    for i in range(len(forecasts))
    ]

    # get accumulated rainfall at the end of the period 
    precip_end = [
    forecasts[i]
    .get('precipitation', {})
    .get('precipPeriods', [{}])[0]
    .get('end', {})
    .get('en', 0)
    for i in range(len(forecasts))
    ]

    # build forecast dataframe 
    forecast_df = pd.DataFrame({
    'period': period,
    'temps': temps,
    'precip_start': precip_start,
    'precip_end': precip_end
    })

    # get precipitation for the period 
    forecast_df['precipitation'] = forecast_df['precip_end'] - forecast_df['precip_start']

    # split period 
    forecast_df[['day', 'time']] = forecast_df['period'].str.extract(r'(\w+)\s*(night)?', expand=True)
    forecast_df['time'] = forecast_df['time'].fillna('day')
    forecast_df.drop(columns=['period'], inplace=True)

    # omit current day forecasts 
    if forecast_df.loc[0, 'time'] == 'night':
        forecast_df = forecast_df.iloc[1:]
    else:
        forecast_df = forecast_df.iloc[2:]

    forecast_df.reset_index(inplace=True, drop=True)

    return forecast_df

if "forecast_df" not in st.session_state:
    forecast_df = fetch_forecast()
    last_update = datetime.datetime.now() - datetime.timedelta(hours=8)

if st.button("🔄 Update Weather Data"):
    forecast_df = fetch_forecast()
    last_update = datetime.datetime.now() - datetime.timedelta(hours=8) 

st.write(f'Weather data as of: {last_update.strftime("%Y-%m-%d %H:%M:%S")}')

# calculate predictions 
temp_forecast_1 = np.mean([forecast_df.loc[0, 'temps'], forecast_df.loc[1, 'temps']])
temp_forecast_2 = np.mean([forecast_df.loc[2, 'temps'], forecast_df.loc[3, 'temps']])
temp_forecast_3 = np.mean([forecast_df.loc[4, 'temps'], forecast_df.loc[5, 'temps']])
temp_forecast_4 = np.mean([forecast_df.loc[6, 'temps'], forecast_df.loc[7, 'temps']])
temp_forecast_5 = np.mean([forecast_df.loc[8, 'temps'], forecast_df.loc[9, 'temps']])

precip_forecast_1 = np.sum([forecast_df.loc[0, 'precipitation'], forecast_df.loc[1, 'precipitation']])
precip_forecast_2 = np.sum([forecast_df.loc[2, 'precipitation'], forecast_df.loc[3, 'precipitation']])
precip_forecast_3 = np.sum([forecast_df.loc[4, 'precipitation'], forecast_df.loc[5, 'precipitation']])
precip_forecast_4 = np.sum([forecast_df.loc[6, 'precipitation'], forecast_df.loc[7, 'precipitation']])
precip_forecast_5 = np.sum([forecast_df.loc[8, 'precipitation'], forecast_df.loc[9, 'precipitation']])
    

st.markdown('### Five day forecasts:')

# side bar elements 
with st.sidebar:
    st.markdown('### Select forecasting inputs')

    with st.expander("One day forecast"):

        hours_1 = st.number_input(
            "Store opening hours", value=11, min_value=0, max_value=24, key="hours_1"
        )

        snow_1 = st.number_input(
            "What is the forecasted snow level?", value=0, min_value=0, max_value=100
        )

        is_long_weekend_1 = st.selectbox(
            "Is it a long weekend?", 
            (False, True),
            key="is_long_weekend_1"
        )

        is_HCF_1 = st.selectbox(
            "Is it Hot Chocolate Festival?", 
            (False, True),
            key="is_HCF_1"
        )

        is_ICF_1 = st.selectbox(
            "Is it Ice Cream Festival?", 
            (False, True),
            key='is_ICF_1'
        )

        is_holiday_1 = st.selectbox(
            "Is it a Holiday?", 
            (False, True),
            key='is_holiday_1'
        )

        competitor_1 = st.selectbox(
            "Is Competitor present today?", 
            (False, True),
            key='competitor_1'
        )
    
    with st.expander("Two day forecast"):

        hours_2 = st.number_input(
            "Store opening hours", value=11, min_value=0, max_value=24, key="hours_2"
        )

        snow_2 = st.number_input(
            "What is the forecasted snow level?", value=0, min_value=0, max_value=100, key='snow_2'
        )

        is_long_weekend_2 = st.selectbox(
            "Is it a long weekend?", 
            (False, True),
            key="is_long_weekend_2"
        )

        is_HCF_2 = st.selectbox(
            "Is it Hot Chocolate Festival?", 
            (False, True),
            key="is_HCF_2"
        )

        is_ICF_2 = st.selectbox(
            "Is it Ice Cream Festival?", 
            (False, True),
            key='is_ICF_2'
        )

        is_holiday_2 = st.selectbox(
            "Is it a Holiday?", 
            (False, True),
            key='is_holiday_2'
        )

        competitor_2 = st.selectbox(
            "Is Competitor present today?", 
            (False, True),
            key='competitor_2'
        )

    with st.expander("Three day forecast"):

        hours_3 = st.number_input(
            "Store opening hours", value=11, min_value=0, max_value=24, key="hours_3"
        )

        snow_3 = st.number_input(
            "What is the forecasted snow level?", value=0, min_value=0, max_value=100, key='snow_3'
        )

        is_long_weekend_3 = st.selectbox(
            "Is it a long weekend?", 
            (False, True),
            key="is_long_weekend_3"
        )

        is_HCF_3 = st.selectbox(
            "Is it Hot Chocolate Festival?", 
            (False, True),
            key="is_HCF_3"
        )

        is_ICF_3 = st.selectbox(
            "Is it Ice Cream Festival?", 
            (False, True),
            key='is_ICF_3'
        )

        is_holiday_3 = st.selectbox(
            "Is it a Holiday?", 
            (False, True),
            key='is_holiday_3'
        )

        competitor_3 = st.selectbox(
            "Is Competitor present today?", 
            (False, True),
            key='competitor_3'
        )

    with st.expander("Four day forecast"):


        hours_4 = st.number_input(
            "Store opening hours", value=11, min_value=0, max_value=24, key="hours_4"
        )

        snow_4 = st.number_input(
            "What is the forecasted snow level?", value=0, min_value=0, max_value=100, key='snow_4'
        )

        is_long_weekend_4 = st.selectbox(
            "Is it a long weekend?", 
            (False, True),
            key="is_long_weekend_4"
        )

        is_HCF_4 = st.selectbox(
            "Is it Hot Chocolate Festival?", 
            (False, True),
            key="is_HCF_4"
        )

        is_ICF_4 = st.selectbox(
            "Is it Ice Cream Festival?", 
            (False, True),
            key='is_ICF_4'
        )

        is_holiday_4 = st.selectbox(
            "Is it a Holiday?", 
            (False, True),
            key='is_holiday_4'
        )

        competitor_4 = st.selectbox(
            "Is Competitor present today?", 
            (False, True),
            key='competitor_4'
        )

    with st.expander("Five day forecast"):

        hours_5 = st.number_input(
            "Store opening hours", value=11, min_value=0, max_value=24, key="hours_5"
        )

        snow_5 = st.number_input(
            "What is the forecasted snow level?", value=0, min_value=0, max_value=100, key='snow_5'
        )

        is_long_weekend_5 = st.selectbox(
            "Is it a long weekend?", 
            (False, True),
            key="is_long_weekend_5"
        )

        is_HCF_5 = st.selectbox(
            "Is it Hot Chocolate Festival?", 
            (False, True),
            key="is_HCF_5"
        )

        is_ICF_5 = st.selectbox(
            "Is it Ice Cream Festival?", 
            (False, True),
            key='is_ICF_5'
        )

        is_holiday_5 = st.selectbox(
            "Is it a Holiday?", 
            (False, True),
            key='is_holiday_5'
        )

        competitor_5 = st.selectbox(
            "Is Competitor present today?", 
            (False, True),
            key='competitor_5'
        )

# load trained models 
with open("model/lr_pipe_net_sales.pkl", 'rb') as f:
        lr_pipe_net = pickle.load(f)

with open("model/lr_pipe_item_A_sales.pkl", 'rb') as f:
        lr_pipe_A = pickle.load(f)

with open("model/lr_pipe_item_B_sales.pkl", 'rb') as f:
        lr_pipe_B = pickle.load(f)

with open("model/pr_pipe_orders.pkl", 'rb') as f:
        pr_pipe = pickle.load(f)

# Making prediction - 1 day ahead 

day_1 = today + datetime.timedelta(days=1)
day_of_the_week_1 = day_1.strftime('%A')
season_1 = get_season(day_1)

data = {
 'hours_opened': hours_1,
 'avg_temperature': temp_forecast_1,
 'rain': precip_forecast_1,
 'snow': snow_1,
 'is_long_weekend': is_long_weekend_1,
 'HCF?': is_HCF_1,
 'ICF?': is_ICF_1,
 'season': season_1,
 'day_of_week': day_of_the_week_1,
 'is_holiday': is_holiday_1,
 'Kim\'s?': competitor_1}

input_df = pd.DataFrame(data, index=[0])

# show predictions

prediction_net = lr_pipe_net.predict(input_df)[0].astype(int)
prediction_A = lr_pipe_A.predict(input_df)[0].astype(int)
prediction_B = lr_pipe_B.predict(input_df)[0].astype(int)
prediction_order = pr_pipe.predict(input_df)[0].astype(int)

st.markdown(f'#### {day_of_the_week_1 }, {day_1.year}-{day_1.month}-{day_1.day}')
st.markdown(f'Forecast average temperature: **{temp_forecast_1}°C** |  Forecast precipitation: **{precip_forecast_1} mm**')

col_1_1, col_1_2, col_1_3, col_1_4 = st.columns(4)

with col_1_1:
    st.metric(label= "Net sales", value=f"${prediction_net:,}", border=True)

with col_1_2:
    st.metric(label= "Taiyaki sales", value=f"${prediction_A:,}", border=True)

with col_1_3:
    st.metric(label= "Soft serve sales", value=f"${prediction_B:,}", border=True)

with col_1_4:
    st.metric(label= "Total orders", value=f"{prediction_order}", border=True)

# Making prediction - 2 day head

day_2 = today + datetime.timedelta(days=2)
day_of_the_week_2 = day_2.strftime('%A')
season_2 = get_season(day_2)

data = {
 'hours_opened': hours_2,
 'avg_temperature': temp_forecast_2,
 'rain': precip_forecast_2,
 'snow': snow_2,
 'is_long_weekend': is_long_weekend_2,
 'HCF?': is_HCF_2,
 'ICF?': is_ICF_2,
 'season': season_2,
 'day_of_week': day_of_the_week_2,
 'is_holiday': is_holiday_2,
 'Kim\'s?': competitor_2}

input_df = pd.DataFrame(data, index=[0])

# show predictions

prediction_net = lr_pipe_net.predict(input_df)[0].astype(int)
prediction_A = lr_pipe_A.predict(input_df)[0].astype(int)
prediction_B = lr_pipe_B.predict(input_df)[0].astype(int)
prediction_order = pr_pipe.predict(input_df)[0].astype(int)

st.markdown(f'#### {day_of_the_week_2 }, {day_2.year}-{day_2.month}-{day_2.day}')
st.markdown(f'Forecast average temperature: **{temp_forecast_2}°C** |  Forecast precipitation: **{precip_forecast_2} mm**')

col_2_1, col_2_2, col_2_3, col_2_4 = st.columns(4)

with col_2_1:
    st.metric(label= "Net sales", value=f"${prediction_net:,}", border=True)

with col_2_2:
    st.metric(label= "Taiyaki sales", value=f"${prediction_A:,}", border=True)

with col_2_3:
    st.metric(label= "Soft serve sales", value=f"${prediction_B:,}", border=True)

with col_2_4:
    st.metric(label= "Total orders", value=f"{prediction_order}", border=True)

# Making prediction - 3 day head

day_3 = today + datetime.timedelta(days=3)
day_of_the_week_3 = day_3.strftime('%A')
season_3 = get_season(day_3)

data = {
 'hours_opened': hours_3,
 'avg_temperature': temp_forecast_3,
 'rain': precip_forecast_3,
 'snow': snow_3,
 'is_long_weekend': is_long_weekend_3,
 'HCF?': is_HCF_3,
 'ICF?': is_ICF_3,
 'season': season_3,
 'day_of_week': day_of_the_week_3,
 'is_holiday': is_holiday_3,
 'Kim\'s?': competitor_3}

input_df = pd.DataFrame(data, index=[0])

# show predictions

prediction_net = lr_pipe_net.predict(input_df)[0].astype(int)
prediction_A = lr_pipe_A.predict(input_df)[0].astype(int)
prediction_B = lr_pipe_B.predict(input_df)[0].astype(int)
prediction_order = pr_pipe.predict(input_df)[0].astype(int)

st.markdown(f'#### {day_of_the_week_3 }, {day_3.year}-{day_3.month}-{day_3.day}')
st.markdown(f'Forecast average temperature: **{temp_forecast_3}°C** |  Forecast precipitation: **{precip_forecast_3} mm**')

col_3_1, col_3_2, col_3_3, col_3_4 = st.columns(4)

with col_3_1:
    st.metric(label= "Net sales", value=f"${prediction_net:,}", border=True)

with col_3_2:
    st.metric(label= "Taiyaki sales", value=f"${prediction_A:,}", border=True)

with col_3_3:
    st.metric(label= "Soft serve sales", value=f"${prediction_B:,}", border=True)

with col_3_4:
    st.metric(label= "Total orders", value=f"{prediction_order}", border=True)

# Making prediction - 4 day head

day_4 = today + datetime.timedelta(days=4)
day_of_the_week_4 = day_4.strftime('%A')
season_4 = get_season(day_4)

data = {
 'hours_opened': hours_4,
 'avg_temperature': temp_forecast_4,
 'rain': precip_forecast_4,
 'snow': snow_4,
 'is_long_weekend': is_long_weekend_4,
 'HCF?': is_HCF_4,
 'ICF?': is_ICF_4,
 'season': season_4,
 'day_of_week': day_of_the_week_4,
 'is_holiday': is_holiday_4,
 'Kim\'s?': competitor_4}

input_df = pd.DataFrame(data, index=[0])

# show predictions

prediction_net = lr_pipe_net.predict(input_df)[0].astype(int)
prediction_A = lr_pipe_A.predict(input_df)[0].astype(int)
prediction_B = lr_pipe_B.predict(input_df)[0].astype(int)
prediction_order = pr_pipe.predict(input_df)[0].astype(int)

st.markdown(f'#### {day_of_the_week_4 }, {day_4.year}-{day_4.month}-{day_4.day}')
st.markdown(f'Forecast average temperature: **{temp_forecast_4}°C** |  Forecast precipitation: **{precip_forecast_4} mm**')

col_4_1, col_4_2, col_4_3, col_4_4 = st.columns(4)

with col_4_1:
    st.metric(label= "Net sales", value=f"${prediction_net:,}", border=True)

with col_4_2:
    st.metric(label= "Taiyaki sales", value=f"${prediction_A:,}", border=True)

with col_4_3:
    st.metric(label= "Soft serve sales", value=f"${prediction_B:,}", border=True)

with col_4_4:
    st.metric(label= "Total orders", value=f"{prediction_order}", border=True)

# Making prediction - 5 day head

day_5 = today + datetime.timedelta(days=5)
day_of_the_week_5 = day_5.strftime('%A')
season_5 = get_season(day_5)

data = {
 'hours_opened': hours_5,
 'avg_temperature': temp_forecast_5,
 'rain': precip_forecast_5,
 'snow': snow_5,
 'is_long_weekend': is_long_weekend_5,
 'HCF?': is_HCF_5,
 'ICF?': is_ICF_5,
 'season': season_5,
 'day_of_week': day_of_the_week_5,
 'is_holiday': is_holiday_5,
 'Kim\'s?': competitor_5}

input_df = pd.DataFrame(data, index=[0])

# show predictions

prediction_net = lr_pipe_net.predict(input_df)[0].astype(int)
prediction_A = lr_pipe_A.predict(input_df)[0].astype(int)
prediction_B = lr_pipe_B.predict(input_df)[0].astype(int)
prediction_order = pr_pipe.predict(input_df)[0].astype(int)

st.markdown(f'#### {day_of_the_week_5 }, {day_5.year}-{day_5.month}-{day_5.day}')
st.markdown(f'Forecast average temperature: **{temp_forecast_5}°C** |  Forecast precipitation: **{precip_forecast_5} mm**')

col_5_1, col_5_2, col_5_3, col_5_4 = st.columns(4)

with col_5_1:
    st.metric(label= "Net sales", value=f"${prediction_net:,}", border=True)

with col_5_2:
    st.metric(label= "Taiyaki sales", value=f"${prediction_A:,}", border=True)

with col_5_3:
    st.metric(label= "Soft serve sales", value=f"${prediction_B:,}", border=True)

with col_5_4:
    st.metric(label= "Total orders", value=f"{prediction_order}", border=True)