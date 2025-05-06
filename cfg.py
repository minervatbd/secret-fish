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
cmd_weather = cmd_prefix + "weather"
cmd_cutlines = cmd_prefix + "cut"

update_hookstillactive = 60 * 60 * 1
update_timeline = 60 * 10

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

weather_types = [
    "nonplussed",
    "sultry",
    "spiky",
    "dripping",
    "smudged",
    "rapturous",
]

weather_default = weather_types[0]

role_fisher = 1368682228770672843
role_admin = 1368953452906156103

channel_lakefront = 1327418589627682856
channel_shop = 1329604548314271875

channel_leaderboard = "top-fish"

fishing_channels = [
    channel_lakefront
]

shopping_channels = [
    channel_shop
]

no_bite_text = []

no_bite_text.extend(filehelpers.ParseBiteText("no_bite_text.json"))
no_bite_text.extend(filehelpers.ParseBiteText("extra_no_bite_text.json"))

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
tab_timelines = "timelines"

# database row titles
col_id_user = "id_user"
col_id_server = "id_server"
col_display_name = "display_name"
col_points = "points"
col_identity = "identity"

col_id_fish = "id_fish"
col_catch_count = "catch_count"
col_dex_count = "dex_count"

col_time_lasttick = "time_lasttick"
col_clock = "clock"
col_weather = "weather"
col_day = "day"
col_global_catch_count = "global_catch_count"

# sql credentials
db_host = "localhost"
db_username = "fishmaster"
db_password = "secret"
db_dbname = "fish"
db_charset = "utf8mb4"