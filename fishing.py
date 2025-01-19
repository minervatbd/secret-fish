import time
import asyncio
import random

import utils
import cfg

class FishFisher:
	fishing = False
	bite = False
	current_fish = ""
	current_size = ""
	pier = ""
	bait = False
	high = False
	fishing_id = 0
	inhabitant_id = None
	fleshling_reeled = False
	ghost_reeled = False

	def stop(self): 
		self.fishing = False
		self.bite = False
		self.current_fish = ""
		self.current_size = ""
		self.pier = ""
		self.bait = False
		self.high = False
		self.fishing_id = 0
		self.inhabitant_id = None
		self.fleshling_reeled = False
		self.ghost_reeled = False

fishers = {}
fishing_counter = 0

async def test(cmd):
	response = 'tested'
	return await utils.send_message(cmd.message.channel, cmd.message.author, response)

""" Casts a line into the Water """
async def cast(cmd):
	time_now = round(time.time())
	author = cmd.message.author
	channel = cmd.message.channel
	has_reeled = False

	if author.id not in fishers.keys():
		fishers[author.id] = FishFisher()
	
	fisher = fishers[author.id]

	if channel.id not in cfg.fishing_channels:
		response = 'You attempt to cast your line with no water in sight. The hook falls unceremoniously to the ground. You should probably try this at #the-lakefront'

	# Players who are already cast a line cannot cast another one.
	elif fisher.fishing is True:
		response = "You've already cast a line."
	
	else:
		fisher.fishing = True

		response = "You cast your fishing line into the glowing blue lake."

		await utils.send_message(channel, author, response)

		nobite_text = "No bite yet."
		bite_text = "Bite!"

		global fishing_counter
		fishing_counter += 1
		current_fishing_id = fisher.fishing_id = fishing_counter
		
		# User has a 1/10 chance to get a bite
		fun = 100

		bun = 0

		while not utils.TERMINATE:
			
			if fun <= 0:
				fun = 1
			else:
				damp = random.randrange(fun)
			
			await asyncio.sleep(60)

			if current_fishing_id != fisher.fishing_id:
				return

			if fisher.fishing == False:
				return

			if damp > 10:
				await utils.send_message(channel, author, nobite_text)
				fun -= 2
				bun += 1
				if bun >= 5:
					fun -= 1
				if bun >= 15:
					fun -= 1
				continue
			else:
				break
		
		fisher.bite = True

		await utils.send_message(channel, author, bite_text)

		await asyncio.sleep(10)

		if fisher.bite != False:
			response = "The fish got away..."
			return await utils.send_message(channel, author, response)
		
		else:
			has_reeled = True
	
	# Don't send out a response if the user actually reeled in a fish, since that gets sent by the reel command instead.
	if has_reeled is False:
		return await utils.send_message(channel, author, response)