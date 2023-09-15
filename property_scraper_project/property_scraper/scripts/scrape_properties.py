
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from property_scraper.models import Property
from django.utils import timezone

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_properties():
    # Initialize Chrome options
    options = Options()
    options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors

    # Initialize ChromeDriver service (optional)
    chrome_service = Service()  # Replace with your path

    # Initialize WebDriver with options
    driver = webdriver.Chrome(service=chrome_service, options=options)


    # List of cities and their URLs
    cities = [
        {'name': 'Hyderabad', 'url': 'https://www.99acres.com/search/property/buy/hyderabad-all?city=38&preference=S&area_unit=1&res_com=R'},
       
    ]

    for city in cities:
        driver.get(city['url'])
        time.sleep(5)  # Adjust as needed to allow page to load

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract property details
        property_listings = soup.find_all('div', class_='property-listing')

        for listing in property_listings:
            property_name = listing.find('div', class_='heading-18').text.strip()
            property_cost = listing.find('div', class_='price').text.strip()
            property_type = listing.find('div', class_='type').text.strip()
            property_area = listing.find('div', class_='size').text.strip()
            property_locality = listing.find('div', class_='locality').text.strip()
            property_city = city['name']
            property_link = listing.find('a', class_='body-14')['href']

            # Save the scraped data to MongoDB
            Property.objects.create(
                name=property_name,
                cost=property_cost,
                type=property_type,
                area=property_area,
                locality=property_locality,
                city=property_city,
                link=property_link,
                scraped_at=timezone.now()
            )

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    scrape_properties()
