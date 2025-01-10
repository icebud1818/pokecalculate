from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Automatically handles driver management

# Set up Chrome in headless mode (no GUI)
options = Options()
options.headless = True  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Specify the path for the WebDriver using Service (for Selenium 4)
service = Service(ChromeDriverManager().install())  # Automatically downloads and uses the appropriate chromedriver

# Initialize the WebDriver with the specified options and service
driver = webdriver.Chrome(service=service, options=options)

# Navigate to a webpage
driver.get('https://www.example.com')

# Print the title of the page
print("Page Title:", driver.title)

# Close the browser
driver.quit()

