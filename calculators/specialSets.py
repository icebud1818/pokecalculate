import requests
from calculators import myUtils
# import myUtils

def dragonVault():

    totalCards = 0
    totalHoloValue = 0
    totalSecretRareValue = 0

    holoCount = 0
    secretRareCount = 0

    unique_cards = {}

   # Make the GET request
    response = requests.get("https://infinite-api.tcgplayer.com/priceguide/set/1426/cards/?rows=5000&productTypeID=1")    
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
        # Process Holofoil if it exists
        if product["holofoil"]:
            rarity = product["holofoil"]["rarity"]
            marketPrice = product["holofoil"]["marketPrice"]
            name = product["holofoil"]["productName"]
            number = product["holofoil"]["number"]

            if name == "Kyurem":
                secretRareCount += 1
                totalSecretRareValue += marketPrice
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                totalCards += 1

    # Convert dictionary to list and sort by price to get top 5 unique cards
    all_unique_cards = list(unique_cards.values())
    top_5_cards = sorted(all_unique_cards, key=lambda x: x['price'], reverse=True)[:5]

    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/98948/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(705.5)

    expValue = 0

    allHolos = totalHoloValue / holoCount * 5 * .96
    secretRare = (totalHoloValue / holoCount * 4 + totalSecretRareValue) * .04

    expValue += allHolos + secretRare

    print("\n")
    print("Dragon Vault")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Secret Rares: " + str(secretRareCount) + ", Value: $" + f"{totalSecretRareValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def doubleCrisis():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalHoloValue = 0
    totalUltraRareValue = 0
    totalReverseValue = 0

    commonCount = 0
    uncommonCount = 0
    holoCount = 0
    ultraRareCount = 0
    reverseCount = 0

    unique_cards = {}

# Make the GET request
    response = requests.get("https://infinite-api.tcgplayer.com/priceguide/set/1525/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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
            setName = product["holofoil"]["setName"]

            if rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            elif rarity == "Ultra Rare":
                ultraRareCount += 1
                totalUltraRareValue += marketPrice
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

    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/229226/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(804.5)

    expValue = 0
    expValue += (totalCommonValue / commonCount * 3)
    expValue += (totalUncommonValue / uncommonCount * 2)
    expValue += (totalUltraRareValue / ultraRareCount * (5/36))
    expValue += (totalHoloValue / holoCount * (1 - (5/36)))
    expValue += (totalReverseValue / reverseCount)

    print("\n")
    print("Double Crisis")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Ultra Rares: " + str(ultraRareCount) + ", Value: $" + f"{totalUltraRareValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def shiningLegends():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalHoloValue = 0
    totalGxValue = 0
    totalReverseValue = 0
    totalFaValue = 0
    totalShiningValue = 0
    totalSecretValue = 0
    totalRainbowValue = 0

    commonCount = 0
    uncommonCount = 0
    holoCount = 0
    gxCount = 0
    reverseCount = 0
    gxCount = 0
    faCount = 0
    shiningCount = 0
    secretCount = 0
    rainbowCount = 0

    unique_cards = {}

# Make the GET request
    response = requests.get("https://infinite-api.tcgplayer.com/priceguide/set/2054/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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
            setName = product["holofoil"]["setName"]

            if(rarity == "Shiny Holo Rare" and "Mewtwo" in name):
                secretCount += 1
                totalSecretValue += marketPrice
            elif(rarity == "Shiny Holo Rare"):
                shiningCount += 1
                totalShiningValue += marketPrice
            elif(rarity == "Secret Rare"):
                rainbowCount += 1
                totalRainbowValue += marketPrice
            elif(rarity == "Ultra Rare" and "Full Art" in name):
                faCount += 1
                totalFaValue += marketPrice
            elif(rarity == "Ultra Rare"):
                gxCount += 1
                totalGxValue += marketPrice
            elif(rarity == "Holo Rare"):
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

    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/155880/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(902.5)

    expValue = 0
    expValue += (totalCommonValue / commonCount * 5)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += (totalGxValue / gxCount * (1/9))
    expValue += (totalFaValue / faCount * (1/25))
    expValue += (totalSecretValue / secretCount * (1/108))
    expValue += (totalRainbowValue / rainbowCount * (1/64))
    expValue += (totalShiningValue / shiningCount * (1/12))
    expValue += (totalHoloValue / holoCount * .7406)
    expValue += (totalReverseValue / reverseCount)

    print("\n")
    print("Shining Legends")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("GXs: " + str(gxCount) + ", Value: $" + f"{totalGxValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Rainbow Rares: " + str(rainbowCount) + ", Value: $" + f"{totalRainbowValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("Shining Pokemon: " + str(shiningCount) + ", Value: $" + f"{totalShiningValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def dragonMajesty():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalHoloValue = 0
    totalGxValue = 0
    totalReverseValue = 0
    totalFaValue = 0
    totalPrismValue = 0
    totalSecretValue = 0
    totalRainbowValue = 0

    commonCount = 0
    uncommonCount = 0
    holoCount = 0
    gxCount = 0
    reverseCount = 0
    gxCount = 0
    faCount = 0
    prismCount = 0
    secretCount = 0
    rainbowCount = 0

    unique_cards = {}

# Make the GET request
    response = requests.get("https://infinite-api.tcgplayer.com/priceguide/set/2295/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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
            setName = product["holofoil"]["setName"]

            if(rarity == "Secret Rare"):
                secretCount += 1
                totalSecretValue += marketPrice
            elif(rarity == "Prism Rare"):
                prismCount += 1
                totalPrismValue += marketPrice
            elif(rarity == "Ultra Rare" and "Full Art" in name):
                faCount += 1
                totalFaValue += marketPrice
            elif(rarity == "Ultra Rare"):
                gxCount += 1
                totalGxValue += marketPrice
            elif(rarity == "Holo Rare"):
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
    
    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/173392/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(906.5)

    expValue = 0
    expValue += (totalCommonValue / commonCount * 5)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += (totalGxValue / gxCount * (1/6))
    expValue += (totalFaValue / faCount * (1/14))
    expValue += (totalSecretValue / secretCount * (86/2795))
    expValue += (totalPrismValue / prismCount * (1/9))
    expValue += (totalHoloValue / holoCount * .7309)
    expValue += (totalReverseValue / reverseCount * (1 - (1/9)))

    print("\n")
    print("Dragon Majesty")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("GXs: " + str(gxCount) + ", Value: $" + f"{totalGxValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("Prism Rares: " + str(prismCount) + ", Value: $" + f"{totalPrismValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def championsPath():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalHoloValue = 0
    totalVValue = 0
    totalVmaxValue = 0
    totalReverseValue = 0
    totalFaValue = 0
    totalSecretValue = 0

    commonCount = 0
    uncommonCount = 0
    holoCount = 0
    vCount = 0
    vmaxCount = 0
    reverseCount = 0
    faCount = 0
    secretCount = 0

    unique_cards = {}

# Make the GET request
    response = requests.get("https://infinite-api.tcgplayer.com/priceguide/set/2685/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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
            setName = product["holofoil"]["setName"]

            if(rarity == "Secret Rare"):
                secretCount += 1
                totalSecretValue += marketPrice
            elif(rarity == "Ultra Rare" and "Full Art" in name):
                faCount += 1
                totalFaValue += marketPrice
            elif(rarity == "Ultra Rare" and "VMAX" in name):
                vmaxCount += 1
                totalVmaxValue += marketPrice
            elif(rarity == "Ultra Rare"):
                vCount += 1
                totalVValue += marketPrice
            elif(rarity == "Holo Rare"):
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

    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/218789/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1002.5)

    expValue = 0
    expValue += (totalCommonValue / commonCount * 5)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += (totalVValue / vCount * (1/6))
    expValue += (totalVmaxValue / vmaxCount * (1/30))
    expValue += (totalFaValue / faCount * (1/19))
    expValue += (totalSecretValue / secretCount * (15/512))
    expValue += (totalHoloValue / holoCount * .7178)
    expValue += (totalReverseValue / reverseCount)

    print("\n")
    print("Champions Path")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Vs: " + str(vCount) + ", Value: $" + f"{totalVValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("VMAX: " + str(vmaxCount) + ", Value: $" + f"{totalVmaxValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def pokemonGo():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalHoloValue = 0
    totalVValue = 0
    totalVmaxValue = 0
    totalReverseValue = 0
    totalFaValue = 0
    totalSecretValue = 0
    totalAltValue = 0
    totalRadiantValue = 0
    totalVstarValue = 0

    commonCount = 0
    uncommonCount = 0
    holoCount = 0
    vCount = 0
    vmaxCount = 0
    reverseCount = 0
    faCount = 0
    secretCount = 0
    altCount = 0
    radiantCount = 0
    vstarCount = 0

    unique_cards = {}

# Make the GET request
    response = requests.get("https://infinite-api.tcgplayer.com/priceguide/set/3064/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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
            setName = product["holofoil"]["setName"]

            if(rarity == "Secret Rare"):
                secretCount += 1
                totalSecretValue += marketPrice
            elif(rarity == "Ultra Rare" and "Alternate" in name):
                altCount += 1
                totalAltValue += marketPrice
            elif(rarity == "Ultra Rare" and "Full Art" in name):
                faCount += 1
                totalFaValue += marketPrice
            elif(rarity == "Ultra Rare" and "VMAX" in name):
                vmaxCount += 1
                totalVmaxValue += marketPrice
            elif(rarity == "Ultra Rare" and "VSTAR" in name):
                vstarCount += 1
                totalVstarValue += marketPrice
            elif(rarity == "Ultra Rare"):
                vCount += 1
                totalVValue += marketPrice
            elif(rarity == "Holo Rare" and "Ditto" not in name):
                holoCount += 1
                totalHoloValue += marketPrice
            elif(rarity == "Radiant Rare"):
                radiantCount += 1
                totalRadiantValue += marketPrice
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
    
    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/274421/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1101.5)

    expValue = 0
    expValue += (totalCommonValue / commonCount * 5)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += (totalVValue / vCount * (.159))
    expValue += (totalVmaxValue / vmaxCount * (.0216))
    expValue += (totalVstarValue / vstarCount * (.0377))
    expValue += (totalFaValue / faCount * (.0479))
    expValue += (totalSecretValue / secretCount * (.0375))
    expValue += (totalAltValue / altCount * (.006))
    expValue += (totalRadiantValue / radiantCount * (.0539))
    expValue += (totalHoloValue / holoCount * .6901)
    expValue += (totalReverseValue / reverseCount * .9461)

    print("\n")
    print("Pokemon Go")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Vs: " + str(vCount) + ", Value: $" + f"{totalVValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("VMAX: " + str(vmaxCount) + ", Value: $" + f"{totalVmaxValue:.2f}")
    print("VSTARs: " + str(vstarCount) + ", Value: $" + f"{totalVstarValue:.2f}")
    print("Radiant Rares: " + str(radiantCount) + ", Value: $" + f"{totalRadiantValue:.2f}")
    print("Alternate Arts: " + str(altCount) + ", Value: $" + f"{totalAltValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def pokemon151():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalDoubleRareValue = 0
    totalReverseValue = 0
    totalUltraRareValue = 0
    totalHyperRareValue = 0
    totalIrValue = 0
    totalSirValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    doubleRareCount = 0
    reverseCount = 0
    ultraRareCount = 0
    hyperCount = 0
    irCount = 0
    sirCount = 0

    unique_cards = {}

# Make the GET request
    response = requests.get("https://infinite-api.tcgplayer.com/priceguide/set/23237/cards/?rows=5000&productTypeID=1")    
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

            if(rarity == "Hyper Rare"):
                hyperCount += 1
                totalHyperRareValue += marketPrice
            elif(rarity == "Ultra Rare"):
                ultraRareCount += 1
                totalUltraRareValue += marketPrice
            elif(rarity == "Double Rare"):
                doubleRareCount += 1
                totalDoubleRareValue += marketPrice
            elif(rarity == "Illustration Rare"):
                irCount += 1
                totalIrValue += marketPrice
            elif(rarity == "Special Illustration Rare"):
                sirCount += 1
                totalSirValue += marketPrice
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += marketPrice
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
    
    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/504467/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1202.5)

    expValue = 0
    expValue += (totalCommonValue / commonCount * 4)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += (totalDoubleRareValue / doubleRareCount * (1/8)) #rare slot
    expValue += (totalUltraRareValue / ultraRareCount * (1/16)) #rare slot
    expValue += (totalHyperRareValue / hyperCount * (1/51)) #reverse slot 2
    expValue += (totalIrValue / irCount * (1/12)) #reverse slot 2
    expValue += (totalSirValue / sirCount * (1/32)) #reverse slot 2
    expValue += (totalRareValue / rareCount * (1 - (1/8) - (1/16))) #rare slot
    expValue += (totalReverseValue / reverseCount * (1 + (1 - (1/32) - (1/12) - (1/51)))) #1 Guaranteed

    print("\n")
    print("Pokemon 151")
    print("Total Cards: " + str(totalCards))
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Double Rares: " + str(doubleRareCount) + ", Value: $" + f"{totalDoubleRareValue:.2f}")
    print("Hyper Rares: " + str(hyperCount) + ", Value: $" + f"{totalHyperRareValue:.2f}")
    print("Ultra Rares: " + str(ultraRareCount) + ", Value: $" + f"{totalUltraRareValue:.2f}")
    print("IRs: " + str(irCount) + ", Value: $" + f"{totalIrValue:.2f}")
    print("SIRs: " + str(sirCount) + ", Value: $" + f"{totalSirValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def shroudedFable():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalDoubleRareValue = 0
    totalReverseValue = 0
    totalUltraRareValue = 0
    totalHyperRareValue = 0
    totalIrValue = 0
    totalSirValue = 0
    totalAceSpecValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    doubleRareCount = 0
    reverseCount = 0
    ultraRareCount = 0
    hyperCount = 0
    irCount = 0
    sirCount = 0
    aceSpecCount = 0

    unique_cards = {}

# Make the GET request
    response = requests.get("https://infinite-api.tcgplayer.com/priceguide/set/23529/cards/?rows=5000&productTypeID=1")    
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

            if(rarity == "Hyper Rare"):
                hyperCount += 1
                totalHyperRareValue += marketPrice
            elif(rarity == "Ultra Rare"):
                ultraRareCount += 1
                totalUltraRareValue += marketPrice
            elif(rarity == "Double Rare"):
                doubleRareCount += 1
                totalDoubleRareValue += marketPrice
            elif(rarity == "Illustration Rare"):
                irCount += 1
                totalIrValue += marketPrice
            elif(rarity == "Special Illustration Rare"):
                sirCount += 1
                totalSirValue += marketPrice
            elif(rarity == "ACE SPEC Rare"):
                aceSpecCount += 1
                totalAceSpecValue += marketPrice
            elif(rarity == "Rare"):
                rareCount += 1
                totalRareValue += marketPrice
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

    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/552997/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1205.5)


    expValue = 0
    expValue += (totalCommonValue / commonCount * 4)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += (totalDoubleRareValue / doubleRareCount * (1/6)) #rare slot
    expValue += (totalUltraRareValue / ultraRareCount * (1/15)) #rare slot
    expValue += (totalHyperRareValue / hyperCount * (1/144)) #reverse slot 2
    expValue += (totalIrValue / irCount * (1/12)) #reverse slot 2
    expValue += (totalSirValue / sirCount * (1/67)) #reverse slot 2
    expValue += (totalAceSpecValue / aceSpecCount * (1/20)) #reverse slot 1
    expValue += (totalRareValue / rareCount * (1 - (1/6) - (1/15))) #rare slot
    expValue += (totalReverseValue / reverseCount * ((1 - (1/20)) + (1 - (1/144) - (1/12) - (1/67)))) #1 Guaranteed unless ace

    print("\n")
    print("Shrouded Fable")
    print("Total Cards: " + str(totalCards))
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Double Rares: " + str(doubleRareCount) + ", Value: $" + f"{totalDoubleRareValue:.2f}")
    print("Hyper Rares: " + str(hyperCount) + ", Value: $" + f"{totalHyperRareValue:.2f}")
    print("Ultra Rares: " + str(ultraRareCount) + ", Value: $" + f"{totalUltraRareValue:.2f}")
    print("IRs: " + str(irCount) + ", Value: $" + f"{totalIrValue:.2f}")
    print("SIRs: " + str(sirCount) + ", Value: $" + f"{totalSirValue:.2f}")
    print("ACE SPECs: " + str(aceSpecCount) + ", Value: $" + f"{totalAceSpecValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def paldeanFates():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalDoubleRareValue = 0
    totalReverseValue = 0
    totalUltraRareValue = 0
    totalHyperRareValue = 0
    totalIrValue = 0
    totalSirValue = 0
    totalShinyValue = 0
    totalShinyUltraValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    doubleRareCount = 0
    reverseCount = 0
    ultraRareCount = 0
    hyperCount = 0
    irCount = 0
    sirCount = 0
    shinyCount = 0
    shinyUltraCount = 0

    unique_cards = {}

# Make the GET request
    response = requests.get("https://infinite-api.tcgplayer.com/priceguide/set/23353/cards/?rows=5000&productTypeID=1")    
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

            if(rarity == "Hyper Rare"):
                hyperCount += 1
                totalHyperRareValue += marketPrice
            elif(rarity == "Ultra Rare"):
                ultraRareCount += 1
                totalUltraRareValue += marketPrice
            elif(rarity == "Double Rare"):
                doubleRareCount += 1
                totalDoubleRareValue += marketPrice
            elif(rarity == "Illustration Rare"):
                irCount += 1
                totalIrValue += marketPrice
            elif(rarity == "Special Illustration Rare"):
                sirCount += 1
                totalSirValue += marketPrice
            elif(rarity == "Shiny Ultra Rare"):
                shinyUltraCount += 1
                totalShinyUltraValue += marketPrice
            elif(rarity == "Shiny Rare"):
                shinyCount += 1
                totalShinyValue += marketPrice
            elif(rarity == "Rare"):
                rareCount += 1
                totalRareValue += marketPrice
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

    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/528038/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1203.5)

    expValue = 0
    expValue += (totalCommonValue / commonCount * 4)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += (totalDoubleRareValue / doubleRareCount * (1/6)) #rare slot
    expValue += (totalUltraRareValue / ultraRareCount * (1/15)) #rare slot
    expValue += (totalHyperRareValue / hyperCount * (1/62)) #reverse slot 2
    expValue += (totalIrValue / irCount * (1/14)) #reverse slot 2
    expValue += (totalSirValue / sirCount * (1/58)) #reverse slot 2
    expValue += (totalShinyUltraValue / shinyUltraCount * (1/13)) #reverse slot 1
    expValue += (totalShinyValue / shinyCount * (1/4)) #reverse slot 1
    expValue += (totalRareValue / rareCount * (1 - (1/6) - (1/15))) #rare slot
    expValue += (totalReverseValue / reverseCount * ((1 - (1/4) - (1/13)) + (1 - (1/62) - (1/14) - (1/58)))) 

    print("\n")
    print("Paldean Fates")
    print("Total Cards: " + str(totalCards))
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Double Rares: " + str(doubleRareCount) + ", Value: $" + f"{totalDoubleRareValue:.2f}")
    print("Hyper Rares: " + str(hyperCount) + ", Value: $" + f"{totalHyperRareValue:.2f}")
    print("Ultra Rares: " + str(ultraRareCount) + ", Value: $" + f"{totalUltraRareValue:.2f}")
    print("IRs: " + str(irCount) + ", Value: $" + f"{totalIrValue:.2f}")
    print("SIRs: " + str(sirCount) + ", Value: $" + f"{totalSirValue:.2f}")
    print("Shiny Ultra Rares: " + str(shinyUltraCount) + ", Value: $" + f"{totalShinyUltraValue:.2f}")
    print("Shiny Rares: " + str(shinyCount) + ", Value: $" + f"{totalShinyValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def hiddenFates():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalGxValue = 0
    totalReverseValue = 0
    totalFaValue = 0
    totalFaVaultValue = 0
    totalRainbowValue = 0
    totalShinyValue = 0
    totalShinyGXValue = 0
    totalGoldValue = 0

    commonCount = 0
    uncommonCount = 0
    holoCount = 0
    gxCount = 0
    reverseCount = 0
    gxCount = 0
    faCount = 0
    rainbowCount = 0
    rareCount = 0
    shinyCount = 0
    shinyGxCount = 0
    faVaultCount = 0
    goldCount = 0

    unique_cards = {}


       # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/2480/cards/?rows=5000&productTypeID=1")    
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

            if(rarity == "Secret Rare"):
                rainbowCount += 1
                totalRainbowValue += marketPrice
            elif(rarity == "Ultra Rare" and "Full Art" in name):
                faCount += 1
                totalFaValue += marketPrice
            elif(rarity == "Ultra Rare"):
                gxCount += 1
                totalGxValue += marketPrice
            elif(rarity == "Holo Rare"):
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

    # Second price guide ----------------------------------

    # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/2594/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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

            if("GX" in name and number != "SV91/SV94" and number != "SV92/SV94" and number != "SV93/SV94" and number != "SV94/SV94"):
                shinyGxCount += 1
                totalShinyGXValue += marketPrice
            elif(number == "SV81/SV94" or number == "SV82/SV94" or number == "SV83/SV94" or number == "SV84/SV94" or number == "SV85/SV94" or number == "SV86/SV94"):
                faVaultCount += 1
                totalFaVaultValue += marketPrice
            elif(number == "SV87/SV94" or number == "SV88/SV94" or number == "SV89/SV94" or number == "SV90/SV94" or number == "SV91/SV94" or number == "SV92/SV94" or number == "SV93/SV94" or number == "SV94/SV94"):
                goldCount += 1
                totalGoldValue += marketPrice
            elif(rarity == "Shiny Holo Rare"):
                shinyCount += 1
                totalShinyValue += marketPrice
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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/198634/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(910.5)

    rareSlot = 0
    reverseSlot = 0

    rareSlot += (totalRareValue / rareCount * .67 )
    rareSlot += (totalHoloValue / holoCount * .1244 )
    rareSlot += (totalGxValue / gxCount * (1/7) )
    rareSlot += (totalFaValue / faCount * (1/22) )
    rareSlot += (totalRainbowValue / rainbowCount * (1/58) )

    reverseSlot += (totalReverseValue / reverseCount * .6076 )
    reverseSlot += (totalShinyValue / shinyCount * .25 )
    reverseSlot += (totalShinyGXValue / shinyGxCount * (1/9) )
    reverseSlot += (totalFaVaultValue / faVaultCount * (1/73) )
    reverseSlot += (totalGoldValue / goldCount * (1/57) )

    expValue = 0
    expValue += (totalCommonValue / commonCount * 5)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += rareSlot
    expValue += reverseSlot

    print("\n")
    print("Hidden Fates")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("GXs: " + str(gxCount) + ", Value: $" + f"{totalGxValue:.2f}")
    print("Rainbow Rares: " + str(rainbowCount) + ", Value: $" + f"{totalRainbowValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("Shiny Holos: " + str(shinyCount) + ", Value: $" + f"{totalShinyValue:.2f}")
    print("Shiny GXs: " + str(shinyGxCount) + ", Value: $" + f"{totalShinyGXValue:.2f}")
    print("Vault Full Arts: " + str(faVaultCount) + ", Value: $" + f"{totalFaVaultValue:.2f}")
    print("Gold Cards: " + str(goldCount) + ", Value: $" + f"{totalGoldValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards


def shiningFates():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalVValue = 0
    totalVmaxValue = 0
    totalReverseValue = 0
    totalFaValue = 0
    totalRainbowValue = 0
    totalShinyValue = 0
    totalShinyVmaxValue = 0
    totalShinyVValue = 0
    totalGoldValue = 0
    totalAmazingRareValue = 0

    commonCount = 0
    uncommonCount = 0
    holoCount = 0
    reverseCount = 0
    vCount = 0
    vmaxCount = 0
    faCount = 0
    rainbowCount = 0
    rareCount = 0
    shinyCount = 0
    shinyVmaxCount = 0
    shinyVCount = 0
    goldCount = 0
    amazingRareCount = 0

    unique_cards = {}


       # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/2754/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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

            if(rarity == "Secret Rare"):
                rainbowCount += 1
                totalRainbowValue += marketPrice
            elif(rarity == "Ultra Rare" and "Full Art" in name):
                faCount += 1
                totalFaValue += marketPrice
            elif(rarity == "Ultra Rare" and "VMAX" in name):
                vmaxCount += 1
                totalVmaxValue += marketPrice
            elif(rarity == "Ultra Rare"):
                vCount += 1
                totalVValue += marketPrice
            elif(rarity == "Holo Rare"):
                holoCount += 1
                totalHoloValue += marketPrice
            elif(rarity == "Amazing Rare"):
                amazingRareCount += 1
                totalAmazingRareValue += marketPrice
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

    # Second price guide ----------------------------------

    # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/2781/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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

            if(number == "SV121/SV122" or number == "SV122/SV122"):
                goldCount += 1
                totalGoldValue += marketPrice
            elif("VMAX" in name):
                shinyVmaxCount += 1
                totalShinyVmaxValue += marketPrice
            elif(" V" in name):
                shinyVCount += 1
                totalShinyVValue += marketPrice
            elif(rarity == "Shiny Holo Rare"):
                shinyCount += 1
                totalShinyValue += marketPrice
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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/232636/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1003.5)

    rareSlot = 0
    reverseSlot = 0

    rareSlot += (totalRareValue / rareCount * .5251 )
    rareSlot += (totalHoloValue / holoCount * .2 )
    rareSlot += (totalVValue / vCount * (1/9) )
    rareSlot += (totalVmaxValue / vmaxCount * (.0534) )
    rareSlot += (totalFaValue / faCount * (.08) )
    rareSlot += (totalRainbowValue / rainbowCount * (1/33) )

    reverseSlot += (totalReverseValue / reverseCount * .6464 )
    reverseSlot += (totalShinyValue / shinyCount * .25 )
    reverseSlot += (totalShinyVmaxValue / shinyVmaxCount * (1/39) )
    reverseSlot += (totalShinyVValue / shinyVCount * (1/14) )
    reverseSlot += (totalAmazingRareValue / amazingRareCount * (1/19) )
    reverseSlot += (totalGoldValue / goldCount * (1/155) )

    expValue = 0
    expValue += (totalCommonValue / commonCount * 5)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += rareSlot
    expValue += reverseSlot

    print("\n")
    print("Shining Fates")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("V Cards: " + str(vCount) + ", Value: $" + f"{totalVValue:.2f}")
    print("VMAX: " + str(vmaxCount) + ", Value: $" + f"{totalVmaxValue:.2f}")
    print("Rainbow Rares: " + str(rainbowCount) + ", Value: $" + f"{totalRainbowValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("Shiny Holos: " + str(shinyCount) + ", Value: $" + f"{totalShinyValue:.2f}")
    print("Shiny Vs: " + str(shinyVCount) + ", Value: $" + f"{totalShinyVValue:.2f}")
    print("Shiny VMAX: " + str(shinyVmaxCount) + ", Value: $" + f"{totalShinyVmaxValue:.2f}")
    print("Gold Cards: " + str(goldCount) + ", Value: $" + f"{totalGoldValue:.2f}")
    print("Amazing Rares: " + str(amazingRareCount) + ", Value: $" + f"{totalAmazingRareValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def generations():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalExValue = 0
    totalReverseValue = 0
    totalRcCommonValue = 0
    totalRcUncommonValue = 0
    totalRcUltraValue = 0

    commonCount = 0
    uncommonCount = 0
    holoCount = 0
    reverseCount = 0
    exCount = 0
    rcCommonCount = 0
    rcUncommonCount = 0
    rareCount = 0
    rcUltraCount = 0

    unique_cards = {}

       # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/1728/cards/?rows=5000&productTypeID=1")    
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

            if(rarity == "Ultra Rare"):
                exCount += 1
                totalExValue += marketPrice
            elif(rarity == "Holo Rare"):
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

    # Second price guide ----------------------------------

    # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/1729/cards/?rows=5000&productTypeID=1")    
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
                rcCommonCount += 1
                totalRcCommonValue += marketPrice
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += marketPrice
            elif rarity == "Rare":
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

            if(rarity == "Ultra Rare"):
                rcUltraCount += 1
                totalRcUltraValue += marketPrice
            elif(rarity == "Uncommon"):
                rcUncommonCount += 1
                totalRcUncommonValue += marketPrice
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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/187238/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(808.5)

    rareSlot = 0
    reverseSlot = 0
    rcCommonSlot = 0
    rcSlot = 0

    rareSlot += (totalRareValue / rareCount * .654 )
    rareSlot += (totalHoloValue / holoCount * .13 )
    rareSlot += (totalExValue / exCount * (.216) )

    reverseSlot += (totalReverseValue / reverseCount)

    rcCommonSlot += (totalRcCommonValue / rcCommonCount)

    rcSlot += (totalRcUncommonValue / rcUncommonCount * .732 )
    rcSlot += (totalRcUltraValue / rcUltraCount * .268 )

    expValue = 0
    expValue += (totalCommonValue / commonCount * 4)
    expValue += (totalUncommonValue / uncommonCount * 2)
    expValue += rareSlot
    expValue += reverseSlot
    expValue += rcSlot
    expValue += rcCommonSlot

    print("\n")
    print("Generations")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("EXs: " + str(exCount) + ", Value: $" + f"{totalExValue:.2f}")
    print("Radiant Commons: " + str(rcCommonCount) + ", Value: $" + f"{totalRcCommonValue:.2f}")
    print("Radiant Uncommons: " + str(rcUncommonCount) + ", Value: $" + f"{totalRcUncommonValue:.2f}")
    print("Radiant Ultra Rares: " + str(rcUltraCount) + ", Value: $" + f"{totalRcUltraValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def crownZenith():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalVValue = 0
    totalVmaxValue = 0
    totalReverseValue = 0
    totalFaValue = 0
    totalRadiantValue = 0
    totalGgValue = 0
    totalGgUltraValue = 0
    totalGoldValue = 0
    totalSecretValue = 0
    totalEnergyValue = 0

    commonCount = 0
    uncommonCount = 0
    holoCount = 0
    reverseCount = 0
    vCount = 0
    vmaxCount = 0
    faCount = 0
    radiantCount = 0
    energyCount = 0
    rareCount = 0
    ggCount = 0
    ggUltraCount = 0
    goldCount = 0
    secretCount = 0

    unique_cards = {}


       # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/17688/cards/?rows=5000&productTypeID=1")    
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

            if(rarity == "Secret Rare"):
                secretCount += 1
                totalSecretValue += marketPrice
            elif(rarity == "Ultra Rare" and "Energy" in name):
                energyCount += 1
                totalEnergyValue += marketPrice
            elif(rarity == "Ultra Rare" and ("VMAX" in name or "VSTAR" in name)):
                vmaxCount += 1
                totalVmaxValue += marketPrice
            elif(rarity == "Ultra Rare" and "Full Art" in name):
                faCount += 1
                totalFaValue += marketPrice
            elif(rarity == "Ultra Rare"):
                vCount += 1
                totalVValue += marketPrice
            elif(rarity == "Holo Rare"):
                holoCount += 1
                totalHoloValue += marketPrice
            elif(rarity == "Radiant Rare"):
                radiantCount += 1
                totalRadiantValue += marketPrice
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

    # Second price guide ----------------------------------

    # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/17689/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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

            if(rarity == "Secret Rare"):
                goldCount += 1
                totalGoldValue += marketPrice
            elif((("V" in name) or (number == "GG57/GG70" or number == "GG58/GG70" or number == "GG59/GG70" or number == "GG60/GG70" or number == "GG61/GG70" or number == "GG62/GG70" or number == "GG63/GG70" or number == "GG64/GG70" or number == "GG65/GG70" or number == "GG66/GG70")) and (number != "GG01/GG70")):
                ggUltraCount += 1
                totalGgUltraValue += marketPrice
            else:
                ggCount += 1
                totalGgValue += marketPrice
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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/453466/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1103.5)

    rareSlot = 0
    reverseSlot = 0

    rareSlot += (totalRareValue / rareCount * .3848)
    rareSlot += (totalHoloValue / holoCount * .4016 )
    rareSlot += (totalVValue / vCount * (1/8) )
    rareSlot += (totalVmaxValue / vmaxCount * (1/19) )
    rareSlot += (totalFaValue / faCount * (1/105) )
    rareSlot += (totalEnergyValue / energyCount * (1/53) )
    rareSlot += (totalSecretValue / secretCount * (1/133))


    reverseSlot += (totalReverseValue / reverseCount * .5715 )
    reverseSlot += (totalGgValue / ggCount * .25 )
    reverseSlot += (totalRadiantValue / radiantCount * (1/22) )
    reverseSlot += (totalGgUltraValue / ggUltraCount * (1/8) )
    reverseSlot += (totalGoldValue / goldCount * (1/125) )

    expValue = 0
    expValue += (totalCommonValue / commonCount * 5)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += rareSlot
    expValue += reverseSlot

    print("\n")
    print("Crown Zenith")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("V Cards: " + str(vCount) + ", Value: $" + f"{totalVValue:.2f}")
    print("VMAX and VSTAR " + str(vmaxCount) + ", Value: $" + f"{totalVmaxValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("GGs: " + str(ggCount) + ", Value: $" + f"{totalGgValue:.2f}")
    print("GG Ultra Rares: " + str(ggUltraCount) + ", Value: $" + f"{totalGgUltraValue:.2f}")
    print("Radiant Rares: " + str(radiantCount) + ", Value: $" + f"{totalRadiantValue:.2f}")
    print("Gold Cards: " + str(goldCount) + ", Value: $" + f"{totalGoldValue:.2f}")
    print("Ultra Rare Energy: " + str(energyCount) + ", Value: $" + f"{totalEnergyValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def celebrations():

    totalCards = 0
    totalHoloValue = 0
    totalUltraValue = 0
    totalSecretValue = 0
    blastoise = charizard = claydol = cleffa = gyarados = donphan = garchomp = gardevoir = teamRocket = imposter = luxray = rayquaza = mew = mewtwo = reshiram = admin = zapdos = magikarp = tapulele = groudon = umbreon = venusaur = zekrom = xerneas = pikachu = 0

    holoCount = 0
    ultraCount = 0
    secretCount = 0

    unique_cards = {}


       # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/2867/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += marketPrice

        # Process Holofoil if it exists
        if product["holofoil"]:
            rarity = product["holofoil"]["rarity"]
            marketPrice = product["holofoil"]["marketPrice"]
            name = product["holofoil"]["productName"]
            number = product["holofoil"]["number"]

            if(rarity == "Secret Rare"):
                secretCount += 1
                totalSecretValue += marketPrice
            elif(number == "005/025"):
                ultraCount += 1
                totalUltraValue += marketPrice
            elif(rarity == "Holo Rare"):
                holoCount += 1
                totalHoloValue += marketPrice
            elif(rarity == "Ultra Rare"):
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

    # Second price guide ----------------------------------

    # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/2931/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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

            if(number == "2/102"):
                blastoise += marketPrice
            elif(number == "4/102"):
                charizard += marketPrice
            elif(number == "15/106"):
                claydol += marketPrice
            elif(number == "20/111"):
                cleffa += marketPrice
            elif(number == "8/82"):
                gyarados += marketPrice
            elif(number == "107/123"):
                donphan += marketPrice
            elif(number == "145/147"):
                garchomp += marketPrice
            elif(number == "93/101"):
                gardevoir += marketPrice
            elif(number == "15/82"):
                teamRocket += marketPrice
            elif(number == "73/102"):
                imposter += marketPrice
            elif(number == "109/111"):
                luxray += marketPrice
            elif(number == "76/108"):
                rayquaza += marketPrice
            elif(number == "88/92"):
                mew += marketPrice
            elif(number == "54/99"):
                mewtwo += marketPrice
            elif(number == "4/102"):
                charizard += marketPrice
            elif(number == "113/114"):
                reshiram += marketPrice
            elif(number == "86/109"):
                admin += marketPrice
            elif(number == "15/132"):
                zapdos += marketPrice
            elif(number == "66/164"):
                magikarp += marketPrice
            elif(number == "60/145"):
                tapulele += marketPrice
            elif(number == "9/195"):
                groudon += marketPrice
            elif(number == "17/17"):
                umbreon += marketPrice
            elif(number == "15/102"):
                venusaur += marketPrice
            elif(number == "97/146"):
                xerneas += marketPrice
            elif(number == "114/114"):
                zekrom += marketPrice
            elif(number == "24/53"):
                pikachu += marketPrice
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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/248577/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1006.5)

    rareSlot = 0
    reverseSlot = 0

    classicCollection = (
    blastoise + charizard + claydol + cleffa + gyarados + donphan + garchomp + gardevoir +
    teamRocket + imposter + luxray + rayquaza + mew + mewtwo + reshiram + admin +
    zapdos + magikarp + tapulele + groudon + umbreon + venusaur + zekrom + xerneas + pikachu
)

    rareSlot += (totalUltraValue / ultraCount * .4021)
    rareSlot += (totalHoloValue / holoCount * .5903 )
    rareSlot += (totalSecretValue / secretCount * (1/130))

    reverseSlot += (blastoise * (14/541) )
    reverseSlot += (charizard * (7/541) )
    reverseSlot += (venusaur * (14/541) )
    reverseSlot += (imposter * (10/541) )
    reverseSlot += (gyarados * (6/541) )
    reverseSlot += (teamRocket * (1/35.4) )
    reverseSlot += (zapdos * (12/541) )
    reverseSlot += (pikachu * (16/541) )
    reverseSlot += (cleffa * (1/55.6) )
    reverseSlot += (magikarp * (6/541) )
    reverseSlot += (mew * (7/541) )
    reverseSlot += (claydol * (1/27.8) )
    reverseSlot += (groudon * (1/33.8) )
    reverseSlot += (gardevoir * (6/541) )
    reverseSlot += (luxray * (4/541) )
    reverseSlot += (admin * (1/45.8) )
    reverseSlot += (umbreon * (4/541) )
    reverseSlot += (garchomp * (8/541) )
    reverseSlot += (donphan * (1/77.8) )
    reverseSlot += (mewtwo * (4/541) )
    reverseSlot += (tapulele * (7/541) )
    reverseSlot += (reshiram * (3/541) )
    reverseSlot += (zekrom * (8/541) )
    reverseSlot += (zekrom * (6/541) )
    reverseSlot += (rayquaza * (2/541) )
    reverseSlot += (totalHoloValue / holoCount * .6)

    expValue = 0
    expValue += (totalHoloValue / holoCount * 2)
    expValue += rareSlot
    expValue += reverseSlot

    print("\n")
    print("Celebrations")
    print("Total Cards: " + str(totalCards))
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Ultra Rares and Pikachu: " + str(ultraCount) + ", Value: $" + f"{totalUltraValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Classic Collection: " + str("25") + ", Value: $" + f"{classicCollection:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def prismaticEvolutions():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalAceValue = 0
    totalDoubleValue = 0
    totalReverseValue = 0
    totalUltraValue = 0
    totalHyperValue = 0
    totalPokeballValue = 0
    totalMasterballValue = 0
    totalSirValue = 0


    commonCount = 0
    uncommonCount = 0
    reverseCount = 0
    aceCount = 0
    doubleCount = 0
    ultraCount = 0
    hyperCount = 0
    rareCount = 0
    pokeballCount = 0
    masterballCount = 0
    sirCount = 0

    unique_cards = {}

      # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/23821/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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

            if(rarity == "Hyper Rare"):
                hyperCount += 1
                totalHyperValue += marketPrice
            elif(rarity == "Ultra Rare"):
                ultraCount += 1
                totalUltraValue += marketPrice
            elif(rarity == "ACE SPEC Rare"):
                aceCount += 1
                totalAceValue += marketPrice
            elif(rarity == "Double Rare"):
                doubleCount += 1
                totalDoubleValue += marketPrice
            elif(rarity == "Special Illustration Rare"):
                sirCount += 1
                totalSirValue += marketPrice
            elif("Master Ball Pattern" in name):
                masterballCount += 1
                totalMasterballValue += marketPrice
            elif("Poke Ball Pattern" in name):
                pokeballCount += 1
                totalPokeballValue += marketPrice
            elif(rarity == "Rare"):
                rareCount += 1
                totalRareValue += marketPrice
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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/593294/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1207.5)

    rareSlot = 0
    reverseSlot1 = 0
    reverseSlot2 = 0

    rareSlot += (totalRareValue / rareCount * (1 - (1/6) - (1/13)))
    rareSlot += (totalDoubleValue / doubleCount * (1/6) )
    rareSlot += (totalUltraValue / ultraCount * (1/13) )

    reverseSlot1 += (totalReverseValue / reverseCount * (1 - (1/3) - (1/21)) )
    reverseSlot1 += (totalPokeballValue / pokeballCount * (1/3) )
    reverseSlot1 += (totalAceValue / aceCount * (1/21) )
    
    reverseSlot2 += (totalReverseValue / reverseCount * (1 - (1/20) - (1/45) - (1/180)) )
    reverseSlot2 += (totalMasterballValue / masterballCount * (1/20) )
    reverseSlot2 += (totalSirValue / sirCount * (1/45) )
    reverseSlot2 += (totalHyperValue / hyperCount * (1/180) )

    expValue = 0
    expValue += (totalCommonValue / commonCount * 4)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += rareSlot
    expValue += reverseSlot1
    expValue += reverseSlot2


    print("\n")
    print("Prismatic Evolutions")
    print("Total Cards: " + str(totalCards))
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Double Rares: " + str(doubleCount) + ", Value: $" + f"{totalDoubleValue:.2f}")
    print("Ultra Rares: " + str(ultraCount) + ", Value: $" + f"{totalUltraValue:.2f}")
    print("SIRs: " + str(sirCount) + ", Value: $" + f"{totalSirValue:.2f}")
    print("ACE SPECs: " + str(aceCount) + ", Value: $" + f"{totalAceValue:.2f}")
    print("Poke Ball Patterns: " + str(pokeballCount) + ", Value: $" + f"{totalPokeballValue:.2f}")
    print("Master Ball Patterns: " + str(masterballCount) + ", Value: $" + f"{totalMasterballValue:.2f}")
    print("Hyper Rares: " + str(hyperCount) + ", Value: $" + f"{totalHyperValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def blackBolt():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalDoubleValue = 0
    totalReverseValue = 0
    totalUltraValue = 0
    totalHyperValue = 0 #using this for black white rare
    totalPokeballValue = 0
    totalMasterballValue = 0
    totalSirValue = 0
    totalIrValue = 0


    commonCount = 0
    uncommonCount = 0
    reverseCount = 0
    doubleCount = 0
    ultraCount = 0
    hyperCount = 0 #using this for black white rare
    rareCount = 0
    pokeballCount = 0
    masterballCount = 0
    sirCount = 0
    irCount = 0

    unique_cards = {}

      # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/24325/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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

            if(rarity == "Black White Rare"):
                hyperCount += 1
                totalHyperValue += marketPrice
            elif(rarity == "Ultra Rare" or rarity == "Secret Rare"):
                ultraCount += 1
                totalUltraValue += marketPrice
            elif(rarity == "Double Rare"):
                doubleCount += 1
                totalDoubleValue += marketPrice
            elif(rarity == "Special Illustration Rare"):
                sirCount += 1
                totalSirValue += marketPrice
            elif(rarity == "Illustration Rare"):
                irCount += 1
                totalIrValue += marketPrice
            elif("Master Ball Pattern" in name):
                masterballCount += 1
                totalMasterballValue += marketPrice
            elif("Poke Ball Pattern" in name):
                pokeballCount += 1
                totalPokeballValue += marketPrice
            elif(rarity == "Rare"):
                rareCount += 1
                totalRareValue += marketPrice
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
    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/642597/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1209.51)

    rareSlot = 0
    reverseSlot1 = 0
    reverseSlot2 = 0

    rareSlot += (totalRareValue / rareCount * (1 - (1/5) - (1/17)))
    rareSlot += (totalDoubleValue / doubleCount * (1/5) )
    rareSlot += (totalUltraValue / ultraCount * (1/17) )

    reverseSlot1 += (totalReverseValue / reverseCount * (1 - (1/3)) )
    reverseSlot1 += (totalPokeballValue / pokeballCount * (1/3) )
    
    reverseSlot2 += (totalReverseValue / reverseCount * (1 - (1/19) - (1/80) - (1/496) - (1/6)) )
    reverseSlot2 += (totalMasterballValue / masterballCount * (1/19) )
    reverseSlot2 += (totalSirValue / sirCount * (1/80) )
    reverseSlot2 += (totalHyperValue / hyperCount * (1/496) )
    reverseSlot2 += (totalIrValue / irCount * (1/6))

    expValue = 0
    expValue += (totalCommonValue / commonCount * 4)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += rareSlot
    expValue += reverseSlot1
    expValue += reverseSlot2


    print("\n")
    print("Black Bolt")
    print("Total Cards: " + str(totalCards))
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Double Rares: " + str(doubleCount) + ", Value: $" + f"{totalDoubleValue:.2f}")
    print("Ultra Rares: " + str(ultraCount) + ", Value: $" + f"{totalUltraValue:.2f}")
    print("SIRs: " + str(sirCount) + ", Value: $" + f"{totalSirValue:.2f}")
    print("IRs: " + str(irCount) + ", Value: $" + f"{totalIrValue:.2f}")
    print("Poke Ball Patterns: " + str(pokeballCount) + ", Value: $" + f"{totalPokeballValue:.2f}")
    print("Master Ball Patterns: " + str(masterballCount) + ", Value: $" + f"{totalMasterballValue:.2f}")
    print("Black White Rares: " + str(hyperCount) + ", Value: $" + f"{totalHyperValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def whiteFlare():

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalDoubleValue = 0
    totalReverseValue = 0
    totalUltraValue = 0
    totalHyperValue = 0 #using this for black white rare
    totalPokeballValue = 0
    totalMasterballValue = 0
    totalSirValue = 0
    totalIrValue = 0


    commonCount = 0
    uncommonCount = 0
    reverseCount = 0
    doubleCount = 0
    ultraCount = 0
    hyperCount = 0 #using this for black white rare
    rareCount = 0
    pokeballCount = 0
    masterballCount = 0
    sirCount = 0
    irCount = 0

    unique_cards = {}


      # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/24326/cards/?rows=5000&productTypeID=1")    
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
            elif rarity == "Rare":
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

            if(rarity == "Black White Rare"):
                hyperCount += 1
                totalHyperValue += marketPrice
            elif(rarity == "Ultra Rare" or rarity == "Secret Rare"):
                ultraCount += 1
                totalUltraValue += marketPrice
            elif(rarity == "Double Rare"):
                doubleCount += 1
                totalDoubleValue += marketPrice
            elif(rarity == "Special Illustration Rare"):
                sirCount += 1
                totalSirValue += marketPrice
            elif(rarity == "Illustration Rare"):
                irCount += 1
                totalIrValue += marketPrice
            elif("Master Ball Pattern" in name):
                masterballCount += 1
                totalMasterballValue += marketPrice
            elif("Poke Ball Pattern" in name):
                pokeballCount += 1
                totalPokeballValue += marketPrice
            elif(rarity == "Rare"):
                rareCount += 1
                totalRareValue += marketPrice
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
    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/630699/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(1209.52)

    rareSlot = 0
    reverseSlot1 = 0
    reverseSlot2 = 0

    rareSlot += (totalRareValue / rareCount * (1 - (1/5) - (1/17)))
    rareSlot += (totalDoubleValue / doubleCount * (1/5) )
    rareSlot += (totalUltraValue / ultraCount * (1/17) )

    reverseSlot1 += (totalReverseValue / reverseCount * (1 - (1/3)) )
    reverseSlot1 += (totalPokeballValue / pokeballCount * (1/3) )
    
    reverseSlot2 += (totalReverseValue / reverseCount * (1 - (1/19) - (1/80) - (1/496) - (1/6)) )
    reverseSlot2 += (totalMasterballValue / masterballCount * (1/19) )
    reverseSlot2 += (totalSirValue / sirCount * (1/80) )
    reverseSlot2 += (totalHyperValue / hyperCount * (1/496) )
    reverseSlot2 += (totalIrValue / irCount * (1/6))

    expValue = 0
    expValue += (totalCommonValue / commonCount * 4)
    expValue += (totalUncommonValue / uncommonCount * 3)
    expValue += rareSlot
    expValue += reverseSlot1
    expValue += reverseSlot2


    print("\n")
    print("White Flare")
    print("Total Cards: " + str(totalCards))
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Double Rares: " + str(doubleCount) + ", Value: $" + f"{totalDoubleValue:.2f}")
    print("Ultra Rares: " + str(ultraCount) + ", Value: $" + f"{totalUltraValue:.2f}")
    print("SIRs: " + str(sirCount) + ", Value: $" + f"{totalSirValue:.2f}")
    print("IRs: " + str(irCount) + ", Value: $" + f"{totalIrValue:.2f}")
    print("Poke Ball Patterns: " + str(pokeballCount) + ", Value: $" + f"{totalPokeballValue:.2f}")
    print("Master Ball Patterns: " + str(masterballCount) + ", Value: $" + f"{totalMasterballValue:.2f}")
    print("Black White Rares: " + str(hyperCount) + ", Value: $" + f"{totalHyperValue:.2f}")
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Reverse Holos: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards