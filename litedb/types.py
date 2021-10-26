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

    def ToSQL(self, engine_type : LdbEngine):
        return {
            LdbType.STRING  : 'VARCHAR',
            LdbType.TEXT    : 'TEXT',
            LdbType.INT     : 'INT',
            LdbType.FLOAT   : 'FLOAT',
            LdbType.DECIMAL : 'DECIMAL',
            LdbType.BLOB    : 'BLOB',
            LdbType.DATETIME: 'DATETIME',
            LdbType.DATE    : 'DATE',
            LdbType.TIME    : 'TIME',
            LdbType.SET     : 'SET',
            LdbType.JSON    : 'JSON',
        }[self]

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
            if t in LdbType.__members__:
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