import pandas as pd
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


st.write("Stock Scoring")

# Set Alpaca API key and secret key
alpaca_api_key = "PK2E1G7V4QCB3SHLL3I8"
alpaca_secret_key = "22pJHmdw6fIv0EihrhuaaL9VAzqcKyVgS1qyTSUz"
type(alpaca_secret_key)

# Create the Alpaca REST object
alpaca = tradeapi.REST(alpaca_api_key, alpaca_secret_key, api_version="v2")

td_consumer_key = 'YXGDGMF1UR0KBX7H77MZJS2WLN7PXYIK'
stock = st.text_input("Please enter a 3-4 letter stock ticker.")
stock_score = 0

trading_endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes'
trading_url = trading_endpoint.format(stock_ticker=stock)

trade_page = requests.get(url=trading_url, params={'apikey': td_consumer_key})
trade = json.loads(trade_page.content)

endpoint = 'https://api.tdameritrade.com/v1/instruments?apikey=YXGDGMF1UR0KBX7H77MZJS2WLN7PXYIK&symbol={stock_ticker}&projection=fundamental'
full_url = endpoint.format(stock_ticker=stock)

page = requests.get(url=full_url, params={'apikey': td_consumer_key})
content = json.loads(page.content)

#Price-to-earnings ratio
if 13 <= content[stock]['fundamental']['peRatio'] <= 15:
    stock_score = stock_score + 1
elif content[stock]['fundamental']['peRatio'] > 15:
    stock_score = stock_score + 2
elif content[stock]['fundamental']['peRatio'] < 13:
    stock_score = stock_score

#Price/Earnings to Growth pegRatio
if content[stock]['fundamental']['pegRatio'] < 1:
    stock_score = stock_score
elif content[stock]['fundamental']['pegRatio'] >= 1:
    stock_score = stock_score + 2

#Price to Book Ratio pbRatio
if content[stock]['fundamental']['pbRatio'] <= 1:
    stock_score = stock_score + 2
elif 1 < content[stock]['fundamental']['pbRatio'] <= 3:
    stock_score = stock_score + 1
elif content[stock]['fundamental']['pbRatio'] > 3:
    stock_score = stock_score

#Current Ratio
if 1 <= content[stock]['fundamental']['currentRatio'] <= 3:
    stock_score = stock_score + 2
elif content[stock]['fundamental']['currentRatio'] > 3:
    stock_score = stock_score + 1
elif content[stock]['fundamental']['currentRatio'] < 1:
    stock_score = stock_score

#Quick Ratio
if (1 / 2) <= content[stock]['fundamental']['quickRatio'] <= 1:
    stock_score = stock_score + 1
elif content[stock]['fundamental']['quickRatio'] > 1:
    stock_score = stock_score + 2
elif content[stock]['fundamental']['quickRatio'] < (1 / 2):
    stock_score = stock_score

#Debt-to-Equity Ratio
if content[stock]['fundamental']['totalDebtToEquity'] > 2:
    stock_score = stock_score
elif 2 > content[stock]['fundamental']['totalDebtToEquity'] > 1:
    stock_score = stock_score + 1
elif content[stock]['fundamental']['totalDebtToEquity'] <= 1:
    stock_score = stock_score + 2

#Net profit margin netProfitMarginMRQ
if content[stock]['fundamental']['netProfitMarginMRQ'] >= 20:
    stock_score = stock_score + 2
elif 5 <= content[stock]['fundamental']['netProfitMarginMRQ'] <= 10:
    stock_score = stock_score + 1
elif content[stock]['fundamental']['netProfitMarginMRQ'] < 5:
    stock_score = stock_score

#Return on Equity  returnOnEquity
if content[stock]['fundamental']['returnOnEquity'] >= 15:
    stock_score = stock_score + 2
elif content[stock]['fundamental']['returnOnEquity'] < 15:
    stock_score = stock_score

#Gross Margin  grossMarginMRQ
if 50 <= content[stock]['fundamental']['grossMarginMRQ'] <= 60:
    stock_score = stock_score + 2
elif content[stock]['fundamental']['grossMarginMRQ'] > 60:
    stock_score = stock_score + 1
elif content[stock]['fundamental']['grossMarginMRQ'] < 50:
    stock_score = stock_score

#Operating Margin operatingMarginMRQ
if content[stock]['fundamental']['operatingMarginMRQ'] >= 15:
    stock_score = stock_score + 2
elif content[stock]['fundamental']['operatingMarginMRQ'] < 15:
    stock_score = stock_score

#Return on Assets returnOnAssets
if content[stock]['fundamental']['returnOnAssets'] >= 5:
    stock_score = stock_score + 2
elif content[stock]['fundamental']['returnOnAssets'] < 5:
    stock_score = stock_score

#Beta beta
if content[stock]['fundamental']['beta'] == 1:
    stock_score = stock_score + 2
elif content[stock]['fundamental']['beta'] < 1:
    stock_score = stock_score + 1
elif content[stock]['fundamental']['beta'] > 1:
    stock_score = stock_score

#Final score output & suggestion
st.write(f"The score for {stock} is {stock_score}.")

if stock_score >= 18:
    st.write("This company has good financial health. Recommendation: Invest")
elif 12 <= stock_score < 18:
    st.write(
        "This company's financial health is so-so. Recommendation: Seek further information."
    )
elif stock_score < 12:
    st.write(
        "This company may not have provided all the information necessary to accurately score their stock, or the company's financial health is poor. Recommendation: Invest Elsewhere"
    )

start_date = pd.Timestamp("2017-01-01", tz="America/New_York").isoformat()
end_date = pd.Timestamp("2021-12-31", tz="America/New_York").isoformat()

limit_rows = 1000

prices = alpaca.get_barset(stock,
                           timeframe='1D',
                           start=start_date,
                           end=end_date,
                           limit=limit_rows).df

from MCForecastTools import MCSimulation

MC_fiveyear = MCSimulation(portfolio_data=prices,
                           weights=[1.00],
                           num_simulation=500,
                           num_trading_days=252 * 5)

MC_fiveyear.calc_cumulative_return()
MC_sim_line_plot = MC_fiveyear.plot_simulation()


MC_summary_statistics = MC_fiveyear.summarize_cumulative_return()

ci_95_lower_cumulative_return = MC_summary_statistics[8] * 10000
ci_95_upper_cumulative_return = MC_summary_statistics[9] * 10000

st.write(
    f"There is a 95% chance that an initial investment of $10000"
    f" will, in 5 years, turn into an amount between"
    f" ${ci_95_lower_cumulative_return: .2f} and ${ci_95_upper_cumulative_return: .2f}."
)

prices = prices.reset_index()
prices.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

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

#add button to reset