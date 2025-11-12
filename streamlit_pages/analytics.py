import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import datetime

#st.set_page_config(layout="wide")

today = datetime.datetime.now()

# title 
st.title('Analytics')

# read in data 
sales_df = pd.read_csv('data/processed/sales.csv', index_col=0, parse_dates=True)
sales_df['sales_per_order'] = sales_df['total_sales_normalized'] / sales_df['in_store_orders'] 
sales_df['month'] = sales_df.index.month_name()
sales_df[sales_df.select_dtypes(include='number').columns] = sales_df[sales_df.select_dtypes(include='number').columns].round(1)

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

with st.sidebar:
    st.markdown('### Select customization')
    day_range = st.selectbox(
        "Select day range for KPIs",
            [7, 14, 30, 90, 180],   
            index=1)
    
    aggregation_level = st.selectbox(
              "Select aggregation level for trend graphs",
              ('Weekly', 'Monthly')
         )

# if day_range == 'All':
#     input_df = sales_df 
# else:
#     input_df = sales_df.iloc[-day_range:]

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


# metric boxes 

## calculate figures 

### orders 
in_store_orders = sales_df['in_store_orders'].iloc[-day_range:].sum().astype(int)
ubereats_orders = sales_df['ubereats_orders'].iloc[-day_range:].sum().astype(int)
pickup_orders = sales_df['pickup_orders'].iloc[-day_range:].sum().astype(int)

### sales 
sales = sales_df['net_sales_normalized'].iloc[-day_range:].sum().astype(int)
sales_A = sales_df['item_A_sales'].iloc[-day_range:].sum().astype(int)
sales_B = sales_df['item_B_sales'].iloc[-day_range:].sum().astype(int)
sales_C = sales_df['item_C_sales'].iloc[-day_range:].sum().astype(int)

### sales per order 
total_sales = sales_df['net_sales_normalized'].iloc[-day_range:].sum()
total_orders = sales_df['in_store_orders'].iloc[-day_range:].sum()
sales_per_order = total_sales/total_orders

## calculate deltas compared to previous period 

### orders 
in_store_orders_last_period = sales_df['in_store_orders'].iloc[-day_range*2:-day_range].sum().astype(int)
ubereats_orders_last_period = sales_df['ubereats_orders'].iloc[-day_range*2:-day_range].sum().astype(int)
pickup_orders_last_period = sales_df['pickup_orders'].iloc[-day_range*2:-day_range].sum().astype(int)

in_store_orders_delta = in_store_orders - in_store_orders_last_period
in_store_orders_pct = (in_store_orders_delta / in_store_orders_last_period) * 100
in_store_orders_delta_text = f"{in_store_orders_delta:,.0f} ({in_store_orders_pct:+.1f}%)"

ubereats_orders_delta = ubereats_orders - ubereats_orders_last_period
ubereats_orders_pct = (ubereats_orders_delta / ubereats_orders_last_period) * 100
ubereats_orders_delta_text = f"{ubereats_orders_delta:,.0f} ({ubereats_orders_pct:+.1f}%)"

pickup_orders_delta = pickup_orders - pickup_orders_last_period
pickup_orders_pct = (pickup_orders_delta / pickup_orders_last_period) * 100
pickup_orders_delta_text = f"{pickup_orders_delta:,.0f} ({pickup_orders_pct:+.1f}%)"


### sales
sales_last_period = sales_df['net_sales_normalized'].iloc[-day_range*2:-day_range].sum().astype(int)
sales_A_last_period = sales_df['item_A_sales'].iloc[-day_range*2:-day_range].sum().astype(int)
sales_B_last_period = sales_df['item_B_sales'].iloc[-day_range*2:-day_range].sum().astype(int)
sales_C_last_period = sales_df['item_C_sales'].iloc[-day_range*2:-day_range].sum().astype(int)

sales_delta = sales - sales_last_period
sales_delta_pct = (sales_delta / sales_last_period) * 100
sales_order_delta_text = f"{sales_delta:,.0f} ({sales_delta_pct:+.1f}%)"

sales_A_delta = sales_A - sales_A_last_period
sales_A_delta_pct = (sales_A_delta / sales_A_last_period) * 100
sales_A_delta_text = f"{sales_A_delta:,.0f} ({sales_A_delta_pct:+.1f}%)"

sales_B_delta = sales_B - sales_B_last_period
sales_B_delta_pct = (sales_B_delta / sales_B_last_period) * 100
sales_B_delta_text = f"{sales_B_delta:,.0f} ({sales_B_delta_pct:+.1f}%)"

sales_C_delta = sales_C - sales_C_last_period
sales_C_delta_pct = (sales_C_delta / sales_C_last_period) * 100
sales_C_delta_text = f"{sales_C_delta:,.0f} ({sales_C_delta_pct:+.1f}%)"

orders_last_period = sales_df['in_store_orders'].iloc[-day_range*2:-day_range].sum()
sales_per_order_last_period = sales_last_period / orders_last_period
sales_per_order_delta = sales_per_order - sales_per_order_last_period
sales_per_order_delta_pct = (sales_per_order_delta / sales_per_order_last_period) * 100
sales_per_order_delta_text = f"{sales_per_order_delta:,.1f} ({sales_per_order_delta_pct:+.1f}%)"

st.markdown(f'#### Key Performance Metrics')
st.markdown(f'###### Last {day_range} days')
st.markdown('(Delta vs. preceding period)')

col_1_1, col_1_2, col_1_3, col_1_4 = st.columns(4)

with col_1_1:
      st.metric(label= f"Net sales - Total", value=f"${sales:,}", delta=sales_order_delta_text, border=True)

with col_1_2:
      st.metric(label=f"Net sales - A", value=f"${sales_A:,}", delta=sales_A_delta_text, border=True) 

with col_1_3:
     st.metric(label=f"Net sales - B", value=f"${sales_B:,}", delta=sales_B_delta_text, border=True)

with col_1_4: 
     st.metric(label=f"Net sales - C", value=f"${sales_C:,}", delta=sales_C_delta_text, border=True)


col_2_1, col_2_2, col_2_3, col_2_4 = st.columns(4)

with col_2_1:
      st.metric(label= f"In Store Orders", value=f"{in_store_orders:,}", delta=in_store_orders_delta_text, border=True)

with col_2_2:
      st.metric(label=f"Uber Orders", value=f"{ubereats_orders:,}", delta=ubereats_orders_delta_text, border=True) 

with col_2_3:
     st.metric(label=f"Pick Up Orders", value=f"{pickup_orders:,}", delta=pickup_orders_delta_text, border=True)

with col_2_4: 
     st.metric(label=f"Average Sale Per Order", value=f"${sales_per_order:,.1f}", delta=sales_per_order_delta_text, border=True)


# line trend graphs 
if aggregation_level == 'Weekly':
    agg='W'
else:
    agg='M'

core_product_sales = sales_df[['net_sales_normalized', 'item_A_sales', 'item_B_sales', 'item_C_sales']]

sales_trend_graph = make_trend_graph(core_product_sales, agg, height=320)
sales_trend_graph.update_layout(
    title=dict(
        text=f'{aggregation_level} sales trend',
        y=0.925),
    xaxis_title='Date',
    yaxis_title='Average daily net sales ($)',
    width=1230,
    height=400,
    legend=dict(
    orientation='h',         # horizontal
    yanchor='top',
    y=-0.1,                  # adjust vertical position
    xanchor='center',
    x=0.5                    # center the legend
    )
)
sales_trend_graph.update_yaxes(gridcolor="lightgrey")


#  line graph - number of orders vs sales per order trend 

grouped_df = sales_df.resample(agg).mean(numeric_only=True).round(1)
sales_spo = make_subplots(specs=[[{"secondary_y": True}]])
sales_spo.add_trace(go.Line(x=grouped_df.index, y=grouped_df['in_store_orders'], name='number of orders', mode='lines'))
sales_spo.add_trace(go.Line(x=grouped_df.index, y=grouped_df['sales_per_order'], name='sales per order', mode='lines', line=dict(color='red')), 
                    secondary_y=True)


sales_spo.update_layout(
    title=f'{aggregation_level} orders vs. sales per order',
    yaxis=dict(
        title='Orders'
    ),
    yaxis2=dict(
        title='Sales per order'
    ),
    width=1230,
    height=400,
    legend=dict(
        orientation='h',         # horizontal
        yanchor='top',
        y=-0.1,                  # adjust vertical position
        xanchor='center',
        x=0.5                    # center the legend
    )
)

sales_spo.update_yaxes( gridcolor="lightgrey")

col_2_1, col_2_2 = st.columns(2)

with col_2_1:
    st.plotly_chart(sales_trend_graph)

with col_2_2:
    st.plotly_chart(sales_spo)