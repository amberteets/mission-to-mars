# Add dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemispheres_dict = mars_hemispheres(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres_dict,
        }

    # Stop webdriver and return data
    browser.quit()
    return data

## Featured Article

def mars_news(browser):

    # Scrape Mars News
    # Visit the NASA site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Setup HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

## Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

## Mars Facts

def mars_facts():

    try:
        # Scrape table with Pandas
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # Assign columns and set index of DataFrame
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert back to HTML-ready code with Bootstrap component
    return df.to_html(classes="table table-striped", justify="center")

def mars_hemispheres(browser):

    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create list to hold image links and titles
    hemisphere_image_urls = []

    for hemisphere in range(4):
        # Initialize dictionary to hold title, url
        hemispheres = {}

        try:
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
        except BaseException:
            return None
    
    return hemisphere_image_urls

# Tell Flask that script is ready to be run, and print results of scraping
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())