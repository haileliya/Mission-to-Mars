#We are refractoring the code so that it can be reused often to pull the most recent data. 
#We are adding a function to enable this capability by bundling our code into something that is easy for us to use an druse as need

#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#Let's define this function as "scrape_all" and then initiate the browser.
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #Set out news title and paragraph variables. this code tells python that we will be using our mars_news funtion to pull this data
    news_title, news_paragraph = mars_news(browser)

    #Create data dictionary
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

#Adding a function to our scraping
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling. always before the scraping
    try:
    
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None 
    return news_title, news_p

#We need to add an argument to the function by updating first command to def mars_news(broswer)
#When we add the word "browser" to our function, we're telling Python that we'll be using the browser variable we defined outside the function. 
#All of our scraping code utilizes an automated browser

###Error Handling

#in web scraping the most common cause of an error is when the webpage's 
#format has changed and the scraping code no longer matches the new HTML elements.

#We're going to add a try and except clause addressing AttributeErrors. By adding this error handling, 
#we are able to continue with our other scraping portions even if this one doesn't work.
#it needs to be added before the scraping starts

###Featured Image Scraping

def featured_image(browser):
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

    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None, None    
    
    # Use the base URL to create an absolute URL
    #We're using an f-string for this print statement because it's a cleaner way to create print statements; 
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

### Table Scraping

#Similar as above but will be adding BaseException for error handling. Use this because we are using read_html() function to pull data instead of beautiful soup and splinter

def mars_facts():
    
    #Add try/except for error handling
    try: 
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    #assign columns to the new DataFrame for additional clarity.
    df.columns=['description', 'Mars', 'Earth']
    
    #turning the Description column into the DataFrame's index. inplace=True means that 
    #the updated index will remain in place, without having to reassign the DataFrame to a new variable.
    df.set_index('description', inplace=True)

    #How do we add the DataFrame to a web application? and make sure that is updated live when the html is updated
    #use the .to_html() function.
    #Convert dataframe into HTML format, add bootstrap
    return df.to_html()

###Establishing the link between scraped data and the database
#To do this at the top of the script, after dependecies we need to add one more function that initializes the browser, 
#creates a data dictionary, and ends the webdrive and returns the scraped data.
#Please go see first function in script. 

#This last block of code tells Flask that our script is complete and ready for action. 
# The print statement will print out the results of our scraping to our terminal after executing the code.
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())