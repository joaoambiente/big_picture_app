import streamlit as st
import numpy as np
import pandas as pd
import requests
import time
import json
import webbrowser

st.title('''The Big Picture''')

# Form example
#with st.form(key='my_form'):
#    text_input = st.text_input(label='Enter your name')
#    submit_button = st.form_submit_button(label='Submit')

# This is the initial claim for our project:
text = "Enhance your perspectives on the news... with AI!"
t = st.empty()
for i in range(len(text) + 1):
    t.markdown("## %s" % text[0:i])
    time.sleep(0.0001)

query = st.text_input("Search terms (english only): ")
# st.write("You've requested these search terms:  ", query)

if st.button('Get news!', key=1):
    # Retrieving the prediction from the **JSON** returned by the API...
    # response = requests.get(url + endpoint, params=news_params)
    # response_json = response.json()
    # news_list = response_json["news_list"]

    # Example .json
    get_search_output = open('./data/example_search_output.json',) 
    news_list = json.load(get_search_output)
    get_search_output.close()
    news_list = news_list["articles"]
    
    for index, news in enumerate(news_list[0:10]):
        # Widget within an expander
        #my_expander = st.beta_expander("Click to expand", expanded=False)
        # Widget/buttons skeleton
        #with my_expander:
        col1,col2,col3 = st.beta_columns(3)
        with col1:
            #link = '[GitHub](http://github.com)'
            #st.markdown(link, unsafe_allow_html=True)
            st.write(f'{news["title"]}')
            
        with col2:
            st.button(f'Get sentiment analysis report', key=index+1)
            #st.write(f'Url: {news["url"]}')
            #st.button(f'Result {index+1}: {news["title"]}', key=index+1)
        with col3:
            #st.write(f'Url: {news["url"]}')
            st.write(f'[Read this news article]({news["url"]})')
            #st.button(f'Result {index+1}: {news["title"]}', key=index+1)

            
            #st.button(f'Result {index+1}: {news["title"]}', key=index+2)
            #url = news["url"]
            #if st.button('Open browser'):
             #   link = f'[url](http://github.com)'
              #  st.markdown(link, unsafe_allow_html=True)
                
        # print will be visible in server output, not in the page
        # st.write(f'Source: {news_list[0]["source"]["name"]}')
        # st.write(f'Author: {news_list[0]["author"]}')
        
        # st.write(f'Description: {news_list[0]["description"]}')
        # st.write(f'Url: {news_list[0]["url"]}')
        # st.write(f'Url to image: {news_list[0]["urlToImage"]}')
        # st.write(f'Published At: {news_list[0]["publishedAt"]}')    
        # st.write(f'Content: {news_list[0]["content"]}')
else:
    st.write('Click this button to get a list of 10 news based on a simple query.')

st.markdown('''  
## Advanced query:
''')

date_from = st.date_input("Please select how far back you want to get the news from: ")
date_from = date_from.strftime("%Y-%m-%d")

# st.write("You've requested these search terms:  ", date_from)

st.markdown('''#### Title''')
title = st.text_input("Select search terms within a title (english only): ", key=1)

st.markdown('''#### Sources''')

get_sources = open('./support_data/sources.json',) 
data = json.load(get_sources)
get_sources.close()
sources_df = pd.DataFrame(data["sources"])
sources_df = sources_df[sources_df["language"] == "en"]
sources_list = sources_df.id.to_list()
domains_list = sources_df.url.to_list()

source = st.multiselect("Select one or more sources for the news sources you want headlines from (english sources only, max. 20 sources): ",
    sources_list)
source = ','.join(source)

st.markdown('''#### Domain''')
label = st.multiselect("Input domains separated by commas (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search: ",
    domains_list)
label = ','.join(label)

# Se a lista de domains não funcionar bem podemos usar antes isto:
# label = st.text_input("Input domains separated by commas (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search: ", key=2)

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

if st.button('Get news!', key=2):
    # Retrieving the prediction from the **JSON** returned by the API...
    # response = requests.get(url + endpoint, params=news_params)
    # response_json = response.json()
    # news_list = response_json["news_list"]
    get_search_output = open('./data/example_search_output.json',) 
    news_list = json.load(get_search_output)
    get_search_output.close()
    news_list = news_list["articles"]

    for article in news_list:
        # print will be visible in server output, not in the page
        # st.write(f'Source: {news_list[0]["source"]["name"]}')
        # st.write(f'Author: {news_list[0]["author"]}')
        st.write(f'Title: {news_list[0]["title"]}')
        # st.write(f'Description: {news_list[0]["description"]}')
        # st.write(f'Url: {news_list[0]["url"]}')
        # st.write(f'Url to image: {news_list[0]["urlToImage"]}')
        # st.write(f'Published At: {news_list[0]["publishedAt"]}')    
        # st.write(f'Content: {news_list[0]["content"]}')
else:
    st.write('Click this button to get a list of 10 news based on your advanced search parameters.')

# my_dict = news_list[0]
my_dict = {}

# Dictionary containing the parameters for our Sentiment Analysis (from or model)...
endpoint = "predict"
sentiment_params = {
        "sample": my_dict
            }

st.markdown('''  
## Sentiment Analysis:
''')

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



