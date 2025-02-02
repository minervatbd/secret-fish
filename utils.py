import datetime
import discord
import json
import os

from models import Fish

TERMINATE = False

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
    return "*{}*: {}".format(user_target.display_name, message).replace("@", "\{at\}")

""" read a file named fname and return its contents as a string """
def getValueFromFileContents(fname):
	token = ""

	try:
		f_token = open(fname, "r")
		f_token_lines = f_token.readlines()

		for line in f_token_lines:
			line = line.rstrip()
			if len(line) > 0:
				token = line
	except IOError:
		token = ""
		print("Could not read {} file.".format(fname))
	finally:
		f_token.close()

	return token

""" get a list of strings from a file """
def getStrListFromFileContents(fname):
    str_list = []

    try:
        file = open(fname, "r")
        str_list = file.readlines()
    except IOError:
        print("Could not read {} file.".format(fname))
    finally:
        file.close()

    return str_list

""" get the Discord API token from the config file on disk """
def getToken():
	return getValueFromFileContents("token")

""" attempts to get extra fish objects from a json file fname in the directory """
def getExtraFish(fname):
    outlist = []
    try:  
        with open(fname) as f:
            fish = json.load(f)
            for i in fish:
                currentfish = fish[i]
                outlist.append(
                    Fish(
                        id_fish = currentfish['id_fish'],
                        str_name = currentfish['str_name'],
                        size = currentfish['size'],
                        rarity = currentfish['rarity'],
                        catch_time = currentfish['catch_time'],
                        catch_weather = currentfish['catch_weather'],
                        str_desc = currentfish['str_desc'],
                        salinity = currentfish['salinity'],
                    ))
    except FileNotFoundError:
        logMsg("No extra fish JSON found.")

    return outlist