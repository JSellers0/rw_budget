import myfb
import mariadb
import sys

class RW_Budget_DB:
    def __init__(self) -> None:
        conn_params = {
            "user": myfb.DB_U,
            "password": myfb.DB_P,
            "host": myfb.DB_H,
            "port": int(myfb.DB_PRT),
            "database": myfb.DB_N
        }
        try:
            self.pool: mariadb.ConnectionPool = mariadb.ConnectionPool(
                pool_name="finances pool",
                pool_size=2,
                **conn_params
            )
        except Exception as e:
            print(e)
            sys.exit(1)
            
    