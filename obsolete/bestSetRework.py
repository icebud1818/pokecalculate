
import requests
import json
import os

# ------------------------------------------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import json
from datetime import datetime
from openpyxl.styles import numbers
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from datetime import datetime



class BoosterBox:
    def __init__(self, name, setNumber, productId):
        self.name = name
        self.setNumber = setNumber
        self.productId = productId

class VintageSet:
    def __init__(self, name, url, secretOdds, commonsPer, productId, tcgId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.commonsPer = commonsPer 
        self.holoOdds = .33 - self.secretOdds
        self.productId = productId
        self.tcgId = tcgId

class EarlyReverseSet:
    def __init__(self, name, url, secretOdds, commonsPer, uncommonsPer, productId, tcgId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.commonsPer = commonsPer 
        self.uncommonsPer = uncommonsPer
        self.holoOdds = .33 - self.secretOdds
        self.productId = productId
        self.tcgId = tcgId

class EarlyExSet:
    def __init__(self, name, url, secretOdds, ultraOdds, productId, tcgId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds
        self.productId = productId
        self.tcgId = tcgId

class GoldStarSet:
    def __init__(self, name, url, secretOdds, ultraOdds, goldStarOdds, productId, tcgId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.goldStarOdds = goldStarOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds - self.goldStarOdds
        self.productId = productId
        self.tcgId = tcgId

class LevelXSet:
    def __init__(self, name, url, secretOdds, ultraOdds, shinyOdds, rotomOdds, arceusOdds, productId, tcgId):
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

class HgssSet:
    def __init__(self, name, url, secretOdds, primeOdds, legendOdds, shinyOdds, productId, tcgId):
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

class BWSet:
    def __init__(self, name, url, secretOdds, exOdds, faOdds, aceOdds, productId, tcgId):
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

class XYSet:
    def __init__(self, name, url, secretOdds, exOdds, faOdds, breakOdds, productId, tcgId):
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

class SMSet:
    def __init__(self, name, url, secretOdds, gxOdds, faOdds, prismOdds, galleryOdds, productId, tcgId):
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

class SWSHSet:
    def __init__(self, name, url, secretOdds, vOdds, vmaxOdds, faOdds, arOdds, altOdds, productId, tcgId):
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

class lateSWSHSet:
    def __init__(self, name, url, url2, holoOdds, secretOdds, vOdds, vmaxOdds, vstarOdds, faOdds, altOdds, tgOdds, radiantOdds, productId, tcgId1, tcgId2):
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

class svSet:
    def __init__(self, name, url, hyperOdds, doubleOdds, ultraOdds, irOdds, sirOdds, aceOdds, productId, tcgId):
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
    VintageSet("Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/base-set", 0, 5, 138130, 604),
    VintageSet("Jungle", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/jungle", 0, 7, 138129, 635),
    VintageSet("Fossil", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/fossil", 0, 7, 138134, 630),
    VintageSet("Base Set 2", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/base-set-2", 0, 7, 138149, 605),
    VintageSet("Team Rocket", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-rocket", 1/81, 7, 138135, 1373),
    VintageSet("Gym Heroes", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/gym-heroes", 0, 7, 138138, 1441),
    VintageSet("Gym Challenge", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/gym-challenge", 0, 7, 138139, 1440),
    VintageSet("Neo Genesis", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-genesis", 0, 7, 138142, 1396),
    VintageSet("Neo Discovery", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-discovery", 0, 7, 138143, 1434),
    VintageSet("Neo Revelation", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-revelation", 1/18, 7, 138146, 1389),
    VintageSet("Neo Destiny", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-destiny", 1/12, 7, 138147, 1444)
]

earlyReverseSetList = [
    EarlyReverseSet("Legendary Collection", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-collection", 0, 6, 3, 138150, 1374),
    EarlyReverseSet("Expedition", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/expedition", 0, 5, 2, 138151, 1375),
    EarlyReverseSet("Aquapolis", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/aquapolis", 1/36, 5, 2, 138152, 1397),
    EarlyReverseSet("Skyridge", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/skyridge", 1/15, 5, 2, 138153, 1372)
]

earlyExSetList = [
    EarlyExSet("Ruby and Sapphire", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/ruby-and-sapphire", 0, 1/15, 98558, 1393),
    EarlyExSet("Sandstorm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sandstorm", 0, 1/15, 98565, 1392),
    EarlyExSet("Dragon", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon", 1/36, 1/15, 98519, 1376),
    EarlyExSet("Team Magma vs Team Aqua", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-magma-vs-team-aqua", 1/36, 1/15, 98550, 1377),
    EarlyExSet("Hidden Legends", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/hidden-legends", 0, 1/15, 98595, 1416),
    EarlyExSet("FireRed & LeafGreen", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/firered-and-leafgreen", 1/36, 1/15, 98946, 1419),
    EarlyExSet("Emerald", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/emerald", 0, 1/15, 98546, 1410)
]

goldStarSetList = [
    GoldStarSet("Team Rocket Returns", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-rocket-returns", 1/36, 1/15, 1/72, 98578, 1428),
    GoldStarSet("Deoxys", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/deoxys", 0, 1/15, 1/72, 98562, 1404),
    GoldStarSet("Unseen Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/unseen-forces", 1/36, 1/15, 1/72, 98577, 1398),
    GoldStarSet("Delta Species", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/delta-species", 0, 1/15, 1/72, 98944, 1429),
    GoldStarSet("Legend Maker", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legend-maker", 0, 1/15, 1/72, 98557, 1378),
    GoldStarSet("Holon Phantoms", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/holon-phantoms", 0, 1/36, 1/72, 98522, 1379),
    GoldStarSet("Crystal Guardians", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/crystal-guardians", 0, 1/15, 1/72, 98566, 1395),
    GoldStarSet("Dragon Frontiers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon-frontiers", 0, 1/15, 1/72, 98533, 1411),
    GoldStarSet("Power Keepers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/power-keepers", 0, 1/10, 1/54, 98529, 1383)
]

levelXSetList = [
    LevelXSet("Diamond and Pearl", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/diamond-and-pearl", 0, 1/36, 0, 0, 0, 98525, 1430),
    LevelXSet("Mysterious Treasures", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/mysterious-treasures", 1/72, 1/36, 0, 0, 0, 98561, 1368),
    LevelXSet("Secret Wonders", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/secret-wonders", 0, 1/36, 0, 0, 0, 98569, 1380),
    LevelXSet("Great Encounters", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/great-encounters", 0, 1/36, 0, 0, 0, 98545, 1405),
    LevelXSet("Majestic Dawn", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/majestic-dawn", 0, 1/36, 0, 0, 0, 98585, 1390),
    LevelXSet("Legends Awakened", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legends-awakened", 0, 1/12, 0, 0, 0, 98537, 1417),
    LevelXSet("Stormfront", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/stormfront", 1/36, 1/12, 1/36, 0, 0, 98589, 1369),
    LevelXSet("Platinum", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/platinum", 1/36, 1/12, 1/36, 0, 0, 98591, 1406),
    LevelXSet("Rising Rivals", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/rising-rivals", 1/36, 1/12, 0, 1/18, 0, 98542, 1367),
    LevelXSet("Supreme Victors", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/supreme-victors", 1/36, 1/12, 1/36, 0, 0, 98574, 1384),
    LevelXSet("Arceus", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/arceus", 0, 1/12, 1/36, 0, 1/4, 98594, 1391)
]

hgssSetList = [
    HgssSet("HeartGold SoulSilver", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/heartgold-soulsilver", 1/108, 1/6, 1/12, 0, 98530, 1402),
    HgssSet("Unleashed", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/unleashed", 1/108, 1/7, 1/12, 0, 98582, 1399),
    HgssSet("Undaunted", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/undaunted", 1/108, 1/7, 1/12, 0, 98586, 1403),
    HgssSet("Triumphant", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/triumphant", 1/108, 1/7, 1/12, 0, 98534, 1381),
    HgssSet("Call of Legends", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/call-of-legends", 0, 0, 0, 1/18, 98515, 1415)
]

bwSetList = [
    BWSet("Black and White", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/black-and-white", 1/72, 0, 1/36, 0, 98553, 1400),
    BWSet("Emerging Powers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/emerging-powers", 0, 0, 1/36, 0, 98549, 1424),
    BWSet("Noble Victories", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/noble-victories", 1/72, 0, 1/18, 0, 98570, 1385),
    BWSet("Next Destinies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/next-destinies", 1/72, 1/18, 1/36, 0, 98538, 1412),
    BWSet("Dark Explorers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dark-explorers", 1/72, 1/18, 1/36, 0, 98521, 1386),
    BWSet("Dragons Exalted", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragons-exalted", 1/72, 1/18, 1/36, 0, 98541, 1394),
    BWSet("Boundaries Crossed", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/boundaries-crossed", 1/72, 1/18, 1/36, 1/36, 98554, 1408),
    BWSet("Plasma Storm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-storm", 1/72, 1/18, 1/36, 1/36, 98526, 1413),
    BWSet("Plasma Freeze", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-freeze", 1/72, 1/18, 1/36, 1/36, 98517, 1382),
    BWSet("Plasma Blast", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-blast", 1/72, 1/18, 1/36, 1/36, 98573, 1370)
]

legendaryTreasuresUrl = "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures"
legendaryTreasuresRadiantUrl = "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures-radiant-collection"

xySetList = [
    XYSet("XY Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-base-set", 0, 1/18, 1/36, 0, 91602, 1387),
    XYSet("XY - Flashfire", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-flashfire", 1/72, 1/12, 1/18, 0, 91595, 1464),
    XYSet("XY - Furious Fists", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-furious-fists", 1/72, 1/12, 1/18, 0, 92169, 1481),
    XYSet("XY - Phantom Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-phantom-forces", 1/72, 1/9, 1/18, 0, 94622, 1494),
    XYSet("XY - Primal Clash", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-primal-clash", 1/72, 1/9, 1/18, 0, 97751, 1509),
    XYSet("XY - Roaring Skies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-roaring-skies", 1/72, 1/9, 1/18, 0, 129906, 1534),
    XYSet("XY - Ancient Origins", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-ancient-origins", 1/72, 1/6, 1/12, 0, 100490, 1576),
    XYSet("XY - BREAKthrough", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-breakthrough", 1/72, 1/6, 1/12, 1/12, 107666, 1661),
    XYSet("XY - BREAKpoint", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-breakpoint", 1/72, 1/6, 1/12, 1/12, 111279, 1701),
    XYSet("XY - Fates Collide", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-fates-collide", 1/72, 1/6, 1/12, 1/12, 168114, 1780),
    XYSet("XY - Steam Siege", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-steam-siege", 1/72, 1/6, 1/12, 1/12, 130013, 1815),
    XYSet("XY - Evolutions", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-evolutions", 0, 1/6, 1/12, 1/12, 129907, 1842)
]

smSetList = [
    SMSet("SM Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-base-set", .0277, 1/9, 1/24, 0, 0, 129385, 1863),
    SMSet("SM - Guardians Rising", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-guardians-rising", .0265, 1/9, 1/28, 0, 0, 129889, 1919),
    SMSet("SM - Burning Shadows", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-burning-shadows", .0276, 1/9, 1/25, 0, 0, 133774, 1957),
    SMSet("SM - Crimson Invasion", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-crimson-invasion", .0222, 1/12, 1/22, 0, 0, 146996, 2071),
    SMSet("SM - Ultra Prism", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-ultra-prism", .0254, 1/12, 1/22, 1/12, 0, 155662, 2178),
    SMSet("SM - Forbidden Light", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-forbidden-light", .0227, 1/12, 1/28, 1/12, 0, 164297, 2209),
    SMSet("SM - Celestial Storm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-celestial-storm", .0229, 1/9, 1/28, 1/18, 0, 170274, 2278),
    SMSet("SM - Lost Thunder", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-lost-thunder", .0255, 1/10, 1/22, 1/9, 0, 175510, 2328),
    SMSet("SM - Team Up", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-team-up", 0.0176, 1/10, 1/22, 1/18, 0, 181699, 2377),
    SMSet("SM - Unbroken Bonds", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-unbroken-bonds", .0228, 1/10, 1/22, 0, 0, 185718, 2420),
    SMSet("SM - Unified Minds", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-unified-minds", .0228, 1/8, 1/22, 0, 0, 191883, 2464),
    SMSet("SM - Cosmic Eclipse", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-cosmic-eclipse", 0.02861, 1/9, 1/27, 0, 1/9, 199263, 2534)
]

swshSetList = [
    SWSHSet("SWSH01: Sword & Shield Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh01-sword-and-shield-base-set", 0.0237, 1/7, 1/45, 1/27, 0, 0, 206028, 2585),
    SWSHSet("SWSH02: Rebel Clash", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh02-rebel-clash", 0.0263, 1/8, 1/30, 1/27, 0, 0, 210562, 2626),
    SWSHSet("SWSH03: Darkness Ablaze", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh03-darkness-ablaze", 0.0239, 1/8, 1/26, 1/27, 0, 0, 216852, 2675),
    SWSHSet("SWSH04: Vivid Voltage", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh04-vivid-voltage", 0.0452, 1/8, 1/24, 1/24, 1/20, 0, 221312, 2701),
    SWSHSet("SWSH05: Battle Styles", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh05-battle-styles", 0.0187, 1/8, 1/24, 1/48 + 1/94, 0, 1/201 + 1/703, 229276, 2765),
    SWSHSet("SWSH06: Chilling Reign", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh06-chilling-reign", 0.0196, 1/8, 1/24, 1/49 + 1/78, 0, 1/147 + 1/454, 236257, 2807),
    SWSHSet("SWSH07: Evolving Skies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh07-evolving-skies", 0.0225, 1/8, 1/18, 1/197 + 1/56, 0, 1/82 + 1/283, 244337, 2848),
    SWSHSet("SWSH08: Fusion Strike", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh08-fusion-strike", 0.0160, 1/8, 1/30, 1/64 + 1/58, 0, 1/180 + 1/332, 247646, 2906),
]

lateSwshSetList = [
    lateSWSHSet("SWSH09: Brilliant Stars", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh09-brilliant-stars", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh09-brilliant-stars-trainer-gallery", .264, .0191, 1/7, 1/96, 1/43, 1/30, 1/127, 0.1944, 0, 256124, 2948, 3020 ),
    lateSWSHSet("SWSH10: Astral Radiance", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh10-astral-radiance", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh10-astral-radiance-trainer-gallery", .255, .0141, .1512, .0081, .0026, .0537, 1/135, .125, .0488, 265521, 3040, 3068),
    lateSWSHSet("SWSH11: Lost Origin", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh11-lost-origin", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh11-lost-origin-trainer-gallery", .265, .0316, .1309, .0167, .0418, .046, 14/2211, .1146, .0404, 277325, 3118, 3172),
    lateSWSHSet("SWSH12: Silver Tempest", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh12-silver-tempest", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh12-silver-tempest-trainer-gallery", .254, .0287, .1295, .0167, .0279, .0599, 1/684+1/636+1/636+1/741, .1146, .0557, 283388, 3170, 17674),
]

svSetList = [
    svSet("SV01: Scarlet & Violet Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv01-scarlet-and-violet-base-set", .0185, .1428, .0666, .0769, .03125, 0, 476451, 22873 ),
    svSet("SV02: Paldea Evolved", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv02-paldea-evolved", .0175, .1428, .0666, .0769, .03125, 0, 493976, 23120 ),
    svSet("SV03: Obsidian Flames", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv03-obsidian-flames", .0192, .1428, .0666, .0769, .03125, 0, 501256, 23228 ),
    svSet("SV04: Paradox Rift", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv04-paradox-rift", .0121, .1666, .0666, .0769, .0212, 0, 512822, 23286 ),
    svSet("SV05: Temporal Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv05-temporal-forces", .0071, .1666, .0666, .0769, .0116, .05, 532841, 23381 ),
    svSet("SV06: Twilight Masquerade", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv06-twilight-masquerade", .0175, .1666, .0666, .0769, .0116, .05, 543843, 23473 ),
    svSet("SV07: Stellar Crown", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv07-stellar-crown", .0192, .1666, .0666, .0769, .0111, .05, 557331, 23537 ),
    svSet("SV08: Surging Sparks", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv08-surging-sparks", .0121, .1666, .0666, .0769, .0114, .05, 565604, 23651 ),
    svSet("SV09: Journey Together", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv09-journey-together", .0072, .2, .0667, .0833, .0116, 0, 610935, 24073),
    svSet("SV10: Destined Rivals", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv10-destined-rivals", .0067, .2, .0625, .0833, .0106, 0, 624683, 24269),
    svSet("ME01: Mega Evolution", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/me01-mega-evolution", .0008, .2, .0833, .1111, .0099, 0, 644352, 24380),
    svSet("ME02: Phantasmal Flames", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/me02-phantasmal-flames", .0008, .2, .0833, .1111, .0099, 0, 654144, 24448)

]

# Load previous data if available
previous_data = []
if os.path.exists('full_output_with_all_columns.json'):
    with open('full_output_with_all_columns.json', 'r') as f:
        previous_data = json.load(f)

# Load previous data if available
previous_box_data = []
if os.path.exists('boxData.json'):
    with open('boxData.json', 'r') as g:
        previous_box_data = json.load(g)

# Function to get last Pack Value by Set Name
def get_last_pack_value(set_name):
    for entry in reversed(previous_data):
        if entry.get("Set Name") == set_name:
            return entry.get("Pack Value")

def get_last_box_value(set_name):
    for entry in reversed(previous_box_data):
        if entry.get("Set Name") == set_name:
            return entry.get("Box Price")

def findSet(name, list):
    for set in list:
        if set.name == name:
            return set
    return None


def getBoxPrices(boxSet):

    response = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{boxSet.productId}/details?mpfev=3442")   
    data = response.json() 
    
    price = data.get("marketPrice") or data.get("medianPrice") or data.get("lowestPrice") or get_last_box_value(boxSet.name)
    pricePer = float(price/36)

    print("\n")
    print("Set Name: " + boxSet.name)
    print("Box Price: $" + str(price))
    print(f"Price Per Pack: ${pricePer:.2f}")

    return price, round(pricePer, 2), boxSet.name, boxSet.setNumber

def gen1Calculate(set):

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

    # Make the GET request
    response = requests.get(f"https://infinite-api.tcgplayer.com/priceguide/set/{set.tcgId}/cards/?rows=5000&productTypeID=1")    
    data = response.json() 

    for item in data.get("result", []):  
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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)

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

    return (expValue / (packPrice)), packPrice, expValue

def earlyReverseSets(set):
    
    #need some variables for a couple special sets still
    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    totalReverseValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0

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
                    "marketPrice": marketPrice
                }

        # Check if this is the best condition Holofoil for this productID
        elif is_holofoil:
            if (best_cards[product_id]["holofoil"] is None or
                    holo_condition_priority.index(condition) < holo_condition_priority.index(best_cards[product_id]["holofoil"]["condition"])):
                best_cards[product_id]["holofoil"] = {
                    "condition": condition,
                    "rarity": rarity,
                    "marketPrice": marketPrice
                }

        # Check if this is the best condition Normal for this productID
        elif is_normal:
            if (best_cards[product_id]["normal"] is None or
                    condition_priority.index(condition) < condition_priority.index(best_cards[product_id]["normal"]["condition"])):
                best_cards[product_id]["normal"] = {
                    "condition": condition,
                    "rarity": rarity,
                    "marketPrice": marketPrice
                }

    # Now, process the best available cards
    for product in best_cards.values():
        # Process Normal if it exists
        if product["normal"]:
            rarity = product["normal"]["rarity"]
            marketPrice = product["normal"]["marketPrice"]

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

            if rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice

        # Process Reverse Holo if it exists
        if product["reverse"]:
            reverseCount += 1
            totalReverseValue += product["reverse"]["marketPrice"]
       

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)


    expValue = 0
    if(secretCount > 0):
        expValue += (totalSecretValue / secretCount * set.secretOdds)
    expValue += ((totalCommonValue / commonCount * set.commonsPer) + (totalUncommonValue / uncommonCount * set.uncommonsPer) + (totalRareValue / rareCount * .66) + (totalHoloValue / holoCount * set.holoOdds) + (totalReverseValue / reverseCount)) 

    print("\n")
    print(set.name)
    print("Total Cards: " + str(totalCards))
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Reverses: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")

    return (expValue / (packPrice)), packPrice, expValue

def earlyExSets(set):

    #need some variables for a couple special sets still
    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    totalReverseValue = 0
    totalUltraRareValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    ultraRareCount = 0

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
                    "marketPrice": marketPrice
                }

        # Check if this is the best condition Holofoil for this productID
        elif is_holofoil:
            if (best_cards[product_id]["holofoil"] is None or
                    holo_condition_priority.index(condition) < holo_condition_priority.index(best_cards[product_id]["holofoil"]["condition"])):
                best_cards[product_id]["holofoil"] = {
                    "condition": condition,
                    "rarity": rarity,
                    "marketPrice": marketPrice
                }

        # Check if this is the best condition Normal for this productID
        elif is_normal:
            if (best_cards[product_id]["normal"] is None or
                    condition_priority.index(condition) < condition_priority.index(best_cards[product_id]["normal"]["condition"])):
                best_cards[product_id]["normal"] = {
                    "condition": condition,
                    "rarity": rarity,
                    "marketPrice": marketPrice
                }

    # Now, process the best available cards
    for product in best_cards.values():
        # Process Normal if it exists
        if product["normal"]:
            rarity = product["normal"]["rarity"]
            marketPrice = product["normal"]["marketPrice"]

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

            if rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
            elif rarity == "Ultra Rare":
                ultraRareCount += 1
                totalUltraRareValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                totalCards += 1

        # Process Reverse Holo if it exists
        if product["reverse"]:
            reverseCount += 1
            totalReverseValue += product["reverse"]["marketPrice"]

    commonQuantity = 5
    uncommonQuantity = 2

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)

    expValue = 0
    if(set.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * set.secretOdds)

    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * .66)
    expValue += (totalHoloValue / holoCount * set.holoOdds)
    expValue += (totalUltraRareValue / ultraRareCount * set.ultraOdds)
    expValue += (totalReverseValue / reverseCount)

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
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")

    return (expValue / (packPrice)), packPrice, expValue

def goldStarSets(set):

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

        # Process Holofoil if it exists
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

        # Process Reverse Holo if it exists
        if product["reverse"]:
            reverseCount += 1
            totalReverseValue += product["reverse"]["marketPrice"]

    commonQuantity = 5
    uncommonQuantity = 2

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)


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

    return (expValue / (packPrice)), packPrice, expValue

def dpSets(set):

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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)


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

    return (expValue / (packPrice)), packPrice, expValue

def hgssSets(set):

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    totalReverseValue = 0
    totalPrimeValue = 0
    totalShinyValue = 0
    totalLegendValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    primeCount = 0
    shinyCount = 0
    legendCount = 0

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
                reverseCount += 1
                totalReverseValue += marketPrice
            elif number == "SL1" or number == "SL2" or number == "SL3" or number == "SL4" or number == "SL5" or number == "SL6" or number == "SL7" or number == "SL8" or number == "SL9" or number == "SL10" or number == "SL11":
                shinyCount += 1
                totalShinyValue += marketPrice
            elif number == "ONE" or number == "TWO" or number == "THREE" or number == "FOUR":
                secretCount += 1
                totalSecretValue += marketPrice
            elif "(TOP)" in name.upper() or "(BOTTOM)" in name.upper():
                legendCount += 1
                totalLegendValue += marketPrice
            elif "(Prime)" in name:
                primeCount += 1
                totalPrimeValue += marketPrice
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
    if(set.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * set.secretOdds)
    if(set.shinyOdds > 0):
        expValue += (totalShinyValue /max(shinyCount, 1) * set.shinyOdds)
    if(set.primeOdds > 0):
        expValue += (totalPrimeValue /primeCount * set.primeOdds)
    if(set.legendOdds > 0):
        expValue += (totalLegendValue /max(legendCount, 1) * set.legendOdds)

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
    print("Primes: " + str(primeCount) + ", Value: $" + f"{totalPrimeValue:.2f}")
    print("Reverses: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Shinies: " + str(shinyCount) + ", Value: $" + f"{totalShinyValue:.2f}")
    print("Legends: " + str(legendCount) + ", Value: $" + f"{totalLegendValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice ):.2f}")

    return (expValue / (packPrice )), packPrice, expValue

def bwSets(set):

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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)

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

    return (expValue / (packPrice)), packPrice, expValue

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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/98581/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)

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

    return (expValue / (packPrice )), packPrice, expValue

def xySets(set):

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    totalReverseValue = 0
    totalExValue = 0
    totalFaValue = 0
    totalBreakValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    exCount = 0
    faCount = 0
    breakCount = 0
    codeCardCount = 0

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
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
            if(rarity != "Code Card" and rarity != "Promo"):
                totalCards += 1

        # Process Holofoil if it exists
        if product["holofoil"]:
            rarity = product["holofoil"]["rarity"]
            marketPrice = product["holofoil"]["marketPrice"]
            name = product["holofoil"]["productName"]
            number = product["holofoil"]["number"]
            setName = product["holofoil"]["setName"]

            if name == "Chesnaught BREAK":
                breakCount += 1
                totalBreakValue += marketPrice
            elif name == "Skyla" and setName == "XY - BREAKpoint":
                faCount += 1
                totalFaValue += marketPrice
            elif name == "Professor Sycamore" and setName == "XY - Steam Siege":
                faCount += 1
                totalFaValue += marketPrice
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += marketPrice
            elif rarity == "Rare BREAK":
                breakCount += 1
                totalBreakValue += marketPrice
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



    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)


    commonQuantity = 5
    uncommonQuantity = 3
    rareOdds = 1 - set.exOdds - set.faOdds - set.holoOdds - set.secretOdds

    expValue = 0
    if(set.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * set.secretOdds)
    if(set.breakOdds > 0):
        expValue += (totalBreakValue /max(breakCount, 1) * set.breakOdds)

    expValue += (totalFaValue /max(faCount, 1) * set.faOdds)
    expValue += (totalExValue /exCount * set.exOdds)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    if(set.name == "XY - Evolutions"):
        expValue += ((totalUncommonValue + totalSecretValue) / (uncommonCount + secretCount) * uncommonQuantity)
    else:
        expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * rareOdds)
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
    print("Breaks: " + str(breakCount) + ", Value: $" + f"{totalBreakValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")

    return (expValue / (packPrice)), packPrice, expValue

def smSets(set):

    totalCards = 0
    totalCommonValue = 0
    totalUncommonValue = 0
    totalRareValue = 0
    totalHoloValue = 0
    totalSecretValue = 0
    totalReverseValue = 0
    totalGxValue = 0
    totalFaValue = 0
    totalPrismValue = 0
    totalGalleryValue = 0

    commonCount = 0
    uncommonCount = 0
    rareCount = 0
    holoCount = 0
    secretCount = 0
    reverseCount = 0
    gxCount = 0
    faCount = 0
    codeCardCount = 0
    prismCount = 0
    galleryCount = 0


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
            elif rarity == "Prism Rare":
                prismCount += 1
                totalPrismValue += marketPrice
            elif setName == "SM - Cosmic Eclipse" and (number == "237/236" or number == "238/236" or number == "239/236" or number == "240/236" or number == "241/236" or number == "242/236" or number == "243/236" or number == "244/236" or number == "245/236" or number == "246/236" or number == "247/236" or number == "248/236"):
                galleryCount += 1
                totalGalleryValue += marketPrice
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += marketPrice
            elif "Full Art" in name:
                faCount += 1
                totalFaValue += marketPrice
            elif "GX" in name:
                gxCount += 1
                totalGxValue += marketPrice
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

    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
    if(set.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * set.secretOdds)
    if(set.prismOdds > 0):
        expValue += (totalPrismValue /max(prismCount, 1) * set.prismOdds)
    if(set.galleryOdds > 0):
        expValue += (totalGalleryValue /max(galleryCount, 1) * set.galleryOdds)

    expValue += (totalFaValue /faCount * set.faOdds)
    expValue += (totalGxValue /gxCount * set.gxOdds)
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
    print("GXs: " + str(gxCount) + ", Value: $" + f"{totalGxValue:.2f}")
    print("Reverses: " + str(reverseCount) + ", Value: $" + f"{totalReverseValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Full Arts: " + str(faCount) + ", Value: $" + f"{totalFaValue:.2f}")
    print("Prisms: " + str(prismCount) + ", Value: $" + f"{totalPrismValue:.2f}")
    print("Gallery Cards: " + str(galleryCount) + ", Value: $" + f"{totalGalleryValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")

    return (expValue / (packPrice)), packPrice, expValue

def swshSets(set):

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

    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)


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

    return (expValue / (packPrice )), packPrice, expValue

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

    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)

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

    return (expValue / (packPrice )), packPrice, expValue

def svsets(set):

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


    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/{set.productId}/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(set.name)

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

    return (expValue / (packPrice )), packPrice, expValue

def dragonVault():

    totalCards = 0
    totalHoloValue = 0
    totalSecretRareValue = 0

    holoCount = 0
    secretRareCount = 0

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


    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/98948/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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


    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/229226/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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
    

    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/155880/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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
    
    
    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/173392/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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
    
    
    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/218789/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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

    
    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/274421/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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

    
    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/504467/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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

    
    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/552997/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)


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

    return (expValue / (packPrice )), packPrice, expValue

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

    
    packResponse = requests.get("https://mp-search-api.tcgplayer.com/v2/product/528038/details?mpfev=3442")   
    packData = packResponse.json() 
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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


    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/198634/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue


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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/232636/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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


    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/187238/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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


    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/453466/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

def celebrations():

    totalCards = 0
    totalHoloValue = 0
    totalUltraValue = 0
    totalSecretValue = 0
    blastoise = charizard = claydol = cleffa = gyarados = donphan = garchomp = gardevoir = teamRocket = imposter = luxray = rayquaza = mew = mewtwo = reshiram = admin = zapdos = magikarp = tapulele = groudon = umbreon = venusaur = zekrom = xerneas = pikachu = 0

    holoCount = 0
    ultraCount = 0
    secretCount = 0


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

    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/248577/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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

    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/593294/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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

    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/642597/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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

    
    packResponse = requests.get(f"https://mp-search-api.tcgplayer.com/v2/product/630699/details?mpfev=3442")   
    packData = packResponse.json() 
    
    packPrice = packData.get("marketPrice") or packData.get("medianPrice") or packData.get("lowestPrice") or get_last_pack_value(setName)

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

    return (expValue / (packPrice )), packPrice, expValue

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

def getSetName(set):
    return set.name

num = 0

for set in vintageSetList:
    adjev, price, ev = gen1Calculate(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(100 + num)
    num += 1

num = 0


for set in earlyReverseSetList:
    adjev, price, ev = earlyReverseSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(200 + num)
    num += 1

num = 0

for set in earlyExSetList:
    adjev, price, ev = earlyExSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(300 + num)
    num += 1

num = 0

for set in goldStarSetList:
    adjev, price, ev = goldStarSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(400 + num)
    num += 1

num = 0

for set in levelXSetList:
    adjev, price, ev = dpSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(500 + num)
    num += 1

num = 0

for set in hgssSetList:
    adjev, price, ev = hgssSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(600 + num)
    num += 1

num = 0

for set in bwSetList:
    adjev, price, ev = bwSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(700 + num)
    num += 1   

adjev, price, ev = legendaryTreasures()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Legendary Treasures")
actualEvList.append(ev)
setNumberList.append(710)

num = 0

for set in xySetList:
    adjev, price, ev = xySets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(800 + num)
    num += 1

num = 0

for set in smSetList:
    adjev, price, ev = smSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(900 + num)
    num += 1

num = 0

for set in swshSetList:
    adjev, price, ev = swshSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(1000 + num)
    num += 1

num = 0

for set in lateSwshSetList:
    adjev, price, ev = lateSwshSets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(1100 + num)
    num += 1

num = 0

for set in svSetList:
    adjev, price, ev = svsets(set)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(1200 + num)
    num += 1

adjev, price, ev = dragonVault()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Dragon Vault")
actualEvList.append(ev)
setNumberList.append(705.5)

adjev, price, ev = doubleCrisis()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Double Crisis")
actualEvList.append(ev)
setNumberList.append(804.5)

adjev, price, ev = shiningLegends()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Shining Legends")
actualEvList.append(ev)
setNumberList.append(902.5)

adjev, price, ev = dragonMajesty()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Dragon Majesty")
actualEvList.append(ev)
setNumberList.append(906.5)

adjev, price, ev = championsPath()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Champions Path")
actualEvList.append(ev)
setNumberList.append(1002.5)

adjev, price, ev = pokemonGo()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Pokemon Go")
actualEvList.append(ev)
setNumberList.append(1101.5)

adjev, price, ev = pokemon151()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Pokemon 151")
actualEvList.append(ev)
setNumberList.append(1202.5) 

adjev, price, ev = paldeanFates()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Paldean Fates")
actualEvList.append(ev)
setNumberList.append(1203.5) 

adjev, price, ev = shroudedFable()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Shrouded Fable")
actualEvList.append(ev)
setNumberList.append(1205.5) 

adjev, price, ev = hiddenFates()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Hidden Fates")
actualEvList.append(ev)
setNumberList.append(910.5) 

adjev, price, ev = shiningFates()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Shining Fates")
actualEvList.append(ev)
setNumberList.append(1003.5) 

adjev, price, ev = generations()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Generations")
actualEvList.append(ev)
setNumberList.append(808.5)

adjev, price, ev = crownZenith()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Crown Zenith")
actualEvList.append(ev)
setNumberList.append(1103.5)

adjev, price, ev = celebrations()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Celebrations")
actualEvList.append(ev)
setNumberList.append(1006.5) 

adjev, price, ev = prismaticEvolutions()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Prismatic Evolutions")
actualEvList.append(ev)
setNumberList.append(1207.5) 

adjev, price, ev = blackBolt()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("Black Bolt")
actualEvList.append(ev)
setNumberList.append(1209.51) 

adjev, price, ev = whiteFlare()
expectedValueList.append(adjev)
packValueList.append(price)
setNameList.append("White Flare")
actualEvList.append(ev)
setNumberList.append(1209.52)

for bb in boosterBoxList:
    boxPrice, boxPricePer, setName, setNumber = getBoxPrices(bb)
    boxPriceList.append(boxPrice)
    boxPricePerList.append(boxPricePer)
    boxSetNameList.append(setName)
    boxSetNumberList.append(setNumber)


last_updated_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#need to fix loading for all functions?
print("\n")


#excel sheet stuff below
#-----------------------

# Prepare the data to be written into JSON format
output_data = []
for i in range(len(setNameList)):
    output_data.append({
        "Set Name": setNameList[i],
        "Adj. EV": expectedValueList[i],
        "Pack Value": packValueList[i],
        "EV": actualEvList[i],
        "Last Updated": last_updated_timestamp,
        "SetNumber": setNumberList[i]
    })

# Write the output data to a JSON file
with open('full_output_with_all_columns.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

# Optionally, print the JSON to the console for verification
print(json.dumps(output_data, indent=4))

#Booster Box JSON

boxOutput_data = []
for i in range(len(boxSetNameList)):
    boxOutput_data.append({
        "Set Name": boxSetNameList[i],
        "Box Price": boxPriceList[i],
        "Price Per": boxPricePerList[i],
        "Last Updated": last_updated_timestamp,
        "Set Number": boxSetNumberList[i]
    })

# Write the output data to a JSON file
with open('boxData.json', 'w') as json_file:
    json.dump(boxOutput_data, json_file, indent=4)

# Optionally, print the JSON to the console for verification
print(json.dumps(boxOutput_data, indent=4))