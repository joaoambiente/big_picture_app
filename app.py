import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from urllib.parse import urlparse
from utils.logos import get_logos
import pickle
import SessionState
import random
from PIL import Image

def get_news(search='simple'):
    session_state = SessionState.get(checkboxed=False, checkboxed2=False)
    if search == "simple":
        modifier = 1
        news_params = {
        "query": query,
        }
        session_condition = session_state.checkboxed
    else:
        news_params = {
           "query": query,
           "source": source,
           "date_from": date_from
           }
        modifier = 2
        session_condition = session_state.checkboxed2
    
    if (st.button('Get news', key=100*modifier) and news_params['query']) or session_condition:
        if search == "simple":
            session_state.checkboxed = True
        else:
            session_state.checkboxed2 = True
        ## Retrieving the prediction from the **JSON** returned by the API...
        url = "https://api-s4zpk52g3a-ew.a.run.app/"
        endpoint = "search"
        response = requests.get(url + endpoint, params=news_params)
        news_list = response.json()

        hr = f'<hr class="divider"></hr>'
        st.markdown(hr, unsafe_allow_html=True)

        # Organizing buttons in columns
        for keys, news in news_list.items():
            col1,col2,col3 = st.beta_columns([0.1,2,0.3])

            src = news['url']  
            domain = urlparse(src).netloc.strip("www.")
            logo_url = get_logos(domain)

            with col1:
                logo_img = f'<img class="image_logo" src="{logo_url}">'
                st.markdown(logo_img, unsafe_allow_html=True)        
            with col2:
                try:
                    news_title = f'<p class="article-title">{news["publishedAt"]+" | "+news["title"]}</h2>'
                    st.markdown(news_title, unsafe_allow_html=True)
                except:
                    news_title = f'<p class="article-title">{news["title"]}</h2>'
                    st.markdown(news_title, unsafe_allow_html=True)
            with col3:
                st.write(f'[Read from source]({news["url"]})')
            
            my_expander = st.beta_expander("Get sentiment analysis report for this news article", expanded=False)
            
            with my_expander:
                col1,col2 = st.beta_columns([1,5])
                col7, col8 = st.beta_columns([1,1])
                col9, col10 = st.beta_columns([1,1])
                col4_1, col4,col5,col6 = st.beta_columns([0.2,4,1,2])

                with col1:
                    if st.button("Analyse", key=keys*modifier):

                        url = "http://35.184.150.29:8080/predict"
                        response = requests.post(url, json=news)
                        data = response.json()
                        topic = data['topic']
                        data_df = json.loads(data['data'])
                        data_df = pd.DataFrame(data_df)

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
                                if article['SA'] > data_df.iloc[0,5]:
                                    st.markdown('<p class="green_arrow">\u25B2</p>', unsafe_allow_html=True)
                                else:
                                    st.markdown('<p class="red_arrow">\u25BC</p>', unsafe_allow_html=True)
                            with col4:
                                try:
                                    if len(article['title']) > 60:
                                        article["publishedAt"]+" | "+article['title'][:60]
                                    else:
                                        article["publishedAt"]+" | "+article['title']
                                except:
                                    if len(article['title']) > 60:
                                        article['title'][:60]
                                    else:
                                        article['title']
                            with col5:
                                st.write(f'[show article]({article["url"]})')

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

                            y = np.linspace(0,100)
                            x = y*0 + data_df.iloc[0,5]

                            if data_df.iloc[0,5] > 0:
                                color = [0,data_df.iloc[0,5],0]
                            else:
                                color = [-data_df.iloc[0,5],0,0]

                            plt.xlim(-1,1)
                            axes = plt.gca()
                            plt.ylim(axes.get_ylim())

                            plt.plot(x,y, color=color)
                            plt.axis('off')

                            st.write(figure)

                            figure = plt.figure(figsize = (8, 8), facecolor = None)
                            plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3),
                                    interpolation="bilinear")
                            plt.axis("off")
                            plt.tight_layout(pad = 0)

                            st.write(figure)

    else:
        st.markdown('<p class="small-font">Click this button to get a list of 10 news based on a simple query</p>', unsafe_allow_html=True)

st.set_page_config(
    page_title="The Big Picture App",
    #page_icon="????",
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

st.markdown("<h2 style='text-align: center; color: white;'>Enhance your perspectives on the news with sentiment analysis.</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'>Search for news  >  Choose your article  >  Know where your article stands amongst similar articles</h1>", unsafe_allow_html=True)

query = st.text_input("Search terms (english only): ")

get_news()

st.markdown('''  
## Advanced query:
''')
# Advanced idget within an expander
my_expander = st.beta_expander("Click to expand", expanded=False)
with my_expander:
    # st.markdown('''#### Search terms''')
    query = st.text_input("Search terms (english only): ", key=1)

    st.markdown('''#### Date''')
    date_from = st.date_input("Please select how far back you want to get the news from: ")
    date_from = date_from.strftime("%Y-%m-%d")

    st.markdown('''#### Sources''')  
    with open ('./support_data/domains_list.txt', 'rb') as fp:
        sources_list = pickle.load(fp)
 
    source = st.multiselect("Input domains separated by commas (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search: ",
        sources_list)
    source = ','.join(source)

# Calling our Big Picture API using the `requests` package and returning a value with a button
get_news('advanced')
