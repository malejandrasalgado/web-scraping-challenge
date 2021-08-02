# Import dependencies and setup
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from IPython.display import HTML
import time


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    print("----------------STARTING---------------")
    browser = init_browser()

#################################################
# NASA Mars News
#################################################

    # Connecting to the NASA
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Scrape the Mars News Site
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")
    # Scrape the Latest News Title
    news_title = slide_element.find("div", class_="content_title").get_text()

    # Scrape the Latest News Paragraph
    news_paragraph = slide_element.find(
        "div", class_="article_teaser_body").get_text()


#################################################
# JPL Mars Space Images
#################################################

    # Connecting to the spaceimages
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    # Find the image url for the current Featured Mars Image and assign the url string to a variable
    browser.click_link_by_partial_text('FULL IMAGE')

    # Save a complete url string for this image
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    featuredurl = ""
    for link in image_soup.find_all('img'):
        if "featured" in link.get('src'):
            featuredurl = link.get('src')

    featured_image = f"https://spaceimages-mars.com/{featuredurl}"
    print(featured_image)

#################################################
# Mars Facts
#################################################

    # Use Pandas to scrape the table containing facts
    mars_facts = pd.read_html("https://galaxyfacts-mars.com/")

    # Take table for Mars facts
    df = mars_facts[1]

    # Rename columns and set index
    df.columns = ['description', 'value']

    # Use Pandas to convert the data to a HTML table string.
    mars_facts_table = [df.to_html(
        classes='data table table-borderless', index=False, header=False, border=0)]


#################################################
# Mars Hemispheres
#################################################

    # Connecting to the NASA visit the astrogeology site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Save Hemisphere title containing the hemisphere name
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = []

    # Search for the names of all four hemispheres
    results = soup.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')

    # Get text and store in list
    for name in hemispheres:
        title.append(name.text)

    # Search for thumb class links
    thumb_results = results[0].find_all('a')
    thumb_links = []

    for thumb in thumb_results:

        # Find if the thumb element has an image
        if (thumb.img):

            # then attached link
            thumb_url = 'https://astrogeology.usgs.gov/' + thumb['href']

            # Append list with thumb url
            thumb_links.append(thumb_url)

    # Find full resolution images

    full_images = []

    for url in thumb_links:

        # Click through each thumb link
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Scrape each page for the image path
        results = soup.find_all('img', class_='wide-image')
        image_path = results[0]['src']

        # Add the image path to get the full url
        image_link = 'https://astrogeology.usgs.gov/' + image_path

        # Append full image links to a list
        full_images.append(image_link)

    # compile together the hemisphere title and full image links
    # Using  the zip() funtion

    mars_results = zip(thumb_links, full_images)

    hemisphere_image_urls = []

    # Iterate through the zipped object
    for title, img in mars_results:

        mars_hemisphere = {}

        # Add hemisphere title to dictionary
        mars_hemisphere['title'] = title

        # Add image url to dictionary
        mars_hemisphere['img_url'] = img

        # Append the list with dictionaries
        hemisphere_image_urls.append(mars_hemisphere)


#################################################
#  Store data in a dictionary
#################################################
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image,
        "mars_facts": mars_facts_table,
        "hemispheres": hemisphere_image_urls
    }
    print(mars_data)
    print("----------------FINISHING---------------")
    # Close the browser
    browser.quit()

    # Return results
    return mars_data


# print("--------------------RUNNING--------------------")
# print(scrape())
# print("--------------------FINISHED--------------------")
