
import requests
from calculators import (
    gen1, earlyReverse, specialSets, earlyEx, goldStar,
    dp, hgss, bw, xy, sm, swsh, sv, myUtils, sealedProduct
)
# import gen1
# import earlyReverse
# import specialSets
# import earlyEx
# import goldStar
# import dp
# import hgss
# import bw
# import xy
# import sm
# import swsh
# import sv
# import myUtils

# ------------------------------------------------------------------------------------------------------------------
from datetime import datetime

# import firebase_admin
# from firebase_admin import credentials, firestore
# from datetime import datetime

# if os.getenv("FIREBASE_SERVICE_ACCOUNT"):
#     service_account_info = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
#     cred = credentials.Certificate(service_account_info)
# else:
#     cred = credentials.Certificate("serviceAccountKey.json")

# firebase_admin.initialize_app(cred)

# db = firestore.client()

class BoosterBox:
    def __init__(self, name, setNumber, productId):
        self.name = name
        self.setNumber = setNumber
        self.productId = productId

class VintageSet:
    def __init__(self, name, url, secretOdds, commonsPer, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.commonsPer = commonsPer 
        self.holoOdds = .33 - self.secretOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class EarlyReverseSet:
    def __init__(self, name, url, secretOdds, commonsPer, uncommonsPer, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.commonsPer = commonsPer 
        self.uncommonsPer = uncommonsPer
        self.holoOdds = .33 - self.secretOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class EarlyExSet:
    def __init__(self, name, url, secretOdds, ultraOdds, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class GoldStarSet:
    def __init__(self, name, url, secretOdds, ultraOdds, goldStarOdds, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.goldStarOdds = goldStarOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds - self.goldStarOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class LevelXSet:
    def __init__(self, name, url, secretOdds, ultraOdds, shinyOdds, rotomOdds, arceusOdds, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.shinyOdds = shinyOdds
        self.rotomOdds = rotomOdds
        self.arceusOdds = arceusOdds
        self.reverseOdds = 1 - self.shinyOdds - self.rotomOdds - self.arceusOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class HgssSet:
    def __init__(self, name, url, secretOdds, primeOdds, legendOdds, shinyOdds, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.primeOdds = primeOdds
        self.legendOdds = legendOdds
        self.shinyOdds = shinyOdds
        self.reverseOdds = 1 - self.primeOdds - self.shinyOdds
        self.holoOdds = .33 - self.secretOdds - self.legendOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class BWSet:
    def __init__(self, name, url, secretOdds, exOdds, faOdds, aceOdds, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.exOdds = exOdds
        self.faOdds = faOdds
        self.aceOdds = aceOdds
        self.reverseOdds = 1 - self.aceOdds
        self.holoOdds = .33 - self.secretOdds - self.exOdds - self.faOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class XYSet:
    def __init__(self, name, url, secretOdds, exOdds, faOdds, breakOdds, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.exOdds = exOdds
        self.faOdds = faOdds
        self.breakOdds = breakOdds
        self.reverseOdds = 1 - self.breakOdds
        self.holoOdds = (1/6)
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class SMSet:
    def __init__(self, name, url, secretOdds, gxOdds, faOdds, prismOdds, galleryOdds, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.gxOdds = gxOdds
        self.faOdds = faOdds
        self.prismOdds = prismOdds
        self.galleryOdds = galleryOdds
        self.reverseOdds = 1 - galleryOdds - prismOdds
        self.holoOdds = .33 - secretOdds - gxOdds - faOdds
        self.rareOdds = 1 - self.holoOdds - secretOdds - gxOdds - faOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class SWSHSet:
    def __init__(self, name, url, secretOdds, vOdds, vmaxOdds, faOdds, arOdds, altOdds, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.vOdds = vOdds
        self.faOdds = faOdds
        self.vmaxOdds = vmaxOdds
        self.arOdds = arOdds
        self.altOdds = altOdds
        self.reverseOdds = 1 - arOdds
        self.holoOdds = .33 - secretOdds - vOdds - vmaxOdds - faOdds - altOdds
        self.rareOdds = 1 - self.holoOdds - vOdds - vmaxOdds - faOdds - secretOdds - altOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

class lateSWSHSet:
    def __init__(self, name, url, url2, holoOdds, secretOdds, vOdds, vmaxOdds, vstarOdds, faOdds, altOdds, tgOdds, radiantOdds, productId, tcgId1, tcgId2, setNumber):
        self.name = name
        self.url = url
        self.url2 = url2
        self.secretOdds = secretOdds
        self.vOdds = vOdds
        self.faOdds = faOdds
        self.vmaxOdds = vmaxOdds
        self.vstarOdds = vstarOdds
        self.altOdds = altOdds
        self.tgOdds = tgOdds
        self.reverseOdds = 1 - tgOdds
        self.holoOdds = holoOdds
        self.radiantOdds = radiantOdds
        self.rareOdds = 1 - vOdds - vmaxOdds - faOdds - secretOdds - altOdds - holoOdds
        self.productId = productId
        self.tcgId1 = tcgId1
        self.tcgId2 = tcgId2
        self.setNumber = setNumber

class svSet:
    def __init__(self, name, url, hyperOdds, doubleOdds, ultraOdds, irOdds, sirOdds, aceOdds, productId, tcgId, setNumber):
        self.name = name
        self.url = url
        self.hyperOdds = hyperOdds
        self.doubleOdds = doubleOdds
        self.ultraOdds = ultraOdds
        self.irOdds = irOdds
        self.sirOdds = sirOdds
        self.aceOdds = aceOdds
        self.reverseOdds = (1 - aceOdds) + (1 - irOdds - sirOdds)
        self.rareOdds = 1 - doubleOdds - ultraOdds
        self.productId = productId
        self.tcgId = tcgId
        self.setNumber = setNumber

boosterBoxList = [
    BoosterBox("XY Base Set", 800, 91601),
    BoosterBox("Flashfire", 801, 91594),
    BoosterBox("Furious Fists", 802, 92168),
    BoosterBox("Phantom Forces", 803, 94623),
    BoosterBox("Primal Clash", 804, 97750),
    BoosterBox("Roaring Skies", 805, 98026),
    BoosterBox("Ancient Origins", 806, 100489),
    BoosterBox("BREAKthrough", 807, 107101),
    BoosterBox("BREAKpoint", 808, 111278),
    BoosterBox("Fates Collide", 809, 117478),
    BoosterBox("Steam Siege", 810, 120076),
    BoosterBox("Evolutions", 811, 123446),
    BoosterBox("Sun and Moon", 900, 126048),
    BoosterBox("Guardians Rising", 901, 129888),
    BoosterBox("Burning Shadows", 902, 133773),
    BoosterBox("Crimson Invasion", 903, 146995),
    BoosterBox("Ultra Prism", 904, 155661),
    BoosterBox("Forbidden Light", 905, 164296),
    BoosterBox("Celestial Storm", 906, 170273),
    BoosterBox("Lost Thunder", 907, 175509),
    BoosterBox("Team Up", 908, 181698),
    BoosterBox("Unbroken Bonds", 909, 185717),
    BoosterBox("Unified Minds", 910, 191882),
    BoosterBox("Cosmic Eclipse", 911, 199261),
    BoosterBox("Sword and Shield", 1000, 206027),
    BoosterBox("Rebel Clash", 1001, 210561),
    BoosterBox("Darkness Ablaze", 1002, 216853),
    BoosterBox("Vivid Voltage", 1003, 221313),
    BoosterBox("Battle Styles", 1004, 229277),
    BoosterBox("Chilling Reign", 1005, 236258),
    BoosterBox("Evolving Skies", 1006, 242436),
    BoosterBox("Fusion Strike", 1007, 247654),
    BoosterBox("Brilliant Stars", 1100, 256141),
    BoosterBox("Astral Radiance", 1101, 265519),
    BoosterBox("Lost Origin", 1102, 277324),
    BoosterBox("Silver Tempest", 1103, 283389),
    BoosterBox("Scarlet and Violet", 1200, 476452),
    BoosterBox("Paldea Evolved", 1201, 493975),
    BoosterBox("Obsidian Flames", 1202, 501257),
    BoosterBox("Paradox Rift", 1203, 512821),
    BoosterBox("Temporal Forces", 1204, 536225),
    BoosterBox("Twilight Masquerade", 1205, 543846),
    BoosterBox("Stellar Crown", 1206, 557354),
    BoosterBox("Surging Sparks", 1207, 565606),
    BoosterBox("Journey Together", 1208, 610931),
    BoosterBox("Destined Rivals", 1209, 624679),
    BoosterBox("Mega Evolution", 1210, 644298),
    BoosterBox("Phantasmal Flames", 1211, 654137)
]
vintageSetList = [
    VintageSet("Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/base-set", 0, 5, 138130, 604, 100),
    VintageSet("Jungle", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/jungle", 0, 7, 138129, 635, 101),
    VintageSet("Fossil", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/fossil", 0, 7, 138134, 630, 102),
    VintageSet("Base Set 2", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/base-set-2", 0, 7, 138149, 605, 103),
    VintageSet("Team Rocket", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-rocket", 1/81, 7, 138135, 1373, 104),
    VintageSet("Gym Heroes", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/gym-heroes", 0, 7, 138138, 1441, 105),
    VintageSet("Gym Challenge", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/gym-challenge", 0, 7, 138139, 1440, 106),
    VintageSet("Neo Genesis", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-genesis", 0, 7, 138142, 1396, 107),
    VintageSet("Neo Discovery", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-discovery", 0, 7, 138143, 1434, 108),
    VintageSet("Neo Revelation", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-revelation", 1/18, 7, 138146, 1389, 109),
    VintageSet("Neo Destiny", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-destiny", 1/12, 7, 138147, 1444, 110)
]

earlyReverseSetList = [
    EarlyReverseSet("Legendary Collection", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-collection", 0, 6, 3, 138150, 1374, 200),
    EarlyReverseSet("Expedition", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/expedition", 0, 5, 2, 138151, 1375, 201),
    EarlyReverseSet("Aquapolis", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/aquapolis", 1/36, 5, 2, 138152, 1397, 202),
    EarlyReverseSet("Skyridge", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/skyridge", 1/15, 5, 2, 138153, 1372, 203)
]

earlyExSetList = [
    EarlyExSet("Ruby and Sapphire", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/ruby-and-sapphire", 0, 1/15, 98558, 1393, 300),
    EarlyExSet("Sandstorm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sandstorm", 0, 1/15, 98565, 1392, 301),
    EarlyExSet("Dragon", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon", 1/36, 1/15, 98519, 1376, 302),
    EarlyExSet("Team Magma vs Team Aqua", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-magma-vs-team-aqua", 1/36, 1/15, 98550, 1377, 303),
    EarlyExSet("Hidden Legends", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/hidden-legends", 0, 1/15, 98595, 1416, 304),
    EarlyExSet("FireRed & LeafGreen", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/firered-and-leafgreen", 1/36, 1/15, 98946, 1419, 305),
    EarlyExSet("Emerald", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/emerald", 0, 1/15, 98546, 1410, 306)
]

goldStarSetList = [
    GoldStarSet("Team Rocket Returns", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-rocket-returns", 1/36, 1/15, 1/72, 98578, 1428, 400),
    GoldStarSet("Deoxys", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/deoxys", 0, 1/15, 1/72, 98562, 1404, 401),
    GoldStarSet("Unseen Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/unseen-forces", 1/36, 1/15, 1/72, 98577, 1398, 402),
    GoldStarSet("Delta Species", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/delta-species", 0, 1/15, 1/72, 98944, 1429, 403),
    GoldStarSet("Legend Maker", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legend-maker", 0, 1/15, 1/72, 98557, 1378, 404),
    GoldStarSet("Holon Phantoms", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/holon-phantoms", 0, 1/36, 1/72, 98522, 1379, 405),
    GoldStarSet("Crystal Guardians", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/crystal-guardians", 0, 1/15, 1/72, 98566, 1395, 406),
    GoldStarSet("Dragon Frontiers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon-frontiers", 0, 1/15, 1/72, 98533, 1411, 407),
    GoldStarSet("Power Keepers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/power-keepers", 0, 1/10, 1/54, 98529, 1383, 408)
]

levelXSetList = [
    LevelXSet("Diamond and Pearl", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/diamond-and-pearl", 0, 1/36, 0, 0, 0, 98525, 1430, 500),
    LevelXSet("Mysterious Treasures", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/mysterious-treasures", 1/72, 1/36, 0, 0, 0, 98561, 1368, 501),
    LevelXSet("Secret Wonders", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/secret-wonders", 0, 1/36, 0, 0, 0, 98569, 1380, 502),
    LevelXSet("Great Encounters", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/great-encounters", 0, 1/36, 0, 0, 0, 98545, 1405, 503),
    LevelXSet("Majestic Dawn", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/majestic-dawn", 0, 1/36, 0, 0, 0, 98585, 1390, 504),
    LevelXSet("Legends Awakened", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legends-awakened", 0, 1/12, 0, 0, 0, 98537, 1417, 505),
    LevelXSet("Stormfront", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/stormfront", 1/36, 1/12, 1/36, 0, 0, 98589, 1369, 506),
    LevelXSet("Platinum", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/platinum", 1/36, 1/12, 1/36, 0, 0, 98591, 1406, 507),
    LevelXSet("Rising Rivals", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/rising-rivals", 1/36, 1/12, 0, 1/18, 0, 98542, 1367, 508),
    LevelXSet("Supreme Victors", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/supreme-victors", 1/36, 1/12, 1/36, 0, 0, 98574, 1384, 509),
    LevelXSet("Arceus", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/arceus", 0, 1/12, 1/36, 0, 1/4, 98594, 1391, 510)
]

hgssSetList = [
    HgssSet("HeartGold SoulSilver", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/heartgold-soulsilver", 1/108, 1/6, 1/12, 0, 98530, 1402, 600),
    HgssSet("Unleashed", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/unleashed", 1/108, 1/7, 1/12, 0, 98582, 1399, 601),
    HgssSet("Undaunted", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/undaunted", 1/108, 1/7, 1/12, 0, 98586, 1403, 602),
    HgssSet("Triumphant", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/triumphant", 1/108, 1/7, 1/12, 0, 98534, 1381, 603),
    HgssSet("Call of Legends", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/call-of-legends", 0, 0, 0, 1/18, 98515, 1415, 604)
]

bwSetList = [
    BWSet("Black and White", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/black-and-white", 1/72, 0, 1/36, 0, 98553, 1400, 700),
    BWSet("Emerging Powers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/emerging-powers", 0, 0, 1/36, 0, 98549, 1424, 701),
    BWSet("Noble Victories", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/noble-victories", 1/72, 0, 1/18, 0, 98570, 1385, 702),
    BWSet("Next Destinies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/next-destinies", 1/72, 1/18, 1/36, 0, 98538, 1412, 703),
    BWSet("Dark Explorers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dark-explorers", 1/72, 1/18, 1/36, 0, 98521, 1386, 704),
    BWSet("Dragons Exalted", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragons-exalted", 1/72, 1/18, 1/36, 0, 98541, 1394, 705),
    BWSet("Boundaries Crossed", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/boundaries-crossed", 1/72, 1/18, 1/36, 1/36, 98554, 1408, 706),
    BWSet("Plasma Storm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-storm", 1/72, 1/18, 1/36, 1/36, 98526, 1413, 707),
    BWSet("Plasma Freeze", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-freeze", 1/72, 1/18, 1/36, 1/36, 98517, 1382, 708),
    BWSet("Plasma Blast", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-blast", 1/72, 1/18, 1/36, 1/36, 98573, 1370, 709)
]

legendaryTreasuresUrl = "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures"
legendaryTreasuresRadiantUrl = "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures-radiant-collection"

xySetList = [
    XYSet("XY Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-base-set", 0, 1/18, 1/36, 0, 91602, 1387, 800),
    XYSet("XY - Flashfire", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-flashfire", 1/72, 1/12, 1/18, 0, 91595, 1464, 801),
    XYSet("XY - Furious Fists", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-furious-fists", 1/72, 1/12, 1/18, 0, 92169, 1481, 802),
    XYSet("XY - Phantom Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-phantom-forces", 1/72, 1/9, 1/18, 0, 94622, 1494, 803),
    XYSet("XY - Primal Clash", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-primal-clash", 1/72, 1/9, 1/18, 0, 97751, 1509, 804),
    XYSet("XY - Roaring Skies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-roaring-skies", 1/72, 1/9, 1/18, 0, 129906, 1534, 805),
    XYSet("XY - Ancient Origins", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-ancient-origins", 1/72, 1/6, 1/12, 0, 100490, 1576, 806),
    XYSet("XY - BREAKthrough", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-breakthrough", 1/72, 1/6, 1/12, 1/12, 107666, 1661, 807),
    XYSet("XY - BREAKpoint", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-breakpoint", 1/72, 1/6, 1/12, 1/12, 111279, 1701, 808),
    XYSet("XY - Fates Collide", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-fates-collide", 1/72, 1/6, 1/12, 1/12, 168114, 1780, 809),
    XYSet("XY - Steam Siege", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-steam-siege", 1/72, 1/6, 1/12, 1/12, 130013, 1815, 810),
    XYSet("XY - Evolutions", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-evolutions", 0, 1/6, 1/12, 1/12, 129907, 1842, 811)
]

smSetList = [
    SMSet("SM Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-base-set", .0277, 1/9, 1/24, 0, 0, 129385, 1863, 900),
    SMSet("SM - Guardians Rising", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-guardians-rising", .0265, 1/9, 1/28, 0, 0, 129889, 1919, 901),
    SMSet("SM - Burning Shadows", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-burning-shadows", .0276, 1/9, 1/25, 0, 0, 133774, 1957, 902),
    SMSet("SM - Crimson Invasion", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-crimson-invasion", .0222, 1/12, 1/22, 0, 0, 146996, 2071, 903),
    SMSet("SM - Ultra Prism", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-ultra-prism", .0254, 1/12, 1/22, 1/12, 0, 155662, 2178, 904),
    SMSet("SM - Forbidden Light", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-forbidden-light", .0227, 1/12, 1/28, 1/12, 0, 164297, 2209, 905),
    SMSet("SM - Celestial Storm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-celestial-storm", .0229, 1/9, 1/28, 1/18, 0, 170274, 2278, 906),
    SMSet("SM - Lost Thunder", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-lost-thunder", .0255, 1/10, 1/22, 1/9, 0, 175510, 2328, 907),
    SMSet("SM - Team Up", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-team-up", 0.0176, 1/10, 1/22, 1/18, 0, 181699, 2377, 908),
    SMSet("SM - Unbroken Bonds", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-unbroken-bonds", .0228, 1/10, 1/22, 0, 0, 185718, 2420, 909),
    SMSet("SM - Unified Minds", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-unified-minds", .0228, 1/8, 1/22, 0, 0, 191883, 2464, 910),
    SMSet("SM - Cosmic Eclipse", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-cosmic-eclipse", 0.02861, 1/9, 1/27, 0, 1/9, 199263, 2534, 911)
]

swshSetList = [
    SWSHSet("SWSH01: Sword & Shield Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh01-sword-and-shield-base-set", 0.0237, 1/7, 1/45, 1/27, 0, 0, 206028, 2585, 1000),
    SWSHSet("SWSH02: Rebel Clash", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh02-rebel-clash", 0.0263, 1/8, 1/30, 1/27, 0, 0, 210562, 2626, 1001),
    SWSHSet("SWSH03: Darkness Ablaze", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh03-darkness-ablaze", 0.0239, 1/8, 1/26, 1/27, 0, 0, 216852, 2675, 1002),
    SWSHSet("SWSH04: Vivid Voltage", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh04-vivid-voltage", 0.0452, 1/8, 1/24, 1/24, 1/20, 0, 221312, 2701, 1003),
    SWSHSet("SWSH05: Battle Styles", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh05-battle-styles", 0.0187, 1/8, 1/24, 1/48 + 1/94, 0, 1/201 + 1/703, 229276, 2765, 1004),
    SWSHSet("SWSH06: Chilling Reign", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh06-chilling-reign", 0.0196, 1/8, 1/24, 1/49 + 1/78, 0, 1/147 + 1/454, 236257, 2807, 1005),
    SWSHSet("SWSH07: Evolving Skies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh07-evolving-skies", 0.0225, 1/8, 1/18, 1/197 + 1/56, 0, 1/82 + 1/283, 244337, 2848, 1006),
    SWSHSet("SWSH08: Fusion Strike", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh08-fusion-strike", 0.0160, 1/8, 1/30, 1/64 + 1/58, 0, 1/180 + 1/332, 247646, 2906, 1007),
]

lateSwshSetList = [
    lateSWSHSet("SWSH09: Brilliant Stars", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh09-brilliant-stars", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh09-brilliant-stars-trainer-gallery", .264, .0191, 1/7, 1/96, 1/43, 1/30, 1/127, 0.1944, 0, 256124, 2948, 3020, 1100),
    lateSWSHSet("SWSH10: Astral Radiance", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh10-astral-radiance", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh10-astral-radiance-trainer-gallery", .255, .0141, .1512, .0081, .0026, .0537, 1/135, .125, .0488, 265521, 3040, 3068, 1101),
    lateSWSHSet("SWSH11: Lost Origin", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh11-lost-origin", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh11-lost-origin-trainer-gallery", .265, .0316, .1309, .0167, .0418, .046, 14/2211, .1146, .0404, 277325, 3118, 3172, 1102),
    lateSWSHSet("SWSH12: Silver Tempest", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh12-silver-tempest", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh12-silver-tempest-trainer-gallery", .254, .0287, .1295, .0167, .0279, .0599, 1/684+1/636+1/636+1/741, .1146, .0557, 283388, 3170, 17674, 1103),
]

svSetList = [
    svSet("SV01: Scarlet & Violet Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv01-scarlet-and-violet-base-set", .0185, .1428, .0666, .0769, .03125, 0, 476451, 22873, 1200),
    svSet("SV02: Paldea Evolved", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv02-paldea-evolved", .0175, .1428, .0666, .0769, .03125, 0, 493976, 23120, 1201),
    svSet("SV03: Obsidian Flames", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv03-obsidian-flames", .0192, .1428, .0666, .0769, .03125, 0, 501256, 23228, 1202 ),
    svSet("SV04: Paradox Rift", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv04-paradox-rift", .0121, .1666, .0666, .0769, .0212, 0, 512822, 23286, 1203 ),
    svSet("SV05: Temporal Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv05-temporal-forces", .0071, .1666, .0666, .0769, .0116, .05, 532841, 23381, 1204 ),
    svSet("SV06: Twilight Masquerade", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv06-twilight-masquerade", .0175, .1666, .0666, .0769, .0116, .05, 543843, 23473, 1205 ),
    svSet("SV07: Stellar Crown", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv07-stellar-crown", .0192, .1666, .0666, .0769, .0111, .05, 557331, 23537, 1206 ),
    svSet("SV08: Surging Sparks", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv08-surging-sparks", .0121, .1666, .0666, .0769, .0114, .05, 565604, 23651, 1207 ),
    svSet("SV09: Journey Together", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv09-journey-together", .0072, .2, .0667, .0833, .0116, 0, 610935, 24073, 1208),
    svSet("SV10: Destined Rivals", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv10-destined-rivals", .0067, .2, .0625, .0833, .0106, 0, 624683, 24269, 1209),
    svSet("ME01: Mega Evolution", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/me01-mega-evolution", .0008, .2, .0833, .1111, .0099, 0, 644352, 24380, 1210),
    svSet("ME02: Phantasmal Flames", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/me02-phantasmal-flames", .0008, .2, .0833, .1111, .0125, 0, 654144, 24448, 1211)

]

# Function to get the last Box Value by Set Number
def get_last_box_value(set_number):
    doc_ref = myUtils.db.collection("boosterBoxes").document(str(set_number))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("boxPrice")
    return None  # if document doesn't exist

def findSet(name, list):
    for set in list:
        if set.name == name:
            return set
    return None


def getBoxPrices(boxSet):

    response = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{boxSet.productId}/details?mpfev=3442")   
    data = response.json() 
    
    price = data.get("marketPrice") or data.get("medianPrice") or data.get("lowestPrice") or get_last_box_value(boxSet.setNumber)
    pricePer = float(price/36)

    print("\n")
    print("Set Name: " + boxSet.name)
    print("Box Price: $" + str(price))
    print(f"Price Per Pack: ${pricePer:.2f}")

    return price, round(pricePer, 2), boxSet.name, boxSet.setNumber



expectedValueList = []
setNameList = []
packValueList = []
actualEvList = []
setNumberList = []

boxSetNameList = []
boxSetNumberList = []
boxPriceList = []
boxPricePerList = []
boxSetNumberList = []
top5CardsList = []

def getSetName(set):
    return set.name

num = 0

for set in vintageSetList:
    adjev, price, ev, top_5_cards = gen1.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(100 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0


for set in earlyReverseSetList:
    adjev, price, ev, top_5_cards = earlyReverse.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(200 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0

for set in earlyExSetList:
    adjev, price, ev, top_5_cards = earlyEx.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(300 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0

for set in goldStarSetList:
    adjev, price, ev, top_5_cards = goldStar.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(400 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0

for set in levelXSetList:
    adjev, price, ev, top_5_cards = dp.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(500 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0

for set in hgssSetList:
    adjev, price, ev, top_5_cards = hgss.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(600 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0

for set in bwSetList:
    adjev, price, ev, top_5_cards = bw.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(700 + num)
    top5CardsList.append(top_5_cards)
    num += 1   

adjev, price, ev, top_5_cards = bw.legendaryTreasures()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Legendary Treasures")
actualEvList.append(ev)
setNumberList.append(710)
top5CardsList.append(top_5_cards)

num = 0

for set in xySetList:
    adjev, price, ev, top_5_cards = xy.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(800 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0

for set in smSetList:
    adjev, price, ev, top_5_cards = sm.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(900 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0

for set in swshSetList:
    adjev, price, ev, top_5_cards = swsh.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(1000 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0

for set in lateSwshSetList:
    adjev, price, ev, top_5_cards = swsh.lateSwshSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(1100 + num)
    top5CardsList.append(top_5_cards)
    num += 1

num = 0

for set in svSetList:
    adjev, price, ev, top_5_cards = sv.calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(1200 + num)
    top5CardsList.append(top_5_cards)
    num += 1
    

adjev, price, ev, top_5_cards = specialSets.dragonVault()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Dragon Vault")
actualEvList.append(ev)
setNumberList.append(705.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.doubleCrisis()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Double Crisis")
actualEvList.append(ev)
setNumberList.append(804.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.shiningLegends()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Shining Legends")
actualEvList.append(ev)
setNumberList.append(902.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.dragonMajesty()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Dragon Majesty")
actualEvList.append(ev)
setNumberList.append(906.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.championsPath()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Champions Path")
actualEvList.append(ev)
setNumberList.append(1002.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.pokemonGo()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Pokemon Go")
actualEvList.append(ev)
setNumberList.append(1101.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.pokemon151()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Pokemon 151")
actualEvList.append(ev)
setNumberList.append(1202.5)
top5CardsList.append(top_5_cards) 

adjev, price, ev, top_5_cards = specialSets.paldeanFates()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Paldean Fates")
actualEvList.append(ev)
setNumberList.append(1203.5)
top5CardsList.append(top_5_cards) 

adjev, price, ev, top_5_cards = specialSets.shroudedFable()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Shrouded Fable")
actualEvList.append(ev)
setNumberList.append(1205.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.hiddenFates()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Hidden Fates")
actualEvList.append(ev)
setNumberList.append(910.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.shiningFates()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Shining Fates")
actualEvList.append(ev)
setNumberList.append(1003.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.generations()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Generations")
actualEvList.append(ev)
setNumberList.append(808.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.crownZenith()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Crown Zenith")
actualEvList.append(ev)
setNumberList.append(1103.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.celebrations()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Celebrations")
actualEvList.append(ev)
setNumberList.append(1006.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.prismaticEvolutions()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Prismatic Evolutions")
actualEvList.append(ev)
setNumberList.append(1207.5)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.blackBolt()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Black Bolt")
actualEvList.append(ev)
setNumberList.append(1209.51)
top5CardsList.append(top_5_cards)

adjev, price, ev, top_5_cards = specialSets.whiteFlare()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("White Flare")
actualEvList.append(ev)
setNumberList.append(1209.52)
top5CardsList.append(top_5_cards)

for bb in boosterBoxList:
    boxPrice, boxPricePer, setName, setNumber = getBoxPrices(bb)
    boxPriceList.append(boxPrice)
    boxPricePerList.append(boxPricePer)
    boxSetNameList.append(setName)
    boxSetNumberList.append(setNumber)
    
last_updated_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#excel sheet stuff below
#-----------------------

# Prepare the data to be written into JSON format
output_data = []
for i in range(len(setNameList)):
    output_data.append({
        "setName": setNameList[i],
        "adjustedEv": expectedValueList[i],
        "packValue": packValueList[i],
        "ev": actualEvList[i],
        "lastUpdated": datetime.strptime(last_updated_timestamp, "%Y-%m-%d %H:%M:%S"),
        "setNumber": setNumberList[i],
        "top5Cards": top5CardsList[i]  # Add the top 5 cards array
    })

for record in output_data:
    doc_id = str(record["setNumber"])
    myUtils.db.collection("sets").document(doc_id).set(record)


# #Booster Box 

box_output_data = []

for i in range(len(boxSetNameList)):
    box_output_data.append({
        "setName": boxSetNameList[i],
        "boxPrice": boxPriceList[i],
        "pricePer": boxPricePerList[i],
        "setNumber": boxSetNumberList[i],
        "lastUpdated": datetime.strptime(
            last_updated_timestamp, "%Y-%m-%d %H:%M:%S"
        )
    })

for box in box_output_data:
    doc_id = str(box["setNumber"])

    myUtils.db.collection("boosterBoxes").document(doc_id).set(box)


