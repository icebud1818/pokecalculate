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






class VintageSet:
    def __init__(self, name, url, secretOdds, commonsPer):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.commonsPer = commonsPer 
        self.holoOdds = .33 - self.secretOdds

class EarlyReverseSet:
    def __init__(self, name, url, secretOdds, commonsPer, uncommonsPer):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.commonsPer = commonsPer 
        self.uncommonsPer = uncommonsPer
        self.holoOdds = .33 - self.secretOdds

class EarlyExSet:
    def __init__(self, name, url, secretOdds, ultraOdds):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds

class GoldStarSet:
    def __init__(self, name, url, secretOdds, ultraOdds, goldStarOdds):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.goldStarOdds = goldStarOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds - self.goldStarOdds

class LevelXSet:
    def __init__(self, name, url, secretOdds, ultraOdds, shinyOdds, rotomOdds, arceusOdds):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.ultraOdds = ultraOdds
        self.shinyOdds = shinyOdds
        self.rotomOdds = rotomOdds
        self.arceusOdds = arceusOdds
        self.reverseOdds = 1 - self.shinyOdds - self.rotomOdds - self.arceusOdds
        self.holoOdds = .33 - self.secretOdds - self.ultraOdds

class HgssSet:
    def __init__(self, name, url, secretOdds, primeOdds, legendOdds, shinyOdds):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.primeOdds = primeOdds
        self.legendOdds = legendOdds
        self.shinyOdds = shinyOdds
        self.reverseOdds = 1 - self.primeOdds - self.shinyOdds
        self.holoOdds = .33 - self.secretOdds - self.legendOdds

class BWSet:
    def __init__(self, name, url, secretOdds, exOdds, faOdds, aceOdds):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.exOdds = exOdds
        self.faOdds = faOdds
        self.aceOdds = aceOdds
        self.reverseOdds = 1 - self.aceOdds
        self.holoOdds = .33 - self.secretOdds - self.exOdds - self.faOdds

class XYSet:
    def __init__(self, name, url, secretOdds, exOdds, faOdds, breakOdds):
        self.name = name
        self.url = url
        self.secretOdds = secretOdds
        self.exOdds = exOdds
        self.faOdds = faOdds
        self.breakOdds = breakOdds
        self.reverseOdds = 1 - self.breakOdds
        self.holoOdds = (1/6)

class SMSet:
    def __init__(self, name, url, secretOdds, gxOdds, faOdds, prismOdds, galleryOdds):
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

class SWSHSet:
    def __init__(self, name, url, secretOdds, vOdds, vmaxOdds, faOdds, arOdds, altOdds):
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

class lateSWSHSet:
    def __init__(self, name, url, url2, holoOdds, secretOdds, vOdds, vmaxOdds, vstarOdds, faOdds, altOdds, tgOdds, radiantOdds):
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

class svSet:
    def __init__(self, name, url, hyperOdds, doubleOdds, ultraOdds, irOdds, sirOdds, aceOdds):
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


