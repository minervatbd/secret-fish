import datetime
import discord
import json


import cfg

from models import Fish

TERMINATE = False

caches = []
enabled_caches = []

cache_type_to_load_fn = {}

""" internal console log messages """
def logMsg(string):
    print("[{}] {}".format(datetime.datetime.now(), string))

    return string

async def send_message(channel, user_target = None, text = None, embed = None, delete_after = None):
    try:
        if text is not None:
            
            if user_target is not None:
                  text = formatMessage(user_target, text)
                  
            return await channel.send(content=text, delete_after=delete_after)
        if embed is not None:
            return await channel.send(embed=embed)
    except discord.errors.Forbidden:
        logMsg('Could not message user: {}\n{}'.format(channel, text))
        raise
    except:
        logMsg('Failed to send message to channel: {}\n{}'.format(channel, text))

def formatMessage(user_target, message):
    return "*{}*: {}".format(user_target.display_name, message).replace("@", "\\{at\\}")

"""
	Find a chat channel by name in a server.
"""
def get_channel(server = None, channel_name = ""):
	channel = None

	for chan in server.channels:
		if chan.name == channel_name:
			channel = chan
	
	if channel == None:
		logMsg('Error: In get_channel(), could not find channel using channel_name "{}"'.format(channel_name))

	return channel