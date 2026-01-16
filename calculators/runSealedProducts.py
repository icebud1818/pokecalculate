# import sealedProduct
# import myUtils
from calculators import (
myUtils, sealedProduct
)

class SealedProduct:
    def __init__(self, name, productId, packs, promos):
        self.name = name
        self.productId = productId
        self.packs = packs
        self.promos = promos

sealedProductList = [
    SealedProduct("Hidden Fates Tin (Raichu)", 193438, [910.5, 910.5, 910.5, 910.5], [197876]),
    SealedProduct("Hidden Fates Tin (Charizard)", 193437, [910.5, 910.5, 910.5, 910.5], [197874]),
    SealedProduct("Empoleon Lv. X Tin", 10029356, [500, 500, 501, 501], [85207])
]

# Sealed Products
sealed_output_data = []
for product in sealedProductList:
    productPrice, promoPrice, packTotal = sealedProduct.calculate(product)
    sealed_output_data.append({
        "name": product.name,
        "productId": product.productId,
        "price": productPrice,
        "promoPrice": promoPrice,
        "packTotal": packTotal,
    })

for product in sealed_output_data:
    doc_id = str(product["productId"])
    myUtils.db.collection("sealedProducts").document(doc_id).set(product)