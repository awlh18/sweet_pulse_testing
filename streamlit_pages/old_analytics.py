import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import datetime



today = datetime.datetime.now()

# title 
st.title('Analytics')

# read in data 
combined_df = pd.read_csv('data/processed/combined.csv', index_col=0, parse_dates=True)
combined_df['sales_per_order'] = combined_df['total_sales_normalized'] / combined_df['in_store_orders'] 
combined_df['month'] = combined_df.index.month_name()
combined_df[combined_df.select_dtypes(include='number').columns] = combined_df[combined_df.select_dtypes(include='number').columns].round(1)

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

with st.sidebar:
    st.markdown('### Select range')
    day_range = st.selectbox(
        "Select day range for analytics",
            ['All', 7, 30, 90, 180])

if day_range == 'All':
    input_df = combined_df 
else:
    input_df = combined_df.iloc[-day_range:]

# average sales table 
grouped_df = input_df.groupby('type_of_day').agg({
    'total_sales_normalized':['mean'],
    'tips_normalized':['mean'],
    'item_A_sales':['mean'],
    'item_B_sales':['mean'],
    'item_C_sales':['mean'],
    'sales_per_order': ['mean']
}).reset_index()

grouped_df.columns = ['Type of day','Total Sales', 'Tips', 'Item A sales', 'Item B sales', 'Item C sales', 'Sales per order']
grouped_df.set_index('Type of day', inplace=True)
grouped_df = grouped_df.reindex(['Weekday', 'Friday', 'Weekend', 'Holiday'], fill_value=0)

st.markdown('##### Average Sales by Type of Day')
st.table(grouped_df.style.format("{:.1f}"))

col_1_1, col_1_2 = st.columns(2)

with col_1_1:
         
    # sales per order vs number of orders by day of the week 

    rev_decomp = input_df.groupby('type_of_day').agg({
        'total_sales_normalized':['mean'],
        'sales_per_order':['mean'],
        'in_store_orders':['mean']
    }).round(2).reset_index()

    rev_decomp.columns = ['type_of_day', 'total_sales_normalized', 'sales_per_order', 'in_store_orders']
    rev_decomp.set_index('type_of_day', inplace=True)
    rev_decomp = rev_decomp.reindex(['Weekday', 'Friday', 'Weekend', 'Holiday'], fill_value=0)

    rev_decomp_fig = make_subplots(
        specs=[[{"secondary_y": True}]])

    rev_decomp_fig.add_trace(
        go.Bar(x=rev_decomp.index, 
            y=rev_decomp['in_store_orders'], 
            name='in-store orders',
            text=rev_decomp['in_store_orders'].round(0),
            textposition='inside',
            marker_color='darkorange'),
    )

    rev_decomp_fig.add_trace(
        go.Scatter(x=rev_decomp.index, 
                y=rev_decomp['sales_per_order'], 
                name='sales per order', 
                mode='lines+markers+text',
                text=rev_decomp['sales_per_order'].round(1),
                textposition='bottom center',
                line=dict(color='steelblue')), 
        secondary_y=True
    )

    rev_decomp_fig.update_layout(
        title=dict(
            text='In store orders vs. sales per order',
            y=0.95),
        yaxis=dict(
            title='# of orders'
        ),
        yaxis2=dict(
            title='Sales per order ($)'
        ),
        height=450,
        legend=dict(
            orientation='h',         # horizontal
            yanchor='top',
            y=-0.1,                  # adjust vertical position
            xanchor='center',
            x=0.5                    # center the legend
    ))

    st.plotly_chart(rev_decomp_fig)

# with col_1_2:
# # sales by day of week 
# st.markdown(f'#### Sales Distribution By Day Of Week')

# col_1_1, col_1_2 = st.columns(2)

# with col_1_1:
#     sales_by_day = px.box(input_df, 
#                           x='day_of_week', 
#                           y='total_sales_normalized', 
#                           color='is_holiday', 
#                           category_orders={'day_of_week': weekday_order}, 
#                           color_discrete_map={False: '#636EFA',  
#                                                True: '#EF553B'})

#     sales_by_day.update_layout(
#     title='Total sales',
#     xaxis_title='Day of week',
#     yaxis=dict(
#         title='Total sales ($)',
#         tickformat=','),
#     legend_title=dict(text='Holiday'))
#     sales_by_day.update_yaxes(gridcolor="lightgrey")

#     st.plotly_chart(sales_by_day)

with col_1_2:
    sales_by_day_A = px.box(input_df, 
                            x='day_of_week', 
                            y='item_A_sales', 
                            color='is_holiday', 
                            category_orders={'day_of_week': weekday_order},
                            color_discrete_map={False: '#636EFA',  
                                               True: '#EF553B'})
    sales_by_day_A.update_layout(
    title='Item A sales by day of week',
    xaxis_title='Day of week',
    yaxis=dict(
        title='Item A sales ($)',
        tickformat=','),
    legend_title=dict(text='Holiday'))
    sales_by_day_A.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(sales_by_day_A)

col_2_1, col_2_2 = st.columns(2)

with col_2_1:
   
    sales_by_day_B = px.box(input_df, 
                        x='day_of_week', 
                        y='item_B_sales', 
                        color='is_holiday', 
                        category_orders={'day_of_week': weekday_order},
                        color_discrete_map={False: '#636EFA',  
                                            True: '#EF553B'})
    sales_by_day_B.update_layout(
    title='Item B sales by day of week',
    xaxis_title='Day of week',
    yaxis=dict(
        title='Item B sales ($)',
        tickformat=','),
    legend_title=dict(text='Holiday'))
    sales_by_day_B.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(sales_by_day_B)

with col_2_2:
    sales_by_day_C = px.box(input_df, 
                        x='day_of_week', 
                        y='item_C_sales', 
                        color='is_holiday', 
                        category_orders={'day_of_week': weekday_order},
                        color_discrete_map={False: '#636EFA',  
                                            True: '#EF553B'})
    sales_by_day_C.update_layout(
    title='Item C sales by day of week',
    xaxis_title='Day of week',
    yaxis=dict(
        title='Item C sales ($)',
        tickformat=','),
    legend_title=dict(text='Holiday'))
    sales_by_day_C.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(sales_by_day_C)


# st.markdown(f'#### Orders & Sales Per Order By Day Of Week')

# col_3_1, col_3_2 = st.columns(2)

# with col_3_1:
#     order_by_day = px.box(input_df, 
#                     x='day_of_week', 
#                     y='in_store_orders', 
#                     color='is_holiday', 
#                     category_orders={'day_of_week': weekday_order},
#                     color_discrete_map={False: '#636EFA',  
#                                         True: '#EF553B'})
#     order_by_day.update_layout(
#     title='In store orders',
#     xaxis_title='Day of week',
#     yaxis=dict(
#         title='Number of orders',
#         tickformat=','),
#     legend_title=dict(text='Holiday'))
#     order_by_day.update_yaxes( gridcolor="lightgrey")

#     st.plotly_chart(order_by_day)

# with col_3_2:
#     sop_by_day = px.box(input_df, 
#                 x='day_of_week', 
#                 y='sales_per_order', 
#                 color='is_holiday', 
#                 category_orders={'day_of_week': weekday_order},
#                 color_discrete_map={False: '#636EFA',  
#                                     True: '#EF553B'})
#     sop_by_day.update_layout(
#     title='Sales per order',
#     xaxis_title='Day of week',
#     yaxis=dict(
#         title='Sales per order ($)',
#         tickformat=','),
#     legend_title=dict(text='Holiday'))
#     sop_by_day.update_yaxes(gridcolor="lightgrey")

#     st.plotly_chart(sop_by_day)

st.markdown(f'##### Hot Chocolate Festival Sales Impact')

col_4_1, col_4_2 = st.columns(2)

with col_4_1:
    input_df_winter = combined_df[combined_df['season'] == 'Winter']


    A_HCF = px.box(input_df_winter, 
                x='day_of_week', 
                y='item_A_sales', 
                color='is_HCF', 
                category_orders={'day_of_week': weekday_order},
                color_discrete_map={False: '#636EFA',  
                                    True: '#EF553B'})

    A_HCF.update_layout(
        title='Item A sales during HCF vs. rest of Winter',
        xaxis_title='Day of week',
        yaxis_title='Item A sales ($)',
        legend_title=dict(text='HCF'))
    A_HCF.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(A_HCF)

with col_4_2:
    combined_df_winter = combined_df[combined_df['month'] == 'February']

    B_HCF = px.box(input_df_winter, 
                x='day_of_week', 
                y='item_B_sales', 
                color='is_HCF', 
                category_orders={'day_of_week': weekday_order},
                color_discrete_map={False: '#636EFA',  
                                    True: '#EF553B'})

    B_HCF.update_layout(
        title='Item B sales during HCF vs. rest of Winter',
        xaxis_title='Day of week',
        yaxis_title='Item B sales ($)',
        legend_title=dict(text='HCF'))
    B_HCF.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(B_HCF)

