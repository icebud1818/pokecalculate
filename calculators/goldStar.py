import requests
from calculators import myUtils
def calculate(set):

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    totalReverseValue = 0
    totalUltraRareValue = 0
    totalGoldStarValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    ultraRareCount = 0
    goldStarCount = 0

    # Dictionary to track unique cards for top 5
    unique_cards = {}

    # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/{set.tcgId}/cards/?rows=5000&productTypeID=1")    
    data = response.json() 

    # Define condition priority lists (best to worst)
    condition_priority = ["Near Mint", "Lightly Played", "Moderately Played", "Heavily Played", "Damaged"]
    reverse_condition_priority = ["Near Mint Reverse Holofoil", "Lightly Played Reverse Holofoil", "Moderately Played Reverse Holofoil", "Heavily Played Reverse Holofoil", "Damaged Reverse Holofoil"]
    holo_condition_priority = ["Near Mint Holofoil", "Lightly Played Holofoil", "Moderately Played Holofoil", "Heavily Played Holofoil", "Damaged Holofoil"]

    # Dictionary to store the best available card per productID
    best_cards = {}

    # First pass: Find the best condition for each card type (Normal, Holofoil, Reverse Holo)
    for item in data.get("result", []):
        product_id = item.get("productID")
        condition = item.get("condition")
        rarity = item.get("rarity")
        printing = item.get("printing")
        marketPrice = item.get("marketPrice") or 0
        productName = item.get("productName")
        number = item.get("number")
        
        # Track for top 5 cards
        card_name_raw = item.get('productName', 'Unknown')
        card_name = myUtils.clean_card_name(card_name_raw)        
        card_number = item.get('number', 'N/A')
        
        # Only keep the highest price version of each card
        if card_name not in unique_cards or marketPrice > unique_cards[card_name]['price']:
            unique_cards[card_name] = {
                'name': card_name,
                'price': marketPrice,
                'rarity': rarity,
                'condition': condition,
                'number': card_number
            }

        # Identify if this is a Reverse Holo, Holofoil, or Normal card
        is_reverse = condition in reverse_condition_priority
        is_holofoil = condition in holo_condition_priority
        is_normal = printing == "Normal" and condition in condition_priority

        if not (is_reverse or is_holofoil or is_normal):
            continue

        if product_id not in best_cards:
            best_cards[product_id] = {"normal": None, "holofoil": None, "reverse": None}

        if is_reverse:
            if (best_cards[product_id]["reverse"] is None or
                    reverse_condition_priority.index(condition) < reverse_condition_priority.index(best_cards[product_id]["reverse"]["condition"])):
                best_cards[product_id]["reverse"] = {
                    "condition": condition,
                    "rarity": rarity,
                    "marketPrice": marketPrice,
                    "productName": productName,
                    "number": number
                }

        elif is_holofoil:
            if (best_cards[product_id]["holofoil"] is None or
                    holo_condition_priority.index(condition) < holo_condition_priority.index(best_cards[product_id]["holofoil"]["condition"])):
                best_cards[product_id]["holofoil"] = {
                    "condition": condition,
                    "rarity": rarity,
                    "marketPrice": marketPrice,
                    "productName": productName,
                    "number": number
                }

        elif is_normal:
            if (best_cards[product_id]["normal"] is None or
                    condition_priority.index(condition) < condition_priority.index(best_cards[product_id]["normal"]["condition"])):
                best_cards[product_id]["normal"] = {
                    "condition": condition,
                    "rarity": rarity,
                    "marketPrice": marketPrice,
                    "productName": productName,
                    "number": number
                }

    # Process the best available cards
    for product in best_cards.values():
        if product["normal"]:
            rarity = product["normal"]["rarity"]
            marketPrice = product["normal"]["marketPrice"]
            cardNumber = product["normal"]["number"]

            if rarity == "Common":
                commonCount += 1
                totalCommonValue += marketPrice
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += marketPrice
            if rarity == "Rare":
                rareCount += 1
                totalRareValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                totalCards += 1

        if product["holofoil"]:
            rarity = product["holofoil"]["rarity"]
            marketPrice = product["holofoil"]["marketPrice"]
            name = product["holofoil"]["productName"]

            if rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
            elif rarity == "Ultra Rare" and " Star" not in name:
                ultraRareCount += 1
                totalUltraRareValue += marketPrice
            elif rarity == "Ultra Rare" and " Star" in name:
                goldStarCount += 1
                totalGoldStarValue += marketPrice
            elif rarity == "Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                totalCards += 1

        if product["reverse"]:
            reverseCount += 1
            totalReverseValue += product["reverse"]["marketPrice"]

    # Convert to top 5 list
    all_unique_cards = list(unique_cards.values())
    top_5_cards = sorted(all_unique_cards, key=lambda x: x['price'], reverse=True)[:5]

    commonQuantity = 5
    uncommonQuantity = 2

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(set.setNumber)

    expValue = 0
    if(set.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * set.secretOdds)

    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * .66)
    expValue += (totalHoloValue / holoCount * set.holoOdds)
    expValue += (totalUltraRareValue / ultraRareCount * set.ultraOdds)
    expValue += (totalReverseValue / reverseCount)
    expValue += (totalGoldStarValue / max(goldStarCount, 1) * set.goldStarOdds)

    print("\n")
    print(set.name)
    print("Total Cards: " + str(totalCards))
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Ultra Rares: " + str(ultraRareCount) + ", Value: $" + f"{totalUltraRareValue:.2f}")
    print("Reverses: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Gold Stars: " + str(goldStarCount) + ", Value: $" + f"{totalGoldStarValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")

    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards