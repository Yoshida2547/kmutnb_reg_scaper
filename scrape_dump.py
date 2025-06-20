from selenium import webdriver
from selenium.webdriver.common.by import By

import time

def scraper(driver):

    # find elements by class name 'product-name'
    products = driver.find_elements(By.CLASS_NAME, "product-item")

    scraped_data = []

    # iterate over found elements and print their text content
    for product in products:
        product_name = product.find_element(By.CLASS_NAME, "product-name")
        product_price = product.find_element(By.CLASS_NAME, "product-price")

        data = {
            "name": product_name.text,
            "price": product_price.text,
        }

        # append the data to the empty list
        scraped_data.append(data)

    # return the scraped data
    return scraped_data

# instantiate options for Chrome
options = webdriver.ChromeOptions()

# run the browser in headless mode
options.add_argument("--headless=new")

print('Open Driver')

# instantiate Chrome WebDriver with options
driver = webdriver.Chrome(options=options)

# open the specified URL in the browser
driver.get("https://www.scrapingcourse.com/infinite-scrolling")

# execute the scraper function and print the scraped data
result = scraper(driver)

import json

with open('result.json', 'w') as f:
    f.write(json.dumps(result))

# close the browser
driver.quit()
