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


class CollectrScraper:
    """
    Reusable browser instance for scraping Collectr prices
    """
    def __init__(self, max_requests=50):
        self.max_requests = max_requests
        self.request_count = 0
        self.driver = None
        self._init_driver()
    
    def _init_driver(self):
        """Initialize or restart the Chrome driver"""
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Close existing driver if it exists
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.request_count = 0
    
    def get_price(self, product_id):
        """
        Scrape the market price from Collectr using Selenium
        """
        # Restart browser after max_requests to prevent memory issues
        if self.request_count >= self.max_requests:
            print(f"Restarting browser after {self.request_count} requests")
            self._init_driver()
        
        try:
            self.driver.get(f"https://app.getcollectr.com/explore/product/{product_id}")
            
            wait = WebDriverWait(self.driver, 30)
            
            # First, wait for the page structure to load (wait for image or main content)
            # This ensures the JavaScript has started running
            try:
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
                print("Page structure loaded (image found)")
            except:
                print("Warning: No image found, continuing anyway")
            
            # Give JavaScript extra time to fetch and populate data
            time.sleep(2)
            
            # Now wait for price element with non-zero value
            def price_is_valid(driver):
                try:
                    element = driver.find_element(By.XPATH, 
                        "//span[contains(@class, 'font-bold') and contains(@class, 'text-white') and contains(text(), '$')]"
                    )
                    price_text = element.text.replace('$', '').replace(',', '').strip()
                    if price_text:
                        price = float(price_text)
                        if price > 0:
                            print(f"Found valid price: ${price}")
                            return True
                        else:
                            print(f"Price is still $0, waiting...")
                except Exception as e:
                    print(f"Price element not ready: {e}")
                return False
            
            # Wait up to 30 seconds for valid price
            wait.until(price_is_valid)
            
            # Get the final price
            price_element = self.driver.find_element(By.XPATH, 
                "//span[contains(@class, 'font-bold') and contains(@class, 'text-white') and contains(text(), '$')]"
            )
            price_text = price_element.text
            price = float(price_text.replace('$', '').replace(',', ''))
            
            self.request_count += 1
            return price
            
        except Exception as e:
            print(f"Error scraping Collectr price for product {product_id}: {e}")
            # Try restarting the browser on error
            try:
                self._init_driver()
            except:
                pass
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support"""
        self.close()


# Global scraper instance (optional - for convenience)
_global_scraper = None

def get_collectr_price(product_id, scraper=None):
    """
    Scrape the market price from Collectr using Selenium
    If scraper is provided, use it. Otherwise use global scraper.
    """
    global _global_scraper
    
    # Use provided scraper, or global scraper, or create new one
    if scraper is not None:
        return scraper.get_price(product_id)
    
    # Initialize global scraper if needed
    if _global_scraper is None:
        _global_scraper = CollectrScraper()
    
    return _global_scraper.get_price(product_id)


def cleanup_scraper():
    """Clean up the global scraper (call this when you're done)"""
    global _global_scraper
    if _global_scraper is not None:
        _global_scraper.close()
        _global_scraper = None


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


def calculate(product, scraper=None):
    """
    Calculate product value
    
    Args:
        product: Product object with productId, promos, packs, and name
        scraper: Optional CollectrScraper instance for reusing browser
    """
    # Try to get price from Collectr first
    productPrice = get_collectr_price(product.productId, scraper)
    
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