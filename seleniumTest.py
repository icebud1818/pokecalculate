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
    def __init__(self, name, url, secretOdds, commonsPer, productId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.commonsPer = commonsPer 
        self.holoOdds = .33 - self.secretOdds
        self.productId = productId

class EarlyReverseSet:
    def __init__(self, name, url, secretOdds, commonsPer, uncommonsPer, productId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.commonsPer = commonsPer 
        self.uncommonsPer = uncommonsPer
        self.holoOdds = .33 - self.secretOdds
        self.productId = productId

class EarlyExSet:
    def __init__(self, name, url, secretOdds, ultraOdds, productId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds
        self.productId = productId

class GoldStarSet:
    def __init__(self, name, url, secretOdds, ultraOdds, goldStarOdds, productId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.goldStarOdds = goldStarOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds - self.goldStarOdds
        self.productId = productId

class LevelXSet:
    def __init__(self, name, url, secretOdds, ultraOdds, shinyOdds, rotomOdds, arceusOdds, productId):
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

class HgssSet:
    def __init__(self, name, url, secretOdds, primeOdds, legendOdds, shinyOdds, productId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.primeOdds = primeOdds
        self.legendOdds = legendOdds
        self.shinyOdds = shinyOdds
        self.reverseOdds = 1 - self.primeOdds - self.shinyOdds
        self.holoOdds = .33 - self.secretOdds - self.legendOdds
        self.productId = productId

class BWSet:
    def __init__(self, name, url, secretOdds, exOdds, faOdds, aceOdds, productId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.exOdds = exOdds
        self.faOdds = faOdds
        self.aceOdds = aceOdds
        self.reverseOdds = 1 - self.aceOdds
        self.holoOdds = .33 - self.secretOdds - self.exOdds - self.faOdds
        self.productId = productId

class XYSet:
    def __init__(self, name, url, secretOdds, exOdds, faOdds, breakOdds, productId):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.exOdds = exOdds
        self.faOdds = faOdds
        self.breakOdds = breakOdds
        self.reverseOdds = 1 - self.breakOdds
        self.holoOdds = (1/6)
        self.productId = productId

class SMSet:
    def __init__(self, name, url, secretOdds, gxOdds, faOdds, prismOdds, galleryOdds, productId):
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

class SWSHSet:
    def __init__(self, name, url, secretOdds, vOdds, vmaxOdds, faOdds, arOdds, altOdds, productId):
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

class lateSWSHSet:
    def __init__(self, name, url, url2, holoOdds, secretOdds, vOdds, vmaxOdds, vstarOdds, faOdds, altOdds, tgOdds, radiantOdds, productId):
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

class svSet:
    def __init__(self, name, url, hyperOdds, doubleOdds, ultraOdds, irOdds, sirOdds, aceOdds, productId):
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
    BoosterBox("Surging Sparks", 1207, 565606)
]

vintageSetList = [
    VintageSet("Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/base-set", 0, 5, 138130),
    VintageSet("Jungle", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/jungle", 0, 7, 138129),
    VintageSet("Fossil", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/fossil", 0, 7, 138134),
    VintageSet("Base Set 2", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/base-set-2", 0, 7, 138149),
    VintageSet("Team Rocket", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-rocket", 1/81, 7, 138135),
    VintageSet("Gym Heroes", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/gym-heroes", 0, 7, 138138),
    VintageSet("Gym Challenge", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/gym-challenge", 0, 7, 138139),
    VintageSet("Neo Genesis", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-genesis", 0, 7, 138142),
    VintageSet("Neo Discovery", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-discovery", 0, 7, 138143),
    VintageSet("Neo Revelation", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-revelation", 1/18, 7, 138146),
    VintageSet("Neo Destiny", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-destiny", 1/12, 7, 138147)
]

earlyReverseSetList = [
    EarlyReverseSet("Legendary Collection", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-collection", 0, 6, 3, 138150),
    EarlyReverseSet("Expedition", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/expedition", 0, 5, 2, 138151),
    EarlyReverseSet("Aquapolis", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/aquapolis", 1/36, 5, 2, 138152),
    EarlyReverseSet("Skyridge", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/skyridge", 1/15, 5, 2, 138153)
]

earlyExSetList = [
    EarlyExSet("Ruby and Sapphire", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/ruby-and-sapphire", 0, 1/15, 98558),
    EarlyExSet("Sandstorm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sandstorm", 0, 1/15, 98565),
    EarlyExSet("Dragon", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon", 1/36, 1/15, 98519),
    EarlyExSet("Team Magma vs Team Aqua", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-magma-vs-team-aqua", 1/36, 1/15, 98550),
    EarlyExSet("Hidden Legends", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/hidden-legends", 0, 1/15, 98595),
    EarlyExSet("FireRed & LeafGreen", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/firered-and-leafgreen", 1/36, 1/15, 98946),
    EarlyExSet("Emerald", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/emerald", 0, 1/15, 98546)
]

goldStarSetList = [
    GoldStarSet("Team Rocket Returns", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-rocket-returns", 1/36, 1/15, 1/72, 98578),
    GoldStarSet("Deoxys", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/deoxys", 0, 1/15, 1/72, 98562),
    GoldStarSet("Unseen Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/unseen-forces", 1/36, 1/15, 1/72, 98577),
    GoldStarSet("Delta Species", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/delta-species", 0, 1/15, 1/72, 98944),
    GoldStarSet("Legend Maker", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legend-maker", 0, 1/15, 1/72, 98557),
    GoldStarSet("Holon Phantoms", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/holon-phantoms", 0, 1/36, 1/72, 98522),
    GoldStarSet("Crystal Guardians", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/crystal-guardians", 0, 1/15, 1/72, 98566),
    GoldStarSet("Dragon Frontiers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon-frontiers", 0, 1/15, 1/72, 98533),
    GoldStarSet("Power Keepers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/power-keepers", 0, 1/10, 1/54, 98529)
]

levelXSetList = [
    LevelXSet("Diamond and Pearl", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/diamond-and-pearl", 0, 1/36, 0, 0, 0, 98525),
    LevelXSet("Mysterious Treasures", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/mysterious-treasures", 1/72, 1/36, 0, 0, 0, 98561),
    LevelXSet("Secret Wonders", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/secret-wonders", 0, 1/36, 0, 0, 0, 98569),
    LevelXSet("Great Encounters", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/great-encounters", 0, 1/36, 0, 0, 0, 98545),
    LevelXSet("Majestic Dawn", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/majestic-dawn", 0, 1/36, 0, 0, 0, 98585),
    LevelXSet("Legends Awakened", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legends-awakened", 0, 1/12, 0, 0, 0, 98537),
    LevelXSet("Stormfront", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/stormfront", 1/36, 1/12, 1/36, 0, 0, 98589),
    LevelXSet("Platinum", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/platinum", 1/36, 1/12, 1/36, 0, 0, 98591),
    LevelXSet("Rising Rivals", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/rising-rivals", 1/36, 1/12, 0, 1/18, 0, 98542),
    LevelXSet("Supreme Victors", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/supreme-victors", 1/36, 1/12, 1/36, 0, 0, 98574),
    LevelXSet("Arceus", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/arceus", 0, 1/12, 1/36, 0, 1/4, 98594)
]

hgssSetList = [
    HgssSet("HeartGold SoulSilver", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/heartgold-soulsilver", 1/108, 1/6, 1/12, 0, 98530),
    HgssSet("Unleashed", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/unleashed", 1/108, 1/7, 1/12, 0, 98582),
    HgssSet("Undaunted", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/undaunted", 1/108, 1/7, 1/12, 0, 98586),
    HgssSet("Triumphant", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/triumphant", 1/108, 1/7, 1/12, 0, 98534),
    HgssSet("Call of Legends", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/call-of-legends", 0, 0, 0, 1/18, 98515)
]

bwSetList = [
    BWSet("Black and White", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/black-and-white", 1/72, 0, 1/36, 0, 98553),
    BWSet("Emerging Powers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/emerging-powers", 0, 0, 1/36, 0, 98549),
    BWSet("Noble Victories", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/noble-victories", 1/72, 0, 1/18, 0, 98570),
    BWSet("Next Destinies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/next-destinies", 1/72, 1/18, 1/36, 0, 98538),
    BWSet("Dark Explorers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dark-explorers", 1/72, 1/18, 1/36, 0, 98521),
    BWSet("Dragons Exalted", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragons-exalted", 1/72, 1/18, 1/36, 0, 98541),
    BWSet("Boundaries Crossed", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/boundaries-crossed", 1/72, 1/18, 1/36, 1/36, 98554),
    BWSet("Plasma Storm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-storm", 1/72, 1/18, 1/36, 1/36, 98526),
    BWSet("Plasma Freeze", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-freeze", 1/72, 1/18, 1/36, 1/36, 98517),
    BWSet("Plasma Blast", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-blast", 1/72, 1/18, 1/36, 1/36, 98573)
]

legendaryTreasuresUrl = "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures"
legendaryTreasuresRadiantUrl = "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures-radiant-collection"

xySetList = [
    XYSet("XY Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-base-set", 0, 1/18, 1/36, 0, 91602),
    XYSet("XY - Flashfire", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-flashfire", 1/72, 1/12, 1/18, 0, 91595),
    XYSet("XY - Furious Fists", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-furious-fists", 1/72, 1/12, 1/18, 0, 92169),
    XYSet("XY - Phantom Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-phantom-forces", 1/72, 1/9, 1/18, 0, 94622),
    XYSet("XY - Primal Clash", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-primal-clash", 1/72, 1/9, 1/18, 0, 97751),
    XYSet("XY - Roaring Skies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-roaring-skies", 1/72, 1/9, 1/18, 0, 129906),
    XYSet("XY - Ancient Origins", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-ancient-origins", 1/72, 1/6, 1/12, 0, 100490),
    XYSet("XY - BREAKthrough", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-breakthrough", 1/72, 1/6, 1/12, 1/12, 107666),
    XYSet("XY - BREAKpoint", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-breakpoint", 1/72, 1/6, 1/12, 1/12, 111279),
    XYSet("XY - Fates Collide", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-fates-collide", 1/72, 1/6, 1/12, 1/12, 168114),
    XYSet("XY - Steam Siege", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-steam-siege", 1/72, 1/6, 1/12, 1/12, 130013),
    XYSet("XY - Evolutions", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-evolutions", 0, 1/6, 1/12, 1/12, 129907)
]

smSetList = [
    SMSet("SM Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-base-set", .0277, 1/9, 1/24, 0, 0, 129385),
    SMSet("SM - Guardians Rising", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-guardians-rising", .0265, 1/9, 1/28, 0, 0, 129889),
    SMSet("SM - Burning Shadows", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-burning-shadows", .0276, 1/9, 1/25, 0, 0, 133774),
    SMSet("SM - Crimson Invasion", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-crimson-invasion", .0222, 1/12, 1/22, 0, 0, 146996),
    SMSet("SM - Ultra Prism", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-ultra-prism", .0254, 1/12, 1/22, 1/12, 0, 155662),
    SMSet("SM - Forbidden Light", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-forbidden-light", .0227, 1/12, 1/28, 1/12, 0, 164297),
    SMSet("SM - Celestial Storm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-celestial-storm", .0229, 1/9, 1/28, 1/18, 0, 170274),
    SMSet("SM - Lost Thunder", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-lost-thunder", .0255, 1/10, 1/22, 1/9, 0, 175510),
    SMSet("SM - Team Up", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-team-up", 0.0176, 1/10, 1/22, 1/18, 0, 181699),
    SMSet("SM - Unbroken Bonds", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-unbroken-bonds", .0228, 1/10, 1/22, 0, 0, 185718),
    SMSet("SM - Unified Minds", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-unified-minds", .0228, 1/8, 1/22, 0, 0, 191883),
    SMSet("SM - Cosmic Eclipse", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-cosmic-eclipse", 0.02861, 1/9, 1/27, 0, 1/9, 199263)
]

swshSetList = [
    SWSHSet("SWSH01: Sword & Shield Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh01-sword-and-shield-base-set", 0.0237, 1/7, 1/45, 1/27, 0, 0, 206028),
    SWSHSet("SWSH02: Rebel Clash", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh02-rebel-clash", 0.0263, 1/8, 1/30, 1/27, 0, 0, 210562),
    SWSHSet("SWSH03: Darkness Ablaze", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh03-darkness-ablaze", 0.0239, 1/8, 1/26, 1/27, 0, 0, 216852),
    SWSHSet("SWSH04: Vivid Voltage", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh04-vivid-voltage", 0.0452, 1/8, 1/24, 1/24, 1/20, 0, 221312),
    SWSHSet("SWSH05: Battle Styles", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh05-battle-styles", 0.0187, 1/8, 1/24, 1/48 + 1/94, 0, 1/201 + 1/703, 229276),
    SWSHSet("SWSH06: Chilling Reign", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh06-chilling-reign", 0.0196, 1/8, 1/24, 1/49 + 1/78, 0, 1/147 + 1/454, 236257),
    SWSHSet("SWSH07: Evolving Skies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh07-evolving-skies", 0.0225, 1/8, 1/18, 1/197 + 1/56, 0, 1/82 + 1/283, 244337),
    SWSHSet("SWSH08: Fusion Strike", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh08-fusion-strike", 0.0160, 1/8, 1/30, 1/64 + 1/58, 0, 1/180 + 1/332, 247646),
]

lateSwshSetList = [
    lateSWSHSet("SWSH09: Brilliant Stars", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh09-brilliant-stars", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh09-brilliant-stars-trainer-gallery", .264, .0191, 1/7, 1/96, 1/43, 1/30, 1/127, 0.1944, 0, 256124 ),
    lateSWSHSet("SWSH10: Astral Radiance", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh10-astral-radiance", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh10-astral-radiance-trainer-gallery", .255, .0141, .1512, .0081, .0026, .0537, 1/135, .125, .0488, 265521),
    lateSWSHSet("SWSH11: Lost Origin", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh11-lost-origin", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh11-lost-origin-trainer-gallery", .265, .0316, .1309, .0167, .0418, .046, 14/2211, .1146, .0404, 277325),
    lateSWSHSet("SWSH12: Silver Tempest", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh12-silver-tempest", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh12-silver-tempest-trainer-gallery", .254, .0287, .1295, .0167, .0279, .0599, 1/684+1/636+1/636+1/741, .1146, .0557, 283388),
]

svSetList = [
    svSet("SV01: Scarlet & Violet Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv01-scarlet-and-violet-base-set", .0185, .1428, .0666, .0769, .03125, 0, 476451 ),
    svSet("SV02: Paldea Evolved", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv02-paldea-evolved", .0175, .1428, .0666, .0769, .03125, 0, 493976 ),
    svSet("SV03: Obsidian Flames", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv03-obsidian-flames", .0192, .1428, .0666, .0769, .03125, 0, 501256 ),
    svSet("SV04: Paradox Rift", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv04-paradox-rift", .0121, .1666, .0666, .0769, .0212, 0, 512822 ),
    svSet("SV05: Temporal Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv05-temporal-forces", .0071, .1666, .0666, .0769, .0116, .05, 532841 ),
    svSet("SV06: Twilight Masquerade", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv06-twilight-masquerade", .0175, .1666, .0666, .0769, .0116, .05, 543843 ),
    svSet("SV07: Stellar Crown", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv07-stellar-crown", .0192, .1666, .0666, .0769, .0111, .05, 557331 ),
    svSet("SV08: Surging Sparks", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv08-surging-sparks", .0121, .1666, .0666, .0769, .0114, .05, 565604 ),
]

def findSet(name, list):
    for set in list:
        if set.name == name:
            return set
    return None

def setReverse():

    wait = WebDriverWait(driver, 15)
    #only for sets w/ reverses
    preferences = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/section[2]/section/div[3]/div/div/div/div[1]/div/button')))
    preferences.click()

    time.sleep(10)
    menu = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[3]/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[6]/div[2]/div[1]/div[2]')))
    options = menu.find_elements(By.TAG_NAME, "div")

    for option in options:
        checkbox = option.find_element(By.CSS_SELECTOR, "input.tcg-input-checkbox__input")  
        if(option.text == "Normal" or option.text == "Holofoil"):
            driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(10)
    saveChanges = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[3]/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[7]/button[1]')))
    time.sleep(10)
    saveChanges.click()

def reverseOn():
    wait = WebDriverWait(driver, 15)
    #only for sets w/ reverses
    preferences = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/section[2]/section/div[3]/div/div/div/div[1]/div/button')))
    preferences.click()
    time.sleep(10)

    menu = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[3]/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[6]/div[2]/div[1]/div[2]')))
    options = menu.find_elements(By.TAG_NAME, "div")
    for option in options:
        checkbox = option.find_element(By.CLASS_NAME, "tcg-input-checkbox__input")  
        driver.execute_script("arguments[0].click();", checkbox)

    time.sleep(10)
    saveChanges = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/section[2]/section/div[3]/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[7]/button[1]')))
    time.sleep(10)
    saveChanges.click()

def reset():
    wait = WebDriverWait(driver, 15)
    #only for sets w/ reverses
    preferences = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/section[2]/section/div[3]/div/div/div/div[1]/div/button')))
    preferences.click()
    time.sleep(10)

    menu = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[3]/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[6]/div[2]/div[1]/div[2]')))
    options = menu.find_elements(By.TAG_NAME, "div")
    for option in options:
        checkbox = option.find_element(By.CLASS_NAME, "tcg-input-checkbox__input")  
        if(option.text == "Reverse Holofoil"):
            driver.execute_script("arguments[0].click();", checkbox)

    time.sleep(10)
    saveChanges = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/section[2]/section/div[3]/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[7]/button[1]')))
    time.sleep(10)
    saveChanges.click()

# Set up Chrome options
'''
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver as per your configuration
webdriver_service = Service("/Users/gavinschrader/Downloads/chromedriver-mac-x643/chromedriver")

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)'''

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--window-size=1920,1080")  # Set window size for headless mode

# Set path to chromedriver in the GitHub Actions environment
webdriver_service = Service("/usr/bin/chromedriver")  # Adjust for your CI setup

# Initialize the WebDriver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


def getBoxPrices(boxSet):

    driver.get("https://app.getcollectr.com/explore/product/" + str(boxSet.productId))
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 30)

    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    price = float(priceElement.text.replace("$", "").replace(",", ""))
    pricePer = float(price/36)

    print("\n")
    print("Set Name: " + boxSet.name)
    print("Box Price: $" + str(price))
    print(f"Price Per Pack: ${pricePer:.2f}")

    return price, round(pricePer, 2), boxSet.name, boxSet.setNumber

def gen1Calculate(url):


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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "")

    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:

                rarity = cells[5].text
                price = float(cells[7].text.replace("$", ""))
                roundedPrice = format(price, ".2f")
                if rarity == "Common":
                    commonCount += 1
                    totalCommonValue += price
                elif rarity == "Uncommon":
                    uncommonCount += 1
                    totalUncommonValue += price
                elif rarity == "Rare":
                    rareCount += 1
                    totalRareValue += price
                elif rarity == "Holo Rare":
                    holoCount += 1
                    totalHoloValue += price
                elif rarity == "Secret Rare":
                    secretCount += 1
                    totalSecretValue += price
                totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            print(f"Error processing row: {e}")

    tempSet = findSet(setName.strip(), vintageSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    expValue = 0
    if(tempSet.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)
    expValue += ((totalCommonValue / commonCount * tempSet.commonsPer) + (totalUncommonValue / uncommonCount * 3) + (totalRareValue / rareCount * .66) + (totalHoloValue / holoCount * tempSet.holoOdds)) 

    print("\n")
    print(tempSet.name)
    print("Total Cards: " + str(totalCards))
    print("Commons: " + str(commonCount) + ", Value: $" + f"{totalCommonValue:.2f}")
    print("Uncommons: " + str(uncommonCount) + ", Value: $" + f"{totalUncommonValue:.2f}")
    print("Rares: " + str(rareCount) + ", Value: $" + f"{totalRareValue:.2f}")
    print("Holos: " + str(holoCount) + ", Value: $" + f"{totalHoloValue:.2f}")
    print("Secret Rares: " + str(secretCount) + ", Value: $" + f"{totalSecretValue:.2f}")
    print("Expected Value: $" + f"{expValue:.2f}")
    print("Pack Price: $" + f"{packPrice:.2f}")
    print("Adj. Expected Value: $" + f"{expValue / (packPrice):.2f}")

    time.sleep(10)
    return (expValue / (packPrice)), packPrice, expValue

def earlyReverseSets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "")

    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:

                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                #roundedPrice = format(price, ".2f")
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            #if len(cells) > 7:
            rarity = cells[5].text
            name = cells[2].text
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            roundedPrice = format(price, ".2f")
            if rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            totalCards += 1
        #else:
         #   print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row:")
    reset()

    tempSet = findSet(setName.strip(), earlyReverseSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    expValue = 0
    if(secretCount > 0):
        expValue += (totalSecretValue / secretCount * tempSet.secretOdds)
    expValue += ((totalCommonValue / commonCount * tempSet.commonsPer) + (totalUncommonValue / uncommonCount * tempSet.uncommonsPer) + (totalRareValue / rareCount * .66) + (totalHoloValue / holoCount * tempSet.holoOdds) + (totalReverseValue / reverseCount)) 

    print("\n")
    print(setName)
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

    time.sleep(10)
    return (expValue / (packPrice)), packPrice, expValue

def earlyExSets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "")
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:

                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                #roundedPrice = format(price, ".2f")
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            #if len(cells) > 7:
            rarity = cells[5].text
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            roundedPrice = format(price, ".2f")
            if rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            elif rarity == "Ultra Rare":
                ultraRareCount += 1
                totalUltraRareValue += price
            totalCards += 1
        #else:
         #   print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    tempSet = findSet(setName.strip(), earlyExSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))
    

    commonQuantity = 5
    uncommonQuantity = 2

    expValue = 0
    if(tempSet.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)

    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * .66)
    expValue += (totalHoloValue / holoCount * tempSet.holoOdds)
    expValue += (totalUltraRareValue / ultraRareCount * tempSet.ultraOdds)
    expValue += (totalReverseValue / reverseCount)

    print("\n")
    print(tempSet.name)
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

    time.sleep(10)
    return (expValue / (packPrice)), packPrice, expValue

def goldStarSets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 30)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "")
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:

                rarity = cells[5].text
                price = float(cells[7].text.replace("$", ""))
                #roundedPrice = format(price, ".2f")
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            #if len(cells) > 7:
            rarity = cells[5].text
            name = cells[2].text
            #print(name)
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            roundedPrice = format(price, ".2f")
            if rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            elif ((rarity == "Ultra Rare") and (" Star" not in name)):
                ultraRareCount += 1
                totalUltraRareValue += price
            elif ((rarity == "Ultra Rare") and (" Star" in name)):
                goldStarCount += 1
                totalGoldStarValue += price
            totalCards += 1
        #else:
         #   print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    tempSet = findSet(setName.strip(), goldStarSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    commonQuantity = 5
    uncommonQuantity = 2

    expValue = 0
    if(tempSet.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)

    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * .66)
    expValue += (totalHoloValue / holoCount * tempSet.holoOdds)
    expValue += (totalUltraRareValue / ultraRareCount * tempSet.ultraOdds)
    expValue += (totalReverseValue / reverseCount)
    expValue += (totalGoldStarValue / max(goldStarCount, 1) * tempSet.goldStarOdds)




    print("\n")
    print(tempSet.name)
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

    time.sleep(10)
    return (expValue / (packPrice)), packPrice, expValue

def dpSets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "")
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                number = cells[6].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if rarity == "Shiny Holo Rare":
                    shinyCount += 1
                    totalShinyValue += price
                    totalCards += 1
                elif number == "RT1" or number == "RT2" or number == "RT3" or number == "RT4" or number == "RT5" or number == "RT6":
                    rotomCount += 1
                    totalRotomValue += price
                else:
                    reverseCount += 1
                    totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    #tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            #if len(cells) > 7:
            rarity = cells[5].text
            name = cells[2].text
            number = cells[6].text
            #print(name)
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            roundedPrice = format(price, ".2f")
            if rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            #hard coded for mysterious treasures
            elif name == "Time-Space Distortion":
                secretCount += 1
                totalSecretValue += price
            elif number == "AR1" or number == "AR2" or number == "AR3" or number == "AR4" or number == "AR5" or number == "AR6" or number == "AR7" or number == "AR8" or number == "AR9":
                    arceusCount += 1
                    totalArceusValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            elif (rarity == "Ultra Rare"):
                ultraRareCount += 1
                totalUltraRareValue += price
            totalCards += 1
        #else:
         #   print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    tempSet = findSet(setName.strip(), levelXSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
    if(tempSet.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)
    if(tempSet.shinyOdds > 0):
        expValue += (totalShinyValue /max(shinyCount, 1) * tempSet.shinyOdds)
    if(tempSet.rotomOdds > 0):
        expValue += (totalRotomValue /max(rotomCount, 1) * tempSet.rotomOdds)
    if(tempSet.arceusOdds > 0):
        expValue += (totalArceusValue /max(arceusCount, 1) * tempSet.arceusOdds)

    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * .66)
    expValue += (totalHoloValue / holoCount * tempSet.holoOdds)
    expValue += (totalUltraRareValue / ultraRareCount * tempSet.ultraOdds)
    expValue += (totalReverseValue / reverseCount * tempSet.reverseOdds)


    print("\n")
    print(tempSet.name)
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

    time.sleep(10)
    return (expValue / (packPrice)), packPrice, expValue

def hgssSets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "")
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                number = cells[6].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    #tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            #if len(cells) > 7:
            rarity = cells[5].text
            cardName = cells[2].text
            number = cells[6].text
            foil = cells[3].text
            #print(name)
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            roundedPrice = format(price, ".2f")
            if rarity == "Common" and foil == "Holofoil":
                reverseCount += 1
                totalReverseValue += price
            elif rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif number == "SL1" or number == "SL2" or number == "SL3" or number == "SL4" or number == "SL5" or number == "SL6" or number == "SL7" or number == "SL8" or number == "SL9" or number == "SL10" or number == "SL11":
                shinyCount += 1
                totalShinyValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif number == "ONE" or number == "TWO" or number == "THREE" or number == "FOUR":
                secretCount += 1
                totalSecretValue += price
            elif "(Top)" in cardName or "(Bottom)" in cardName:
                legendCount += 1
                totalLegendValue += price
            elif "(Prime)" in cardName:
                    primeCount += 1
                    totalPrimeValue += price
            totalCards += 1
        #else:
         #   print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    tempSet = findSet(setName.strip(), hgssSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
    if(tempSet.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)
    if(tempSet.shinyOdds > 0):
        expValue += (totalShinyValue /max(shinyCount, 1) * tempSet.shinyOdds)
    if(tempSet.primeOdds > 0):
        expValue += (totalPrimeValue /primeCount * tempSet.primeOdds)
    if(tempSet.legendOdds > 0):
        expValue += (totalLegendValue /max(legendCount, 1) * tempSet.legendOdds)

    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * .66)
    expValue += (totalHoloValue / holoCount * tempSet.holoOdds)
    expValue += (totalReverseValue / reverseCount * tempSet.reverseOdds)


    print("\n")
    print(tempSet.name)
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

    time.sleep(3)
    return (expValue / (packPrice )), packPrice, expValue

def bwSets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "")
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                number = cells[6].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    #tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            #if len(cells) > 7:
            rarity = cells[5].text
            cardName = cells[2].text
            number = cells[6].text
            foil = cells[3].text
            #print(name)
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            if rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Rare Ace":
                aceCount += 1
                totalAceValue += price
            elif "Full Art" in cardName:
                faCount += 1
                totalFaValue += price
            elif "EX" in cardName:
                exCount += 1
                totalExValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            if(rarity != "Code Card"):
                totalCards += 1
        #else:
         #   print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    tempSet = findSet(setName.strip(), bwSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
    if(tempSet.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)
    if(tempSet.exOdds > 0):
        expValue += (totalExValue /exCount * tempSet.exOdds)
    if(tempSet.faOdds > 0):
        expValue += (totalFaValue /max(faCount, 1) * tempSet.faOdds)
    if(tempSet.aceOdds > 0):
        expValue += (totalAceValue /max(aceCount, 1) * tempSet.aceOdds)

    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * .66)
    expValue += (totalHoloValue / holoCount * tempSet.holoOdds)
    expValue += (totalReverseValue / reverseCount * tempSet.reverseOdds)


    print("\n")
    print(tempSet.name)
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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "")
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    #tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            rarity = cells[5].text
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            if rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Ultra Rare":
                exCount += 1
                totalExValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            if(rarity != "Code Card"):
                totalCards += 1
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    time.sleep(10)
    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures-radiant-collection")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            rarity = cells[5].text
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            if rarity == "Common":
                rcCommonCount += 1
                totalRcCommonValue += price
            elif rarity == "Uncommon":
                rcUncommonCount += 1
                totalRcUncommonValue += price
            elif rarity == "Ultra Rare":
                rcUltraCount += 1
                totalRcUltraValue += price
            totalCards += 1
        except Exception as e:
            pass
            #print(f"Error processing row:")

    driver.get("https://app.getcollectr.com/explore/product/98581")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
    return (expValue / (packPrice )), packPrice, expValue

def xySets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            rarity = cells[5].text
            cardName = cells[2].text
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            if rarity == "Code Card":
                codeCardCount += 1
            elif cardName == "Chesnaught BREAK":
                breakCount += 1
                totalBreakValue += price
            elif cardName == "Skyla" and setName == "XY - BREAKpoint":
                faCount += 1
                totalFaValue += price
            elif cardName == "Professor Sycamore" and setName == "XY - Steam Siege":
                faCount += 1
                totalFaValue += price
            elif rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Rare BREAK":
                breakCount += 1
                totalBreakValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            elif "Full Art" in cardName:
                faCount += 1
                totalFaValue += price
            elif "EX" in cardName:
                exCount += 1
                totalExValue += price
            if(rarity != "Code Card"):
                totalCards += 1
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    tempSet = findSet(setName.strip(), xySetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    commonQuantity = 5
    uncommonQuantity = 3
    rareOdds = 1 - tempSet.exOdds - tempSet.faOdds - tempSet.holoOdds - tempSet.secretOdds

    expValue = 0
    if(tempSet.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)
    if(tempSet.breakOdds > 0):
        expValue += (totalBreakValue /max(breakCount, 1) * tempSet.breakOdds)

    expValue += (totalFaValue /max(faCount, 1) * tempSet.faOdds)
    expValue += (totalExValue /exCount * tempSet.exOdds)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    if(tempSet.name == "XY - Evolutions"):
        expValue += ((totalUncommonValue + totalSecretValue) / (uncommonCount + secretCount) * uncommonQuantity)
    else:
        expValue += (totalUncommonValue / uncommonCount * uncommonQuantity) 
    expValue += (totalRareValue / rareCount * rareOdds)
    expValue += (totalHoloValue / holoCount * tempSet.holoOdds)
    expValue += (totalReverseValue / reverseCount * tempSet.reverseOdds)


    print("\n")
    print(tempSet.name)
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

    time.sleep(10)
    return (expValue / (packPrice)), packPrice, expValue

def smSets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            rarity = cells[5].text
            cardName = cells[2].text
            number = cells[6].text
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            if rarity == "Code Card":
                codeCardCount += 1
            elif rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Prism Rare":
                prismCount += 1
                totalPrismValue += price
            elif setName == "SM - Cosmic Eclipse" and (number == "237/236" or number == "238/236" or number == "239/236" or number == "240/236" or number == "241/236" or number == "242/236" or number == "243/236" or number == "244/236" or number == "245/236" or number == "246/236" or number == "247/236" or number == "248/236"):
                galleryCount += 1
                totalGalleryValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            elif "Full Art" in cardName:
                faCount += 1
                totalFaValue += price
            elif "GX" in cardName:
                gxCount += 1
                totalGxValue += price
            if(rarity != "Code Card"):
                totalCards += 1
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    tempSet = findSet(setName.strip(), smSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
    if(tempSet.secretOdds > 0):
        expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)
    if(tempSet.prismOdds > 0):
        expValue += (totalPrismValue /max(prismCount, 1) * tempSet.prismOdds)
    if(tempSet.galleryOdds > 0):
        expValue += (totalGalleryValue /max(galleryCount, 1) * tempSet.galleryOdds)

    expValue += (totalFaValue /faCount * tempSet.faOdds)
    expValue += (totalGxValue /gxCount * tempSet.gxOdds)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity)
    expValue += (totalRareValue / rareCount * tempSet.rareOdds)
    expValue += (totalHoloValue / holoCount * tempSet.holoOdds)
    expValue += (totalReverseValue / reverseCount * tempSet.reverseOdds)


    print("\n")
    print(tempSet.name)
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

    time.sleep(10)
    return (expValue / (packPrice)), packPrice, expValue

def swshSets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            rarity = cells[5].text
            cardName = cells[2].text
            number = cells[6].text
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            if rarity == "Code Card":
                codeCardCount += 1
            elif rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Amazing Rare":
                arCount += 1
                totalArValue += price
            elif "Alternate" in cardName:
                altCount += 1
                totalAltValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            elif "Full Art" in cardName:
                faCount += 1
                totalFaValue += price
            elif "VMAX" in cardName:
                vmaxCount += 1
                totalVmaxValue += price
            elif " V" in cardName:
                vCount += 1
                totalVValue += price
            if(rarity != "Code Card"):
                totalCards += 1
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    tempSet = findSet(setName.strip(), swshSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
        
    if(tempSet.arOdds > 0):
        expValue += (totalArValue /max(arCount, 1) * tempSet.arOdds)
    if(tempSet.altOdds > 0):
        expValue += (totalAltValue /max(altCount, 1) * tempSet.altOdds)
        

    expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)
    expValue += (totalFaValue /faCount * tempSet.faOdds)
    expValue += (totalVValue /vCount * tempSet.vOdds)
    expValue += (totalVmaxValue /vmaxCount * tempSet.vmaxOdds)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity)
    expValue += (totalRareValue / rareCount * tempSet.rareOdds)
    expValue += (totalHoloValue / holoCount * tempSet.holoOdds)
    expValue += (totalReverseValue / reverseCount * tempSet.reverseOdds)


    print("\n")
    print(tempSet.name)
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

    time.sleep(10)
    return (expValue / (packPrice )), packPrice, expValue

def lateSwshSets(url, url2):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            rarity = cells[5].text
            cardName = cells[2].text
            number = cells[6].text
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            if rarity == "Code Card":
                codeCardCount += 1
            elif rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Holo Rare":
                holoCount += 1
                totalHoloValue += price
            elif rarity == "Radiant Rare":
                radiantCount += 1
                totalRadiantValue += price
            elif "Alternate" in cardName:
                altCount += 1
                totalAltValue += price
            elif rarity == "Secret Rare":
                secretCount += 1
                totalSecretValue += price
            elif "Full Art" in cardName:
                faCount += 1
                totalFaValue += price
            elif "VMAX" in cardName:
                vmaxCount += 1
                totalVmaxValue += price
            elif "VSTAR" in cardName:
                vstarCount += 1
                totalVstarValue += price
            elif " V" in cardName:
                vCount += 1
                totalVValue += price
            if(rarity != "Code Card"):
                totalCards += 1
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()


    driver.get(url2)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                tgCount += 1
                totalTgValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass

    tempSet = findSet(setName.strip(), lateSwshSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    commonQuantity = 5
    uncommonQuantity = 3

    expValue = 0
        
    if(tempSet.radiantOdds > 0):
        expValue += (totalRadiantValue /radiantCount * tempSet.radiantOdds)
        
        
    expValue += (totalAltValue /max(altCount, 1) * tempSet.altOdds)
    expValue += (totalSecretValue / max(secretCount, 1) * tempSet.secretOdds)
    expValue += (totalFaValue /faCount * tempSet.faOdds)
    expValue += (totalVValue /vCount * tempSet.vOdds)
    expValue += (totalVmaxValue /vmaxCount * tempSet.vmaxOdds)
    expValue += (totalVstarValue /vstarCount * tempSet.vstarOdds)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity)
    expValue += (totalRareValue / rareCount * tempSet.rareOdds)
    expValue += (totalHoloValue / holoCount * tempSet.holoOdds)
    expValue += (totalReverseValue / reverseCount * tempSet.reverseOdds)
    expValue += (totalTgValue /tgCount * tempSet.tgOdds)


    print("\n")
    print(tempSet.name)
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

    time.sleep(10)
    return (expValue / (packPrice )), packPrice, expValue

def svsets(url):

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

    driver.get(url)
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    time.sleep(10)
    tbody_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tcg-table-body"))
)
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            rarity = cells[5].text
            cardName = cells[2].text
            number = cells[6].text
            price = float(cells[7].text.replace("$", "").replace(",", ""))
            if rarity == "Code Card":
                codeCardCount += 1
            elif rarity == "Common":
                commonCount += 1
                totalCommonValue += price
            elif rarity == "Uncommon":
                uncommonCount += 1
                totalUncommonValue += price
            elif rarity == "Rare":
                rareCount += 1
                totalRareValue += price
            elif rarity == "Double Rare":
                doubleCount += 1
                totalDoubleValue += price
            elif rarity == "Hyper Rare":
                hyperCount += 1
                totalHyperValue += price
            elif rarity == "Illustration Rare":
                irCount += 1
                totalIrValue += price
            elif rarity == "Special Illustration Rare":
                sirCount += 1
                totalSirValue += price
            elif rarity == "ACE SPEC Rare":
                aceCount += 1
                totalAceValue += price
            elif rarity == "Ultra Rare":
                ultraCount += 1
                totalUltraValue += price
            if(rarity != "Code Card"):
                totalCards += 1
        except Exception as e:
            pass
            #print(f"Error processing row:")

    reset()

    tempSet = findSet(setName.strip(), svSetList)

    driver.get("https://app.getcollectr.com/explore/product/" + str(tempSet.productId))
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    commonQuantity = 4
    uncommonQuantity = 3

    expValue = 0
        
    if(tempSet.aceOdds > 0):
        expValue += (totalAceValue /max(aceCount, 1) * tempSet.aceOdds)
        

    expValue += (totalHyperValue / max(hyperCount, 1) * tempSet.hyperOdds)
    expValue += (totalUltraValue /ultraCount * tempSet.ultraOdds)
    expValue += (totalDoubleValue /doubleCount * tempSet.doubleOdds)
    expValue += (totalIrValue /irCount * tempSet.irOdds)
    expValue += (totalCommonValue / commonCount * commonQuantity)
    expValue += (totalUncommonValue / uncommonCount * uncommonQuantity)
    expValue += (totalRareValue / rareCount * tempSet.rareOdds)
    expValue += (totalSirValue / sirCount * tempSet.sirOdds)
    expValue += (totalReverseValue / reverseCount * tempSet.reverseOdds)


    print("\n")
    print(tempSet.name)
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

    time.sleep(10)
    return (expValue / (packPrice )), packPrice, expValue

def dragonVault():

    totalCards = 0
    totalHoloValue = 0
    totalSecretRareValue = 0

    holoCount = 0
    secretRareCount = 0

    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon-vault")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(cardName == "Kyurem"):
                    secretRareCount += 1
                    totalSecretRareValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    driver.get("https://app.getcollectr.com/explore/product/98948")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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

    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/double-crisis")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Ultra Rare"):
                    ultraRareCount += 1
                    totalUltraRareValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://app.getcollectr.com/explore/product/229226")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/shining-legends")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Shiny Holo Rare" and "Mewtwo" in cardName):
                    secretCount += 1
                    totalSecretValue += price
                elif(rarity == "Shiny Holo Rare"):
                    shiningCount += 1
                    totalShiningValue += price
                elif(rarity == "Secret Rare"):
                    rainbowCount += 1
                    totalRainbowValue += price
                elif(rarity == "Ultra Rare" and "Full Art" in cardName):
                    faCount += 1
                    totalFaValue += price
                elif(rarity == "Ultra Rare"):
                    gxCount += 1
                    totalGxValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://app.getcollectr.com/explore/product/155880")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon-majesty")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Secret Rare"):
                    secretCount += 1
                    totalSecretValue += price
                elif(rarity == "Prism Rare"):
                    prismCount += 1
                    totalPrismValue += price
                elif(rarity == "Ultra Rare" and "Full Art" in cardName):
                    faCount += 1
                    totalFaValue += price
                elif(rarity == "Ultra Rare"):
                    gxCount += 1
                    totalGxValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://app.getcollectr.com/explore/product/173392")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/champions-path")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Secret Rare"):
                    secretCount += 1
                    totalSecretValue += price
                elif(rarity == "Ultra Rare" and "Full Art" in cardName):
                    faCount += 1
                    totalFaValue += price
                elif(rarity == "Ultra Rare" and "VMAX" in cardName):
                    vmaxCount += 1
                    totalVmaxValue += price
                elif(rarity == "Ultra Rare"):
                    vCount += 1
                    totalVValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://app.getcollectr.com/explore/product/218789")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/pokemon-go")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Secret Rare"):
                    secretCount += 1
                    totalSecretValue += price
                elif(rarity == "Ultra Rare" and "Alternate" in cardName):
                    altCount += 1
                    totalAltValue += price
                elif(rarity == "Ultra Rare" and "Full Art" in cardName):
                    faCount += 1
                    totalFaValue += price
                elif(rarity == "Ultra Rare" and "VMAX" in cardName):
                    vmaxCount += 1
                    totalVmaxValue += price
                elif(rarity == "Ultra Rare" and "VSTAR" in cardName):
                    vstarCount += 1
                    totalVstarValue += price
                elif(rarity == "Ultra Rare"):
                    vCount += 1
                    totalVValue += price
                elif(rarity == "Holo Rare" and "Ditto" not in cardName):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Radiant Rare"):
                    radiantCount += 1
                    totalRadiantValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://app.getcollectr.com/explore/product/274421")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv-scarlet-and-violet-151")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Hyper Rare"):
                    hyperCount += 1
                    totalHyperRareValue += price
                elif(rarity == "Ultra Rare"):
                    ultraRareCount += 1
                    totalUltraRareValue += price
                elif(rarity == "Double Rare"):
                    doubleRareCount += 1
                    totalDoubleRareValue += price
                elif(rarity == "Illustration Rare"):
                    irCount += 1
                    totalIrValue += price
                elif(rarity == "Special Illustration Rare"):
                    sirCount += 1
                    totalSirValue += price
                elif(rarity == "Rare"):
                    rareCount += 1
                    totalRareValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://app.getcollectr.com/explore/product/504467")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv-shrouded-fable")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Hyper Rare"):
                    hyperCount += 1
                    totalHyperRareValue += price
                elif(rarity == "Ultra Rare"):
                    ultraRareCount += 1
                    totalUltraRareValue += price
                elif(rarity == "Double Rare"):
                    doubleRareCount += 1
                    totalDoubleRareValue += price
                elif(rarity == "Illustration Rare"):
                    irCount += 1
                    totalIrValue += price
                elif(rarity == "Special Illustration Rare"):
                    sirCount += 1
                    totalSirValue += price
                elif(rarity == "ACE SPEC Rare"):
                    aceSpecCount += 1
                    totalAceSpecValue += price
                elif(rarity == "Rare"):
                    rareCount += 1
                    totalRareValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://app.getcollectr.com/explore/product/552997")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv-paldean-fates")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Hyper Rare"):
                    hyperCount += 1
                    totalHyperRareValue += price
                elif(rarity == "Ultra Rare"):
                    ultraRareCount += 1
                    totalUltraRareValue += price
                elif(rarity == "Double Rare"):
                    doubleRareCount += 1
                    totalDoubleRareValue += price
                elif(rarity == "Illustration Rare"):
                    irCount += 1
                    totalIrValue += price
                elif(rarity == "Special Illustration Rare"):
                    sirCount += 1
                    totalSirValue += price
                elif(rarity == "Shiny Ultra Rare"):
                    shinyUltraCount += 1
                    totalShinyUltraValue += price
                elif(rarity == "Shiny Rare"):
                    shinyCount += 1
                    totalShinyValue += price
                elif(rarity == "Rare"):
                    rareCount += 1
                    totalRareValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://app.getcollectr.com/explore/product/528038")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(1)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/hidden-fates")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Secret Rare"):
                    rainbowCount += 1
                    totalRainbowValue += price
                elif(rarity == "Ultra Rare" and "Full Art" in cardName):
                    faCount += 1
                    totalFaValue += price
                elif(rarity == "Ultra Rare"):
                    gxCount += 1
                    totalGxValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Rare"):
                    rareCount += 1
                    totalRareValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/hidden-fates-shiny-vault")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                cardNumber = cells[6].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if("GX" in cardName and cardNumber != "SV91/SV94" and cardNumber != "SV92/SV94" and cardNumber != "SV93/SV94" and cardNumber != "SV94/SV94"):
                    shinyGxCount += 1
                    totalShinyGXValue += price
                elif(cardNumber == "SV81/SV94" or cardNumber == "SV82/SV94" or cardNumber == "SV83/SV94" or cardNumber == "SV84/SV94" or cardNumber == "SV85/SV94" or cardNumber == "SV86/SV94"):
                    faVaultCount += 1
                    totalFaVaultValue += price
                elif(cardNumber == "SV87/SV94" or cardNumber == "SV88/SV94" or cardNumber == "SV89/SV94" or cardNumber == "SV90/SV94" or cardNumber == "SV91/SV94" or cardNumber == "SV92/SV94" or cardNumber == "SV93/SV94" or cardNumber == "SV94/SV94"):
                    goldCount += 1
                    totalGoldValue += price
                elif(rarity == "Shiny Holo Rare"):
                    shinyCount += 1
                    totalShinyValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")

    driver.get("https://app.getcollectr.com/explore/product/198634")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

    rareSlot = 0
    reverseSlot = 0

    rareSlot += (totalRareValue / rareCount * .67 )
    rareSlot += (totalHoloValue / holoCount * .1244 )
    rareSlot += (totalGxValue / gxCount * (1/7) )
    rareSlot += (totalFaValue / faCount * (1/22) )
    rareSlot += (totalRainbowValue / rainbowCount * (1/58) )

    reverseSlot += (totalReverseValue / reverseCount * .6076 )
    reverseSlot += (totalShinyValue / shinyCount * .25 )
    reverseSlot += (totalShinyGXValue / gxCount * (1/9) )
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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/shining-fates")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Secret Rare"):
                    rainbowCount += 1
                    totalRainbowValue += price
                elif(rarity == "Ultra Rare" and "Full Art" in cardName):
                    faCount += 1
                    totalFaValue += price
                elif(rarity == "Ultra Rare" and "VMAX" in cardName):
                    vmaxCount += 1
                    totalVmaxValue += price
                elif(rarity == "Ultra Rare"):
                    vCount += 1
                    totalVValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Amazing Rare"):
                    amazingRareCount += 1
                    totalAmazingRareValue += price
                elif(rarity == "Rare"):
                    rareCount += 1
                    totalRareValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/shining-fates-shiny-vault")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                cardNumber = cells[6].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(cardNumber == "SV121/SV122" or cardNumber == "SV122/SV122"):
                    goldCount += 1
                    totalGoldValue += price
                elif("VMAX" in cardName):
                    shinyVmaxCount += 1
                    totalShinyVmaxValue += price
                elif(" V" in cardName):
                    shinyVCount += 1
                    totalShinyVValue += price
                elif(rarity == "Shiny Holo Rare"):
                    shinyCount += 1
                    totalShinyValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")

    driver.get("https://app.getcollectr.com/explore/product/232636")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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



    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/generations")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Ultra Rare"):
                    exCount += 1
                    totalExValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Rare"):
                    rareCount += 1
                    totalRareValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/generations-radiant-collection")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                cardNumber = cells[6].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Ultra Rare"):
                    rcUltraCount += 1
                    totalRcUltraValue += price
                elif(rarity == "Uncommon"):
                    rcUncommonCount += 1
                    totalRcUncommonValue += price
                elif("Common"):
                    rcCommonCount += 1
                    totalRcCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")

    driver.get("https://app.getcollectr.com/explore/product/187238")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/crown-zenith")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Secret Rare"):
                    secretCount += 1
                    totalSecretValue += price
                elif(rarity == "Ultra Rare" and "Energy" in cardName):
                    energyCount += 1
                    totalEnergyValue += price
                elif(rarity == "Ultra Rare" and ("VMAX" in cardName or "VSTAR" in cardName)):
                    vmaxCount += 1
                    totalVmaxValue += price
                elif(rarity == "Ultra Rare" and "Full Art" in cardName):
                    faCount += 1
                    totalFaValue += price
                elif(rarity == "Ultra Rare"):
                    vCount += 1
                    totalVValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Radiant Rare"):
                    radiantCount += 1
                    totalRadiantValue += price
                elif(rarity == "Rare"):
                    rareCount += 1
                    totalRareValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/crown-zenith-galarian-gallery")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(3)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                cardNumber = cells[6].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Secret Rare"):
                    goldCount += 1
                    totalGoldValue += price
                elif((("V" in cardName) or (cardNumber == "GG57/GG70" or cardNumber == "GG58/GG70" or cardNumber == "GG59/GG70" or cardNumber == "GG60/GG70" or cardNumber == "GG61/GG70" or cardNumber == "GG62/GG70" or cardNumber == "GG63/GG70" or cardNumber == "GG64/GG70" or cardNumber == "GG65/GG70" or cardNumber == "GG66/GG70")) and (cardNumber != "GG01/GG70")):
                    ggUltraCount += 1
                    totalGgUltraValue += price
                else:
                    ggCount += 1
                    totalGgValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")

    driver.get("https://app.getcollectr.com/explore/product/453466")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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

    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/celebrations")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                cardNumber = cells[6].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Secret Rare"):
                    secretCount += 1
                    totalSecretValue += price
                elif(cardNumber == "005/025"):
                    ultraCount += 1
                    totalUltraValue += price
                elif(rarity == "Holo Rare"):
                    holoCount += 1
                    totalHoloValue += price
                elif(rarity == "Ultra Rare"):
                    ultraCount += 1
                    totalUltraValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/celebrations-classic-collection")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                cardNumber = cells[6].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(cardNumber == "2/102"):
                    blastoise += price
                elif(cardNumber == "4/102"):
                    charizard += price
                elif(cardNumber == "15/106"):
                    claydol += price
                elif(cardNumber == "20/111"):
                    cleffa += price
                elif(cardNumber == "8/82"):
                    gyarados += price
                elif(cardNumber == "107/123"):
                    donphan += price
                elif(cardNumber == "145/147"):
                    garchomp += price
                elif(cardNumber == "93/101"):
                    gardevoir += price
                elif(cardNumber == "15/82"):
                    teamRocket += price
                elif(cardNumber == "73/102"):
                    imposter += price
                elif(cardNumber == "109/111"):
                    luxray += price
                elif(cardNumber == "76/108"):
                    rayquaza += price
                elif(cardNumber == "88/92"):
                    mew += price
                elif(cardNumber == "54/99"):
                    mewtwo += price
                elif(cardNumber == "4/102"):
                    charizard += price
                elif(cardNumber == "113/114"):
                    reshiram += price
                elif(cardNumber == "86/109"):
                    admin += price
                elif(cardNumber == "15/132"):
                    zapdos += price
                elif(cardNumber == "66/164"):
                    magikarp += price
                elif(cardNumber == "60/145"):
                    tapulele += price
                elif(cardNumber == "9/195"):
                    groudon += price
                elif(cardNumber == "17/17"):
                    umbreon += price
                elif(cardNumber == "15/102"):
                    venusaur += price
                elif(cardNumber == "97/146"):
                    xerneas += price
                elif(cardNumber == "114/114"):
                    zekrom += price
                elif(cardNumber == "24/53"):
                    pikachu += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")

    driver.get("https://app.getcollectr.com/explore/product/248577")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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


    driver.get("https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv-prismatic-evolutions")
    # Allow the page to load completely
    time.sleep(10)
    wait = WebDriverWait(driver, 15)

    setReverse()

    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                reverseCount += 1
                totalReverseValue += price
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")


    reverseOn()
    
    setNameElement = element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/section[2]/section/div[1]/div/div[1]/h1')))
    setName = setNameElement.text.replace(" Price Guide", "").replace("Pokemon", "").replace('\n', '')
    time.sleep(10)
    tbody_element = driver.find_element(By.CSS_SELECTOR, "tbody.tcg-table-body")
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 7:
                rarity = cells[5].text
                cardName = cells[2].text
                price = float(cells[7].text.replace("$", "").replace(",", ""))
                if(rarity == "Hyper Rare"):
                    hyperCount += 1
                    totalHyperValue += price
                elif(rarity == "Ultra Rare"):
                    ultraCount += 1
                    totalUltraValue += price
                elif(rarity == "ACE SPEC Rare"):
                    aceCount += 1
                    totalAceValue += price
                elif(rarity == "Double Rare"):
                    doubleCount += 1
                    totalDoubleValue += price
                elif(rarity == "Special Illustration Rare"):
                    sirCount += 1
                    totalSirValue += price
                elif("Master Ball Pattern" in cardName):
                    masterballCount += 1
                    totalMasterballValue += price
                elif("Poke Ball Pattern" in cardName):
                    pokeballCount += 1
                    totalPokeballValue += price
                elif(rarity == "Rare"):
                    rareCount += 1
                    totalRareValue += price
                elif(rarity == "Uncommon"):
                    uncommonCount += 1
                    totalUncommonValue += price
                elif(rarity == "Common"):
                    commonCount += 1
                    totalCommonValue += price
                if(rarity != "Code Card"):
                    totalCards += 1
            else:
                print("Not enough cells in the row.")
        except Exception as e:
            pass
            #print(f"Error processing row: {e}")
    
    reset()

    driver.get("https://app.getcollectr.com/explore/product/593294")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ml-2.font-bold.dark\\:text-secondaryTextDark.text-secondaryText.text-md')))
    packPrice = float(priceElement.text.replace("$", "").replace(",", ""))

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

    time.sleep(10)
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
    adjev, price, ev = gen1Calculate(set.url)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(100 + num)
    num += 1

num = 0


for set in earlyReverseSetList:
    adjev, price, ev = earlyReverseSets(set.url)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(200 + num)
    num += 1

num = 0

#need to get rid of box toppers?
for set in earlyExSetList:
    adjev, price, ev = earlyExSets(set.url)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(300 + num)
    num += 1

num = 0

for set in goldStarSetList:
    adjev, price, ev = goldStarSets(set.url)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(400 + num)
    num += 1

num = 0

for set in levelXSetList:
    adjev, price, ev = dpSets(set.url)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(500 + num)
    num += 1

num = 0

#may need to treat red gyarados special
for set in hgssSetList:
    adjev, price, ev = hgssSets(set.url)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(600 + num)
    num += 1

num = 0

for set in bwSetList:
    adjev, price, ev = bwSets(set.url)
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
    adjev, price, ev = xySets(set.url)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(800 + num)
    num += 1

num = 0

for set in smSetList:
    adjev, price, ev = smSets(set.url)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(900 + num)
    num += 1

num = 0

for set in swshSetList:
    adjev, price, ev = swshSets(set.url)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(1000 + num)
    num += 1

num = 0

for set in lateSwshSetList:
    adjev, price, ev = lateSwshSets(set.url, set.url2)
    expectedValueList.append(adjev)
    packValueList.append(price)
    setNameList.append(getSetName(set))
    actualEvList.append(ev)
    setNumberList.append(1100 + num)
    num += 1

num = 0

for set in svSetList:
    adjev, price, ev = svsets(set.url)
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

for bb in boosterBoxList:
    boxPrice, boxPricePer, setName, setNumber = getBoxPrices(bb)
    boxPriceList.append(boxPrice)
    boxPricePerList.append(boxPricePer)
    boxSetNameList.append(setName)
    boxSetNumberList.append(setNumber)


last_updated_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#need to fix loading for all functions?
print("\n")
driver.quit()


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