import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import time
import json
from urllib.parse import urlparse
import pickle
import SessionState
import random
from PIL import Image

st.set_page_config(
    page_title="The Big Picture App",
    #page_icon="🧊",
    layout="wide", # or "centered"
    #initial_sidebar_state="expanded",
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")

# st.markdown("<h1 style='text-align: center; color: white;'>The Big Picture</h1>", unsafe_allow_html=True)
col_a,col_b,col_c = st.beta_columns([3.2,2,3])
with col_b:
    image = Image.open('images/big_picture_logo.png')
    st.image(image, use_column_width=False,width=250)

st.markdown("<h2 style='text-align: center; color: white;'>Enhance your perspectives on the news... with AI!</h1>", unsafe_allow_html=True)


query = st.text_input("Search terms (english only): ")

session_state = SessionState.get(checkboxed=False)
if st.button('Get news!', key=1) or session_state.checkboxed:
    session_state.checkboxed = True
    ## Retrieving the prediction from the **JSON** returned by the API...
    # url = "https://api-s4zpk52g3a-ew.a.run.app/"
    # endpoint = "search"
    # news_params = {
    #        "query": query,
    #        }
    # response = requests.get(url + endpoint, params=news_params)
    # news_list = response.json()

    ## Retrieving the prediction from the **JSON** placeholder...
    get_sources = open('./data/example_search_output.json',) 
    news_list = json.load(get_sources)
    get_sources.close()

    hr = f'<hr class="divider"></hr>'
    st.markdown(hr, unsafe_allow_html=True)

    # Organizing buttons in columns
    for keys, news in news_list.items():
        col1,col2 = st.beta_columns([2,1])

        with col1:
            news_title = f'<p class="article-title">{news["title"]}</h2>'
            st.markdown(news_title, unsafe_allow_html=True)
        with col2:
            st.write(f'[Read from source]({news["url"]})')
        my_expander = st.beta_expander("Get sentiment analysis report for this news article", expanded=False)
        
        with my_expander:
            col1,col2 = st.beta_columns([1,5])
            col7, col8 = st.beta_columns([1,1])
            col9, col10 = st.beta_columns([1,1])
            col4_1, col4,col5,col6 = st.beta_columns([0.2,4,1,2])

            with col1:
                if st.button("Make Prediction", key=keys):
                    # Import .json
                    # # df = pd.Dataframe()
                    get_sources = open('./data/example_pd_topics.json')
                    data = json.load(get_sources)
                    data_df = json.loads(data['data'])
                    data_df = pd.DataFrame(data_df)
                    topic = data['topic']
                    with col2:
                        if data_df.iloc[0,1] > data_df.SA.mean():
                            if data_df.iloc[0,1] > 0:
                                st.markdown('<p class="article-sub-title">This article is more positive than the average for this topic</p>', unsafe_allow_html=True)

                            else:
                                st.markdown('<p class="article-sub-title">This article is less negative than the average for this topic</p>', unsafe_allow_html=True)
                                
                        else:
                            if data_df.iloc[0,1] > 0:
                                st.markdown('<p class="article-sub-title">This article is less positive than the average</p>', unsafe_allow_html=True)
                                
                            else:
                                st.markdown('<p class="article-sub-title">This article is more negative than the average</p>', unsafe_allow_html=True)
                    
                    with col9:
                        st.write('Similar Articles:')

                        comment_words = ' '.join(topic)
                        
                        def grey_color_func(word, font_size, position, orientation, random_state=None,
                                            **kwargs):
                            return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

                        wordcloud = WordCloud(width = 800, height = 800,
                                        background_color ='black',
                                        min_font_size = 10).generate(comment_words)

                        # plot the WordCloud image	

                    if len(data_df) > 14:
                        max_articles = 14
                    else:
                        max_articles = -1
                    

                    for _ , article in data_df.iloc[1:max_articles,:].iterrows():
                        with col4_1:
                            if article['SA'] > data_df.iloc[0,1]:
                                st.markdown('<p class="green_arrow">\u25B2</p>', unsafe_allow_html=True)
                            else:
                                st.markdown('<p class="red_arrow">\u25BC</p>', unsafe_allow_html=True)
                        with col4:
                            article['title'][:80]
                        with col5:
                            st.write('show article')

                    with col6:

                        figure = plt.figure()
                        sorted_df = data_df.sort_values('SA').reset_index()
                        my_kde = sns.kdeplot(
                            sorted_df.SA,
                            shade=True,
                            color='grey'
                            #marker='o',
                            #markevery=[sorted_df[sorted_df['index'] == '0'].index[0]]
                            )
                        
                        y = np.linspace(0,1)
                        x = y*0 + data_df.iloc[0,1]

                        if data_df.iloc[0,1] > 0:
                            color = [0,data_df.iloc[0,1],0]
                        else:
                            color = [-data_df.iloc[0,1],0,0]

                        plt.plot(x,y, color=color)
                        plt.axis('off')

                        plt.xlim(-1,1)
                        st.write(figure)

                        figure = plt.figure(figsize = (8, 8), facecolor = None)
                        plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3),
                                interpolation="bilinear")
                        plt.axis("off")
                        plt.tight_layout(pad = 0)

                        st.write(figure)
                #     with col4:
                #         if st.checkbox('Predicted Topics', key=keys):
                #             st.write('''
                # This code will only be executed when the check box is checked

                # Streamlit elements injected inside of this block of code will \
                # not get displayed unless it is checked
                # ''')
                #     with col5:
                #         if st.checkbox('Sentiment Analysis and Similar Articles', key=keys*2):
                #             st.write('''
                # This code will only be executed when the check box is checked

                # Streamlit elements injected inside of this block of code will \
                # not get displayed unless it is checked
                # ''')
                #     with col6:
                #         if st.checkbox('Word Cloud', key=keys*3):
                #             st.write('''
                # This code will only be executed when the check box is checked

                # Streamlit elements injected inside of this block of code will \
                # not get displayed unless it is checked
                # ''')

