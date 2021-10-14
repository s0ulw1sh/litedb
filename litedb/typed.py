from enum import Enum, unique

@unique
class Typed(Enum):
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
    UNDEF    = 255

    def __str__(self):
        return Typed.ToSQLStr(self)

    @classmethod
    def ToSQLStr(cls, t):
        if type(t) == type:
            if t == str:     return 'VARCHAR'
            if t == int:     return 'INT'
            if t == complex: return 'DECIMAL'
            if t == float:   return 'FLOAT'
            if t == bool:    return 'INT'
            if t == bytes:   return 'BLOB'
            if t == set:     return 'SET'
        elif type(t) == Typed:
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
            }[t]

        return 'UNDEFINED'

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

        return Typed.UNDEF