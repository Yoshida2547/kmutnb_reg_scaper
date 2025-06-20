# pip3 install selenium
from selenium import webdriver

# instantiate options for Chrome
options = webdriver.ChromeOptions()

# run the browser in headless mode
options.add_argument("--headless=new")

# instantiate Chrome WebDriver with options
driver = webdriver.Chrome(options=options)

# URL of the web page to scrape
url = "https://www.scrapingcourse.com/javascript-rendering"

# open the specified URL in the browser
driver.get(url)

# print the page source
print(driver.page_source)

# close the browser
driver.quit()