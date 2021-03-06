# Copyright 2021 Pavel Rid aka S0ulw1sh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.parse import urlsplit
import string, random
from abc import abstractmethod, ABCMeta

from .expr  import ILdbExpr
from .table import LdbTable
from .types import LdbEngine
from .query import LdbQuery

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

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

class LDbMySQL(LDb):

    def __init__(self, host:str, port:int, database:str, user:str, pwd:str):
        from mysql.connector import pooling

        cfg = {
                    'host'     : host,
                    'port'     : port,
                    'database' : database,
                    'user'     : user,
                    'password' : pwd,
                }

        self.NAME    = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
        self.POOL    = pooling.MySQLConnectionPool(pool_name=self.NAME, pool_size=5, pool_reset_session=True, **cfg)

    def CreateTable(self, table : LdbTable):
        conn = self.POOL.get_connection()
        curs = conn.cursor()

        try:
            curs.execute(table.ToSQL(LdbEngine.MYSQL))
        except BaseException as err:
            return err

        for i in table.ToAlterSQL(LdbEngine.MYSQL):
            try:
                curs.execute(i)
            except BaseException as err:
                return err

        return None

    def DropTable(self, table : LdbTable):
        conn = self.POOL.get_connection()
        curs = conn.cursor()

        for i in table.ToAlterDropSQL(LdbEngine.MYSQL):
            try:
                curs.execute(i)
            except BaseException as err:
                return err

        try:
            curs.execute(table.ToDropSQL(LdbEngine.MYSQL))
        except BaseException as err:
            return err

        return None

    def Execute(self, q : ILdbExpr):
        conn = self.POOL.get_connection()
        curs = conn.cursor()

        try:
            curs.execute(q.ToSQL(LdbEngine.MYSQL))
        except BaseException as err:
            return err

        return None

def create_engine(dsn : str = '', user : str = 'root', password : str = '', host : str = '127.0.0.1', port : int = 3306, database : str = '', pool_size : int = 3):
    if len(dsn) == 0:
        dsn = 'mysql://%s:%s@%s:%d/%s' % (user, password, host, port, database)

    dbn = urlsplit(dsn.strip())
    
    if dbn.scheme.lower() == 'mysql':
        port = dbn.port
        user = dbn.username
        if dbn.port is None or dbn.port == 0: port     = 3306
        if len(dbn.username) == 0:            user = 'root'
        return LDbMySQL(dbn.hostname.lower(), port, dbn.path.strip('/'), user, dbn.password)

    return None