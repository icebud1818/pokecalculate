import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# import myUtils

from calculators import myUtils

def get_collectr_price(product_id):
    """
    Scrape the market price from Collectr using Selenium
    """
    # Set up Chrome options for headless browsing (optional)
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Remove this line if you want to see the browser
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"https://app.getcollectr.com/explore/product/{product_id}")
        
        # Wait for the price element to load
        wait = WebDriverWait(driver, 10)
        
        # Find the price element using the specific classes
        price_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.font-bold.text-2xl.text-white"))
        )
        
        price_text = price_element.text
        # Extract numeric value from price text (remove $ and commas)
        price = float(price_text.replace('$', '').replace(',', ''))
        
        return price
        
    except Exception as e:
        print(f"Error scraping Collectr price: {e}")
        return None
    finally:
        if driver:
            driver.quit()

def calculate(product):
    # Try to get price from Collectr first
    productPrice = get_collectr_price(product.productId)
    
    # Fallback to TCGPlayer if Collectr fails
    if productPrice is None:
        productResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{product.productId}/details?mpfev=3442")   
        productData = productResponse.json() 
        productPrice = productData.get("marketPrice") or productData.get("medianPrice") or productData.get("lowestPrice")
    
    promoPrice = 0
    for promo in product.promos:
        promoResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{promo}/details?mpfev=3442")   
        promoData = promoResponse.json() 
        promoPrice = promoPrice + (promoData.get("marketPrice") or promoData.get("medianPrice") or promoData.get("lowestPrice"))

    packTotal = 0
    for pack in product.packs:
        packTotal = packTotal + myUtils.get_last_pack_value(pack)

    print("Product: " + product.name)
    print("Product Price: " + str(productPrice))
    print("Promo(s) Price: " + str(promoPrice))
    print("Total Pack Value: " + str(packTotal))

    return productPrice, promoPrice, packTotal