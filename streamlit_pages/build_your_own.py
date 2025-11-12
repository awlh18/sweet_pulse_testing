import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import datetime
from sklearn.metrics import mean_absolute_error
from src.feature_functions import *


today = datetime.datetime.now()

# side bar elements 
with st.sidebar:
    st.markdown('### Select inputs')

    with st.expander("Forecasting inputs"):

        day = st.date_input(
            "Forecast date",
            format='DD.MM.YYYY'
        )

        hours = st.number_input(
            "Store opening hours", value=11, min_value=0, max_value=24
        )

        temp = st.number_input(
            "What is the forecasted temperature?", value=5, min_value=-50, max_value=50
        )

        rain = st.number_input(
            "What is the forecasted rain level?", value=5, min_value=0, max_value=100
        )

        snow = st.number_input(
            "What is the forecasted snow level?", value=0, min_value=0, max_value=100
        )

        is_long_weekend = st.selectbox(
            "Is it a long weekend?", 
            (False, True)
        )

        is_HCF = st.selectbox(
            "Is it Hot Chocolate Festival?", 
            (False, True)
        )

        is_ICF = st.selectbox(
            "Is it Ice Cream Festival?", 
            (False, True)
        )

        is_holiday = st.selectbox(
            "Is it a Holiday?", 
            (False, True)
        )

        competitor = st.selectbox(
            "Is Competitor present today?", 
            (False, True)
        )
         
# Making prediction 
day_of_the_week = day.strftime('%A')
season = get_season(day)

data = {
 'hours_opened': hours,
 'avg_temperature': temp,
 'rain': rain,
 'snow': snow,
 'is_long_weekend': is_long_weekend,
 'HCF?': is_HCF,
 'ICF?': is_ICF,
 'season': season,
 'day_of_week': day_of_the_week,
 'is_holiday': is_holiday,
 'Kim\'s?': competitor}

input_df = pd.DataFrame(data, index=[0])

# loading in sales data for plots
sales_df = pd.read_csv('data/processed/sales.csv', index_col=0, parse_dates=True)
sales_df['sales_per_order'] = sales_df['net_sales_normalized'] / sales_df['in_store_orders']

# define plotting functions 
def make_line_graph(input_df, range, width=400, height=300): 
    graph = px.line(
        input_df.iloc[-range:,:], 
        width=width,   # set width in pixels
        height=height   # set height in pixels
)
    return graph

def make_trend_graph(input_df, agg, width=400, height=300): 
    graph = px.line(
        input_df.resample(agg).mean().round(1),
        width=width,
        height=height
    )
    
    return graph

# show predictions

# load pickles 
with open("model/lr_pipe_net_sales.pkl", 'rb') as f:
        lr_pipe_total = pickle.load(f)

with open("model/lr_pipe_item_A_sales.pkl", 'rb') as f:
        lr_pipe_A = pickle.load(f)

with open("model/lr_pipe_item_B_sales.pkl", 'rb') as f:
        lr_pipe_B = pickle.load(f)

with open("model/pr_pipe_orders.pkl", 'rb') as f:
        pr_pipe = pickle.load(f)

prediction_total = lr_pipe_total.predict(input_df)[0].astype(int)
prediction_A = lr_pipe_A.predict(input_df)[0].astype(int)
prediction_B = lr_pipe_B.predict(input_df)[0].astype(int)
prediction_order = pr_pipe.predict(input_df)[0].astype(int)

st.markdown('### Build your own forecast')
st.markdown('Select inputs from side bar to create your own forecast')

col_1_1, col_1_2, col_1_3, col_1_4 = st.columns(4)

with col_1_1:
    st.metric(label= "Net sales", value=f"${prediction_total:,}", border=True)

with col_1_2:
    st.metric(label= "Taiyaki sales", value=f"${prediction_A:,}", border=True)

with col_1_3:
    st.metric(label= "Soft serve sales", value=f"${prediction_B:,}", border=True)

with col_1_4:
    st.metric(label= "Total orders", value=f"{prediction_order}", border=True)


