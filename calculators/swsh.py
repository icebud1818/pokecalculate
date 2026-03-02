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
    totalVValue = 0
    totalFaValue = 0
    totalVmaxValue = 0
    totalArValue = 0
    totalAltValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    vCount = 0
    faCount = 0
    codeCardCount = 0
    vmaxCount = 0
    arCount = 0
    altCount = 0

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
            elif rarity == "Amazing Rare":
                arCount += 1
                totalArValue += marketPrice
            elif "Alternate" in name:
                altCount += 1
                totalAltValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
            elif "Full Art" in name:
                faCount += 1
                totalFaValue += marketPrice
            elif "VMAX" in name:
                vmaxCount += 1
                totalVmaxValue += marketPrice
            elif " V" in name:
                vCount += 1
                totalVValue += marketPrice
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
        
    if(set.arOdds > 0):
        expValue += (totalArValue /max(arCount, 1) * set.arOdds)
    if(set.altOdds > 0):
        expValue += (totalAltValue /max(altCount, 1) * set.altOdds)
        

    expValue += (totalSecretValue / max(secretCount, 1) * set.secretOdds)
    expValue += (totalFaValue /faCount * set.faOdds)
    expValue += (totalVValue /vCount * set.vOdds)
    expValue += (totalVmaxValue /vmaxCount * set.vmaxOdds)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity)
    expValue += (totalRareValue / rareCount * set.rareOdds)
    expValue += (totalHoloValue / holoCount * set.holoOdds)
    expValue += (totalReverseValue / reverseCount * set.reverseOdds)


    print("\n")
    print(set.name)
    print("Total Cards: " + str(totalCards))
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Vs: " + str(vCount) + ", Value: $" + f"{totalVValue:.2f}")
    print("VMAXs: " + str(vmaxCount) + ", Value: $" + f"{totalVmaxValue:.2f}")
    print("Reverses: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("Amazing Rares: " + str(arCount) + ", Value: $" + f"{totalArValue:.2f}")
    print("Alt Arts: " + str(altCount) + ", Value: $" + f"{totalAltValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards

def lateSwshSets(set):

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    totalReverseValue = 0
    totalVValue = 0
    totalFaValue = 0
    totalVmaxValue = 0
    totalVstarValue = 0
    totalRadiantValue = 0
    totalTgValue = 0
    totalAltValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    vCount = 0
    faCount = 0
    codeCardCount = 0
    vmaxCount = 0
    altCount = 0
    vstarCount = 0
    radiantCount = 0
    tgCount = 0

    unique_cards = {}

   # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/{set.tcgId1}/cards/?rows=5000&productTypeID=1")    
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

        # Track for top 5 cards (main set)
        card_name_raw = item.get('productName', 'Unknown')
        card_name = myUtils.clean_card_name(card_name_raw)
        card_number = item.get('number', 'N/A')

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
            elif rarity == "Radiant Rare":
                radiantCount += 1
                totalRadiantValue += marketPrice
            elif "Alternate" in name:
                altCount += 1
                totalAltValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
            elif "Full Art" in name:
                faCount += 1
                totalFaValue += marketPrice
            elif "VMAX" in name:
                vmaxCount += 1
                totalVmaxValue += marketPrice
            elif "VSTAR" in name:
                vstarCount += 1
                totalVstarValue += marketPrice
            elif " V" in name:
                vCount += 1
                totalVValue += marketPrice
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
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/{set.tcgId2}/cards/?rows=5000&productTypeID=1")    
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

            tgCount += 1
            totalTgValue += marketPrice

    # Convert dictionary to list and sort by price to get top 5 unique cards
    all_unique_cards = list(unique_cards.values())
    top_5_cards = sorted(all_unique_cards, key=lambda x: x['price'], reverse=True)[:5]
    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(set.setNumber)

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
        
    if(set.radiantOdds > 0):
        expValue += (totalRadiantValue /radiantCount * set.radiantOdds)
        
        
    expValue += (totalAltValue /max(altCount, 1) * set.altOdds)
    expValue += (totalSecretValue / max(secretCount, 1) * set.secretOdds)
    expValue += (totalFaValue /faCount * set.faOdds)
    expValue += (totalVValue /vCount * set.vOdds)
    expValue += (totalVmaxValue /vmaxCount * set.vmaxOdds)
    expValue += (totalVstarValue /vstarCount * set.vstarOdds)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity)
    expValue += (totalRareValue / rareCount * set.rareOdds)
    expValue += (totalHoloValue / holoCount * set.holoOdds)
    expValue += (totalReverseValue / reverseCount * set.reverseOdds)
    expValue += (totalTgValue /tgCount * set.tgOdds)


    print("\n")
    print(set.name)
    print("Total Cards: " + str(totalCards))
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Vs: " + str(vCount) + ", Value: $" + f"{totalVValue:.2f}")
    print("VMAXs: " + str(vmaxCount) + ", Value: $" + f"{totalVmaxValue:.2f}")
    print("Reverses: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("VSTARs: " + str(vstarCount) + ", Value: $" + f"{totalVstarValue:.2f}")
    print("Radiants: " + str(radiantCount) + ", Value: $" + f"{totalRadiantValue:.2f}")
    print("Alt Arts: " + str(altCount) + ", Value: $" + f"{totalAltValue:.2f}")
    print("Trainer Gallery: " + str(tgCount) + ", Value: $" + f"{totalTgValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards