import filehelpers

# helper functions for building the chance dictionaries
def set_all(d, range, value):
    for s in range:
        d.append(value)

def set_chances(indict):
    outlist = []
    current = 1
    for s in indict.keys():
        set_all(outlist, range(current, current + indict[s]), s)
        current += indict[s]
    return outlist

# all the commands/alt commands
cmd_prefix = "!"
cmd_test = cmd_prefix + "test"
cmd_cast = cmd_prefix + "cast"
cmd_reel = cmd_prefix + "reel"
cmd_id_1 = cmd_prefix + "identify"
cmd_id_2 = cmd_prefix + "identifyas"
cmd_id_3 = cmd_prefix + "setgender"
cmd_stats_1 = cmd_prefix + "status"
cmd_stats_2 = cmd_prefix + "points"
cmd_stats_3 = cmd_prefix + "check"

update_hookstillactive = 60 * 60 * 3

max_id_len = 20

# fish timers in seconds
fish_timer_default = 60
reel_timer_default = 10

# fishing minute count odds
bite_odds_default = {
    1:2,
    2:5,
    3:8,
    4:11,
    5:12,
    6:11,
    7:9,
    8:8,
    9:8,
    10:8,
    11:6,
    12:4,
    13:3,
    14:2,
    15:1,
    16:1,
    17:1,
}

bite_odds_picker = set_chances(bite_odds_default)

# default fish rarity percentages
rarity_default = {
    "common": 55,
    "uncommon": 35,
    "rare": 9,
    "promo": 1,
}

rarity_picker = set_chances(rarity_default)

# default fish size percantages
size_default = {
    "miniscule": 5,
    "small": 20,
    "average": 50,
    "big": 20,
    "huge": 4,
    "colossal": 1
}

size_picker = set_chances(size_default)

bite_text = {
    "miniscule": "You feel a wimpy tug at your fishing pole!",
    "small": "You feel a mediocre tug at your fishing pole!",
    "average": "You feel a modest tug at your fishing pole!",
    "big": "You feel a hefty tug at your fishing pole!",
    "huge": "You feel a ferocious tug at your fishing pole!",
    "colossal": "You feel a tug at your fishing pole so intense it almost sweeps you off your feet!"
}

# point calculation for now will be rarity * size based on these values
# i like how these values range right now, smallest is 1,100 and largest is 110,000
points_vals = {
    "common": 52,
    "uncommon": 103,
    "rare": 234,
    "promo": 497,
    "miniscule": 23,
    "small": 49,
    "average": 87,
    "big": 111,
    "huge": 151,
    "colossal": 223
}

channel_lakefront = 1327418589627682856
channel_shop = 1329604548314271875

fishing_channels = [
    channel_lakefront
]

shopping_channels = [
    channel_shop
]

no_bite_text = [
    "You patiently wait...",
    "You start to slip into an existential crisis...",
	"You hum some sea shanties...",
    "You watch your hook bob...",
    "You make direct eye contact with a fish, only to quickly look away...",
    "Wouldn't it be funny if you just reached into the sea and grabbed one? Haha, yeah, that'd be funny...",
    "You let out a deep sigh, scaring away a fish...",
    "Fish...",
	"You begin to zone-out a bit...",
	"Shouldn't you be doing something productive?",
]

extra_no_bite_text = filehelpers.getStrListFromFileContents("extra_no_bite_text")

for txt in extra_no_bite_text:
    no_bite_text.append(txt)

# All the fish, baby!
fish_list_full = []
fish_map = {}
fish_names = []

fish_list_full.extend(filehelpers.ParseFishJson('fish.json'))
fish_list_full.extend(filehelpers.ParseFishJson('extra_fish.json'))

# Populate fish map, including all aliases.
for fishstatic in fish_list_full:
	fish_map[fishstatic.id_fish] = fishstatic
	fish_names.append(fishstatic.id_fish)

	for alias in fishstatic.alias:
		fish_map[alias] = fishstatic

# table names
tab_users = "users"
tab_dex_entries = "dex_entries"

# database row titles
col_id_user = "id_user"
col_id_server = "id_server"
col_points = "points"
col_identity = "identity"
col_id_fish = "id_fish"
col_catch_count = "catch_count"
col_dex_count = "dex_count"

# sql credentials
db_host = "localhost"
db_username = "fishmaster"
db_password = "secret"
db_dbname = "fish"
db_charset = "utf8mb4"