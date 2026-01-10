import requests
from calculators import myUtils
def calculate(set):

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHyperValue = 0
    totalReverseValue = 0
    totalDoubleValue = 0
    totalUltraValue = 0
    totalIrValue = 0
    totalSirValue = 0
    totalAceValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    hyperCount = 0
    reverseCount = 0
    doubleCount = 0
    ultraCount = 0
    codeCardCount = 0
    irCount = 0
    sirCount = 0
    aceCount = 0

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
        printing = item.get("printing")  # Can be "Normal" or "Holofoil"
        marketPrice = item.get("marketPrice") or 0  # Avoid None errors
        productName = item.get("productName")
        number = item.get("number")
        setName = item.get("set")

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
        is_holofoil = condition in holo_condition_priority  # Checks if it's a Holofoil condition
        is_normal = printing == "Normal" and condition in condition_priority

        # If this card doesn't match any category, skip it
        if not (is_reverse or is_holofoil or is_normal):
            continue

        # Create storage for this productID if it doesn't exist
        if product_id not in best_cards:
            best_cards[product_id] = {"normal": None, "holofoil": None, "reverse": None}

        # Check if this is the best condition Reverse Holo for this productID
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

        # Check if this is the best condition Holofoil for this productID
        elif is_holofoil:
            if (best_cards[product_id]["holofoil"] is None or
                    holo_condition_priority.index(condition) < holo_condition_priority.index(best_cards[product_id]["holofoil"]["condition"])):
                best_cards[product_id]["holofoil"] = {
                    "condition": condition,
                    "rarity": rarity,
                    "marketPrice": marketPrice,
                    "productName": productName,
                    "number": number,
                    "setName": setName
                }

        # Check if this is the best condition Normal for this productID
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

    # Now, process the best available cards
    for product in best_cards.values():
        # Process Normal if it exists
        if product["normal"]:
            rarity = product["normal"]["rarity"]
            marketPrice = product["normal"]["marketPrice"]
            number = product["normal"]["number"]

            if rarity == "Common":
                commonCount += 1
                totalCommonValue += marketPrice
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                totalCards += 1

        # Process Holofoil if it exists
        if product["holofoil"]:
            rarity = product["holofoil"]["rarity"]
            marketPrice = product["holofoil"]["marketPrice"]
            name = product["holofoil"]["productName"]
            number = product["holofoil"]["number"]
            setName = product["holofoil"]["setName"]

            if rarity == "Rare" or rarity == "Holo Rare" and "Prerelease" not in name:
                rareCount += 1
                totalRareValue += marketPrice
            elif rarity == "Double Rare":
                doubleCount += 1
                totalDoubleValue += marketPrice
            elif rarity == "Hyper Rare" or rarity == "Mega Hyper Rare":
                hyperCount += 1
                totalHyperValue += marketPrice
            elif rarity == "Illustration Rare":
                irCount += 1
                totalIrValue += marketPrice
            elif rarity == "Special Illustration Rare":
                sirCount += 1
                totalSirValue += marketPrice
            elif rarity == "ACE SPEC Rare":
                aceCount += 1
                totalAceValue += marketPrice
            elif rarity == "Ultra Rare":
                ultraCount += 1
                totalUltraValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                totalCards += 1

        # Process Reverse Holo if it exists
        if product["reverse"]:
            rarity = product["reverse"]["rarity"]
            marketPrice = product["reverse"]["marketPrice"]
            name = product["reverse"]["productName"]
            number = product["reverse"]["number"]
            
            reverseCount += 1
            totalReverseValue += marketPrice

    # Convert dictionary to list and sort by price to get top 5 unique cards
    all_unique_cards = list(unique_cards.values())
    top_5_cards = sorted(all_unique_cards, key=lambda x: x['price'], reverse=True)[:5]

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(set.setNumber)

    commonQuantity = 4
    uncommonQuantity = 3

    expValue = 0
        
    if(set.aceOdds > 0):
        expValue += (totalAceValue /max(aceCount, 1) * set.aceOdds)
        

    expValue += (totalHyperValue / max(hyperCount, 1) * set.hyperOdds)
    expValue += (totalUltraValue /ultraCount * set.ultraOdds)
    expValue += (totalDoubleValue /doubleCount * set.doubleOdds)
    expValue += (totalIrValue /irCount * set.irOdds)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity)
    expValue += (totalRareValue / rareCount * set.rareOdds)
    expValue += (totalSirValue / sirCount * set.sirOdds)
    expValue += (totalReverseValue / reverseCount * set.reverseOdds)


    print("\n")
    print(set.name)
    print("Total Cards: " + str(totalCards))
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Hyper Rares: " + str(hyperCount) + ", Value: $" + f"{totalHyperValue:.2f}")
    print("Double Rares: " + str(doubleCount) + ", Value: $" + f"{totalDoubleValue:.2f}")
    print("Ultra Rares: " + str(ultraCount) + ", Value: $" + f"{totalUltraValue:.2f}")
    print("Reverses: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Illustration Rares: " + str(irCount) + ", Value: $" + f"{totalIrValue:.2f}")
    print("Special Illustration Rares: " + str(sirCount) + ", Value: $" + f"{totalSirValue:.2f}")
    print("Ace Specs: " + str(aceCount) + ", Value: $" + f"{totalAceValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards