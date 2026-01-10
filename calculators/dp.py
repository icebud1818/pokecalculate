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
    totalShinyValue = 0
    totalRotomValue = 0
    totalArceusValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    ultraRareCount = 0
    shinyCount = 0
    rotomCount = 0
    arceusCount = 0

    # Dictionary to store the highest price for each unique card
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
                totalCards += 1

        # Process Holofoil if it exists
        if product["holofoil"]:
            rarity = product["holofoil"]["rarity"]
            marketPrice = product["holofoil"]["marketPrice"]
            name = product["holofoil"]["productName"]
            number = product["holofoil"]["number"]

            if name == "Time-Space Distortion":
                secretCount += 1
                totalSecretValue += marketPrice
            elif number == "AR1" or number == "AR2" or number == "AR3" or number == "AR4" or number == "AR5" or number == "AR6" or number == "AR7" or number == "AR8" or number == "AR9":
                arceusCount += 1
                totalArceusValue += marketPrice
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
            elif rarity == "Ultra Rare":
                ultraRareCount += 1
                totalUltraRareValue += marketPrice
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
            
            if(rarity == "Shiny Holo Rare"):
                shinyCount += 1
                totalShinyValue += marketPrice
            elif number == "RT1" or number == "RT2" or number == "RT3" or number == "RT4" or number == "RT5" or number == "RT6":
                rotomCount += 1
                totalRotomValue += marketPrice
            else:
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
    if(set.shinyOdds > 0):
        expValue += (totalShinyValue /max(shinyCount, 1) * set.shinyOdds)
    if(set.rotomOdds > 0):
        expValue += (totalRotomValue /max(rotomCount, 1) * set.rotomOdds)
    if(set.arceusOdds > 0):
        expValue += (totalArceusValue /max(arceusCount, 1) * set.arceusOdds)

    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * .66)
    expValue += (totalHoloValue / holoCount * set.holoOdds)
    expValue += (totalUltraRareValue / ultraRareCount * set.ultraOdds)
    expValue += (totalReverseValue / reverseCount * set.reverseOdds)


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
    print("Shinies: " + str(shinyCount) + ", Value: $" + f"{totalShinyValue:.2f}")
    print("Rotoms: " + str(rotomCount) + ", Value: $" + f"{totalRotomValue:.2f}")
    print("Arceus: " + str(arceusCount) + ", Value: $" + f"{totalArceusValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")

    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards