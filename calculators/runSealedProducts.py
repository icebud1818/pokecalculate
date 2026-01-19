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
    SealedProduct("Hidden Fates Tin (Raichu)", 193438, "10/1/2019", [910.5, 910.5, 910.5, 910.5], [197876]),
    SealedProduct("Hidden Fates Tin (Charizard)", 193437, "10/1/2019", [910.5, 910.5, 910.5, 910.5], [197874]),
    SealedProduct("Diamond & Pearl Collector's Tin (Empoleon Lv. X)", 10029356, "9/1/2007", [500, 500, 501, 501], [85207])
]

# Get current timestamp
current_timestamp = firestore.SERVER_TIMESTAMP

# Sealed Products
sealed_output_data = []
for product in sealedProductList:
    productPrice, promoPrice, packTotal, pack_list, promo_list = sealedProduct.calculate(product)
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

for product in sealed_output_data:
    doc_id = str(product["productId"])
    myUtils.db.collection("sealedProducts").document(doc_id).set(product)