vintageSetList = [
    VintageSet("Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/base-set", 0, 5),
    VintageSet("Jungle", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/jungle", 0, 7),
    VintageSet("Fossil", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/fossil", 0, 7),
    VintageSet("Base Set 2", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/base-set-2", 0, 7),
    VintageSet("Team Rocket", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-rocket", 1/81, 7),
    VintageSet("Gym Heroes", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/gym-heroes", 0, 7),
    VintageSet("Gym Challenge", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/gym-challenge", 0, 7),
    VintageSet("Neo Genesis", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-genesis", 0, 7),
    VintageSet("Neo Discovery", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-discovery", 0, 7),
    VintageSet("Neo Revelation", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-revelation", 1/18, 7),
    VintageSet("Neo Destiny", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/neo-destiny", 1/12, 7)
]

earlyReverseSetList = [
    EarlyReverseSet("Legendary Collection", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-collection", 0, 6, 3),
    EarlyReverseSet("Expedition", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/expedition", 0, 5, 2),
    EarlyReverseSet("Aquapolis", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/aquapolis", 1/36, 5, 2),
    EarlyReverseSet("Skyridge", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/skyridge", 1/15, 5, 2)
]

earlyExSetList = [
    EarlyExSet("Ruby and Sapphire", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/ruby-and-sapphire", 0, 1/15),
    EarlyExSet("Sandstorm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sandstorm", 0, 1/15),
    EarlyExSet("Dragon", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon", 1/36, 1/15),
    EarlyExSet("Team Magma vs Team Aqua", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-magma-vs-team-aqua", 1/36, 1/15),
    EarlyExSet("Hidden Legends", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/hidden-legends", 0, 1/15),
    EarlyExSet("FireRed & LeafGreen", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/firered-and-leafgreen", 1/36, 1/15),
    EarlyExSet("Emerald", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/emerald", 0, 1/15)
]

goldStarSetList = [
    GoldStarSet("Team Rocket Returns", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/team-rocket-returns", 1/36, 1/15, 1/72),
    GoldStarSet("Deoxys", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/deoxys", 0, 1/15, 1/72),
    GoldStarSet("Unseen Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/unseen-forces", 1/36, 1/15, 1/72),
    GoldStarSet("Delta Species", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/delta-species", 0, 1/15, 1/72),
    GoldStarSet("Legend Maker", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legend-maker", 0, 1/15, 1/72),
    GoldStarSet("Holon Phantoms", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/holon-phantoms", 0, 1/36, 1/72),
    GoldStarSet("Crystal Guardians", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/crystal-guardians", 0, 1/15, 1/72),
    GoldStarSet("Dragon Frontiers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragon-frontiers", 0, 1/15, 1/72),
    GoldStarSet("Power Keepers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/power-keepers", 0, 1/10, 1/54)
]

levelXSetList = [
    LevelXSet("Diamond and Pearl", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/diamond-and-pearl", 0, 1/36, 0, 0, 0),
    LevelXSet("Mysterious Treasures", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/mysterious-treasures", 1/72, 1/36, 0, 0, 0),
    LevelXSet("Secret Wonders", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/secret-wonders", 0, 1/36, 0, 0, 0),
    LevelXSet("Great Encounters", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/great-encounters", 0, 1/36, 0, 0, 0),
    LevelXSet("Majestic Dawn", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/majestic-dawn", 0, 1/36, 0, 0, 0),
    LevelXSet("Legends Awakened", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legends-awakened", 0, 1/12, 0, 0, 0),
    LevelXSet("Stormfront", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/stormfront", 1/36, 1/12, 1/36, 0, 0),
    LevelXSet("Platinum", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/platinum", 1/36, 1/12, 1/36, 0, 0),
    LevelXSet("Rising Rivals", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/rising-rivals", 1/36, 1/12, 0, 1/18, 0),
    LevelXSet("Supreme Victors", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/supreme-victors", 1/36, 1/12, 1/36, 0, 0),
    LevelXSet("Arceus", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/arceus", 0, 1/12, 1/36, 0, 1/4)
]

hgssSetList = [
    HgssSet("HeartGold SoulSilver", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/heartgold-soulsilver", 1/108, 1/6, 1/12, 0),
    HgssSet("Unleashed", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/unleashed", 1/108, 1/7, 1/12, 0),
    HgssSet("Undaunted", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/undaunted", 1/108, 1/7, 1/12, 0),
    HgssSet("Triumphant", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/triumphant", 1/108, 1/7, 1/12, 0),
    HgssSet("Call of Legends", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/call-of-legends", 0, 0, 0, 1/18)
]

bwSetList = [
    BWSet("Black and White", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/black-and-white", 1/72, 0, 1/36, 0),
    BWSet("Emerging Powers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/emerging-powers", 0, 0, 1/36, 0),
    BWSet("Noble Victories", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/noble-victories", 1/72, 0, 1/18, 0),
    BWSet("Next Destinies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/next-destinies", 1/72, 1/18, 1/36, 0),
    BWSet("Dark Explorers", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dark-explorers", 1/72, 1/18, 1/36, 0),
    BWSet("Dragons Exalted", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/dragons-exalted", 1/72, 1/18, 1/36, 0),
    BWSet("Boundaries Crossed", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/boundaries-crossed", 1/72, 1/18, 1/36, 1/36),
    BWSet("Plasma Storm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-storm", 1/72, 1/18, 1/36, 1/36),
    BWSet("Plasma Freeze", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-freeze", 1/72, 1/18, 1/36, 1/36),
    BWSet("Plasma Blast", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/plasma-blast", 1/72, 1/18, 1/36, 1/36)
]

legendaryTreasuresUrl = "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures"
legendaryTreasuresRadiantUrl = "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/legendary-treasures-radiant-collection"

xySetList = [
    XYSet("XY Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-base-set", 0, 1/18, 1/36, 0),
    XYSet("XY - Flashfire", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-flashfire", 1/72, 1/12, 1/18, 0),
    XYSet("XY - Furious Fists", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-furious-fists", 1/72, 1/12, 1/18, 0),
    XYSet("XY - Phantom Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-phantom-forces", 1/72, 1/9, 1/18, 0),
    XYSet("XY - Primal Clash", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-primal-clash", 1/72, 1/9, 1/18, 0),
    XYSet("XY - Roaring Skies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-roaring-skies", 1/72, 1/9, 1/18, 0),
    XYSet("XY - Ancient Origins", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-ancient-origins", 1/72, 1/6, 1/12, 0),
    XYSet("XY - BREAKthrough", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-breakthrough", 1/72, 1/6, 1/12, 1/12),
    XYSet("XY - BREAKpoint", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-breakpoint", 1/72, 1/6, 1/12, 1/12),
    XYSet("XY - Fates Collide", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-fates-collide", 1/72, 1/6, 1/12, 1/12),
    XYSet("XY - Steam Siege", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-steam-siege", 1/72, 1/6, 1/12, 1/12),
    XYSet("XY - Evolutions", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/xy-evolutions", 0, 1/6, 1/12, 1/12)
]

smSetList = [
    SMSet("SM Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-base-set", .0277, 1/9, 1/24, 0, 0),
    SMSet("SM - Guardians Rising", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-guardians-rising", .0265, 1/9, 1/28, 0, 0),
    SMSet("SM - Burning Shadows", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-burning-shadows", .0276, 1/9, 1/25, 0, 0),
    SMSet("SM - Crimson Invasion", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-crimson-invasion", .0222, 1/12, 1/22, 0, 0),
    SMSet("SM - Ultra Prism", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-ultra-prism", .0254, 1/12, 1/22, 1/12, 0),
    SMSet("SM - Forbidden Light", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-forbidden-light", .0227, 1/12, 1/28, 1/12, 0),
    SMSet("SM - Celestial Storm", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-celestial-storm", .0229, 1/9, 1/28, 1/18, 0),
    SMSet("SM - Lost Thunder", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-lost-thunder", .0255, 1/10, 1/22, 1/9, 0),
    SMSet("SM - Team Up", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-team-up", 0.0176, 1/10, 1/22, 1/18, 0),
    SMSet("SM - Unbroken Bonds", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-unbroken-bonds", .0228, 1/10, 1/22, 0, 0),
    SMSet("SM - Unified Minds", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-unified-minds", .0228, 1/8, 1/22, 0, 0),
    SMSet("SM - Cosmic Eclipse", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sm-cosmic-eclipse", 0.02861, 1/9, 1/27, 0, 1/9)
]

swshSetList = [
    SWSHSet("SWSH01: Sword & Shield Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh01-sword-and-shield-base-set", 0.0237, 1/7, 1/45, 1/27, 0, 0),
    SWSHSet("SWSH02: Rebel Clash", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh02-rebel-clash", 0.0263, 1/8, 1/30, 1/27, 0, 0),
    SWSHSet("SWSH03: Darkness Ablaze", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh03-darkness-ablaze", 0.0239, 1/8, 1/26, 1/27, 0, 0),
    SWSHSet("SWSH04: Vivid Voltage", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh04-vivid-voltage", 0.0452, 1/8, 1/24, 1/24, 1/20, 0),
    SWSHSet("SWSH05: Battle Styles", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh05-battle-styles", 0.0187, 1/8, 1/24, 1/48 + 1/94, 0, 1/201 + 1/703),
    SWSHSet("SWSH06: Chilling Reign", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh06-chilling-reign", 0.0196, 1/8, 1/24, 1/49 + 1/78, 0, 1/147 + 1/454),
    SWSHSet("SWSH07: Evolving Skies", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh07-evolving-skies", 0.0225, 1/8, 1/18, 1/197 + 1/56, 0, 1/82 + 1/283),
    SWSHSet("SWSH08: Fusion Strike", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh08-fusion-strike", 0.0160, 1/8, 1/30, 1/64 + 1/58, 0, 1/180 + 1/332),
]

lateSwshSetList = [
    lateSWSHSet("SWSH09: Brilliant Stars", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh09-brilliant-stars", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh09-brilliant-stars-trainer-gallery", .264, .0191, 1/7, 1/96, 1/43, 1/30, 1/127, 0.1944, 0 ),
    lateSWSHSet("SWSH10: Astral Radiance", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh10-astral-radiance", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh10-astral-radiance-trainer-gallery", .255, .0141, .1512, .0081, .0026, .0537, 1/135, .125, .0488),
    lateSWSHSet("SWSH11: Lost Origin", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh11-lost-origin", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh11-lost-origin-trainer-gallery", .265, .0316, .1309, .0167, .0418, .046, 14/2211, .1146, .0404),
    lateSWSHSet("SWSH12: Silver Tempest", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh12-silver-tempest", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/swsh12-silver-tempest-trainer-gallery", .254, .0287, .1295, .0167, .0279, .0599, 1/684+1/636+1/636+1/741, .1146, .0557),
]

svSetList = [
    svSet("SV01: Scarlet & Violet Base Set", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv01-scarlet-and-violet-base-set", .0185, .1428, .0666, .0769, .03125, 0 ),
    svSet("SV02: Paldea Evolved", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv02-paldea-evolved", .0175, .1428, .0666, .0769, .03125, 0 ),
    svSet("SV03: Obsidian Flames", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv03-obsidian-flames", .0192, .1428, .0666, .0769, .03125, 0 ),
    svSet("SV04: Paradox Rift", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv04-paradox-rift", .0121, .1666, .0666, .0769, .0212, 0 ),
    svSet("SV05: Temporal Forces", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv05-temporal-forces", .0071, .1666, .0666, .0769, .0116, .05 ),
    svSet("SV06: Twilight Masquerade", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv06-twilight-masquerade", .0175, .1666, .0666, .0769, .0116, .05 ),
    svSet("SV07: Stellar Crown", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv07-stellar-crown", .0192, .1666, .0666, .0769, .0111, .05 ),
    svSet("SV08: Surging Sparks", "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/pokemon/price-guides/sv08-surging-sparks", .0121, .1666, .0666, .0769, .0114, .05 ),
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

    if(tempSet.name == "Base Set 2"):
        unlimited = ""
    else:
        unlimited = "+unlimited"
    driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.replace(" ", "+") + unlimited + "+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.replace(" ", "+") + "+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    if(tempSet.name != "Dragon"):
        driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.replace("&", "and").replace(" ", "+") + "+booster+pack")
        priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
        packPrice = float(priceElement.text.replace("$", "").replace(",", ""))
    else:
       packPrice = float(600)
    

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

    driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.replace(" ", "+") + "+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.replace(" ", "+") + "+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.replace(" ", "+") + "+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.replace(" ", "+") + "+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    driver.get("https://app.getcollectr.com/?query=Pokemon+" + "legendary+treasures+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    if(tempSet.name == "XY Base Set"):
        modifier = "XY+base+booster+pack"
    else:
        modifier = tempSet.name.split("-")[1].strip().replace(" ", "+") + "+booster+pack"
    driver.get("https://app.getcollectr.com/?query=Pokemon+" + modifier)
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    if(tempSet.name == "SM Base Set"):
        modifier = "Sun+and+Moon+Base+booster+pack"
    else:
        modifier = tempSet.name.split("-")[1].strip().replace(" ", "+") + "+booster+pack"
    driver.get("https://app.getcollectr.com/?query=Pokemon+" + modifier)
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.split(":")[1].strip().replace("&", "and").replace(" ", "+") + "+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.split(":")[1].strip().replace(" ", "+") + "+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

    driver.get("https://app.getcollectr.com/?query=Pokemon+" + tempSet.name.split(":")[1].strip().replace("&", "and").replace(" ", "+") + "+booster+pack")
    time.sleep(10)
    priceElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div/div/main/div/div/div[4]/h2')))
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

expectedValueList = []
setNameList = []
packValueList = []
actualEvList = []
setNumberList = []

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