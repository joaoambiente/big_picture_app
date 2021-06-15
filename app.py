import streamlit as st
import numpy as np
import pandas as pd
import datetime
import requests

st.markdown(''' 
# The Big Picture 
## Get insights from your news with sentiment analysis.
Please provide your search terms bellow, separated by commas.
''')
search_terms = st.text_input("Search terms: ")
st.write('Requested search terms: ', search_terms)

'''
### Please provide a "start date" and an "end date" to narrow down the search. 
'''
date_from = st.date_input("Start date: ")
date_to = st.date_input("End date: ")

date_from = str(date_from)
date_to = str(date_to)

## Once we have these, let's call our API in order to retrieve a prediction
# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...
# 🤔 How could we call our API ? Of course... The `requests` package 💡

url = 'https://github.com/archifreitas/bg_api'

# 2. Let's build a dictionary containing the parameters for our API...

# dict of params
params = {
        "q": search_terms,
        "from": date_from,
        "to": date_to,
        }

# Calling our Big Picture API using the `requests` package and return a value with a button

if st.button('Get news!'):
    response = requests.get(url, params=params)
    response_json = response.json()

    # Retrieving the prediction from the **JSON** returned by the API...
    news_list = response_json["news_list"]

    # print will be visible in server output, not in the page
    st.write(f'{news_list}')
else:
    st.write('Click this button to get a list of news based on your search parameters.')


if st.button('Get sentiment_analysis_predicition!'):
    response = requests.get(url, params=params)
    response_json = response.json()

    # Retrieving the prediction from the **JSON** returned by the API...
    sentiment_analysis_predicition = response_json["sentiment_analysis_predicition"]

    # print will be visible in server output, not in the page
    st.write(f'{sentiment_analysis_predicition}')
else:
    st.write("Click this button to retrieve a sentiment analysis on the text you've selected.")

# get news list based on API request (considering the predicted tag, cluster aggregation and sentiment analysis result)
@st.cache
def get_news_list():
    print('News List')
    return pd.DataFrame({
          'News Content': np.arange(0, 101, 1),
          'News Tags': np.arange(0, 101, 1),
          'Sentiment Analysis result': list(range(0, 101))
        })

df = get_news_list()

option = st.slider('Select a modulus', 0, 100, 50)

filtered_df = df[df['Sentiment Analysis result'] % option == 0]

st.write(filtered_df)