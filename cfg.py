import utils
import fishstatic

update_hookstillactive = 60 * 60 * 3

fish_timer_default = 60
reel_timer_default = 10

cmd_prefix = "!"
cmd_test = cmd_prefix + "test"
cmd_cast = cmd_prefix + "cast"
cmd_reel = cmd_prefix + "reel"

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

extra_no_bite_text = utils.getStrListFromFileContents("extra_no_bite_text")

for txt in extra_no_bite_text:
    no_bite_text.append(txt)

# All the fish, baby!
fish_list_full = []
fish_map = {}
fish_names = []

fish_list_full.extend(fishstatic.fish_list)
fish_list_full.extend(utils.getExtraFish('extra_fish.json'))

# Populate fish map, including all aliases.
for fishstatic in fish_list_full:
	fish_map[fishstatic.id_fish] = fishstatic
	fish_names.append(fishstatic.id_fish)

	for alias in fishstatic.alias:
		fish_map[alias] = fishstatic