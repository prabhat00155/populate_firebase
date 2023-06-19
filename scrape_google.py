from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def trending(category, location):
  # Configure Chrome options
  chrome_options = Options()
  chrome_options.add_argument("--headless")  # Run Chrome in headless mode

  # Set path to chromedriver executable
  webdriver_service = Service('/opt/homebrew/bin/chromedriver')

  # Create a new instance of the Chrome driver
  driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

  # Define the search query
  query = f"trending {category} in {location}"

  # Perform the Google search
  driver.get(f"https://www.google.com/search?q={query}")

  # Get the page source
  page_source = driver.page_source

  # Close the browser
  driver.quit()

  # Parse the HTML using BeautifulSoup
  soup = BeautifulSoup(page_source, 'html.parser')

  # Find the search results container
  result = soup.find('div', {'id': 'main'})

  lines = result.find_all('div', attrs={'data-entityname': True})
  res = []
  for line in lines:
    res.append(line.text)
  return res
