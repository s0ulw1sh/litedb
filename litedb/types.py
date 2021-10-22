from enum import Enum, unique, Flag, auto
from .types import LdbEngine

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

    def ToSQL(self, engine_type : LdbEngine):
        return {
            Typed.STRING  : 'VARCHAR',
            Typed.TEXT    : 'TEXT',
            Typed.INT     : 'INT',
            Typed.FLOAT   : 'FLOAT',
            Typed.DECIMAL : 'DECIMAL',
            Typed.BLOB    : 'BLOB',
            Typed.DATETIME: 'DATETIME',
            Typed.DATE    : 'DATE',
            Typed.TIME    : 'TIME',
            Typed.SET     : 'SET',
            Typed.JSON    : 'JSON',
        }[self]

    @classmethod
    def FromType(cls, t):

        if type(t) == type:
            if t == str:     return Typed.STRING
            if t == int:     return Typed.INT
            if t == complex: return Typed.DECIMAL
            if t == float:   return Typed.FLOAT
            if t == bool:    return Typed.INT
            if t == bytes:   return Typed.BLOB
            if t == set:     return Typed.SET
        else:
            if t in Typed.__members__:
                return t

        return Typed.NONE

class LdbAttr(Flag):
    DEFAULT = 0
    NOTNULL = auto()
    AI      = auto()
    PK      = auto()
    UNSIGN  = auto()

    def ToSQL(self, engine_type : LdbEngine) -> str:
        items = []

        if attr & LdbAttr.UNSIGN:  items.append('UNSIGNED')
        if attr & LdbAttr.NOTNULL: items.append('NOT NULL')
        if attr & LdbAttr.AI:      items.append('AUTO_INCREMENT')
        if attr & LdbAttr.PK:      items.append('PRIMARY KEY')

        return ' '.join(items)