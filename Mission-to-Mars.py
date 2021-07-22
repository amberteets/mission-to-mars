# Add dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

# Scrape to find most recent article title and description
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

### JPL Space Images Featured Image

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

### Mars Facts

# Scrape table with Pandas
## Searches for HTML tables and pulls first table it encounters
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df.head()

# Convert back to HTML-ready code
df.to_html()

### Mars Weather

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

### Scrape High-Resolution Mars’ Hemisphere Images and Titles

#### Hemispheres

# Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# Create list to hold image links and titles
hemisphere_image_urls = []

# Retrieve full-size image urls and titles for each hemisphere

for hemisphere in range(4):
    # Initialize dictionary to hold title, url
    hemispheres = {}
    # Click link to enhanced image
    browser.find_by_css('a.itemLink.product-item h3')[hemisphere].click()
    html = browser.html
    parsed = soup(html, 'html.parser')
    # Get enhanced image url
    hemispheres['title'] = parsed.find('h2', class_='title').text
    hemispheres['img_url'] = parsed.find('a', text='Sample').get('href')
    hemisphere_image_urls.append(hemispheres)
    # Direct browser back to main page
    browser.back()

# Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

### End Automated Browsing

browser.quit()

