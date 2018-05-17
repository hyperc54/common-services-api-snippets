# -*- coding: utf-8 -*-
"""
Loads comments from a youtube video & performs a wordcloud on them.

Get the Youtube Data API Python client:
    pip install --upgrade google-api-python-client

Get your API key following:
    https://developers.google.com/youtube/registering_an_application?authuser=1

Get the wordcloud package:
    pip install wordcloud
    
List of all Youtube Data API Python client methods:
    https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/
"""

#%% Global parameters
VIDEO_ID = 'U7dA4jkdo1g'
COMMENTS_BY_PAGE = 100 #Number of comments loaded by api request (<=100)
PAGE_LIMIT = 50 #Max number of pages of comments to load

#%% Imports
import pandas as pd
from apiclient.discovery import build
from api_keys import YOUTUBE_API_KEY
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#%% Create client
yc = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

#%% Load pages of comments
pages = []

def load_page(yc, vid, page_token=None):
    return (yc
            .commentThreads()
            .list(pageToken=page_token,
                  maxResults=100,
                  videoId=vid,
                  part='snippet,replies')
            .execute())


pages.append(load_page(yc, VIDEO_ID))

i = 1
while 'nextPageToken' in pages[i-1] and i < PAGE_LIMIT:
    pages.append(load_page(yc, VIDEO_ID, page_token=pages[i-1]['nextPageToken']))
    i += 1
    
#%% Format messages
msgs_obj_list = [message for x in [page['items'] for page in pages] for message in x]

msgs_list = [x['snippet']['topLevelComment']['snippet']['textOriginal'] + ' \n' for x in msgs_obj_list]

#%% Concat ecverything into a big text
text = reduce(lambda x,y:x+y, msgs_list).lower()

#%% Remove common words
for word in ['de', 'il', 'je', 'vous', 'vs', 'et', 'le']:
    text = text.replace(word,'')

#%% Create wordcloud
wordcloud = WordCloud(max_font_size=50).generate(text)
 
#%% Display wordcloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")



