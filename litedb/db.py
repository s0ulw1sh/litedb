from urllib.parse import urlsplit
import string, random
from abc import abstractmethod, ABCMeta

from .expr  import ILdbExpr
from .table import LdbTable
from .types import LdbType
from .query import LdbQuery

class LDb(metaclass=ABCMeta):

    @abstractmethod
    def CreateTable(self, table : LdbTable):
        pass

    @abstractmethod
    def DropTable(self, table : LdbTable):
        pass

    @abstractmethod
    def Execute(self, q : ILdbExpr):
        pass

##   ## ##  ##  ## ##   ## ##  ####
 ## ##  ##  ## ##   ## ##   ##  ##
# ### # ##  ## ####    ##   ##  ##
## # ##  ## ##  #####  ##   ##  ##
##   ##   ##       ### ##   ##  ##
##   ##   ##   ##   ## ##  ##   ##  ##
##   ##   ##    ## ##   ##  ## ### ###

class LDbMySQL(LDb):

    def __init__(self, host:str, port:int, database:str, user:str, pwd:str):
        from mysql.connector import pooling

        self.NAME    = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
        self.POOL    = pooling.MySQLConnectionPool(pool_name = self.NAME, pool_size = pool_size, {
                                                        'host'     : host,
                                                        'port'     : port,
                                                        'database' : database,
                                                        'user'     : user,
                                                        'password' : pwd
                                                    })

    def CreateTable(self, table : LdbTable):
        conn = self.POOL.get_connection()
        curs = conn.cursor()

        sql  = table.ToSQL(LdbType.MYSQL)

        cursor.execute(sql)

        conn.close()

    def DropTable(self, table : LdbTable):
        conn = self.POOL.get_connection()
        curs = conn.cursor()

        sql  = table.ToDropSQL(LdbType.MYSQL)

        cursor.execute(sql)

        conn.close()

    def Execute(self, q : ILdbExpr):
        conn = self.POOL.get_connection()
        curs = conn.cursor()

        sql  = q.ToSQL(LdbType.MYSQL)

        cursor.execute(sql)

        conn.close()

def create_engine(dsn : str = '', user : str = 'root', password : str = '', host : str = '127.0.0.1', port : int = 3306, database : str = '', pool_size : int = 3):
    if len(dsn) == 0:
        dsn = 'mysql://%s:%s@%s:%d/%s' % (user, password, host, port, database)

    dbn = urlsplit(dsn.strip())
    
    if dbn.scheme.lower() == 'mysql':
        return LDbMySQL(dbn.hostname.lower(), dbn.port, dbn.path.strip('/'), dbn.username, dbn.password)

    return None