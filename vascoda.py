# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 21:05:08 2022

@author: mohit
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

import streamlit as st


st.write("""
# CHART MAKER APP
""")


st.sidebar.header('INPUT DATA FILE')

uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)      
    fig = go.Figure(data=[go.Candlestick(x=input_df['date'],
                open=input_df['open'],
                high=input_df['high'],
                low=input_df['low'],
                close=input_df['close'])])
    
    st.plotly_chart(fig)

