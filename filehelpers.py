import json

from models import Fish

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

""" get the Discord API token from the config file on disk """
def getToken():
	return getValueFromFileContents("token")

""" gets a string list from a json of fname """
def ParseBiteText(fname):
    # in case we dont find the file, still need to return an empty list
    outlist = []

    try:
        f = open(fname)
        a = f.read()
        outlist.extend(json.loads(a, ))
    except FileNotFoundError:
        print(fname + " not found.")

    return outlist

""" attempts to get extra fish objects from a json file fname in the directory """
def ParseFishJson(fname):
    outlist = []
    try:  
        with open(fname) as f:
            fish = json.loads(f.read())
            x = 0
            while x < len(fish):
                currentfish = fish[x]
                x += 1
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
        print(fname + " not found.")

    return outlist