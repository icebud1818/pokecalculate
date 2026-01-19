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
    SealedProduct("2009 Spring Collector's Tin (Shaymin Lv. X)", 485824, "3/2/2009", [507, 507, 506, 501], [89116]),
    SealedProduct("2009 Spring Collector's Tin (Dialga Lv. X)", 485825, "3/2/2009", [507, 507, 506, 501], [84814]),
    SealedProduct("2009 Fall Collector's Tin (Garchomp Lv. X)", 485826, "9/2/2009", [509, 509, 508, 506], [85630]),
    SealedProduct("2009 Fall Collector's Tin (Rayquaza Lv. X)", 485827, "9/2/2009", [509, 509, 508, 506], [88641]),
    SealedProduct("Arceus Collector's Tin (Blue)", 485830, "12/16/2009", [510, 510, 507, 502], [83606]),
    SealedProduct("HGSS Trainer Kit", 98731, "5/1/2010", [600], [88521, 85998]),
    SealedProduct("Dialga and Palkia Clash of Legends Box", 206310, "11/3/2010", [601, 510, 509, 508], [87918, 84811]),
    SealedProduct("Darkrai and Cresselia Clash of Legends Box", 206309, "11/3/2010", [601, 510, 509, 508], [84711, 84472]),
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