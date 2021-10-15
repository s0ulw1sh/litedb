from enum import auto
from .expr import Expr

class Fn(Expr):

    NONE     = 0
    PASSWORD = auto()
    MD5      = auto()
    CONCAT   = auto()
    NOW      = auto()
    CTS      = auto()
    CRC      = auto()
    UUID     = auto()

    def __init__(self, t, x : Expr = None, y : Expr = None):
        self.TYPE = t
        self.X    = x
        self.Y    = y

    def ToSQL(self) -> str:

        if self.TYPE == Fn.PASSWORD:
            return 'PASSWORD(' + self.X.ToSQL() + ')'
        elif self.TYPE == Fn.CONCAT:
            return 'CONCAT(' + self.X.ToSQL() + ', ' + self.Y.ToSQL() + ')'
        elif self.TYPE == Fn.MD5:
            return 'MD5(' + self.X.ToSQL() + ')'
        elif self.TYPE == Fn.NOW:
            return 'NOW()'
        elif self.TYPE == Fn.CTS:
            return 'CURRENT_TIMESTAMP()'
        elif self.TYPE == Fn.UUID:
            return 'UUID()'
        elif self.TYPE == Fn.CRC:
            return 'CRC32(' + self.X.ToSQL() + ')'

        return ''

    @classmethod
    def Pwd(cls, x : Expr):
        return Fn(Fn.PASSWORD, x)

    @classmethod
    def Pwd(cls, x : Expr, y : Expr):
        return Fn(Fn.CONCAT, x, y)

    @classmethod
    def MD5(cls, x : Expr):
        return Fn(Fn.MD5, x)

    @classmethod
    def Crc(cls, x : Expr):
        return Fn(Fn.CRC, x)

    @classmethod
    def Now(cls):
        return Fn(Fn.NOW)

    @classmethod
    def Cts(cls):
        return Fn(Fn.CTS)

    @classmethod
    def Uuid(cls):
        return Fn(Fn.UUID)