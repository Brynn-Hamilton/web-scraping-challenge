from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pandas as pd

def init_browser():
    driver_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **driver_path, headless=True)
    return browser

def visit_url(url, browser):
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def mars_news_scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    soup = visit_url(url, browser)
    news_title = soup.find('ul', class_='item_list').find('div', class_='content_title').find('a').text
    news_p = soup.find('ul', class_='item_list').find('div', class_='article_teaser_body').text
    return dict({'news_title':news_title, 'news_paragraph':news_p})

def jpl_mars_scrape():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    soup = visit_url(url, browser)
    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = base_url + featured_image_url
    return dict({'featured_image_url':featured_image_url})

def mars_facts():
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(mars_facts_url)
    df = mars_facts_table[0]
    html_table = df.to_html()
    return dict({'mars_facts_table':html_table})

def mars_hemispheres():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    soup = visit_url(url, browser)
    main_hemispheres_url = soup.find_all('div', class_='item')
    hemisphere_image_urls=[]
    for x in main_hemispheres_url:
        title = x.find('h3').text
        img_url = base_url + x.find('a')['href']
        mars_hemisphere_soup = visit_url(img_url, browser)
        original_hemisphere_img = mars_hemisphere_soup.find('div', class_='downloads').find('a')['href']
        hemisphere_image_urls.append(dict({'title':title, 'img_url':original_hemisphere_img}))
    return dict({'hemisphere_image_urls':hemisphere_image_urls})

def scrape():
    return {**mars_news_scrape(), **jpl_mars_scrape(), **mars_facts(), **mars_hemispheres()}