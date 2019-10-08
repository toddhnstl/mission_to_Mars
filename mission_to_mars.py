#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
# import os
import requests
import time
import re


from bs4 import BeautifulSoup as bs
from splinter import Browser


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # # Scrape everything
    #

    # In[2]:


    # this dictionary will hold everything we pull from all the sites
    scraped_data = {}


    # In[3]:


    # site 1 - "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest" # probably need to replace this since it redirects
    news_response = requests.get(news_url)
    time.sleep(2)

    # use beautiful soup to parse the url above
    news_soup = bs(news_response.text, 'html.parser')
    #newPSoup = bs(news_response.text, 'html.parser')


    # In[4]:


    # # example_title_div = '<div class="content_title"><a href="/news/8520/nasas-mars-2020-rover-tests-descent-stage-separation/" target="_self">NASAs Mars 2020 Rover Tests Descent-Stage Separation</a></div>'
    # # example_paragraph_div = '<div class="article_teaser_body">A crane lifts the rocket-powered descent stage away from NASAs Mars 2020 rover after technicians tested the pyrotechnic charges that separate the two spacecraft.</div>'


    # # use bs to find() the example_title_div and filter on the class_='content_tile'


    # # presults = newPSoup.find_all('li', class_='slide')
    # # print(presults)

    # results = news_soup.find('div', class_='content_title')
    # print("==== News Title =====")
    # print(results)
    # print("")
    # news_title = results.a.text
    # news_title = news_title.replace('\n', '')
    # print(news_title)
    # scraped_data['news_title'] = news_title #- load the dataframe with Key/value pair
    # print("=========")
    # print("")
    # print("")

    # # use bs to find() the example_title_div and filter on the class_='article_teaser_body'
    # presults = news_soup.find('div', class_='article_teaser_body')
    # print("====Paragraph=====")
    # print(presults)
    # print("=========")
    # print("")
    # print("")

    # # # news_p = "FILL IN THE PARAGRAPH"
    # # # scraped_data['news_p'] = news_p


    # # I'm getting nowhere with just BS.  Try site 1 with splinter
    #

    # In[5]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[ ]:





    # In[6]:


    browser.visit(news_url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')



    # Get an article block.
    art_teaser_body = soup.find('li', class_='slide')

    # Parse out the title
    title = art_teaser_body.find('div',  class_='content_title')
    news_title = title.text

    # Parse out the body text
    news_p = art_teaser_body.find('div',  class_='article_teaser_body').text



    # In[7]:


    scraped_data['news_title'] = news_title
    scraped_data['news_p'] = news_p


    # In[8]:


    # site 2 - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    base_url = 'https://www.jpl.nasa.gov'
    # use splinter to connect to the url and navigate, then use bs4 to repeat what you did in site 1
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)

    # object img  class=fancybox-image
    html = browser.html
    soup = bs(html, 'html.parser')

    img_class = soup.find('img', class_='fancybox-image')
    img_url = img_class['src']
    featured_image_url = base_url + img_url
    # print(featured_image_url)

    # Load it to the dataframe
    scraped_data['featured_image_url'] = featured_image_url


    # In[9]:


    # site 3 - https://twitter.com/marswxreport?lang=en

    # grab the latest tweet and be careful its a weather tweet
    # P class='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'
    # Example:
    #mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
    # These seem to always start with 'InSight Sol'
    time.sleep(3)

    twit_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(twit_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(3)

    # Get an article block.
    weather_block = soup.find_all('div', class_='js-tweet-text-container')
    # print("Printing Weather Block")
    # print(weather_block)


    # print("starting for tweet loop")
    for tweet in weather_block:
    #     print("---  Begin inside loop ----")
        p_text = tweet.p.text
    #     print(p_text)



        # do a regex on the string to see if there is 'InSight Sol'
        # at beginning of string.
        #  result = re.match(pattern, string)
        cmpld_str = re.compile('InSight')

        result = cmpld_str.match(p_text)
    #     print(result)
    #     print(result.group())
        if result.group() == 'InSight':
    #         print("Inside if result for RegEx")
    #         print(p_text)

            # Store it in the dataframe
            scraped_data['weather_data'] = p_text
    #         print("")
            break
        # Once we confirm we found a weather post with InSight, exit loop.

    #     print("---  End inside loop ----")
    #     print("")

    # print("End of tweet loop")


    # In[10]:


    # site 4 -
    facts_url = 'https://space-facts.com/mars/'

    # use pandas to parse the table

    facts_df = pd.read_html(facts_url)[0]
    # print(facts_df)


    # convert facts_df to a html string and add to dictionary.
    facts_html_str = facts_df.to_html(index=False, justify='center', table_id='facts_table')
    # print(facts_html_str)

    scraped_data['facts_html_str'] = facts_html_str


    # In[11]:


    # site 5

    # set base URL for this site
    astro_base_url = 'https://astrogeology.usgs.gov'

    # use bs4 to scrape the title and url and add to dictionary
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')


    #- get all the listings.
    hemi_block = soup.find_all('div', class_='description')


    ll_hemi_image_urls = []
    cntr = 0
    for block in hemi_block:
        cntr +=1
    #     print(f'Counter is: {cntr}')
        img_url = block.a['href'] #- this isn't valid yet. have to nav to it then get full link to image
        title = block.a.text
    #     print(f'Url to image page: {img_url}')
    #     print(f'title is: {title}')  #- this is valid.

        full_img_url = astro_base_url + img_url
        browser.visit(full_img_url)
        time.sleep(5)
        iHtml = browser.html
        isoup = bs(iHtml, 'html.parser')
        tmp = isoup.find('div', class_='downloads')
    #     print(f'tmp is now: {tmp}')

        img_url = tmp.a['href']
    #     print(f'img_url is now: {img_url}')
    #     print('==============')
    #     print('')
        ll_hemi_image_urls.append({"title": title, "img_url": img_url})

    # print(ll_hemi_image_urls)
    scraped_data['hemisphere_image_urls'] = ll_hemi_image_urls

    # # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    # ]


    # In[12]:


    # Close the browser
    browser.quit()

    # Print the data gather out
    # print(scraped_data)


    # In[13]:


    # File-> download as python into a new module called scrape_mars.py


    # In[14]:


    # use day 3 09-Ins_Scrape_And_Render/app.py as a blue print on how to finish the homework.

    # replace the contents of def index() and def scraper() appropriately.

    # change the index.html to render the site with all the data.

    return(scraped_data)