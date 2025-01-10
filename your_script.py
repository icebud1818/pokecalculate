from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Configure Chrome options for headless mode
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Disable GPU acceleration
options.add_argument('--no-sandbox')  # Required for some CI environments
options.add_argument('--disable-dev-shm-usage')  # Overcomes limited resource problems
options.add_argument('--remote-debugging-port=9222')  # Debugging
options.add_argument('--window-size=1920,1080')  # Set window size for headless

# Path to the ChromeDriver
service = Service("/usr/bin/chromedriver")  # Adjust path if necessary

# Create a new WebDriver instance
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to a website (example: Google)
    driver.get("https://www.google.com")

    # Interact with the website (example: search for 'GitHub Actions')
    test = driver.find_element(By.XPATH, "/html/body/div[3]/header/div[2]/a[2]")
    '''
    search_box.send_keys("GitHub Actions")
    search_box.send_keys(Keys.RETURN)
'''
    # Wait for results to load and print page title
    driver.implicitly_wait(10)  # Wait for the page to load
    print("Page title is:", test.text)

    # Capture a screenshot (optional)
    driver.save_screenshot("screenshot.png")

    # Output a success message
    print("Selenium script executed successfully!")

finally:
    # Close the WebDriver instance
    driver.quit()

