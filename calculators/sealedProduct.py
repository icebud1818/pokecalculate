import requests
from calculators import myUtils

def calculate(product):

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