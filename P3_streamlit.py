#Import Dependencies 
import numpy as np
from pathlib import Path
import requests
import json
import pandas as pd
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation
import plotly.graph_objects as go
from datetime import datetime
import matplotlib
import streamlit as st
import plotly.express as px 

#title of streamlit app 
st.image("https://i.imgur.com/dUCvdG7.png")
st.info("Find educational resources by expanding the sidebar to the left.")
#Important initial variables 
stock = st.text_input('Please enter a stock ticker and click "Grade this stock!"')

stock_score = 0
missing_ratios = 0 

############### API INFORMATION ######################

#Alpaca API key and secret key 
#hardcoded temporarily for convenience
alpaca_api_key = "PK2E1G7V4QCB3SHLL3I8"
alpaca_secret_key = "22pJHmdw6fIv0EihrhuaaL9VAzqcKyVgS1qyTSUz"
type(alpaca_secret_key)

#alpaca REST object
alpaca = tradeapi.REST(alpaca_api_key, alpaca_secret_key, api_version="v2")


#TD Ameritrade API setup  
td_consumer_key = 'YXGDGMF1UR0KBX7H77MZJS2WLN7PXYIK'
trading_endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes'
trading_url = trading_endpoint.format(stock_ticker=stock)

trade_page = requests.get(url=trading_url, params={'apikey': td_consumer_key})
trade = json.loads(trade_page.content)

endpoint = 'https://api.tdameritrade.com/v1/instruments?apikey=YXGDGMF1UR0KBX7H77MZJS2WLN7PXYIK&symbol={stock_ticker}&projection=fundamental'
full_url = endpoint.format(stock_ticker=stock)

page = requests.get(url=full_url, params={'apikey': td_consumer_key})
content = json.loads(page.content)

quote_endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes'
quote_url = quote_endpoint.format(stock_ticker=stock)

quote_page = requests.get(url=quote_url, params={'apikey': td_consumer_key})
quote = json.loads(quote_page.content)


################################ SIDEBAR #########################################

st.sidebar.markdown("## Links for Learning")
st.sidebar.write("[Stock Market Basics](https://www.investopedia.com/articles/investing/082614/how-stock-market-works.asp)")
st.sidebar.write("[Candlestick Charts](https://www.investopedia.com/trading/candlestick-charting-what-is-it/)")
st.sidebar.write("[Monte Carlo Simulations](https://www.investopedia.com/terms/m/montecarlosimulation.asp)")
st.sidebar.write("[Cumulative Return](https://www.investopedia.com/terms/c/cumulativereturn.asp)")
st.sidebar.write("[Financial Ratios](https://www.investopedia.com/articles/stocks/06/ratios.asp)")
st.sidebar.write("[Market Risk](https://www.investopedia.com/terms/m/marketrisk.asp)")
st.sidebar.write("[Time Value of Money](https://www.investopedia.com/terms/t/timevalueofmoney.asp)")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")

st.sidebar.write("Carefully consider investment objectives, risks, charges and expenses before investing.")

