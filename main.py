import discord
import sys
import asyncio #

import utils

utils.logMsg('Starting up...')
init_complete = False

class MyClient(discord.Client):

    async def on_ready(self):

        # if already initialized, return
        global init_complete
        if init_complete:
            return
        init_complete = True

        # log client
        utils.logMsg('Logged in as {} ({}).'.format(client.user.name, client.user.id))

        # change presence
        try:
            await client.change_presence(activity=discord.CustomActivity(name = "!cast"))
        except:
            utils.logMsg("Failed to change_presence!")

        # end of set-up
        utils.logMsg("Ready!")
    
    async def on_message(self, message):
        return
    
intents = discord.Intents.default()
intents.message_content = True

# find our REST API token
token = utils.getToken()

if token == None or len(token) == 0:
    utils.logMsg('Please place your API token in a file called "token", in the same directory as this script.')
    sys.exit(0)

# connect to discord and run indefinitely
try:
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(token)
finally:
    utils.TERMINATE = True
    utils.logMsg("Main thread terminated!")