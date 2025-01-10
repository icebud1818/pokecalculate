from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome in headless mode (no GUI)
options = Options()
options.headless = True  # Run in headless mode
options.add_argument('--no-sandbox')  # Important for GitHub Actions
options.add_argument('--disable-dev-shm-usage')  # Solve for memory issues
options.add_argument('--remote-debugging-port=9222')  # Avoid 'DevToolsActivePort' issue
options.add_argument('--disable-gpu')  # Disable GPU acceleration
options.add_argument('--disable-software-rasterizer')  # Disable software rasterization

# Specify the path for the WebDriver using Service (for Selenium 4)
service = Service(ChromeDriverManager().install())  # Automatically download and use the correct chromedriver

# Initialize the WebDriver with the specified options and service
driver = webdriver.Chrome(service=service, options=options)

# Navigate to a webpage
driver.get('https://www.example.com')

# Print the title of the page
print("Page Title:", driver.title)

# Close the browser
driver.quit()

