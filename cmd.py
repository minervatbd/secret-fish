import utils
import cfg

from backend import User

""" simple test command """
async def test(cmd):
	response = 'tested'
	return await utils.send_message(cmd.message.channel, cmd.message.author, response) # type: ignore

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

