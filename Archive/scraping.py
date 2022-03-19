#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#set your executable path in the next cell
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
#Secondly, we're also telling our browser to wait one second before searching for components. 
#The optional delay is useful because sometimes dynamic pages take a little while to load,

#Setup the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

#Notice how we've assigned slide_elem as the variable to look for the <div /> tag and its descendent 
#(the other tags within the <div /> element)? This is our parent element. 
#This means that this element holds all of the other elements within it, and we'll reference it when we want to 
#filter search results even further. The . is used for selecting classes, such as list_text, 
#so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. CSS works from right to left, 
#such as returning the last item on the list instead of the first. 
#Because of this, when using select_one, the first matching element returned will be a <li /> element with a 
#class of slide and all nested elements within it.

#HTML attribute will we use to scrape the article’s title
#class="content_title"

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
#With this new code, we’re searching within that element for the title. We’re also stripping the additional 
#HTML attributes and tags with the use of .get_text().
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#add the summary text.
news_summary = slide_elem.find('div', class_="article_teaser_body").get_text()
news_summary

# ###Featured Images
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

#The code above automatically clicked the full image. 
#Now we need to parse it so we can otniue  to scrape the full-size image URL

#Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url
#We're using an f-string for this print statement because it's a cleaner way to create print statements; 
#they're also evaluated at run-time.

####Mars FACTS

#Instead of scraping each row, or the data in each <td />, 
#we're going to scrape the entire table with Pandas' .read_html() function.

#With this line, we're creating a new DataFrame from the HTML table. 
#By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
df = pd.read_html('https://galaxyfacts-mars.com')[0]
#assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'Mars', 'Earth']
#turning the Description column into the DataFrame's index. inplace=True means that 
#the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace=True)
df

#How do we add the DataFrame to a web application? and make sure that is updated live when the html is updated
#use the .to_html() function 

df.to_html()

browser.quit()


