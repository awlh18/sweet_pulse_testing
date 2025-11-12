import streamlit as st

st.set_page_config(layout="wide")

forecasts_page = st.Page("streamlit_pages/prediction.py", title="Forecasts", icon=":material/finance_mode:")
build_your_own_page = st.Page("streamlit_pages/build_your_own.py", title="Build Your Own Forecast", icon=":material/finance_mode:")
analytics_page = st.Page("streamlit_pages/analytics_test.py", title="Sales analytics", icon=":material/finance_mode:")
diagnostics_total_page = st.Page("streamlit_pages/diagnostics_net_sales.py", title="Model diagnostics - Net Sales", icon=":material/monitor_heart:")
diagnostics_item_A_page = st.Page("streamlit_pages/diagnostics_item_A.py", title="Model diagnostics - Taiyaki Sales", icon=":material/monitor_heart:")
diagnostics_item_B_page = st.Page("streamlit_pages/diagnostics_item_B.py", title="Model diagnostics - Soft serve Sales", icon=":material/monitor_heart:")
diagnostics_orders_page = st.Page("streamlit_pages/diagnostics_orders.py", title="Model diagnostics - In Store Orders", icon=":material/monitor_heart:")

pg = st.navigation({"Welcome to SweetPulse!":[forecasts_page, build_your_own_page ,analytics_page]})
pg.run()