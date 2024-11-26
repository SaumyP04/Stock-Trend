import yfinance as yf
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
startDate = "2022-09-10"
endDate = "2024-09-10"


#Need Data Prior to Start Date to show 2 year average
#download 300 days prior to start date to account for days market is closed
startDateDT = datetime.strptime(startDate, "%Y-%m-%d")
extendedStartDateDT = startDateDT - timedelta(days=400)
extendedStartDate = extendedStartDateDT.strftime("%Y-%m-%d")

st.title("Moving Average Stock Trend Predictor")

stockInput = st.text_input(
    label="Enter Stock", 
    placeholder="e.g. AAPL, TSLA, GOOGL...", 
    help="To Fetch Data Enter Stock"
)

enter = st.button("Show Data")



if enter:
    #Check if input is empty
    if stockInput:
        try:
            data = yf.download(stockInput, start=extendedStartDate, end=endDate)
            #if data is empty
            if data.empty:
                st.error("Please enter a valid stock")
            else:
                #Header and moving average calculation
                st.header(stockInput + " Graph With Moving Averages")
                data['50_MA'] = data['Close'].rolling(window=50).mean()
                data['200_MA'] = data['Close'].rolling(window=200).mean()

                #Graph and line
                fig, ax = plt.subplots(figsize=(16, 9))
                ax.plot(data.loc[startDate:]['Close'], label='Closing Price', color='blue')
                ax.plot(data.loc[startDate:]['50_MA'], label='50 Day MA', color='red')
                ax.plot(data.loc[startDate:]['200_MA'], label='200 Day MA', color='green')

                #Labels, Titles, and Legends
                ax.set_title(f'{stockInput.upper()} Stock Price and Moving Averages')
                ax.set_xlabel('Date')
                ax.set_ylabel('Price (USD)')
                ax.legend()
                ax.grid(True)

                #plot graph
                st.pyplot(fig)
        except Exception as e:
            st.error(f"Error occured: {e}")
    else:
        st.warning("Please enter a stock")
else:
    st.write("Enter Stock")



