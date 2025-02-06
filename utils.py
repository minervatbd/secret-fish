import datetime
import discord
import json
import time
import MySQLdb

import cfg

from models import Fish

TERMINATE = False

db_pool = {}
db_pool_id = 0

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

""" connect to the database """
def databaseConnect():
    conn_info = None

    conn_id_todelete = []

    global db_pool
    global db_pool_id

    # Iterate through open connections and find the currently active one.
    for pool_id in db_pool:
        conn_info_iter = db_pool.get(pool_id)

        if conn_info_iter['closed'] == True:
            if conn_info_iter['count'] <= 0:
                conn_id_todelete.append(pool_id)
        else:
            conn_info = conn_info_iter

    # Close and remove dead connections.
    if len(conn_id_todelete) > 0:
        for pool_id in conn_id_todelete:
            conn_info_iter = db_pool[pool_id]
            conn_info_iter['conn'].close()

            del db_pool[pool_id]

    # Create a new connection.
    if conn_info == None:
        db_pool_id += 1
        conn_info = {
        'conn': MySQLdb.connect(host = cfg.db_host, user = cfg.db_username, passwd = cfg.db_password, db = cfg.db_dbname, charset = cfg.db_charset),
            'created': int(time.time()),
            'count': 1,
            'closed': False
        }
        db_pool[db_pool_id] = conn_info
    else:
        conn_info['count'] += 1

    return conn_info

""" close (maybe) the active database connection """
def databaseClose(conn_info):
    conn_info['count'] -= 1

    # Expire old database connections.
    if (conn_info['created'] + 60) < int(time.time()):
        conn_info['closed'] = True

"""
    Execute a given sql_query. (the purpose of this function is to minimize repeated code and keep functions readable)
"""
def execute_sql_query(sql_query = None, sql_replacements = None, fetchone = False, lastrowid = False):
    data = None
    cursor = None
    conn_info = None

    try:
        conn_info = databaseConnect()
        conn = conn_info.get('conn')
        cursor = conn.cursor()
        cursor.execute(sql_query, sql_replacements)

        if sql_query.lower().startswith("select"):
            data = cursor.fetchall() if not fetchone else cursor.fetchone()

        if sql_query.lower().startswith("insert") and lastrowid:
            data = cursor.lastrowid

        conn.commit()

    finally:
        # Clean up the database handles.
        if cursor is not None: cursor.close()
        if conn_info is not None: databaseClose(conn_info)

    return data