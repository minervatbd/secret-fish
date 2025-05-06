import utils
import cfg

from backend import User, Timeline

""" simple test command """
async def test(cmd):
	response = 'test'.format(cmd.message.author.id)
	return await utils.send_message(cmd.message.channel, cmd.message.author, response, mention = cmd.message.author) # type: ignore

""" for give self gender :) """
async def identify(cmd):
    author = cmd.message.author

    if cmd.tokens_count < 2:
        response = "How would you like to ID? (Usage: !identify [gender])"

    else:
        id = cmd.tokens[1]
        
        if len(id) > cfg.max_id_len:
            response = "Sorry, kid. That gender is just too long for our databases. 20 chars or less, please."
        
        else:
            user_data = User(member = author)
            user_data.identity = id
            user_data.persist()

            response = "You are now {}, the fisher{}.".format(author.display_name, id)
    
    return await utils.send_message(cmd.message.channel, author, response)

""" check your own or someone else's status """
async def status(cmd):
    author = cmd.message.author
    response = "You are "
    dex_text = "You "

    if cmd.mentions_count == 0:
        user_data = User(member = author)

    else:
        member = cmd.mentions[0]
        user_data = User(member = member)
        
        if member != author:
            response = "{} is ".format(member.display_name)
            dex_text = " They "
    
    response += "a fisher{} with {} fishpoints.".format(user_data.identity, user_data.points)
    response += dex_text + "have caught {} unique species of fish.".format(user_data.dex_count)
    
    return await utils.send_message(cmd.message.channel, author, response)

""" check the weather """
async def weather(cmd):
    author = cmd.message.author
    timeline = Timeline(id_server = cmd.message.guild.id)
    response = "Current weather: {}".format(timeline.weather)

    return await utils.send_message(cmd.message.channel, author, response)