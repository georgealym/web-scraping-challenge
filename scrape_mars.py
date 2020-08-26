from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import os
import pandas as pd
import requests
from pprint import pprint

### NASA Mars News
url = "https://mars.nasa.gov/news/"
response = requests.get (url)
response
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
browser = init_browser()
browser.visit(url)
html = browser.html 
time.sleep(4)
soup = bs(html, 'html.parser')
time.sleep(2) 
results = soup.find_all("div",class_="list_text")
marsinfo={}
for result in results[:1]:
    try:
        news_title=result.find('div',class_="content_title").a.text
        news_description=result.find('div',class_="article_teaser_body").text
        if(news_description and news_title):
            print("Title:")
            print(news_title)
            print("Description:")
            print(news_description)
    except AttributeError as e:
        print(e)

news_date=result.find('div',class_="list_date").text
print("Date of Article:")
print(news_date)
marsinfo["title"]=news_title
marsinfo["paragraph"]=news_description
marsinfo["date"]=news_date
browser.quit()


### JPL Mars Space Images - Featured Image
url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path)
browser.visit(url)
time.sleep(3)

soup = bs(browser.html, 'html.parser')
featured_image=soup.find('article', class_="carousel_item")
pprint(featured_image)
forurl = featured_image['style'][23:-3]
featured_image_url = 'https://www.jpl.nasa.gov/' + forurl
marsinfo["featured_image"]=featured_image_url
print(featured_image_url)
browser.quit()

### Mars Facts
url = 'https://space-facts.com/mars/'
tables = pd.read_html(url)
pprint(tables)
df = tables[0]
df.columns = ['Data', 'Information']
df
df.to_html('mars_facts.html')
mars_facts = df.to_html()
marsinfo["facts"]=mars_facts
pprint(mars_facts)

### Mars Hemispheres
url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path)
browser.visit(url)
time.sleep(3)
hemisphere_urls = []

# Get a List of All the Hemispheres
urls = browser.find_by_css("a.product-item h3")
for item in range(len(urls)):
    hemisphere = {}
    browser.find_by_css("a.product-item h3")[item].click()
    hemisphere["title"] = browser.find_by_css("h2.title").text
    findelement = browser.links.find_by_text("Sample").first
    hemisphere["image_link"] = findelement["href"]
    hemisphere_urls.append(hemisphere)
    browser.back()
browser.quit()

