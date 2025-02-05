import time
import asyncio
import random

import utils
import cfg

from backend import User, DexEntry

FISH_DEBUG = True

""" class for storing info about a fishing action in progress """
class Fisher:
	fishing = False
	bite = False
	current_fish = ""
	current_rarity = ""
	current_size = ""
	pier = ""
	bait = False
	high = False
	fishing_id = 0

	def stop(self): 
		self.fishing = False
		self.bite = False
		self.current_fish = ""
		self.current_size = ""
		self.pier = ""
		self.bait = False
		self.high = False
		self.fishing_id = 0

fishers = {}
fishing_counter = 0

# generates fish species and size
def gen_fish(fisher):
	fisher.current_size = cfg.size_map[random.randint(1, 100)]
	
	fish_pool = []

	fisher.current_rarity = cfg.rarity_map[random.randint(1, 100)]

	for f in cfg.fish_names:
		if cfg.fish_map[f].rarity == fisher.current_rarity:
			fish_pool.append(f)
	
	# TODO: implement weather/time catching mechanics
	# but for now:

	fisher.current_fish = random.choice(fish_pool)

""" simple test command """
async def test(cmd):
	response = 'tested'
	return await utils.send_message(cmd.message.channel, cmd.message.author, response)

""" Casts a line into the Water """
async def cast(cmd):
	author = cmd.message.author
	channel = cmd.message.channel
	has_reeled = False

	if author.id not in fishers.keys():
		fishers[author.id] = Fisher()
	
	fisher = fishers[author.id]

	# Players must be in a fishing channel.
	if channel.id not in cfg.fishing_channels:
		response = 'You attempt to cast your line with no water in sight. The hook falls unceremoniously to the ground. You should probably try this at #the-lakefront'

	# Players who already cast a line cannot cast another one.
	elif fisher.fishing is True:
		response = "You've already cast a line."
	
	else:
		fisher.fishing = True

		response = "You cast your fishing line into the glowing blue lake."

		min_count = cfg.bite_odds_map[random.randint(1, 100)]
		
		response += " fish will bite in " + str(min_count) + " mins"

		await utils.send_message(channel, author, response)

		gen_fish(fisher)

		# do some stuff with variables for later
		bite_text = cfg.bite_text[fisher.current_size] + " **!REEL NOW!!!!!**"

		global fishing_counter
		fishing_counter += 1
		current_fishing_id = fisher.fishing_id = fishing_counter

		fish_timer = cfg.fish_timer_default
		reel_timer = cfg.reel_timer_default
		
		while not utils.TERMINATE and min_count > 0:
			
			if FISH_DEBUG:
				break

			await asyncio.sleep(fish_timer)

			# if fishing was cancelled
			if current_fishing_id != fisher.fishing_id or not fisher.fishing:
				fisher.stop()
				return

			await utils.send_message(channel, author, random.choice(cfg.no_bite_text))

			min_count -= 1

		
		# bite happens when loop breaks
		fisher.bite = True

		await utils.send_message(channel, author, bite_text)

		await asyncio.sleep(reel_timer)

		if fisher.bite != False and current_fishing_id == fisher.fishing_id:
			response = "The fish got away..."
			fisher.stop()
		
		else:
			has_reeled = True
	
	# Don't send out a response if the user actually reeled in a fish, since that gets sent by the reel command instead.
	if has_reeled == False:
		return await utils.send_message(channel, author, response)
	
""" Reels in the fishing line.. """
async def reel(cmd):
	author = cmd.message.author
	channel = cmd.message.channel

	if author.id not in fishers.keys():
		fishers[author.id] = Fisher()
	
	fisher = fishers[author.id]

	# Players must be in a fishing channel.
	if channel.id not in cfg.fishing_channels:
		response = "You aren't even near water, how do you expect to reel your line in?"

	# Players must cast before they can reel
	elif not fisher.fishing:
		response = "You attempt to reel in your line without even casting it first, causing the hook to get jammed in the rod. Try `!cast`."

	# If a fish isn't biting, then a player reels in nothing.
	elif not fisher.bite:
		response = "You reel in, only to find that no fish had bitten the line yet."
		fisher.stop()

	# On successful reel.
	else:
		response = "You reel in a {}!".format(cfg.fish_map[fisher.current_fish].str_name)

		user_data = User(member = author)

		user_data.points += cfg.points_vals[fisher.current_size] * cfg.points_vals[fisher.current_rarity]

		dex_data = DexEntry(member = author, id_fish = fisher.current_fish)

		dex_data.catch_count += 1

		if dex_data.catch_count == 1:
			user_data.dex_count += 1
			response += " New type of fish!"
		
		user_data.persist()
		dex_data.persist()

		fisher.stop()

	return await utils.send_message(channel, author, response)