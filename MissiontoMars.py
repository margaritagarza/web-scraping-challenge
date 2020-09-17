
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from sqlalchemy import create_engine
import numpy as np
from splinter import Browser

def GetMarsData():

    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    print(soup.prettify())

    # scrap titles
    titles = soup.find(class_='content_title')
    print(titles.text)

    # Print all paragraph texts
    paragraphs = soup.find(class_="rollover_description_inner")
    print(paragraphs.text)

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', executable_path, headless=False)

    # URL of page to be scraped
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    link  = soup.find("a", class_="button fancybox").attrs['data-link']

    print(link )
    browser.visit("https://www.jpl.nasa.gov"+link)

    html1 = browser.html
    imgSoup = bs(html1, 'html.parser')
    img_url= imgSoup.find("img", class_="main_image").attrs['src']
    print(img_url)
    
    
    featured_image_url ="https://www.jpl.nasa.gov"+img_url
    print(featured_image_url)


    #Extract HTML tables into DataFrames
    html_link = "https://space-facts.com/mars/"
    mars_facts=pd.read_html(html_link)

    total_tables_found=len(mars_facts)
    print(f"There's a Total of {total_tables_found} tables found on the Wikipedia HTML")


    df = mars_facts[1]
    df

    # In[14]:

    html_table = df.to_html()
    html_table

    #HEMISPHERES URLs 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
        print(title)
        print(image_url)

    marsdictionary =  {"marstitle":titles.text, "marsparagraph":paragraphs.text, "marsfeatured":featured_image_url, "marsfacts":html_table, "marshemispheres":mars_hemisphere }

    return marsdictionary

#GetMarsData()