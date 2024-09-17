import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from financialstatementfunctions import generate_tabs

def FinVista():
    st.title("FinVista Analyzer")
    st.write("Welcome to FinVista Analyzer – Your Gateway to Financial Insight!")
    st.write("Empower your financial decision-making with our streamlined and intuitive application designed for in-depth analysis of publicly traded companies.")
    st.write("Whether you're an investor, financial analyst, or simply curious about a company's financial health, FinVista Analyzer puts essential financial data at your fingertips.")
    st.write('FinVista connects to Yahoos Finance API to bring you up to date Financial Data')
    st.divider()
    st.header("Let's get started! Choose which companies you wish to compare:")
    # Mapping display values to ticker symbols
    company_tickers = {
        "Apple": "AAPL",
        "Google": "GOOG",
        "Nvidia": "NVDA",
        "Microsoft": "MSFT"
    }

    ## Financials sections
    # Create a list to store user selections
    selected_tickers = []
    # Display the multiselect dropdown menu with display values
    selected_tickers = st.multiselect("Select companies:", list(company_tickers.keys()),default=['Apple','Microsoft'])
    # Convert display values to ticker symbols
    selected_ticker_symbols = [company_tickers[company] for company in selected_tickers]

    generate_tabs(selected_ticker_symbols)

    #st.divider()
    ########################################## Ratio Section and Further Analysis
    #generate_ratio_tabs(selected_ticker_symbols)


