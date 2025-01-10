from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome in headless mode (no GUI)
options = Options()
options.headless = True  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Specify the path for the WebDriver (chromedriver)
driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=options)

# Navigate to a webpage
driver.get('https://www.example.com')

# Print the title of the page
print("Page Title:", driver.title)

# Close the browser
driver.quit()

