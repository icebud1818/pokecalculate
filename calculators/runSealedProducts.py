try:
    from calculators import myUtils, sealedProduct
except ImportError:
    import myUtils
    import sealedProduct

import firebase_admin
from firebase_admin import firestore
from datetime import datetime

class SealedProduct:
    def __init__(self, name, productId, releaseDate, packs, promos):
        self.name = name
        self.productId = productId
        self.packs = packs
        self.promos = promos
        self.releaseDate = releaseDate

sealedProductList = [
    SealedProduct("Diamond & Pearl Collector's Tin (Empoleon Lv. X)", 10029356, "9/1/2007", [500, 500, 501, 501], [85207]),
    SealedProduct("Diamond & Pearl Collector's Tin (Infernape Lv. X)", 10029355, "9/1/2007", [500, 500, 501, 501], [86282]),
    SealedProduct("Diamond & Pearl Collector's Tin (Torterra Lv. X)", 10029354, "9/1/2007", [500, 500, 501, 501], [89990]),
    SealedProduct("Spring Collector's Tin (Shaymin Lv. X)", 485824, "3/2/2009", [507, 507, 506, 501], [89116]),
    SealedProduct("Spring Collector's Tin (Dialga Lv. X)", 485825, "3/2/2009", [507, 507, 506, 501], [84814]),
    SealedProduct("Fall Collector's Tin (Garchomp Lv. X)", 485826, "9/2/2009", [509, 509, 508, 506], [85630]),
    SealedProduct("Fall Collector's Tin (Rayquaza Lv. X)", 485827, "9/2/2009", [509, 509, 508, 506], [88641]),
    SealedProduct("Arceus Collector's Tin (Blue)", 485830, "12/16/2009", [510, 510, 507, 502], [83606]),
    SealedProduct("HGSS Trainer Kit", 98731, "5/1/2010", [600], [88521, 85998]),
    SealedProduct("Dialga and Palkia Clash of Legends Box", 206310, "11/3/2010", [601, 510, 509, 508], [87918, 84811]),
    SealedProduct("Darkrai and Cresselia Clash of Legends Box", 206309, "11/3/2010", [601, 510, 509, 508], [84711, 84472]),
    SealedProduct("New Legends Tins (Reshiram)", 98615, "5/2/2011", [700, 700, 700, 700], [88705]),
    SealedProduct("New Legends Tins (Zekrom)", 98616, "5/2/2011", [700, 700, 700, 700], [90733]),
    SealedProduct("Super Snivy Box", 177530, "9/1/2011", [701, 701, 701], [281967]),
    SealedProduct("Terrific Tepig Box", 177531, "9/1/2011", [701, 701, 701], [153068]),
    SealedProduct("Outstanding Oshawott Box", 177532, "9/1/2011", [701, 701, 701], [211603]),
    SealedProduct("Zoroark-Illusions Collection", 98620, "10/5/2011", [701, 701, 604], [90752]),
    SealedProduct("Reshiram Box", 98621, "10/19/2011", [701, 701, 701, 701], [88706]),
    SealedProduct("Zekrom Box", 98622, "10/19/2011", [701, 701, 701, 701], [90734]),
    SealedProduct("Evolved Battle Action Tin (Serperior) (UPC: 107146)", 98623, "11/2/2011", [701, 701, 700, 604, 603], [89071]),
    SealedProduct("Evolved Battle Action Tin (Samurott) (UPC: 107146)", 98625, "11/2/2011", [701, 701, 700, 604, 603], [88909]),
    SealedProduct("V for Victini Tin", 98632, "12/5/2011", [702, 702, 702, 702, 702], [90346]),
    SealedProduct("Mewtwo Collection", 98635, "2/8/2012", [703, 703, 703], [83739]),
    SealedProduct("Reshiram EX Tin (UPC: 107641)", 98636, "3/21/2012", [703, 703, 702, 701], [88714]),
    SealedProduct("Zekrom EX Tin (UPC: 107641)", 98638, "3/21/2012", [703, 703, 702, 701], [90741]),
    SealedProduct("Kyurem EX Tin (UPC: 107641)", 98637, "3/21/2012", [703, 703, 702, 701], [86567]),
    SealedProduct("Forces of Nature Collection", 98639, "4/18/2012", [701, 701, 604], [89904, 89975, 86592]),
    SealedProduct("Keldeo Box", 206308, "10/8/2012", [705, 705, 702], [96885]),
    SealedProduct("Black Kyurem Box", 206306, "4/24/2013", [707, 706, 703, 701], [83852]),
    SealedProduct("White Kyurem Box", 206307, "4/24/2013", [707, 706, 703, 701], [90587]),
    SealedProduct("Team Plasma Box", 10032255, "5/29/2013", [707, 708, 709], [84703, 85739]),
    SealedProduct("Team Plasma Tin (Lugia EX) (UPC: 108600)", 137095, "9/11/2013", [709, 709, 708, 707], [86914]),
    SealedProduct("Team Plasma Tin (Deoxys EX) (UPC: 108600)", 137096, "9/11/2013", [709, 709, 708, 707], [84776]),
    SealedProduct("Team Plasma Tin (Thundurus EX) (UPC: 108600)", 137097, "9/11/2013", [709, 709, 708, 707], [89908]),
    SealedProduct("Red Genesect Collection", 10032256, "9/25/2013", [707, 709], [85663]),
    SealedProduct("Legendary Dragons of Unova Collection", 206316, "11/1/2013", [709, 705, 703, 706], [227477, 227480, 248804]),
]

# Get current timestamp
current_timestamp = firestore.SERVER_TIMESTAMP

# Sealed Products - Use reusable browser for better performance
sealed_output_data = []

print(f"Processing {len(sealedProductList)} sealed products...")

# Create a single browser instance for all products
with sealedProduct.CollectrScraper() as scraper:
    for i, product in enumerate(sealedProductList, 1):
        print(f"\nProcessing {i}/{len(sealedProductList)}: {product.name}")
        
        productPrice, promoPrice, packTotal, pack_list, promo_list = sealedProduct.calculate(product, scraper)
        sealed_output_data.append({
            "name": product.name,
            "productId": product.productId,
            "price": productPrice,
            "promoPrice": promoPrice,
            "packTotal": packTotal,
            "releaseDate": product.releaseDate,
            "packList": pack_list,
            "promoList": promo_list,
            "lastUpdated": current_timestamp  # Add timestamp to each product
        })

print("\nUploading to Firebase...")

# Upload to Firebase
for product in sealed_output_data:
    doc_id = str(product["productId"])
    myUtils.db.collection("sealedProducts").document(doc_id).set(product)

print("Done!")