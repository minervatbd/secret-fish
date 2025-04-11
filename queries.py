import time
import MySQLdb
import utils
import cfg

db_pool = {}
db_pool_id = 0

""" class for clean sql queries, table should be a string and everything else should be string tuples """
class SqlQuery:
    table = ""
    target_cols = None
    target_vals = None
    key_cols = None
    key_vals = None

    def __init__(self, table = "", target_cols = None, target_vals = None, key_cols = None, key_vals = None):
        self.table = table
        self.target_cols = target_cols
        self.target_vals = target_vals
        self.key_cols = key_cols
        self.key_vals = key_vals
    
    """ query format: SELECT [target_cols] FROM [table] WHERE [key_cols] = [key_vals] """

    def select(self):
        if len(self.key_vals) == 0 or len(self.key_cols) != len(self.key_vals) or len(self.target_cols) == 0:
            utils.logMsg("Error in {} select".format(self.table))

        try:
            conn_info = databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            # build the request
            request = "SELECT "
            t = 0
            while t < len(self.target_cols):
                if t != 0:
                    request += ", "
                request += self.target_cols[t]
                t += 1

            request += " FROM " + self.table + " WHERE "
            v = 0
            while v < len(self.key_vals):
                if v != 0:
                    request += " AND "
                curr_val = self.key_vals[v]
                if type(self.key_vals[v]) is str:
                    curr_val = "\'" + self.key_vals[v] + "\'"
                request += "{} = {}".format(self.key_cols[v], curr_val)
                v += 1

            # Retrieve object
            cursor.execute(request)
            result = []
            for i in cursor:
                result.append(i)
            
        finally:
            # Clean up the database handles.
            cursor.close()
            databaseClose(conn_info)
        
        return result
    
    """ query format: REPLACE INTO [table] ([target_cols]) VALUES([target_vals]) """

    def replace(self):
        if len(self.target_vals) == 0 or len(self.target_cols) != len(self.target_vals):
            utils.logMsg("Error in {} replace".format(self.table))
        
        try:
            conn_info = databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            request = "REPLACE INTO " + self.table + "("

            t = 0
            while t < len(self.target_cols):
                if t != 0:
                    request += ", "
                request += self.target_cols[t]
                t += 1
            
            request += ") VALUES("

            v = 0
            while v < len(self.target_vals):
                if v != 0:
                    request += ", "

                curr_val = ""
                # type conversion/formatting for key_vals
                if type(self.target_vals[v]) is int:
                    curr_val = str(self.target_vals[v])
                elif type(self.target_vals[v]) is str:
                    curr_val = "\'" + self.target_vals[v] + "\'"
                
                request += curr_val
                v += 1
            
            request += ")"

            # Save the object.
            cursor.execute(request)
            conn.commit()

        finally:
            # Clean up the database handles.
            cursor.close()
            databaseClose(conn_info)


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