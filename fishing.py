import time
import asyncio
import random

import utils
import cfg

from backend import User, DexEntry, Timeline

FISH_DEBUG = False
lines_cut = False

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
def gen_fish(fisher, weather):
	fisher.current_size = random.choice(cfg.size_picker)
	
	fish_pool = []

	fisher.current_rarity = random.choice(cfg.rarity_picker)

	for f in cfg.fish_names:
		curr_fish = cfg.fish_map[f]
		# add if the rarity aligns
		if curr_fish.rarity == fisher.current_rarity:
			# add if the weather aligns
			if curr_fish.catch_weather == None or curr_fish.catch_weather == weather:
				fish_pool.append(f)
	

	fisher.current_fish = random.choice(fish_pool)

""" Casts a line into the Water """
async def cast(cmd):
	author = cmd.message.author
	channel = cmd.message.channel
	has_reeled = False

	timeline = Timeline(id_server = cmd.message.guild.id)

	if author.id not in fishers.keys():
		fishers[author.id] = Fisher()
	
	fisher = fishers[author.id]

	# Players must be in a fishing channel.
	if channel.id not in cfg.fishing_channels:
		response = 'You attempt to cast your line with no water in sight. The hook falls unceremoniously to the ground. You should probably try this at #the-lakefront'

	# Players who already cast a line cannot cast another one.
	elif fisher.fishing is True:
		response = "You've already cast a line."
	
	# If the lines cut command has been triggered
	elif lines_cut is True:
		response = "Sorry, no more casting for now. Standby while the bot is being restarted."
	
	else:
		fisher.fishing = True

		response = "You cast your fishing line into the glowing blue lake."

		min_count = random.choice(cfg.bite_odds_picker)

		# debug for counting minute bite averages
		# response += " fish will bite in " + str(min_count) + " mins"

		await utils.send_message(channel, author, response)

		gen_fish(fisher, timeline.weather)

		# do some stuff with variables for later
		bite_text = cfg.bite_text[fisher.current_size] + " **!REEL NOW!!!!!**"

		global fishing_counter
		fishing_counter += 1
		current_fishing_id = fisher.fishing_id = fishing_counter

		fish_timer = cfg.fish_timer_default
		reel_timer = cfg.reel_timer_default
		
		# FISH LOOP
		while not utils.TERMINATE:
			
			#break the loop immediately while debugging
			if FISH_DEBUG:
				break

			await asyncio.sleep(fish_timer)

			# if fishing was cancelled
			if current_fishing_id != fisher.fishing_id or not fisher.fishing:
				fisher.stop()
				return
			
			min_count -= 1

			# break if minute count has run out
			if min_count <= 0:
				break

			# otherwise send a no bite message
			await utils.send_message(channel, author, random.choice(cfg.no_bite_text))
		
		# bite happens when loop breaks
		fisher.bite = True

		# reel now message
		await utils.send_message(channel, author, bite_text, mention = author)

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
		user_data = User(member = author)

		user_data.points += cfg.points_vals[fisher.current_size] * cfg.points_vals[fisher.current_rarity]

		dex_data = DexEntry(member = author, id_fish = fisher.current_fish)

		dex_data.catch_count += 1

		new_text = ""

		if dex_data.catch_count == 1:
			user_data.dex_count += 1
			new_text = "It's a new type of fish!"
		
		fish = cfg.fish_map[fisher.current_fish]

		response = "You reel in a {}! {}\n\n{}".format(fish.str_name, new_text, fish.str_desc)

		user_data.persist()
		dex_data.persist()

		fisher.stop()

	return await utils.send_message(channel, author, response)

""" prevents new lines from being cast for bot testing purposes """
async def cut_all_lines(cmd):
	author = cmd.message.author
	channel = cmd.message.channel

	if author.get_role(cfg.role_admin) is not None:
		global lines_cut
		lines_cut = True
		return await utils.send_message(channel, author, "No new lines can be cast now.")