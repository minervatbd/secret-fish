import random
import discord
import sys
import asyncio
import time
import shlex

import utils
import cfg
import fishing
import filehelpers
import cmd # type: ignore
import leaderboard

from models import Cmd
from backend import Timeline

utils.logMsg('Starting up...')
init_complete = False

cmd_map = {
    cfg.cmd_cast: fishing.cast,
    cfg.cmd_reel: fishing.reel,
    cfg.cmd_test: cmd.test,
    cfg.cmd_id_1: cmd.identify,
    cfg.cmd_id_2: cmd.identify,
    cfg.cmd_id_3: cmd.identify,
    cfg.cmd_stats_1: cmd.status,
    cfg.cmd_stats_2: cmd.status,
    cfg.cmd_stats_3: cmd.status,
    cfg.cmd_weather: cmd.weather,
    cfg.cmd_cutlines: fishing.cut_all_lines
}

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

        """
        Set up for infinite loop to perform periodic tasks.
        """

        time_now = int(time.time())

        # Every three hours we log a message saying the periodic task hook is still active. On startup, we want this to happen within about 60 seconds, and then on the normal 3 hour interval.
        time_last_logged = time_now - cfg.update_hookstillactive + 60

        utils.logMsg('Beginning periodic hook loop.')
        while not utils.TERMINATE:
            time_now = int(time.time())

            # Periodic message to log that this stuff is still running.
            if (time_now - time_last_logged) >= cfg.update_hookstillactive:
                time_last_logged = time_now

                utils.logMsg("Periodic hook still active.")
            
            # Perform periodic server actions
            try:
                for server in client.guilds:

                    # get a timeline
                    timeline_data = Timeline(server.id)

                    if (time_now - timeline_data.time_lasttick) >= cfg.update_timeline:

                        timeline_data.time_lasttick = time_now

                        # advance time
                        timeline_data.clock += 1

                        # advance day counter
                        if timeline_data.clock >= 24 or timeline_data.clock < 0:
                            timeline_data.clock = 0
                            timeline_data.day += 1

                        # utils.logMsg("Time is now {}.".format(timeline_data.clock))

                        # 1/3 chance every tick to change weather
                        if random.randrange(3) == 0 and len(cfg.weather_types) > 1:
                            weather_pool = cfg.weather_types.copy()

                            # pick a weather type that is different from the current one
                            weather_pool.remove(timeline_data.weather)
                            timeline_data.weather = random.choice(weather_pool)
                            
                            utils.logMsg("Weather is now {}.".format(timeline_data.weather))
                        
                        timeline_data.persist()

                        # leaderboards get posted at 6 o clock
                        if timeline_data.clock == 6:
                            await leaderboard.post_leaderboards(client = client, server = server)
            
            except Exception as e:
                utils.logMsg("Could not perform periodic guild actions for {}".format(server.name))

            # Wait a while before running periodic tasks.
            await asyncio.sleep(15)
    
    async def on_message(self, message):

        """ do not interact with our own messages """
        if message.author.id == client.user.id or message.author.bot == True:
            return
        
        """ add role if needed """
        if len(message.author.roles) == 1:
            await message.author.edit(roles = [message.guild.get_role(cfg.role_fisher)])
                
        if message.content.startswith(cfg.cmd_prefix):

            """
                Wake up if we need to respond to messages. Could be:
                    message starts with !
                    direct message (server == None)
                    user is new/has no roles (len(roles) < 2)
                    user is swearing
            """

            # tokenize the message. the command should be the first word.
            try:
                tokens = shlex.split(message.content)  # it's split with shlex now because shlex regards text within quotes as a single token
            except:
                tokens = message.content.split(' ')  # if splitting via shlex doesnt work (odd number of quotes), use the old splitting method so it doesnt give an exception

            tokens_count = len(tokens)
            command = tokens[0].lower() if tokens_count >= 1 else ""

            # remove mentions to us
            mentions = list(filter(lambda user: user.id != client.user.id, message.mentions))

            # Create command object
            cmd_obj = Cmd(
                tokens=tokens,
                message=message,
                client=client,
                mentions=mentions
            )

            # if the message wasn't a command, we can stop here
            if not message.content.startswith(cfg.cmd_prefix):
                return

            # Check the main command map for the requested command.
            global cmd_map
            cmd_fn = cmd_map.get(command)

            if cmd_fn is not None:
                # Execute found command
                return await cmd_fn(cmd_obj)

intents = discord.Intents.default()
intents.message_content = True

# find our REST API token
token = filehelpers.getToken()

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