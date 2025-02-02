import time
import asyncio
import random

import utils
import cfg

from models import Fisher

fishers = {}
fishing_counter = 0

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

		await utils.send_message(channel, author, response)

		# do some stuff with variables for later
		bite_text = "Bite!"

		global fishing_counter
		fishing_counter += 1
		current_fishing_id = fisher.fishing_id = fishing_counter

		fish_timer = cfg.fish_timer_default
		reel_timer = cfg.reel_timer_default
		
		# User has a 1/10 chance to get a bite
		fun = 100

		bun = 0

		# loop that runs until the cast is cancelled or a bite is rolled
		while not utils.TERMINATE:
			
			if fun <= 0:
				fun = 1
			else:
				damp = random.randrange(fun)
			
			await asyncio.sleep(fish_timer)

			# if fishing was cancelled
			if current_fishing_id != fisher.fishing_id or not fisher.fishing:
				fisher.stop()
				return

			if damp > 10:
				await utils.send_message(channel, author, random.choice(cfg.no_bite_text))
				fun -= 2
				bun += 1
				if bun >= 5:
					fun -= 1
				if bun >= 15:
					fun -= 1
				continue
			else:
				break
		
		# bite happens when loop breaks
		fisher.bite = True

		await utils.send_message(channel, author, bite_text)

		await asyncio.sleep(reel_timer)

		if fisher.bite != False:
			response = "The fish got away..."
			return await utils.send_message(channel, author, response)
		
		else:
			has_reeled = True
		
		fisher.stop()
	
	# Don't send out a response if the user actually reeled in a fish, since that gets sent by the reel command instead.
	if has_reeled is False:
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
		response = "You reel in a big fat fish!"
		fisher.stop()

	return await utils.send_message(channel, author, response)