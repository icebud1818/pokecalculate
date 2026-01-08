from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    print("Navigated to Google.")

    # Interact with the website (example: search for 'GitHub Actions')
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("GitHub Actions")
    search_box.send_keys(Keys.RETURN)
    print("Entered search query.")

    # Wait for the page title to contain the search query
    WebDriverWait(driver, 10).until(EC.title_contains("GitHub Actions"))
    print("Page title is:", driver.title)

    # Capture a screenshot (optional)
    driver.save_screenshot("screenshot.png")
    print("Screenshot captured.")

    # Output a success message
    print("Selenium script executed successfully!")

finally:
    # Close the WebDriver instance
    driver.quit()
