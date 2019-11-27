#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
# import os
import requests
import time
import re

# import mars_functions  __init__.py

from mars_functions import *
from bs4 import BeautifulSoup as bs
from splinter import Browser





def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # # Scrape everything

    # this dictionary will hold everything we pull from all the sites
    scraped_data = {}

    news_title, news_p = scrape_news()
    print(news_title, news_p)
    scraped_data['news_title'] = news_title
    scraped_data['news_p'] = news_p

    featured_image_url, featured_image_caption = scrape_jpl()
    scraped_data['featured_image_url'] = featured_image_url
    scraped_data['featured_image_caption'] = featured_image_caption

    wx_text = scrape_twitter()
    print(wx_text)
    scraped_data['weather_data'] = wx_text

    facts_html_str = scrape_facts()
    print(facts_html_str)
    scraped_data['facts_html_str'] = facts_html_str

    ll_hemi_image_urls = scrape_img_urls()
    print(ll_hemi_image_urls)
    scraped_data['hemisphere_image_urls'] = ll_hemi_image_urls

 
    return(scraped_data)