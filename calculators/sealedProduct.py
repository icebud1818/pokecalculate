import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
try:
    from calculators import myUtils
except ImportError:
    import myUtils



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
        time.sleep(1)
        
        # Wait for the price element to load
        wait = WebDriverWait(driver, 30)
        
        # Find the price element using the specific classes
        # Find any span that contains a dollar sign
        price_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'font-bold') and contains(@class, 'text-white') and contains(text(), '$')]"))
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

def get_pack_list_with_names(pack_ids):
    """
    Convert list of pack IDs to a list of pack objects with names, counts, and prices
    Returns: [{"name": "Pack Name", "count": 2, "price": 50.00}, ...]
    """
    from collections import Counter
    
    # Count occurrences of each pack ID
    pack_counts = Counter(pack_ids)
    
    pack_list = []
    for pack_id, count in pack_counts.items():
        pack_name = myUtils.get_set_name(pack_id)
        pack_price = myUtils.get_last_pack_value(pack_id)
        if pack_name:
            pack_list.append({
                "name": pack_name,
                "count": count,
                "price": pack_price
            })
    
    return pack_list

def get_promo_list_with_details(promo_ids):
    """
    Get promo card details including name and price
    Returns: [{"name": "Promo Name", "price": 12.34}, ...]
    """
    promo_list = []
    
    for promo_id in promo_ids:
        try:
            promoResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{promo_id}/details?mpfev=3442")
            promoData = promoResponse.json()
            
            promo_name = promoData.get("productUrlName", "Unknown Promo")
            promo_price = promoData.get("marketPrice") or promoData.get("medianPrice") or promoData.get("lowestPrice") or 0
            
            promo_list.append({
                "name": promo_name,
                "price": promo_price
            })
        except Exception as e:
            print(f"Error fetching promo {promo_id}: {e}")
            promo_list.append({
                "name": "Unknown Promo",
                "price": 0
            })
    
    return promo_list

def calculate(product):
    # Try to get price from Collectr first
    productPrice = get_collectr_price(product.productId)
    
    # Fallback to TCGPlayer if Collectr fails
    if productPrice is None:
        print("failed to get price")
    
    # Get promo list with details
    promo_list = get_promo_list_with_details(product.promos)
    
    # Calculate total promo price
    promoPrice = sum(promo["price"] for promo in promo_list)

    packTotal = 0
    for pack in product.packs:
        packTotal = packTotal + myUtils.get_last_pack_value(pack)

    # Get pack list with names
    pack_list = get_pack_list_with_names(product.packs)

    print("Product: " + product.name)
    print("Product Price: " + str(productPrice))
    print("Promo(s) Price: " + str(promoPrice))
    print("Total Pack Value: " + str(packTotal))
    print("Pack List: " + str(pack_list))
    print("Promo List: " + str(promo_list))

    return productPrice, promoPrice, packTotal, pack_list, promo_list