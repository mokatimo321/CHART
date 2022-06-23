# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 21:05:08 2022

@author: mohit
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

st.write("""
# TIMO -- Made by Mohit
""")

#uploaded_file1 = st.file_uploader("UPLOAD THE BANK NIFTY OR NIFTY DATA FILE for 2min", type=["csv"])
#df1 = pd.read_csv(uploaded_file1)

#uploaded_file2 = st.file_uploader("UPLOAD THE BANK NIFTY OR NIFTY DATA FILE for 5min", type=["csv"])
#df2 = pd.read_csv(uploaded_file2)

#uploaded_file3 = st.file_uploader("UPLOAD THE BANK NIFTY OR NIFTY DATA FILE for 15min", type=["csv"])
#df3 = pd.read_csv(uploaded_file3)


#df_list = []
index_name = ""
strike_type = ""
lot = 0
strike_name = ""

buy_string = ""
sell_string = ""
title = ""


cond_rsi = False
cond_rsi_time = 0
cnt = 0


#now to scan the 15 min df to complete buying
buy_flag = 0
buy_price = 0
cnt = 0

close_price = []
buy_time_list = []
buy_time = 0


#now to sell in the 5 min candle
net = 0
sell_price = 0
cnt = 0

closing_price = []
sell_time = []


rsi_signal_time = []


rsi_signal_string = ""
buy_signal_string = ""
sell_signal_string = ""


temp = 0

#input for rsi for buying
st.subheader('Enter the Value of RSI for Buying!!')
buy_rsi = st.number_input('RSI for Buying (0 to 100)', value=30)

#input for rsi for selling
st.subheader('Enter the Value of RSI for Selling!!')
sell_rsi = st.number_input('RSI for Selling (0 - 100)', value=68)

st.header('UPLOAD HERE!!!')
st.subheader("ATTENTION  -- Enter in sequence of 2min, 15min, 5min")


uploaded_files = st.file_uploader("UPLOAD THE BANK NIFTY OR NIFTY DATA FILE for 2min, 5min & 15min",type=['csv','csv','csv'], accept_multiple_files=True,)
for uploaded_file in uploaded_files:
    temp += 1
    if(temp == 1):
        df = pd.read_csv(uploaded_file)
        for i in df['strike']:
            strike_name = str(i)
            strike_name = strike_name.split(".")[0]
            break
        for i in df['instrument_type']:
            strike_type = str(i)
            break
        for i in df['name']:
            index_name = str(i)
        for i in df['lot_size']:
            lot = int(i)
            break

        for i in df['date']:
            rsi_signal_time.append(i[11:19])

        for i in df['rsi']:
            cnt += 1
            if(i <= buy_rsi):
                cond_rsi = True
                cond_rsi_time = cnt*2
                rsi_signal_string = "RSI Signal in 2 min activated at : " + str(rsi_signal_time[cnt - 1])
                break

    elif(temp == 2):

        df = pd.read_csv(uploaded_file)
        for i in df['close']:
            close_price.append(i)
        for i in df['date']:
            buy_time_list.append(i[11:19])

        cnt = 0

        for i in df['greencandle']:
            cnt += 1
            if(buy_flag == 0 and cond_rsi and cnt*15 >= cond_rsi_time and i == True):
                buy_flag = 1
                buy_price = close_price[cnt - 1]
                buy_time = cnt*15
                buy_signal_string = "Buy Signal in 15 min activated at : " + str(buy_time_list[cnt - 1])
                buy_string = str(buy_time_list[cnt - 1]) + " -> " + "Buy at " + str(buy_price)
                break

    else:
        df = pd.read_csv(uploaded_file)

        for i in df['date']:
            sell_time.append(i[11:19])
        for i in df['close']:
            closing_price.append(i)

        cnt = 0

        for i in df['rsi']:
            cnt += 1
            if(cnt*5 >= buy_time and buy_flag == 1 and i >= sell_rsi):
                sell_price = closing_price[cnt - 1]
                net += (sell_price - buy_price)*lot
                sell_string = str(sell_time[cnt - 1]) + " -> " + "Sell at " + str(sell_price)
                sell_signal_string = "Sell Signal in 5 min activated at : " + str(sell_time[cnt - 1])
                buy_flag = 0

        if(buy_flag == 1):
            sell_price = closing_price[73]
            net += (sell_price - buy_price)*lot
            sell_string = str(sell_time[73]) + " -> " + "Sell at " + str(sell_price) + " due to CutOff Time"
            sell_signal_string = "Sell Signal in 5 min activated at : " + str(sell_time[cnt - 1]) + " due to CutOff Time"

    #df = pd.read_csv(uploaded_file)
    #df_list.append(df)




#df1 = df_list[0]
#df2 = df_list[1]
#df3 = df_list[2]


if(st.button('START TRADING!!')):

    if(temp != 3):
        st.subheader("Please Upload the FIles properly and in Sequence!!!")
    else: 
        st.title(index_name + "  " + strike_name + "  " + strike_type)

        st.header("DETAILS OF ALL TRADES")

        #to scan for first signal in 2 min
        st.write(buy_string)
        st.write(sell_string)

        if(len(buy_string)>0):
            st.subheader("Net Profit : " + str(int(net) - 65) + " -- (Brokerage Included)")
            st.subheader("Max Fund Required : " + str(int(buy_price)*lot))

        st.write(rsi_signal_string)
        st.write(buy_signal_string)
        st.write(sell_signal_string)




st.caption("Mo's ALGO Pvt. Ltd.")