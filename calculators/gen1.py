import requests
import myUtils
def calculate(set):
    #need some variables for a couple special sets still
    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    
    # Dictionary to store the highest price for each unique card
    unique_cards = {}
    
    # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/{set.tcgId}/cards/?rows=5000&productTypeID=1")    
    data = response.json() 
    
    for item in data.get("result", []):
        # Get card identifier (using productName as unique identifier)
        card_name_raw = item.get('productName', 'Unknown')
        card_name = myUtils.clean_card_name(card_name_raw)        
        card_price = item.get('marketPrice', 0)
        card_number = item.get('number', 'N/A')
        
        # Only keep the highest price version of each card
        if card_name not in unique_cards or card_price > unique_cards[card_name]['price']:
            unique_cards[card_name] = {
                'name': card_name,
                'price': card_price,
                'rarity': item.get('rarity', 'Unknown'),
                'condition': item.get('condition', 'Unknown'),
                'number': card_number
            }
        
        if item.get("condition") in ("Near Mint", "Near Mint Unlimited") and item.get("rarity") == "Common":
            commonCount += 1
            totalCommonValue += item.get("marketPrice")
            totalCards += 1
        elif item.get("condition") in ("Near Mint", "Near Mint Unlimited Holofoil", "Near Mint Holofoil") and item.get("rarity") == "Holo Rare":
            holoCount += 1
            totalHoloValue += item.get("marketPrice")
            totalCards += 1
        elif item.get("condition") in ("Near Mint", "Near Mint Unlimited") and item.get("rarity") == "Uncommon":
            uncommonCount += 1
            totalUncommonValue += item.get("marketPrice")
            totalCards += 1
        elif item.get("condition") in ("Near Mint", "Near Mint Unlimited") and item.get("rarity") == "Rare":
            rareCount += 1
            totalRareValue += item.get("marketPrice")
            totalCards += 1
        elif item.get("condition") in ("Near Mint", "Near Mint Unlimited Holofoil", "Near Mint Holofoil") and item.get("rarity") == "Secret Rare":
            secretCount += 1
            totalSecretValue += item.get("marketPrice")
            totalCards += 1
    
    # Convert dictionary to list and sort by price to get top 5 unique cards
    all_unique_cards = list(unique_cards.values())
    top_5_cards = sorted(all_unique_cards, key=lambda x: x['price'], reverse=True)[:5]
    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or myUtils.get_last_pack_value(set.setNumber)
    
    expValue = 0
    if(set.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * set.secretOdds)
    expValue += ((totalCommonValue / commonCount * set.commonsPer) + (totalUncommonValue / uncommonCount * 3) + (totalRareValue / rareCount * .66) + (totalHoloValue / holoCount * set.holoOdds)) 
    
    print("\n")
    print(set.name)
    print("Total Cards: " + str(totalCards))
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")
    
    # Print top 5 most expensive cards
    print("\nTop 5 Most Expensive Cards:")
    for i, card in enumerate(top_5_cards, 1):
        print(f"{i}. {card['name']} - #{card['number']} ({card['rarity']}, {card['condition']}) - ${card['price']:.2f}")
    
    return (expValue / (packPrice)), packPrice, expValue, top_5_cards