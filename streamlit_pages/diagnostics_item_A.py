import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import datetime
from sklearn.metrics import mean_absolute_error
from src.feature_functions import *


# model diagnostics
st.title('Regression model diagnostics - Taiyaki sales')

# load trained model 
with open("model/lr_pipe_item_A_sales.pkl", 'rb') as f:
        lr_pipe = pickle.load(f)

train_df = pd.read_csv('data/modelling/train.csv', index_col=0, parse_dates=True)
test_df = pd.read_csv('data/modelling/test.csv', index_col=0, parse_dates=True)

X_test = test_df.drop(columns=['taiyaki_sales'])
y_test = test_df['taiyaki_sales']
y_pred = lr_pipe.predict(X_test)
mae = round(mean_absolute_error(y_test, y_pred), 2)

st.markdown(f'Training data range: **{train_df.index.min().date()}** -- **{train_df.index.max().date()}**')
st.markdown(f'Test data range: **{test_df.index.min().date()}** -- **{test_df.index.max().date()}**')
st.markdown(f'Mean absolute error on test data = **{mae:.2f}**')

X_train = train_df.drop(columns=['taiyaki_sales'])
y_train = train_df['taiyaki_sales']

X_test = test_df.drop(columns=['taiyaki_sales'])
y_test = test_df['taiyaki_sales']

with open('results/lr_plot_item_A.pkl', 'rb') as f:
   lr_plot = pickle.load(f)

with open('results/resid_fit_plot_item_A.pkl', 'rb') as f:
   resid_fit_plot = pickle.load(f)

with open('results/resid_dist_plot_item_A.pkl', 'rb') as f:
   resid_dist_plot = pickle.load(f)

lr_plot.update_layout(
    title='Actual vs. prediction',
    xaxis_title="Date", 
    yaxis_title="Taiyaki sales ($)"
)

st.plotly_chart(lr_plot)

coef_df = pd.read_csv('results/trained_coef_item_A.csv')
coef_df[['coefficients']] = coef_df[['coefficients']].astype(int).applymap(lambda x: f"{x:,}")

mae_df = pd.read_csv('results/mae_grouped_item_A.csv')
mae_df[['taiyaki_sales', 'y_pred', 'prediction_error']] = mae_df[['taiyaki_sales', 'y_pred', 'prediction_error']].astype(int).applymap(lambda x: f"{x:,}")
mae_df[['error_percentage']] = mae_df[['error_percentage']].applymap(lambda x: f"{x:.1%}")

col_1_1, col_1_2 = st.columns(2)

with col_1_1:
    st.markdown('###### Model coefficients')
    st.dataframe(
        coef_df,
        column_config={
        'features': "Features",
        'coefficients': 'Coefficients'
    },
        hide_index=True
    )

with col_1_2: 
    st.markdown('###### Prediction error by day of the week')
    st.dataframe(
    mae_df,
    
    column_config={
        'day_of_week': "Day",
        'taiyaki_sales': 'Avg taiyaki sales',
        'y_pred': 'Avg prediction',
        'prediction_error': 'Avg error',
        'error_percentage': 'Error %'
    },
    hide_index=True
)

col_2_1, col_2_2 = st.columns(2)

with col_2_1:
    resid_fit_plot.update_layout(
       title='Model predictions vs. residuals',
       xaxis_title="Predicted values",
       yaxis_title="Residuals"
    )

    st.plotly_chart(resid_fit_plot)

with col_2_2:
    resid_dist_plot.update_layout(
    title='Distribution of residuals',
    xaxis_title="Residuals",
    yaxis_title="Count"
    )

    st.plotly_chart(resid_dist_plot)