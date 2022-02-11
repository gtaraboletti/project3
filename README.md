# project3
UNCC FinTech Boot Camp Project 3 (Stock grader) 

launch by using git bash to change directories into the correct folder
enter "streamlit run P3_streamlit.py" 

## Imports 

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

## Contributors 

Giselle Taraboletti 

## Images of Streamlit App 

Beginning State: 
![streamlit screenshot 1](https://user-images.githubusercontent.com/89159824/153523573-e80b8461-8efc-4ac9-b5c5-ac8dd1147b44.png)

Stock Information: 
![streamlit screenshot 2](https://user-images.githubusercontent.com/89159824/153523579-e7d2b2dc-01b8-4c6a-b597-d6bb05b8d880.png)

Monte Carlo Loading: 
![streamlit screenshot 3 loading bar](https://user-images.githubusercontent.com/89159824/153523582-11cc153e-10a3-4889-8ab4-6928426547dd.png)

Monte Carlo Results: 
![streamlit screenshot 4](https://user-images.githubusercontent.com/89159824/153523591-351222da-9595-434b-b1b4-bb52a72b32ca.png)

Error message when user enters invalid ticker: 
![streamlit screenshot 5 invalid ticker](https://user-images.githubusercontent.com/89159824/153523600-ddff2c50-9230-480e-98ea-4ce27b487b4c.png)

## License ##

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

