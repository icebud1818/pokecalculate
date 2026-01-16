import requests
from calculators import myUtils
# import myUtils

def calculate(set):

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    totalReverseValue = 0
    totalExValue = 0
    totalFaValue = 0
    totalAceValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    exCount = 0
    faCount = 0
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
                    "number": number
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
            if rarity == "Rare":
                rareCount += 1
                totalRareValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                if(rarity != "Code Card" and rarity != "Promo"):
                    totalCards += 1

        # Process Holofoil if it exists
        if product["holofoil"]:
            rarity = product["holofoil"]["rarity"]
            marketPrice = product["holofoil"]["marketPrice"]
            name = product["holofoil"]["productName"]
            number = product["holofoil"]["number"]

            if rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            elif rarity == "Rare Ace":
                aceCount += 1
                totalAceValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
            elif "Full Art" in name:
                faCount += 1
                totalFaValue += marketPrice
            elif "EX" in name:
                exCount += 1
                totalExValue += marketPrice
            elif rarity == "Rare":
                holoCount += 1
                totalHoloValue += marketPrice
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

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
    if(set.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * set.secretOdds)
    if(set.exOdds > 0):
        expValue += (totalExValue /exCount * set.exOdds)
    if(set.faOdds > 0):
        expValue += (totalFaValue /max(faCount, 1) * set.faOdds)
    if(set.aceOdds > 0):
        expValue += (totalAceValue /max(aceCount, 1) * set.aceOdds)

    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * .66)
    expValue += (totalHoloValue / holoCount * set.holoOdds)
    expValue += (totalReverseValue / reverseCount * set.reverseOdds)


    print("\n")
    print(set.name)
    print("Total Cards: " + str(totalCards))
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("EXs: " + str(exCount) + ", Value: $" + f"{totalExValue:.2f}")
    print("Reverses: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("Ace Specs: " + str(aceCount) + ", Value: $" + f"{totalAceValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def legendaryTreasures():
    

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    totalReverseValue = 0
    totalExValue = 0
    totalRcUltraValue = 0
    totalRcUncommonValue = 0
    totalRcCommonValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    exCount = 0
    rcUltraCount = 0
    rcUncommonCount = 0
    rcCommonCount = 0

    unique_cards = {}

   # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/1409/cards/?rows=5000&productTypeID=1")    
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
                    "number": number
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
            if rarity == "Rare":
                rareCount += 1
                totalRareValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                totalCards += 1

        # Process Holofoil if it exists
        if product["holofoil"]:
            rarity = product["holofoil"]["rarity"]
            marketPrice = product["holofoil"]["marketPrice"]
            name = product["holofoil"]["productName"]
            number = product["holofoil"]["number"]

            if rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
            elif rarity == "Ultra Rare":
                exCount += 1
                totalExValue += marketPrice
            elif rarity == "Rare":
                holoCount += 1
                totalHoloValue += marketPrice
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




   # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/1465/cards/?rows=5000&productTypeID=1")    
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
                    "number": number
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
            if rarity == "Rare":
                rareCount += 1
                totalRareValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                totalCards += 1

        # Process Holofoil if it exists
        if product["holofoil"]:
            rarity = product["holofoil"]["rarity"]
            marketPrice = product["holofoil"]["marketPrice"]
            name = product["holofoil"]["productName"]
            number = product["holofoil"]["number"]

            if rarity == "Common":
                rcCommonCount += 1
                totalRcCommonValue += marketPrice
            elif rarity == "Uncommon":
                rcUncommonCount += 1
                totalRcUncommonValue += marketPrice
            elif rarity == "Ultra Rare":
                rcUltraCount += 1
                totalRcUltraValue += marketPrice
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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/98581/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(710)

    commonQuantity = 4
    uncommonQuantity = 2
    rcCommonQuantity = 1

    expValue = 0
    slot1Value = 0
    slot2Value = 0
    slot3Value = 0

    slot1Value += (totalHoloValue / holoCount * .5)
    slot1Value += (totalReverseValue / reverseCount * .5)
    slot2Value += (totalSecretValue / secretCount * (1/72))
    slot2Value += (totalExValue /exCount * (1/9))
    slot2Value += (totalRareValue / rareCount * .875)
    slot3Value += (totalRcUltraValue / rcUltraCount * .25)
    slot3Value += (totalRcUncommonValue / rcUncommonCount * .75)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity)
    expValue += (totalRcCommonValue / rcCommonCount * rcCommonQuantity)
    expValue += slot1Value + slot2Value + slot3Value  


    print("\n")
    print("Legendary Treasures")
    print("Total Cards: " + str(totalCards))
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("EXs: " + str(exCount) + ", Value: $" + f"{totalExValue:.2f}")
    print("Reverses: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("RC Ultra Rares: " + str(rcUltraCount) + ", Value: $" + f"{totalRcUltraValue:.2f}")
    print("RC Uncommons: " + str(rcUncommonCount) + ", Value: $" + f"{totalRcUncommonValue:.2f}")
    print("RC Commons: " + str(rcCommonCount) + ", Value: $" + f"{totalRcCommonValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards