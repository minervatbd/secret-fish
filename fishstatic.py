from models import Fish

# All the fish, baby!
fish_list = [
    # Common
    Fish(
        id_fish = "clouttrout",
        str_name = "Clout Trout",
        rarity = "common",
        catch_time = None,
        catch_weather = None,
        str_desc = "This fish has the eyes of a winner.",
        salinity = None,
    ),
    # Uncommon
    Fish(
        id_fish = "italiansnapper",
        str_name = "Italian Snapper",
        rarity = "uncommon",
        catch_time = None,
        catch_weather = None,
        str_desc = "You think you can hear this fish murmur some inarticulate Italian noises on occasion.",
        salinity = None,
    ),
    # Rare
    Fish(
        id_fish = "piranhaha",
        str_name = "Piranhaha",
        rarity = "rare",
        catch_time = None,
        catch_weather = None,
        str_desc = "Its toothy smile gives you the creeps. You don't want to know why it's laughing.",
        salinity = None,
    ),
    # Promo
    Fish(
        id_fish = "bathyphysaheadshark",
        str_name = "Bathyphysahead Shark",
        rarity = "promo",
        catch_time = None,
        catch_weather = "foggy",
        str_desc = "This one looks terrifying. I'm serious.",
        salinity = "saltwater",
    ),
]