#################### STOCK GRADER ###########################
if st.button("Grade this stock!"):
    try: 
        stock = str.upper(stock)
        #alpaca variables/data for MCSimulation and graphs
        start_date = pd.Timestamp("2017-01-01", tz="America/New_York").isoformat()
        end_date = pd.Timestamp("2021-12-31", tz="America/New_York").isoformat()

        limit_rows = 1000

        prices = alpaca.get_barset(stock,
                                timeframe='1D',
                                start=start_date,
                                end=end_date,
                                limit=limit_rows).df

        prices_MC = alpaca.get_barset(stock,
                                timeframe='1D',
                                start=start_date,
                                end=end_date,
                                limit=limit_rows).df
    ################## CURRENT STOCK INFO AND CANDLESTICK ######################## 

        last_price = quote[stock]['lastPrice']
        high_today = quote[stock]["highPrice"]
        low_today = quote[stock]["lowPrice"]
        high52 = quote[stock]["52WkHigh"]
        low52 = quote[stock]["52WkLow"]
        last_price = round(last_price, 2)
        st.markdown(f"### The most recent price of {stock} is {last_price} USD.")
        st.write(f"Today, the price of {stock} has ranged from ${low_today} to ${high_today}.")
        st.write(f"Over the last year, the price of {stock} has ranged from ${low52} to {high52}.")

        prices = prices.reset_index()
        prices.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

        st.markdown(f"## Candlestick Chart for {stock}")

        fig = go.Figure(data=[
            go.Candlestick(x=prices['date'],
                        open=prices['open'],
                        high=prices['high'],
                        low=prices['low'],
                        close=prices['close'])
        ])

        fig.update_layout(xaxis_rangeslider_visible=True,
                        margin=dict(l=20, r=20, t=20, b=20),
                        width=800,
                        height=500)

        st.plotly_chart(fig, use_container_width=False, sharing="streamlit")
        

    #####################################################
        

        #Price-to-earnings ratio
        if 13 <= content[stock]['fundamental']['peRatio'] <= 15:
            stock_score += 1 
        elif content[stock]['fundamental']['peRatio'] > 15:
            stock_score += 2
        elif content[stock]['fundamental']['peRatio'] < 13:
            stock_score = stock_score
        if content[stock]['fundamental']['peRatio'] == 0:
            missing_ratios += 1
            

        #Price/Earnings to Growth pegRatio
        if content[stock]['fundamental']['pegRatio'] < 1:
            stock_score = stock_score
        elif content[stock]['fundamental']['pegRatio'] >= 1:
            stock_score += 2
        if content[stock]['fundamental']['pegRatio'] == 0:
            missing_ratios += 1

        #Price to Book Ratio pbRatio
        if content[stock]['fundamental']['pbRatio'] <= 1:
            stock_score += 2
        elif 1 < content[stock]['fundamental']['pbRatio'] <= 3:
            stock_score += 1
        elif content[stock]['fundamental']['pbRatio'] > 3:
            stock_score = stock_score
        if content[stock]['fundamental']['pbRatio'] == 0:
            missing_ratios += 1
    
        #Current Ratio
        if 1 <= content[stock]['fundamental']['currentRatio'] <= 3:
            stock_score += 2
        elif content[stock]['fundamental']['currentRatio'] > 3:
            stock_score += 1
        elif content[stock]['fundamental']['currentRatio'] < 1:
            stock_score = stock_score
        if content[stock]['fundamental']['currentRatio'] == 0:
            missing_ratios += 1
        
        #Quick Ratio
        if (1 / 2) <= content[stock]['fundamental']['quickRatio'] <= 1:
            stock_score += 1
        elif content[stock]['fundamental']['quickRatio'] > 1:
            stock_score += 2
        elif content[stock]['fundamental']['quickRatio'] < (1 / 2):
            stock_score = stock_score
        if content[stock]['fundamental']['quickRatio'] == 0:
            missing_ratios += 1
        
        #Debt-to-Equity Ratio
        if content[stock]['fundamental']['totalDebtToEquity'] > 2:
            stock_score = stock_score
        elif 2 > content[stock]['fundamental']['totalDebtToEquity'] > 1:
            stock_score += 1
        elif content[stock]['fundamental']['totalDebtToEquity'] <= 1:
            stock_score += 2
        if content[stock]['fundamental']['totalDebtToEquity'] == 0:
            missing_ratios += 1

        #Net profit margin netProfitMarginMRQ
        if content[stock]['fundamental']['netProfitMarginMRQ'] >= 20:
            stock_score += 2
        elif 5 <= content[stock]['fundamental']['netProfitMarginMRQ'] <= 10:
            stock_score += 1
        elif content[stock]['fundamental']['netProfitMarginMRQ'] < 5:
            stock_score = stock_score
        if content[stock]['fundamental']['netProfitMarginMRQ'] == 0:
            missing_ratios += 1

        #Return on Equity  returnOnEquity
        if content[stock]['fundamental']['returnOnEquity'] >= 15:
            stock_score += 2
        elif content[stock]['fundamental']['returnOnEquity'] < 15:
            stock_score = stock_score
        if content[stock]['fundamental']['returnOnEquity'] == 0:
            missing_ratios += 1

        #Gross Margin  grossMarginMRQ
        if 50 <= content[stock]['fundamental']['grossMarginMRQ'] <= 60:
            stock_score += 2
        elif content[stock]['fundamental']['grossMarginMRQ'] > 60:
            stock_score += 1
        elif content[stock]['fundamental']['grossMarginMRQ'] < 50:
            stock_score = stock_score
        if content[stock]['fundamental']['grossMarginMRQ'] == 0:
            missing_ratios += 1
        
        #Operating Margin operatingMarginMRQ
        if content[stock]['fundamental']['operatingMarginMRQ'] >= 15:
            stock_score += 2
        elif content[stock]['fundamental']['operatingMarginMRQ'] < 15:
            stock_score = stock_score
        elif content[stock]['fundamental']['operatingMarginMRQ'] == 0:
            missing_ratios += 1


        #Return on Assets returnOnAssets
        if content[stock]['fundamental']['returnOnAssets'] >= 5:
            stock_score += 2
        elif content[stock]['fundamental']['returnOnAssets'] < 5:
            stock_score = stock_score
        if content[stock]['fundamental']['returnOnAssets'] == 0:
            missing_ratios += 1

        #Beta beta
        if content[stock]['fundamental']['beta'] == 1:
            stock_score += 2
        elif content[stock]['fundamental']['beta'] < 1:
            stock_score += 1
        elif content[stock]['fundamental']['beta'] > 1:
            stock_score = stock_score
        if content[stock]['fundamental']['beta'] == 0:
            missing_ratios += 1

        #Final score output & suggestion
        st.markdown(f"### The score for {stock} is {stock_score} out of 24.*")

        if stock_score >= 18:
            st.write("### This company has good financial health. Recommendation: Invest!")
            st.image("https://i.imgur.com/8QcL9wZ.png", width=300)
        elif 12 <= stock_score < 18:
            st.write(
                "### This company's financial health is so-so. Recommendation: Be careful!")
            st.image("https://i.imgur.com/aDZNNpw.png", width=300)
            
        elif stock_score < 12:
            st.write(
                "### This company may may have poor financial health. Recommendation: Choose a different stock")
            st.image("https://i.imgur.com/GYHL9RG.png", width=300)
        if missing_ratios > 0: 
            st.markdown(f"#### {stock}'s score is missing information for {missing_ratios} out of 12 criteria. {stock}'s true score may be higher.")

        ################# MONTE CARLO SIMULATION ######################
        
      
        with st.spinner("Please be patient as we try to predict the future."):
            
            from MCForecastTools import MCSimulation
            
            MC_fiveyear = MCSimulation(portfolio_data=prices_MC,
                                    weights=[1.00],
                                    num_simulation=500,
                                    num_trading_days=252 * 5)

            MC_fiveyear_df = MC_fiveyear.calc_cumulative_return()
            # MC_fiveyear.calc_cumulative_return()
            
            MC_sim_line_plot = MC_fiveyear.plot_simulation()


            MC_summary_statistics = MC_fiveyear.summarize_cumulative_return()

            ci_95_lower_cumulative_return = MC_summary_statistics[8] * 10000
            ci_95_upper_cumulative_return = MC_summary_statistics[9] * 10000

            st.markdown("## Predictions:")
        
            st.markdown(
                f"##### The model is 95% confident that an initial investment of $10000"
                f" will, in 5 years, turn into an amount between  \n "
                f"##### ${ci_95_lower_cumulative_return: .2f} and ${ci_95_upper_cumulative_return: .2f}.")

            MC_fig= px.line(MC_fiveyear_df, labels={"index":"Trading Days", "value":"Return"})
            GO_fig = go.Figure(data=MC_fig).update_layout(title_text= f"Potential 5-Year Return of {stock} - 500 Possible Futures", showlegend=False, xaxis_title="Trading Days", yaxis_title="Cumulative Return")
            st.plotly_chart(GO_fig, use_container_width=False, sharing="streamlit")

            if st.button("Reset"): 
                st.experimental_memo.clear()

            st.markdown("""
    <style>
    .small-font {
        font-size:13px !important;
    }
    </style>
    """, unsafe_allow_html=True)

            st.markdown('<p class="small-font">*This score is calculated using financial ratios and other important information. This grader may be changed and updated to improve accuracy.</p>', unsafe_allow_html=True)
            
    except:
        st.error("Uh oh! Please enter a valid stock ticker and try again.")

        