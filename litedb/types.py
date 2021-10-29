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

from enum import Enum, unique, Flag, auto

@unique
class LdbEngine(Enum):

    UNDEFINED  = 1
    MYSQL      = 2
    PGSQL      = 3
    MSSQL      = 4

@unique
class LdbType(Enum):

    NONE     = 0
    STRING   = 1
    TEXT     = 2
    INT      = 3
    FLOAT    = 4
    DECIMAL  = 5
    BLOB     = 6
    DATETIME = 7
    DATE     = 8
    TIME     = 9
    SET      = 10
    JSON     = 11

    @classmethod
    def ToSQL(cls, engine_type : LdbEngine, t):
        return {
            cls.STRING  : 'VARCHAR',
            cls.TEXT    : 'TEXT',
            cls.INT     : 'INT',
            cls.FLOAT   : 'FLOAT',
            cls.DECIMAL : 'DECIMAL',
            cls.BLOB    : 'BLOB',
            cls.DATETIME: 'DATETIME',
            cls.DATE    : 'DATE',
            cls.TIME    : 'TIME',
            cls.SET     : 'SET',
            cls.JSON    : 'JSON',
        }[t]

    @classmethod
    def FromType(cls, t):

        if type(t) == type:
            if t == str:     return LdbType.STRING
            if t == int:     return LdbType.INT
            if t == complex: return LdbType.DECIMAL
            if t == float:   return LdbType.FLOAT
            if t == bool:    return LdbType.INT
            if t == bytes:   return LdbType.BLOB
            if t == set:     return LdbType.SET
        else:
            if t in LdbType.__members__.values():
                return t

        return LdbType.NONE

class LdbAttr(Flag):
    DEFAULT = 0
    NOTNULL = auto()
    AI      = auto()
    PK      = auto()
    UNSIGN  = auto()

    def ToSQL(self, engine_type : LdbEngine) -> str:
        items = []

        if self & LdbAttr.UNSIGN:  items.append('UNSIGNED')
        if self & LdbAttr.NOTNULL: items.append('NOT NULL')
        if self & LdbAttr.AI:      items.append('AUTO_INCREMENT')
        if self & LdbAttr.PK:      items.append('PRIMARY KEY')

        return ' '.join(items)