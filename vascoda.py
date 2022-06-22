# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 21:05:08 2022

@author: mohit
"""
import streamlit as st
import pandas as pd
#import plotly.graph_objects as go
#import os
#import webbrowser
from datetime import datetime
import base64

st.write("""
# CHART MAKER APP
""")


st.sidebar.header('User Input Features')

# Collects user input features into dataframe

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)      
    """fig = go.Figure(data=[go.Candlestick(x=input_df['date'],
                open=input_df['open'],
                high=input_df['high'],
                low=input_df['low'],
                close=input_df['close'])])

    fig.write_html("BN.html")
    webbrowser.open_new_tab("BN.html")"""
    st.markdown(filedownload(input_df), unsafe_allow_html=True)

st.subheader('CHART')
