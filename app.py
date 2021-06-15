import streamlit as st
import numpy as np
import pandas as pd
import requests
import time
import json

st.markdown(''' 
# The Big Picture 
''')

text = "Enhance your perspectives on the news... with AI!"

t = st.empty()
for i in range(len(text) + 1):
    t.markdown("## %s" % text[0:i])
    time.sleep(0.0001)

query = st.text_input("Search terms (english only): ")
# st.write("You've requested these search terms:  ", query)

st.markdown('''  
## Advanced query:
''')

date_from = st.date_input("Please select how far back you want to get the news from: ")
date_from = date_from.strftime("%Y-%m-%d")

# st.write("You've requested these search terms:  ", date_from)

st.markdown('''#### Title''')
title = st.text_input("Select search terms within a title (english only): ", key=1)

st.markdown('''#### Sources''')
source = st.text_input('''Input terms separated by commas (maximum 20) 
for the news sources you want headlines from (english sources only) : ''', key=2)

st.markdown('''#### Domain''')
label = st.text_input("Input domains separated by commas (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search: ", key=3)

# URL for our API...
url = 'https://github.com/archifreitas/bg_api/'

# Dictionary containing the parameters for our News API (news obtained from newsAPI)...
endpoint = "search"
news_params = {
        "query": query,
        "title": title,
        "source": source,
        "label" : label,
        "date_from": date_from
        }

# Calling our Big Picture API using the `requests` package and returning a value with a button

if st.button('Get news!', key=1):
    # Retrieving the prediction from the **JSON** returned by the API...
    # response = requests.get(url + endpoint, params=news_params)
    # response_json = response.json()
    # news_list = response_json["news_list"]
    get_search_output = open('./data/example_search_output.json',) 
    news_list = json.load(get_search_output)
    get_search_output.close()
    news_list = news_list["articles"]

    # print will be visible in server output, not in the page
    st.write(f'Title: {news_list}')
else:
    st.write('Click this button to get a list of news based on your search parameters.')


# my_dict = news_list[0]
my_dict = {}

# Dictionary containing the parameters for our Sentiment Analysis (from or model)...
endpoint = "predict"
sentiment_params = {
        "sample": my_dict
            }

if st.button('What is the sentiment of this news article, positive or negative?', key=2):
    response = requests.get(url, params=sentiment_params)
    response_json = response.json()

    # Retrieving the prediction from the **JSON** returned by the API...
    sentiment_analysis_predicition = response_json["sentiment_analysis_predicition"]

    # print will be visible in server output, not in the page
    st.write(f'{sentiment_analysis_predicition}')
else:
    st.write("Click this button to retrieve a sentiment analysis on the text you've selected.")

# get news list based on API request (considering the predicted tag, cluster aggregation and sentiment analysis result)


st.markdown('''#### A want to see an article with a different sentiment score: ''')

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



