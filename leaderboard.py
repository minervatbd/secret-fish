from queries import SqlQuery

import cfg

def make_points_board(server = None):
    board = "▓▓▓▓▓ TOP FISHERS ▓▓▓▓▓\n"

    result = SqlQuery(
        table = cfg.tab_users,
        target_cols = [cfg.col_points, cfg.col_id_user],
        key_cols = [cfg.col_id_server],
        key_vals = [server.id],
        order_col = cfg.col_points,
        limit = 5
    )

    for row in result:
        board += "`{:_>3} | {}`\n".format(
                row[0],
                row[1].replace("`","")
            )
    
    return board