#if st.button('Click me') :
    
 #   if st.button("Click me too !"):
  #      st.write("Hello world")

else:
    st.markdown('<p class="small-font">Click this button to get a list of 10 news based on a simple query</p>', unsafe_allow_html=True)

st.markdown('''  
## Advanced query:
''')
# Advanced idget within an expander
my_expander = st.beta_expander("Click to expand", expanded=False)
with my_expander:
    # st.markdown('''#### Search terms''')
    query = st.text_input("Search terms (english only): ", value="Insert search term here", key=1)

    st.markdown('''#### Date''')
    date_from = st.date_input("Please select how far back you want to get the news from: ")
    date_from = date_from.strftime("%Y-%m-%d")

    # st.markdown('''#### Title''')
    # title = st.text_input("Select search terms within a title (english only): ", value="Insert search term here", key=2)

    st.markdown('''#### Sources''')  
    with open ('./support_data/domains_list.txt', 'rb') as fp:
        sources_list = pickle.load(fp)
 
    source = st.multiselect("Input domains separated by commas (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search: ",
        sources_list)
    source = ','.join(source)

    # Calling our Big Picture API using the `requests` package and returning a value with a button
    if st.button('Get news!', key=2):
        # Retrieving the prediction from the **JSON** returned by the API...
        #url = "https://api-s4zpk52g3a-ew.a.run.app/"
        #endpoint = "search"
        #news_params = {
        #    "query": query,
        #    "title": title,
        #    "source": source,
        #    "label" : label,
        #    "date_from": date_from
        #    }

        # response = requests.get(url + endpoint, params=news_params)
        # news_list = response.json()

        ## Retrieving the prediction from the **JSON** placeholder...
        get_sources = open('./data/example_search_output.json',) 
        news_list = json.load(get_sources)
        get_sources.close()

        for keys, news in news_list.items():
            col1,col2,col3 = st.beta_columns(3)
            with col1:
                st.write(f'{news["title"]}')
            with col2:
                if st.button(f'Get sentiment analysis report', key=int(keys)+11):
                        # predict sentiment analysis based on the key for this news article 
                        pass
            with col3:
                st.write(f'[Read this news article]({news["url"]})')
    else:
        st.markdown('<p class="small-font">Click this button to get a list of 10 news based on your advanced search parameters.</p>', unsafe_allow_html=True)

    # my_dict = news_list[0]
    my_dict = {}

    # Dictionary containing the parameters for our Sentiment Analysis (from or model)...
    endpoint = "predict"
    sentiment_params = {
            "sample": my_dict
                }


# Add time to some text
# t = st.empty()
# for i in range(len(text) + 1):
#     # heading 2
#     t.markdown("## %s" % text[0:i])
#     time.sleep(0.05) # decrease speed before presentation



#get some logos

        # src = news['url']
        # domain = urlparse(src).netloc.strip("www.")
        # url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={domain}"
        # headers = {
        #     'Accept': '*/*',
        #     'Host': 'autocomplete.clearbit.com',
        #     'Origin': 'https://clearbit.com',
        #     'Referer': 'https://clearbit.com/logo',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        #     'Accept-Language': 'pt-PT,pt;q=0.8,en;q=0.5,en-US;q=0.3',
        #     'Connection':'keep-alive',
        #     'Accept-Encoding': 'gzip, deflate, br'
        # }
        # response = requests.get(url, headers=headers)


  #  st.markdown('''  
  #  ## Sentiment Analysis:
  #  ''')

   # if st.button('What is the sentiment of this news article, positive or negative?', key=2):
   #     response = requests.get(url, params=sentiment_params)
   #     response_json = response.json()
#
 #       # Retrieving the prediction from the **JSON** returned by the API...
  #      sentiment_analysis_predicition = response_json["sentiment_analysis_predicition"]
#
 #       # print will be visible in server output, not in the page
  #      st.write(f'{sentiment_analysis_predicition}')
  #  else:
  #      st.write("Click this button to retrieve a sentiment analysis on the text you've selected.")

    # get news list based on API request (considering the predicted tag, cluster aggregation and sentiment analysis result)


 #   st.markdown('''#### A want to see an article with a different sentiment score: ''')

 #   @st.cache
 #   def get_news_list():
 #       print('News List')
 #       return pd.DataFrame({
 #           'News Content': np.arange(0, 101, 1),
 #           'News Tags': np.arange(0, 101, 1),
 #           'Sentiment Analysis result': list(range(0, 101))
 #           })
 #
 #   df = get_news_list()

 #  option = st.slider('Select a modulus', 0, 100, 50)
 #
 #  filtered_df = df[df['Sentiment Analysis result'] % option == 0]
 #
 #  st.write(filtered_df)


#Other stuff
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


# Form example
#  with st.form(key='my_form'):
#    text_input = st.text_input(label='Enter your name')
#    submit_button = st.form_submit_button(label='Submit')