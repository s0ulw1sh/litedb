from urllib.parse import urlsplit
from mysql.connector import pooling
import string, random

from .table import Table
from .types import LdbType

class Db:

    TYPE : LdbType

    def __init__(dbms, name, db, gcn):
        self.TYPE    = dbms
        self.NAME    = name
        self.DB      = db
        self.GETCONN = gcn

    def Conn(self):
        return self.GETCONN()

    def CreateTable(self, tab : Table):
        pass

def create_engine(dsn : str = '', user : str = 'root', password : str = '', host : str = '127.0.0.1', port : int = 3306, database : str = '', pool_size : int = 3):
    if len(dsn) == 0:
        dsn = 'mysql://%s:%s@%s:%d/%s' % (user, password, host, port, database)
    
    db  = None
    dbn = urlsplit(dsn.strip())
    pon = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))

    if dbn.scheme.lower() == 'mysql':
        db = pooling.MySQLConnectionPool(pool_name = pon,
                                         pool_size = pool_size,
                                         {
                                            'host'     : dbn.hostname.lower(),
                                            'port'     : dbn.port,
                                            'database' : dbn.path.strip('/'),
                                            'user'     : dbn.username,
                                            'password' : dbn.password
                                         })

    return Db(LdbType.MYSQL, pon, db, db.get_connection)