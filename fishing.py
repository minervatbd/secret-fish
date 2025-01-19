import time
import asyncio
import random

import utils
import cfg
			
async def test(cmd):
	response = 'tested'
	return await utils.send_message(cmd.message.channel, cmd.message.author, response)

fishers = {}

""" Casts a line into the Water """
async def cast(cmd):
	time_now = round(time.time())
	has_reeled = False

	if cmd.message.author.id not in fishers.keys():
		fishers[cmd.message.author.id] = False
	
	fisher = fishers[cmd.message.author.id]

	if cmd.message.channel.id not in cfg.fishing_channels:
		response = 'You attempt to cast your line with no water in sight. The hook falls unceremoniously to the ground. You should probably try this at #the-lakefront'

	# Players who are already cast a line cannot cast another one.
	elif fisher is True:
		response = "You've already cast a line."
	
	else:
		fishers[cmd.message.author.id] = True

		author = cmd.message.author
		channel = cmd.message.channel

		response = "You cast your fishing line into the glowing Slime Lake"

		await utils.send_message(channel, author, response)

		nobite_text = "No bite yet."
		bite_text = "Bite!"
		
		# User has a 1/10 chance to get a bite
		fun = 100

		bun = 0

		while not utils.TERMINATE:
			
			if fun <= 0:
				fun = 1
			else:
				damp = random.randrange(fun)
			
			await asyncio.sleep(60)

			if fishers[cmd.message.author.id] == False:
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

		await utils.send_message(channel, author, bite_text)

		await asyncio.sleep(10)

		response = "The fish got away..."
		return await utils.send_message(channel, author, response)
	
	# Don't send out a response if the user actually reeled in a fish, since that gets sent by the reel command instead.
	if has_reeled is False:
		return await utils.send_message(cmd.message.channel, cmd.message.author, response)