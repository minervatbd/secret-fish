from queries import SqlQuery

import cfg
import utils

async def post_leaderboards(client = None, server = None):
    leaderboard_channel = utils.get_channel(server = server, channel_name = cfg.channel_leaderboard)

    top_points = make_points_board(server = server)
    await utils.send_message(leaderboard_channel, None, top_points)



def make_points_board(server = None):
    board = "▓▓▓▓▓ TOP FISHERS ▓▓▓▓▓\n"

    result = SqlQuery(
        table = cfg.tab_users,
        target_cols = [cfg.col_points, cfg.col_id_user],
        key_cols = [cfg.col_id_server],
        key_vals = [server.id],
        order_col = cfg.col_points,
        limit = 5
    ).select()

    for row in result:
        board += "`{:_>3} | {}`\n".format(
                row[0],
                row[1],
            )
    
    return board