import pandas as pd
# import os
import requests
import time
import re

from bs4 import BeautifulSoup as bs
from splinter import Browser


# scrape_news
#  returns news_title, news_p
def scrape_news():
    print("IN call to SCRAPE NEWS")
    # site 1 - "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # probably need to replace this since it redirects
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    news_response = requests.get(news_url)
    time.sleep(2)

    # use beautiful soup to parse the url above
    news_soup = bs(news_response.text, 'html.parser')
    #newPSoup = bs(news_response.text, 'html.parser')

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

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

    # scraped_data['news_title'] = news_title
    # scraped_data['news_p'] = news_p
    browser.quit()
    return(news_title, news_p)


##
# JPL
#
#
def scrape_jpl():
    # print("in scrape JPL")
    # site 2 - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    base_url = 'https://www.jpl.nasa.gov'
    # # use splinter to connect to the url and navigate, then use bs4 to repeat what you did in site 1
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # browser.visit(url)

    image_response = requests.get(url)
    time.sleep(2)

    # use beautiful soup to parse the url above
    img_soup = bs(image_response.text, 'html.parser')
    time.sleep(5)
    img = img_soup.find('article', class_='carousel_item')
    str_img = img['style']
    a, featured_image_url, c = str_img.split("'")

    featured_image_url = base_url + featured_image_url
    print(featured_image_url)

    featured_image_caption = img_soup.find(
        'h1', class_='media_feature_title').text
    featured_image_caption = featured_image_caption.strip()
    print(featured_image_caption)

    return(featured_image_url, featured_image_caption)


def scrape_twitter():
    # site 3 - https://twitter.com/marswxreport?lang=en

    # grab the latest tweet and be careful its a weather tweet
    # P class='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'
    # Example:
    #mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
    # These seem to always start with 'InSight Sol'
    print("in scrape_twitter")
    time.sleep(3)

    twit_url = 'https://twitter.com/marswxreport?lang=en'
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
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

            # Now lets split on the hPa and grab first part of string
            # storing only that.
            first, second = p_text.split('hPa')
            first = first + " hPa"  # add back units of measure
            p_text = first

            # Once we confirm we found a weather post with InSight, exit loop.
            break

    #     print("---  End inside loop ----")
    #     print("")

    # print("End of tweet loop")
    browser.quit()
    return(p_text)

##
# Facts table
#


def scrape_facts():
    # print("IN Scrape Facts")
    # site 4 -
    facts_url = 'https://space-facts.com/mars/'

    # use pandas to parse the table

    facts_df = pd.read_html(facts_url)[0]
    # print(facts_df)

    # convert facts_df to a html string and add to dictionary.
    # facts_html_str = facts_df.to_html(index=False, justify='center', table_id='facts_table', escape=False)
    facts_df.to_html('templates/facts_table.html', index=False,
                     justify='center', escape=False, table_id='facts_table')

    # to ensure utf-8 for the html file, i'm going to read it, then write it
    FILEHANDLE_IN = open('templates/facts_table.html', "r")
    facts_str = FILEHANDLE_IN.read()

    facts_str.replace('\\n', '')

    facts_str = str(facts_str)
    FILEHANDLE_OUT = open(
        'templates/facts_table_clean.html', "w+", encoding='utf8')
    FILEHANDLE_OUT.write(facts_str)

    FILEHANDLE_IN.close()
    FILEHANDLE_OUT.close()

    # store it to the string...
    facts_html_str = facts_df.to_html(
        index=False, justify='center', escape=False, table_id='facts_table')
    # print(facts_html_str)
    return (facts_html_str)


##
# S
def scrape_img_urls():
    # set base URL for this site
    print("IN Scrape IMG URLS")
    astro_base_url = 'https://astrogeology.usgs.gov'

    # use bs4 to scrape the title and url and add to dictionary
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(hemi_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    # - get all the listings.
    hemi_block = soup.find_all('div', class_='description')

    ll_hemi_image_urls = []
    cntr = 0
    for block in hemi_block:
        cntr += 1
    #     print(f'Counter is: {cntr}')
        # - this isn't valid yet. have to nav to it then get full link to image
        img_url = block.a['href']
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
    browser.quit()
    return (ll_hemi_image_urls)
